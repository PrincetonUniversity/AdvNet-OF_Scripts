################################################################
# Ryu Application:
#   App for fetching attached switch's features and capabilities
#  - Author: Joon Kim (joonk@princeton.edu)
################################################################

from ryu.base import app_manager 
from ryu.controller import ofp_event
from ryu.controller.handler import CONFIG_DISPATCHER, MAIN_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.ofproto import ofproto_v1_3

from ryu.lib.packet import packet
from ryu.lib.packet import ethernet
from ryu.lib.packet import ipv4


################################### 
# Switch feature request
################################### 


class SwitchInquisitor(app_manager.RyuApp):

    OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION]

    def __init__(self, *args, **kwargs):
        super(SwitchInquisitor, self).__init__(*args, **kwargs)
        self.mac_to_port = {}

        ## Information
        info_str = "\n\n==========================================\n"
        info_str += " Notes\n"
        info_str += "==========================================\n"
        info_str += "* Number of buffers: Maximum number of packets the switch can buffer when sending packets to the controller using packet-in messages\n\n"
        info_str += "* Number of tables: The number of tables supported by the switch. Each table might have different capabilities and features. Further details of each table will be displayed later.\n\n"
        info_str += "* Auxiliary ID: Indication of this switch-controller connection is an auxiliary connection (=non-zero value) or not(=0).\n\n"
        info_str += "* Port block: Switch detects topology loops and blocks ports accordingly to prevent packet loops, without OpenFlow running (e.g., with 802.1D Spanning tree mechanism). If not set, programmer should add mechanisms to OpenFlow control application to prevent packet loops when topology has loops.\n"
        info_str += "==========================================\n\n"

 
        # Save to file
        self.fd = open("./switches_info.txt", 'w+')
        self.fd.write(info_str)
        self.fd.close()


    ## Handle switch feature event, which comes after a switch joins        
    @set_ev_cls(ofp_event.EventOFPSwitchFeatures, CONFIG_DISPATCHER)
    def switch_features_handler(self, ev):

        overview_str = ""
        capab_str = ""
        info_str = ""

        datapath = ev.msg.datapath
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        # Overview of features        
        dpid = str(hex(ev.msg.datapath_id)[2:]).zfill(16)
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
        capab_str += "==========================================\n\n"

        # Send table feature request
        ## OFPTableFeaturesStatsRequest
#        req = parser.OFPTableFeaturesStatsRequest(datapath,0)
#        datapath.send_msg(req)

#        ## OFPGroupDescStatsRequest
#        req = parser.OFPGroupDescStatsRequest(datapath=datapath,flags=0)
#        datapath.send_msg(req)
#
#        ## OFPGroupFeaturesStatsRequest
#        req = parser.OFPGroupFeaturesStatsRequest(datapath,0)
#        datapath.send_msg(req)
#
#        ## OFPMeterFeaturesStatsRequest
#        req = parser.OFPMeterFeaturesStatsRequest(datapath,0)
#        datapath.send_msg(req)
#
#        ## OFPMeterConfigStatsRequest
#        req = parser.OFPMeterConfigStatsRequest(datapath,0, ofproto.OFPM_ALL)
#        datapath.send_msg(req)
#
#        # Print
#        print overview_str,capab_str,info_str
#
#        fd = open("./switches_info.txt", 'a+')
#        fd.write(overview_str+capab_str)
#        fd.close()
#

    ## Handle table feature reply
    @set_ev_cls(ofp_event.EventOFPTableStatsReply, MAIN_DISPATCHER)
    def table_features_handler(self, ev):
        print "HAHAH"
        pass

