################################################################
# Ryu Application:
#   App for fetching attached switch's features and capabilities
#  - Author: Hyojoon Kim (joonk@princeton.edu)
################################################################

################################################################
# Copyright (C) 2015 Hyojoon Kim. Princeton University.
#
# Licensed to the Apache Software Foundation (ASF) under one or more
# contributor license agreements.  See the NOTICE file distributed with this
# work for additional information regarding copyright ownership.  The ASF
# licenses this file to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#   http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.  See the
# License for the specific language governing permissions and limitations
# under the License.
################################################################


import os,sys,math
import pickle
import python_api
import json

from optparse import OptionParser

ipvx_watch_words = ['ipv4', 'ipv6', 'icmpv4', 'icmpv6']
exclude_test_numbers= [22,71,13,10,68,214,220,56,19,28,223,217,31,252,]

SUCCESS_SYMBOL = "O"
FAIL_SYMBOL    = "X"
NA_SYMBOL    = "-"

def sum_up_with_existing_json(old_json_file, new_json_map):
    fd = open(old_json_file,'r')
    old_json = json.loads(fd.read())
    fd.close()

    for n in new_json_map:
        for o in old_json:
            if o["Feature"] == n["Feature"]:
                for k in n.keys():
                    if o.has_key(k) is False:
                        o[k] = n[k]
            if o.has_key("swt-Hp_6600") is True:
                saved_data = o["swt-Hp_6600"]
                if o.has_key("swt-Hp_J9307A-v1") is False:
                    o["swt-Hp_J9307A-v1"] = saved_data
                o.pop("swt-Hp_6600")

    return old_json


def recursive_existence_check(the_map, the_list, level):
    if level==len(the_list)-1 or the_map.has_key(the_list[level]) is False:
        return level
    else:
        the_map = the_map[the_list[level]]
        return recursive_existence_check(the_map, the_list, level+1)

def find_level_of_no_entry(the_list, new_map):
    level = recursive_existence_check(new_map, the_list, 0)

    return level

def recursive_create_map(value,i,the_list,the_map):
    if i==len(the_list)-1:
        return value
    else:
        the_map[the_list[i+1]] = value
        value = the_map
        blank_map = {}
        return recursive_create_map(value,i+1,the_list,blank_map)

def create_map_with_list(the_list):
    the_map = {}
    the_list.reverse()
    result = recursive_create_map(the_list[0],0,the_list,the_map)
    return result

def get_info_from_test_detail(test_detail):
#    packet = test_detail.split('-->')[0]
    return test_detail


def create_json_stub(new_map, category, subcategory, test_item, outcome, test_detail):
    packet = ""
    packet = get_info_from_test_detail(test_detail)

    # Parse outcome
    out_list = eval(outcome)
    pass_or_no = ""
    errmsg = ""
    if len(out_list)>=1 and len(out_list)<3:
        pass_or_no = out_list[0]
        if len(out_list)==2:
            errmsg = out_list[1]
    else:
        print "ABORT: Wrong number of outcome items. Abort"
        sys.exit(1)

#    if pass_or_no=="OK":
#        print category, test_item, packet, "Result",pass_or_no, errmsg

    # Build hierarchy
    if subcategory=="":
        the_list = [category, test_item, packet, "Result",pass_or_no, errmsg]
    else: 
        the_list = [category, subcategory, test_item, packet, "Result", pass_or_no,errmsg]

    # Find the level to insert this entry
    level = find_level_of_no_entry(the_list,new_map)

    # Done if reached last level where the value is stored.
    if level==len(the_list)-1:
        return

    # Create new map on that level 
    fresh_map = create_map_with_list(the_list[level+1:])

    # Store to right level   
    for idx,i in enumerate(the_list):
        if idx==level:
            new_map[i] = fresh_map
            break
        else:
            new_map = new_map[i]
    

def jsonize(report_dict, new_map, items_map ):
    for result_type in sorted(report_dict.keys()):
        tests_list = report_dict[result_type]
        for file_desc, test_detail in tests_list:
            token_list = file_desc.split(":")

            if len(token_list)==3:
                category = token_list[0].strip()
                subcategory = token_list[1].strip()
                test = '_'.join(token_list[2].strip().split('_')[1:])

                item = subcategory + "__" + test
                if items_map.has_key(category) is False:
                    items_map[category]  = set()

                items_map[category].add(item)

#                print category, subcategory, test, result_type, test_detail
                create_json_stub(new_map, category, subcategory, test, result_type,test_detail)

            elif len(token_list)==2:
                category = token_list[0].strip()
                test = '_'.join(token_list[1].strip().split('_')[1:])

                if items_map.has_key(category) is False:
                    items_map[category]  = set()

                items_map[category].add(test)

                create_json_stub(new_map, category, "", test, result_type, test_detail)

            else:
                print "ABORT: Never saw this format: " + token_list
                sys.exit(1)

    # Print JSON
#    print json.dumps(final_dict, sort_keys=True, indent=4)


def readable_text(feature):
    if feature.startswith('set_field__'):
        return "Set_Field:: " + feature[11:]
    if feature=="COPY_TTL_IN":
        return feature + " (Copy TTL inwards)"
    if feature=="COPY_TTL_OUT":
        return feature + " (Copy TTL outwards)"
    if feature=="OUTPUT":
        return feature + " (Output to switchport(s))"
    if feature.startswith("IPV4_SRC") or feature.startswith("IPV4_DST") or feature.startswith("IPV6_SRC") or feature.startswith("IPV6_DST"):
        strlist = feature.split('_')
        return strlist[0] + "_ADDR_" + strlist[1]

    return feature



def interpret_result(feature, result):
    item_text = readable_text(feature)
    if result=='':
        return item_text, NA_SYMBOL
    final_result = SUCCESS_SYMBOL
    subresults = {}
    exclude_list = ['mpls','arp','vlan','itag']

    ARP_List = ['ARP_SHA', 'ARP_TPA', 'ARP_OP', 'ARP_THA', 'ARP_SPA']
    MPLS_List = ['PUSH_MPLS', 'POP_MPLS', 'SET_MPLS_TTL', 'MPLS_TC', 'DEC_MPLS_TTL', 'MPLS_LABEL', 'MPLS_BOS',]
    VLAN_List = ['PUSH_VLAN', 'POP_VLAN','VLAN_PCP','VLAN_VID'] 
    PBB_List = ['PUSH_PBB', 'POP_PBB', 'PBB_ISID']

    is_PBB = False
    is_MPLS = False
    is_PBB = False

    # Exclude list
    ## ARP-related
    for i in ARP_List:
        if feature.count(i) > 0:
            exclude_list.remove('arp')
            break
    for i in MPLS_List:
        if feature.count(i) > 0:
            exclude_list.remove('mpls')
            break
    for i in VLAN_List:
        if feature.count(i) > 0:
            exclude_list.remove('vlan')
            break
    for i in PBB_List:
        if feature.count(i) > 0:
            exclude_list.remove('itag')
            break

    for k in result:
        # Get rid of tests that forward packet to controller
        if k.split('-->')[1].count("output:CONTROLLER") > 0:
            continue
        if exclude_test_numbers.count(int(k[:3])) > 0:
            continue

        # Get rid of tests in exclude_list
        genlist = k.split('-->')[0].split('/')
        eth_type = genlist[1]
        if exclude_list.count(eth_type) > 0:
            continue

        # If not ipv6 test, get rid of ipv6 tests
        if feature.lower().count('ipv6') == 0 and feature.lower().count('icmpv6') == 0:
            if k.split('-->')[0].count('ipv6') > 0:
                continue

#        if len(genlist) > 2:
#            if exclude_list.count(genlist[2]) > 0:
#                continue
 
        result_block = result[k]
        if result_block['Result'].has_key("OK"):
            subresults[k] = "OK"
        else:
            subresults[k] = "ERROR"

    # If there are two or more tests for a test_item, 
    # make sure all tests have passed.  
    # We can enforce this by existing as soon as we see an "ERROR" 
    # in above loop. However, we do it here after the loop for better
    # code readability and extensibility (when we decide to do something different
    # when making the final decision about pass or fail).
    final_result = SUCCESS_SYMBOL
    for s in subresults:
        if subresults[s] != "OK":
#            print feature
#            print len(subresults), ":", subresults
            final_result = FAIL_SYMBOL
            break
            
#    print feature
#    print len(subresults), ":", subresults
    
    
    return item_text, final_result


def combine_maps(input_dir, output_dir):
    final_map_list = []
    final_map_list_simplified = []

    vendor_map_list = []
    vendor_maps = {}
    items_map = {}

    vendor_list = []

    # Read directory, get all vendors
    for f in os.listdir(input_dir):
        if f.endswith(".pkl") is False:
            continue

        # Read each, make json. Build list of categories and items too.
        new_map = {}
        cutidx = f.find(".")
        new_map['name'] = f[:cutidx]
        vendor_list.append(f[:cutidx])

        report_dict = pickle.load(open(input_dir + f, 'rb'))
        jsonize(report_dict, new_map, items_map )
        vendor_map_list.append(new_map)
        vendor_maps[f[:cutidx]] = new_map


    # With knowledge of vendors, list of categories and items, read maps.
    for cat in items_map:
#        print cat
 
        # Sort item_list once        
        # (item_map[cat] is originally a HashSet, so needs sorting.)
        item_list = []
        tmplist = items_map[cat]
        text_to_feature_map = {}
        for i in tmplist:
            text = readable_text(i)
            item_list.append(text)
            text_to_feature_map[text] = i

        for it in sorted(item_list):
#            print "    ",it
            item = text_to_feature_map[it]

            this_map = {}
            this_map['Category'] = cat.title()
            this_map['Feature'] = item

            this_map_simplified = {}
            this_map_simplified['Category'] = cat.title()
            item_text = ""

            # List of vendors
            for v in vendor_list:

                result = ""
                if vendor_maps[v][cat].has_key(item) is True:
                    result = vendor_maps[v][cat][item]
                else:
                    sub_test = item.split('__')
                    if vendor_maps[v][cat].has_key(sub_test[0]) is True:
                        if vendor_maps[v][cat][sub_test[0]].has_key(sub_test[1]) is True:
                            result = vendor_maps[v][cat][sub_test[0]][sub_test[1]] 
                        else:
                            print "Abort: Item (%s - %s) is not found" % (sub_test[0], sub_test[1])
                    else: 
                        print "Abort: Item (%s) is not found" % (sub_test[0])

#                print "              ",result
#                if v=='cisco':#TODO
#                     interpret_result(item,result)
                item_text, final_result = interpret_result(item,result)
                this_map[v] = result

                result_simple = final_result
                this_map_simplified["swt-" + v.title()] = result_simple

            # Append to list           
            final_map_list.append(this_map)
            final_map_list_simplified.append(this_map_simplified)

            this_map_simplified['Feature'] = item_text

    return final_map_list,final_map_list_simplified

def main():
 
    # Parse arguments
    parser = OptionParser()
    parser.add_option("-i", "--input", dest="input_", help="Input file or directory", metavar="FILE")
    parser.add_option("-o", "--output", dest="output_file", help="Output file", metavar="FILE")
    parser.add_option("-j", "--jsonfile", dest="json_file", help="Existing json file", metavar="FILE")

    (options, args) = parser.parse_args()

    # output file
    if options.output_file is None:
        print "No output file. Abort."
        parser.print_help()
        sys.exit(1)

    # Input file
    input_dir = ""
    if os.path.isfile(options.input_) is True:
        if options.input_ is None:
            print "No input file. Abort."
            parser.print_help()
            sys.exit(1)
        else:
            report_dict = pickle.load(open(options.input_, 'rb'))

        # JSONIZE     
        jsonize(report_dict)

#        # Save json file 
#        fd = open(options.output_file,'wb')
#        json.dump(final_dict,fd)
#        fd.close()


    # Read directory
    elif os.path.isdir(options.input_) is True:
        input_dir = python_api.check_directory_and_add_slash(options.input_)
        final_map_list,final_map_list_simplified = combine_maps(input_dir, options.output_file)

        # Print JSON
#        print json.dumps(final_map_list, sort_keys=True, indent=4)
#        print json.dumps(final_map_list_simplified, sort_keys=True, indent=4)

        # Save json file 
#        fd = open(options.output_file,'wb')
#        json.dump(final_map_list,fd)
#        fd.close()
#        fd = open(options.output_file + ".simple",'wb')
#        json.dump(final_map_list_simplified,fd)
#        fd.close()

        # Combined if existing JSON file is given
        if options.json_file is not None:
            combined_json = sum_up_with_existing_json(options.json_file, final_map_list_simplified)
            print json.dumps(combined_json , sort_keys=True, indent=4)
            fd = open(options.output_file + ".simple_combine_usethis",'wb')
            json.dump(combined_json ,fd)
            fd.close()


        
if __name__ == '__main__':
    main()

