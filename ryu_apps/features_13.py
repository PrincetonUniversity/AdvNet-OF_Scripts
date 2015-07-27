################################################################
# Ryu Application:
#   App for fetching attached switch's features and capabilities
#  - Author: Joon Kim (joonk@princeton.edu)
################################################################

import os,sys,math
from ryu.base import app_manager 
from ryu.controller import ofp_event
from ryu.controller.handler import CONFIG_DISPATCHER, MAIN_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.ofproto import ofproto_v1_0
from ryu.ofproto import ofproto_v1_2
from ryu.ofproto import ofproto_v1_3

from ryu.lib.packet import packet
from ryu.lib.packet import ethernet
from ryu.lib.packet import ipv4
from ryu.lib import ofctl_v1_0
from ryu.lib import ofctl_v1_2
from ryu.lib import ofctl_v1_3
from ryu.lib import dpid as dpidlib
import ref as reflib

supported_ofctl = {
    ofproto_v1_0.OFP_VERSION: ofctl_v1_0,
    ofproto_v1_2.OFP_VERSION: ofctl_v1_2,
    ofproto_v1_3.OFP_VERSION: ofctl_v1_3,
}


################################### 
# Switch feature request
################################### 


class SwitchInquisitor(app_manager.RyuApp):

    OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION]

    def __init__(self, *args, **kwargs):
        super(SwitchInquisitor, self).__init__(*args, **kwargs)
        self.mac_to_port = {}

        ## Info files
        self.combined_str = ""
        self.overview_str = ""  

        # Check if "results" folder is present.
        if os.path.isdir("./results") is False:
            ans =  raw_input("\n./results directory does not exist. Creat one now (y or n)?: ")
            if ans=="y":
                os.makedirs("./results")
            else:
                print "Answered n or incorrect input. Aborting...\n"
                sys.exit(1)

        createReadme()

    ## Handle switch feature event, which comes after a switch joins        
    @set_ev_cls(ofp_event.EventOFPSwitchFeatures, CONFIG_DISPATCHER)
    def switch_features_handler(self, ev):

        overview_str = ""
        capab_str = ""

        datapath = ev.msg.datapath
        print "version:",ev.msg.version
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        # Check version
        if ev.msg.version!=4:
            print "This switch is not OpenFlow version v1.3. Skip"
            return


        # Overview of features        
        dpid = dpidlib.dpid_to_str(ev.msg.datapath_id)
#       dpid = str(hex(ev.msg.datapath_id)[2
        n_buf = str(ev.msg.n_buffers)
        n_tables = str(ev.msg.n_tables)
        aux_id = str(ev.msg.auxiliary_id)
        capab_int = int(ev.msg.capabilities)
        capab_b_str = str(bin(capab_int))[2:]

        overview_str = "\n\n==========================================\n"
        overview_str += " Overview: " + dpid + "\n"
        overview_str += "==========================================\n"

        overview_str += "DatapathId(hex):     "+dpid+"\n" +          \
                        "Number of buffers:   "+n_buf+"\n"+       \
                        "Number of tables:    "+n_tables+"\n"+        \
                        "Auxiliary ID:        "+aux_id+"\n"+            \
                        "Capabilities:        "+capab_b_str+"\n"             

        ## Capabilities
        flow_stat = "yes" if ((capab_int) & 1)==1 else "no"; capab_int = capab_int >> 1;
        table_stat = "yes" if ((capab_int) & 1)==1 else "no"; capab_int = capab_int >> 1; 
        port_stat = "yes" if ((capab_int) & 1)==1 else "no"; capab_int = capab_int >> 1; 
        group_stat = "yes" if ((capab_int) & 1)==1 else "no"; capab_int = capab_int >> 1; 
        ip_reasm = "yes" if ((capab_int) & 1)==1 else "no"; capab_int = capab_int >> 1; 
        queue_stat = "yes" if ((capab_int) & 1)==1 else "no"; capab_int = capab_int >> 1; 
        port_block = "yes" if ((capab_int) & 1)==1 else "no"
    
        capab_str = "    Flow stats supported:      "+flow_stat+"\n" +            \
                    "    Table stats supported:     "+table_stat+"\n" +          \
                    "    Port stats supported:      "+port_stat+"\n" +          \
                    "    Group stats supported:     "+group_stat+"\n" +          \
                    "    IP reassembly supported:   "+ip_reasm+"\n" +          \
                    "    Queue stats supported:     "+queue_stat+"\n" +          \
                    "    Port block on:             "+port_block+"\n"
        capab_str += "==========================================\n"

        # Switch features and capabilities - overview
        self.combined_str += (overview_str + capab_str)
        fd = open("./results/switch_" + dpid + "_v13_overview.txt", 'w+')
        fd.write(overview_str+capab_str)
        fd.close()

        ## Send table feature request
        ## OFPTableFeaturesStatsRequest
        req = parser.OFPTableFeaturesStatsRequest(datapath,0)
        datapath.send_msg(req)

        ## Send group table feature request
        ## OFPGroupFeaturesStatsRequest
        req = parser.OFPGroupFeaturesStatsRequest(datapath)
        datapath.send_msg(req)

        ## Send meter table feature request
        ## OFPMeterFeaturesStatsRequest
        req = parser.OFPMeterFeaturesStatsRequest(datapath,0)
        datapath.send_msg(req)

        ## Send description statistics request
        ## OFPTableFeaturesStatsRequest
        req = parser.OFPDescStatsRequest(datapath,0)
        datapath.send_msg(req)


        # Create (or truncate) files in advance
        fd = open("./results/switch_" + dpid + "_v13_table.txt", 'w+')
        fd.write("\n")
        fd.close()
        fd = open("./results/switch_" + dpid +"_v13_group.txt", 'w+')
        fd.write("\n")
        fd.close()
        fd = open("./results/switch_" + dpid + "_v13_meter.txt", 'w+')
        fd.write("\n")
        fd.close()


    ## Handle group table feature reply
    @set_ev_cls(ofp_event.EventOFPGroupFeaturesStatsReply, MAIN_DISPATCHER)
    def group_features_handler(self, ev):
        group_str = ""
        gstat = ev.msg.body
        types = gstat.types
        cap = gstat.capabilities
        actions = gstat.actions

        group_str = "\n\n==========================================\n"
        group_str += " Group Table Feature: \n"
        group_str += "==========================================\n"

        group_str += "* Max num. of groups for each group type:\n" + \
                      ("    - All:\t" + str(gstat.max_groups[0])).expandtabs(25) + "\n" + \
                      ("    - Select:\t" + str(gstat.max_groups[1])).expandtabs(25) + "\n" + \
                      ("    - Indirect:\t" + str(gstat.max_groups[2])).expandtabs(25) +"\n" + \
                      ("    - Fast Failover:\t" + str(gstat.max_groups[3])).expandtabs(25) + "\n\n"

        group_str += "* Types (o:yes, x:no): " + str(bin(types))[2:].zfill(4) + "\n"
        group_str += ("    o" if ((cap) & 1)==1 else "    x") + " All\n"
        types = types >> 1;
        group_str += ("    o" if ((cap) & 1)==1 else "    x") + " Select\n"
        types = types >> 1;
        group_str += ("    o" if ((cap) & 1)==1 else "    x") + " Indirect\n"
        types = types >> 1;
        group_str += ("    o" if ((cap) & 1)==1 else "    x") + " Fast failover\n\n"

        group_str += "* Capabilities (o:yes, x:no): " + str(bin(cap))[2:].zfill(4) + "\n"
        group_str += ("    o" if ((cap) & 1)==1 else "    x") + " Weight for select groups\n"
        cap = cap >> 1;
        group_str += ("    o" if ((cap) & 1)==1 else "    x") + " Liveness for select groups\n"
        cap = cap >> 1;
        group_str += ("    o" if ((cap) & 1)==1 else "    x") + " Chaining groups\n"
        cap = cap >> 1;
        group_str += ("    o" if ((cap) & 1)==1 else "    x") + " Check chanining for loops and delete\n\n"

        group_str += "* Supported Actions Bitmap: " + "\n" + \
                      ("    - All:\t" + str(bin(actions[0]))[2:].zfill(28)).expandtabs(25) + "\n" + \
                      ("    - Select:\t" + str(bin(actions[1]))[2:].zfill(28)).expandtabs(25) + "\n" + \
                      ("    - Indirect:\t" + str(bin(actions[2]))[2:].zfill(28)).expandtabs(25) + "\n" + \
                      ("    - Fast failover:\t" + str(bin(actions[3]))[2:].zfill(28)).expandtabs(25) + "\n"
        group_str += "==========================================\n\n"

        group_dict = {}
        for j in range(4):
            group_dict[j] = []
            for i in range(28):
                bit = long(actions[j]) & long(math.pow(2,i))
                if bit>=1: 
                    group_dict[j].append(i)

        group_str += "* Supported Actions Bitmap Explained (o: yes, x: no)\n"
        group_str += "  -- All (A), Select (S), Indirect (I), Fast failover (F)\n"
        group_str += "  -- Usually, the binary values should be identical among different types.\n"
        group_str += "  -- This action list starts from right-most bit (2^0) of above binary values.\n"
        group_str += "  -- There are no actions defined in the spec for bits from 2^1 to 2^10, inclusive.\n\n"
#        group_str += action_print(action_id_list) + "\n"
        group_str += " A  S  I  F \n"
        group_str += "------------\n"
        group_str += action_print_types(group_dict) + "\n"

        
        # Save 
        fd = open("./results/switch_" + dpidlib.dpid_to_str(ev.msg.datapath.id) + "_v13_group.txt", 'a+')
        fd.write(group_str)
        fd.close()

        # Combined
        self.combined_str += (group_str)
 


    ## Handle meter table feature reply
    @set_ev_cls(ofp_event.EventOFPMeterFeaturesStatsReply, MAIN_DISPATCHER)
    def meter_features_handler(self, ev):
        for stat in ev.msg.body:
            metmax = stat.max_meter
            metbtype = stat.band_types
            metcap = stat.capabilities
            metband = stat.max_bands
            metcol = stat.max_color


            meter_str = "\n\n==========================================\n"
            meter_str += " Meter Table Feature: \n"
            meter_str += "==========================================\n"

            meter_str += ("* Maximum number of meters:\t" + str(metmax)).expandtabs(40) + " \n\n"
            meter_str += ("* Supported band types (o:yes, x:no):\t" + str(bin(metbtype))[2:].zfill(4)).expandtabs(40)  + " \n"
            meter_str += ("    o" if ((metcap) & 1)==1 else "    x") + " Drop packet\n"
            metcap = metcap >> 1
            meter_str += ("    o" if ((metcap) & 1)==1 else "    x") + " Remark DSCP in the IP heaader\n"
            metcap = metcap >> 1
            meter_str += ("    o" if ((metcap>>14) & 1)==1 else "    x") + " Experimenter band\n\n"

            meter_str += ("* Supported meter flags (o:yes, x:no):\t" + str(bin(metcap))[2:].zfill(4)).expandtabs(40) + " \n"
            meter_str += ("    o" if ((metcap) & 1)==1 else "    x") + " Rate value in Kbps: \n"
            metcap = metcap >> 1
            meter_str += ("    o" if ((metcap) & 1)==1 else "    x") + " Rate value in packets/sec \n"
            metcap = metcap >> 1
            meter_str += ("    o" if ((metcap) & 1)==1 else "    x") + " Do burst size\n"
            metcap = metcap >> 1
            meter_str += ("    o" if ((metcap) & 1)==1 else "    x") + " Collect statistics \n\n"

            meter_str += ("* Maximum number of bands per meter:\t" + str(metband)).expandtabs(40) + " \n\n"
            meter_str += ("* Maximum color value:\t" + str(metcol)).expandtabs(40) + " \n"
 
            # Save 
            fd = open("./results/switch_" + dpidlib.dpid_to_str(ev.msg.datapath.id) + "_v13_meter.txt", 'a+')
            fd.write(meter_str)
            fd.close()

            # Combined
            self.combined_str += (meter_str)


      
    ## Handle desc stat reply
    @set_ev_cls(ofp_event.EventOFPDescStatsReply, MAIN_DISPATCHER)
    def switch_desc_handler(self, ev):
        switch_str = ""
        stats = ev.msg.body

        dp_desc = stats.dp_desc
        hw_desc = stats.hw_desc
        mfr_desc = stats.mfr_desc
        serial_num = stats.serial_num
        sw_desc = stats.sw_desc


        switch_str = "\n\n==========================================\n"
        switch_str += " Switch Description: \n"
        switch_str += "==========================================\n"
        switch_str += "* Manufacturer description: \t" + mfr_desc + "\n" 
        switch_str += "* Hardware description: \t" + hw_desc + "\n"
        switch_str += "* Software description: \t" + sw_desc + "\n"
        switch_str += "* Serial number:         \t" + serial_num + "\n"
        switch_str += "* Datapath description: \t" + dp_desc + "\n"
        switch_str += "==========================================\n\n"

        # Save 
        fd = open("./results/switch_" + dpidlib.dpid_to_str(ev.msg.datapath.id) + "_v13_extra.txt", 'a+')
        fd.write(switch_str)
        fd.close()

        # Combined
        self.combined_str += (switch_str)

        # Last handle.. So save combined string
        fd = open("./results/switch_" + dpidlib.dpid_to_str(ev.msg.datapath.id) + "_v13_combined.txt", 'a+')
        fd.write(self.combined_str)
        fd.close()
 

    ## Handle table feature reply
    @set_ev_cls(ofp_event.EventOFPTableFeaturesStatsReply, MAIN_DISPATCHER)
    def table_features_handler(self, ev):

        feature_str = ""
        prop_str = ""

        ## Fields
        print ev.msg.datapath
        table_list = ev.msg.body
        for t in table_list:
            
            table_id = t.table_id
            name = t.name
            metadata_match = t.metadata_match
            metadata_write = t.metadata_write
            #config = t.config   ## Bitmap that is provided for backward compability in OF. 
            max_entries = t.max_entries
            properties = t.properties


            #
            feature_str = "\n\n==========================================\n"
            feature_str += " Table Feature: " + str(table_id) + "\n"
            feature_str += "==========================================\n"
    
            feature_str +=  "Table Id:             "+str(table_id)+"\n" +          \
                            "Name:                 "+str(name)+"\n"+       \
                            "Metadata_match:       "+str(hex(metadata_match))+"\n"+        \
                            "Metadata_write:       "+str(hex(metadata_write))+"\n"+            \
                            "Max entries:          "+str(max_entries)+"\n"
    
            prop_str = self.property_parser(properties)

        # Save
        fd = open("./results/switch_" + dpidlib.dpid_to_str(ev.msg.datapath.id) + "_v13_table.txt", "a+")
        fd.write(feature_str + prop_str)
        fd.close()

        # Combined
        self.combined_str += (feature_str + prop_str)


    def property_parser(self,prop_list):
        prop_str = "Properties:\n"
        prop_str += "==========================================\n"

        for p in prop_list:
            p_type = p.type

            # Instructions
            if p_type==ofproto_v1_3.OFPTFPT_INSTRUCTIONS:
#               or p_type==ofproto_v1_3.OFPTFPT_INSTRUCTIONS_MISS:
                prop_str += "* Possible Instructions (o: yes, x: no)\n" 
                inst_id_list = p.instruction_ids
                inst_type_list = [x.type for x in inst_id_list]

                for idx,i in enumerate(reflib.inst_str_list): 
                    if (idx+1) in inst_type_list:
                        prop_str += ("  o "+ i + ":\tyes\n").expandtabs(20)
                    else:
                        prop_str += ("  x "+ i + ":\tno\n").expandtabs(20)
                    
                prop_str += "\n"

            # Next table
            elif p_type==ofproto_v1_3.OFPTFPT_NEXT_TABLES:
#            elif p_type==ofproto_v1_3.OFPTFPT_NEXT_TABLES or p_type==ofproto_v1_3.OFPTFPT_NEXT_TABLES_MISS:
                prop_str += "* Possible GOTO Table IDs\n"
                next_id_list = sorted(p.table_ids)
                prop_str += "  - Table ID lists: " + str(next_id_list) + "\n\n"

            # Write/Apply actions
            elif p_type==ofproto_v1_3.OFPTFPT_WRITE_ACTIONS:
                prop_str += "* Possible Write Actions (o: yes, x: no)\n"
                prop_str += (write_apply_action_print(p.action_ids) + "\n") 
            elif p_type==ofproto_v1_3.OFPTFPT_APPLY_ACTIONS:
                prop_str += "* Possible Apply Actions (o: yes, x: no)\n"
                prop_str += (write_apply_action_print(p.action_ids) + "\n")

            # Match, wildcard, write/apply setfield
            elif p_type==ofproto_v1_3.OFPTFPT_MATCH:
                prop_str += "* Possible Match Fields (only supported fields are listed)\n"
                prop_str += (match_print(p.oxm_ids) + "\n")
            elif p_type==ofproto_v1_3.OFPTFPT_WILDCARDS:
                prop_str += "* Possible Wildcard Fields (only supported fields are listed)\n"
                prop_str += (match_print(p.oxm_ids) + "\n")
            elif p_type==ofproto_v1_3.OFPTFPT_WRITE_SETFIELD:
                prop_str += "* Possible Write SetFields (only supported fields are listed)\n"
                prop_str += (match_print(p.oxm_ids) + "\n")
            elif p_type==ofproto_v1_3.OFPTFPT_APPLY_SETFIELD:
                prop_str += "* Possible Apply SetFields (only supported fields are listed)\n"
                prop_str += (match_print(p.oxm_ids) + "\n")
                
        return prop_str                         


def action_print_types(group_dict):
    return_str = ""
    for k in reflib.action_map:
        for j in group_dict:
            if k in group_dict[j]:
                return_str += (" o ")
            else:
                return_str += (" x ")
                
        return_str += (reflib.action_map[k] + "\n").expandtabs(65)

    return return_str


def action_print(action_type_list):
    return_str = ""
    for k in reflib.action_map:
        if k in action_type_list: 
            return_str += ("  o " + reflib.action_map[k] + ":\tyes\n").expandtabs(65)
        else:
            return_str += ("  x " + reflib.action_map[k] + ":\tno\n").expandtabs(65)
        
    return return_str

def write_apply_action_print(action_id_list):
    action_type_list = [x.type for x in action_id_list]
    return action_print(action_type_list)


def match_print(oxm_id_list):
    return_str = ""
    return_str += ("  - Field\tBitmasking supported\n").expandtabs(20)
    for o in oxm_id_list:
        if o.hasmask==1:
            return_str += ("  " + o.type + "\tyes\n").expandtabs(20)
        else:
            return_str += ("  " + o.type + "\tno\n").expandtabs(20)
    return return_str



def createReadme():

    ## Information
    info_str = "\n\n==========================================\n"
    info_str += " Notes\n"
    info_str += "==========================================\n"
    info_str += "* Number of buffers: Maximum number of packets the switch can buffer when sending packets to the controller using packet-in messages\n\n"
    info_str += "* Number of tables: The number of tables supported by the switch. Each table might have different capabilities and features. Further details of each table will be displayed later.\n\n"
    info_str += "* Auxiliary ID: Indication of this switch-controller connection is an auxiliary connection (=non-zero value) or not(=0).\n\n"
    info_str += "* Port block: Switch detects topology loops and blocks ports accordingly to prevent packet loops, without OpenFlow running (e.g., with 802.1D Spanning tree mechanism). If not set, programmer should add mechanisms to OpenFlow control application to prevent packet loops when topology has loops.\n"
    info_str += "==========================================\n"

    ## Table Information
    table_info_str = "\n\n==========================================\n"
    table_info_str += " Table Notes\n"
    table_info_str += "==========================================\n"
    table_info_str += "* Metadata_match: Fields that can be matched in metadata field.\n\n"
    table_info_str += "* Metadata_write: Fields that can be written in metadata field.\n\n"
    table_info_str += "* Properties: Property list \n\n"
    table_info_str += "==========================================\n\n"

    # Create (or truncate) file and save initial notes
    fd = open("./results/README_v13", 'w+')
    fd.write(info_str + table_info_str)
    fd.close()

