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


class SwitchInquisitor_V10(app_manager.RyuApp):

    OFP_VERSIONS = [ofproto_v1_0.OFP_VERSION]

    def __init__(self, *args, **kwargs):
        super(SwitchInquisitor_V10, self).__init__(*args, **kwargs)

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
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        # Overview of features        
        dpid = dpidlib.dpid_to_str(ev.msg.datapath_id)
        n_buf = str(ev.msg.n_buffers)
        n_tables = str(ev.msg.n_tables)
        capab_int = int(ev.msg.capabilities)
        capab_b_str = str(bin(capab_int))[2:]
        actions_int = int(ev.msg.actions)
        actions_str = str(bin(actions_int))[2:]
        ports = str(ev.msg.ports)
        n_ports = ((ev.msg.msg_len - ofproto.OFP_SWITCH_FEATURES_SIZE) / ofproto.OFP_PHY_PORT_SIZE)

        overview_str = "\n\n==========================================\n"
        overview_str += " Overview: " + dpid + "\n"
        overview_str += "==========================================\n"

        overview_str += "DatapathId(hex):     "+dpid+"\n" +          \
                        "Number of buffers:   "+n_buf+"\n"+       \
                        "Number of tables:    "+n_tables+"\n"+        \
                        "Capabilities:        "+str(bin(capab_int))[2:].zfill(8)+"\n"             
#                        "Capabilities:        "+capab_b_str+"\n"             

        ## Capabilities
        flow_stat = "yes" if ((capab_int) & 1)==1 else "no"; capab_int = capab_int >> 1;
        table_stat = "yes" if ((capab_int) & 1)==1 else "no"; capab_int = capab_int >> 1; 
        port_stat = "yes" if ((capab_int) & 1)==1 else "no"; capab_int = capab_int >> 1; 
        stp_feat = "yes" if ((capab_int) & 1)==1 else "no"; capab_int = capab_int >> 1; 
        reserved = "-" ; capab_int = capab_int >> 1; 
        ip_reasm = "yes" if ((capab_int) & 1)==1 else "no"; capab_int = capab_int >> 1; 
        queue_stat = "yes" if ((capab_int) & 1)==1 else "no"; capab_int = capab_int >> 1; 
        arp_match = "yes" if ((capab_int) & 1)==1 else "no"
    
        capab_str = "    Flow stats supported:        "+flow_stat+"\n" +            \
                    "    Table stats supported:       "+table_stat+"\n" +          \
                    "    Port stats supported:        "+port_stat+"\n" +          \
                    "    802.1d spanning tree:        "+stp_feat+"\n" +          \
                    "    Reserved (=0. not used):     "+reserved+"\n" +          \
                    "    IP reassembly supported:     "+ip_reasm+"\n" +          \
                    "    Queue stats supported:       "+queue_stat+"\n" +          \
                    "    Match IP address in ARP pkt: "+arp_match+"\n"
        # Actions
#        action_str = "\nActions:              "+actions_str+"\n"
        action_str = "\nActions:              "+str(bin(actions_int))[2:].zfill(28)+"\n"
        action_str += " * Supported Actions Bitmap Explained (o: yes, x: no)\n"
        action_list = []
        for i in range(28):
            bit = long(actions_int) & long(math.pow(2,i))
            if bit>=1: 
                action_list.append(i)
        action_str += action_print(action_list) + "\n"

        # Ports
        offset = ofproto.OFP_SWITCH_FEATURES_SIZE
        port_list = []
        port_str = "Number of Ports:    " + str(n_ports) + "\n"
        for i in range(n_ports):
            port = parser.OFPPhyPort.parser(ev.msg.buf, offset)
            port_list.append(port.port_no)
            offset += ofproto.OFP_PHY_PORT_SIZE
        port_str += "  - Ports: " + str(sorted(port_list)) +"\n"
        port_str += "==========================================\n"
        # Switch features and capabilities - overview
        self.combined_str += (overview_str + capab_str + action_str + port_str)
        fd = open("./results/switch_" + dpid + "_v10_overview.txt", 'w+')
        fd.write(overview_str+capab_str + action_str+port_str)
        fd.close()

        ## Send description statistics request
        ## OFPTableFeaturesStatsRequest
        req = parser.OFPDescStatsRequest(datapath,0)
        datapath.send_msg(req)

        # Create (or truncate) files in advance
        fd = open("./results/switch_" + dpid + "_v10_extra.txt", 'w+')
        fd.write("\n")
        fd.close()


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
        fd = open("./results/switch_" + dpidlib.dpid_to_str(ev.msg.datapath.id) + "_v10_extra.txt", 'a+')
        fd.write(switch_str)
        fd.close()

        # Combined
        self.combined_str += (switch_str)

        # Last handle.. So save combined string
        fd = open("./results/switch_" + dpidlib.dpid_to_str(ev.msg.datapath.id) + "_v10_combined.txt", 'a+')
        fd.write(self.combined_str)
        fd.close()
       

def action_print(action_list):
    return_str = ""
    for k in reflib.action_map_v10:
        if k in action_list: 
            return_str += ("  o " + reflib.action_map_v10[k] + ":\tyes\n").expandtabs(40)
        else:
            return_str += ("  x " + reflib.action_map_v10[k] + ":\tno\n").expandtabs(40)
        
    return return_str


def createReadme():

    ## Information
    info_str = "\n\n==========================================\n"
    info_str += " Notes\n"
    info_str += "==========================================\n"
    info_str += "* "
    info_str += "==========================================\n"

    # Create (or truncate) file and save initial notes
    fd = open("./results/README_v10", 'w+')
    fd.write(info_str)
    fd.close()

