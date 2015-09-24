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

final_dict = {}

def recursive_existence_check(the_map, the_list, level):
    if level==len(the_list)-1 or the_map.has_key(the_list[level]) is False:
        return level
    else:
        the_map = the_map[the_list[level]]
        return recursive_existence_check(the_map, the_list, level+1)

def find_level_of_no_entry(the_list):
    level = recursive_existence_check(final_dict, the_list, 0)

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


def create_json_stub(category, subcategory, test, outcome):
    test_item = '_'.join(test.split('_')[1:])

#    if subcategory=="" and (category == 'action'):
    print category, subcategory, test_item, outcome
    if subcategory=="":
        the_list = [category, test_item, outcome]
    else: 
        the_list = [category, subcategory, test_item, outcome]
    level = find_level_of_no_entry(the_list)

    if level==len(the_list)-1:
        return

    new_map  = create_map_with_list(the_list[level+1:])

    # Store to right level   
    map_ref = final_dict
    for idx,i in enumerate(the_list):
        if idx==level:
            map_ref[i] = new_map
            break
        else:
            map_ref = map_ref[i]
    

def jsonize(report_dict):
    for result_type in sorted(report_dict.keys()):
        tests_list = report_dict[result_type]
#        print report_dict["OK"]
        for file_desc, test_detail in tests_list:
            token_list = file_desc.split(":")
    
            if len(token_list)==3:
                category = token_list[0].strip()
                subcategory = token_list[1].strip()
                test = token_list[2].strip()

                create_json_stub(category, subcategory, test, result_type)

            elif len(token_list)==2:
                category = token_list[0].strip()
                test = token_list[1].strip()

                create_json_stub(category, "", test, result_type)

            else:
                print "Never saw this format: " + token_list
                print "Abort."
                sys.exit(1)

    print json.dumps(final_dict, sort_keys=True, indent=4)
        
def main():
 
    # Parse arguments
    parser = OptionParser()
    parser.add_option("-i", "--input", dest="input_file",
                      help="Input file", metavar="FILE")

    (options, args) = parser.parse_args()

    # input file
    if options.input_file is None:
        print "No input file. Abort."
        sys.exit(1)
    else:
        report_dict = pickle.load(open(options.input_file, 'rb'))

    jsonize(report_dict)
#    print report_dict.keys()
        
if __name__ == '__main__':
    main()

