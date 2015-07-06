################################################################
# Ryu Application:
#   Basic learning switch with mirroring to port #2 
#  - Author: Joon Kim (joonk@princeton.edu)
################################################################

################################################################
# * If using Mininet, 
#   - Instantiate single switch with 4 hosts:
#     - sudo mn --topo single,4 --mac --switch=ovsk,protocols=OpenFlow13 --controller=remote
#   - To see flow table, enter following in Mininet console: 
#     - dpctl dump-flows -O OpenFlow13
################################################################

####
# Change this value to determine where to mirror traffic.
MIRROR_TO_PORT = 2
####


from ryu.base import app_manager 
from ryu.controller import ofp_event
from ryu.controller.handler import CONFIG_DISPATCHER, MAIN_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.ofproto import ofproto_v1_3

from ryu.lib.packet import packet
from ryu.lib.packet import ethernet
from ryu.lib.packet import ipv4


class MyApp(app_manager.RyuApp):

    OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION]

    def __init__(self, *args, **kwargs):
        super(MyApp, self).__init__(*args, **kwargs)
        self.mac_to_port = {}

    ## Handle packet-in event.        
    @set_ev_cls(ofp_event.EventOFPPacketIn, MAIN_DISPATCHER)
    def packet_in_handler(self, ev):
        msg = ev.msg
        datapath = msg.datapath
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser
        actions = []
        out_port = ''

        # Get in_port and dpid
        in_port = msg.match['in_port']
        dpid = datapath.id

        # Ethernet
        pkt = packet.Packet(msg.data)
        eth = pkt.get_protocols(ethernet.ethernet)[0]
        srcMac = eth.src
        dstMac = eth.dst
        etherType = eth.ethertype

        # Set default for for this dpid
        self.mac_to_port.setdefault(dpid, {})

        # IF ARP, flood
        if etherType==0x806:
            out_port = ofproto.OFPP_FLOOD
            actions = [parser.OFPActionOutput(out_port)]

        # If ipv6, ignore
        elif etherType==0x86dd: 
            return

        # If ipv4, log.
        elif etherType==0x800: 
            nw = pkt.get_protocol(ipv4.ipv4)
            srcIp = nw.src
            dstIp = nw.dst

            # Log port-mac for this dpid
            self.mac_to_port[dpid][srcMac] = in_port
    
            # If seen dst mac in this dpid before, forward accordingly.
            if dstMac in self.mac_to_port[dpid]:
                out_port = self.mac_to_port[dpid][dstMac]
            else: # else, flood
                out_port = ofproto.OFPP_FLOOD

            # If out_port is not flood, mirror traffic
            if out_port != ofproto.OFPP_FLOOD:
                actions.append(parser.OFPActionOutput(MIRROR_TO_PORT))

            # Add to action list
            actions.append(parser.OFPActionOutput(out_port))

        # If out_port is empty, do nothing
        if out_port=='':
            print "No output port value assigned. Do nothing"
            return

        # install a flow to avoid packet_in next time
        if out_port != ofproto.OFPP_FLOOD:
            match = parser.OFPMatch(in_port=in_port, eth_src=srcMac, eth_dst=dstMac,eth_type=etherType)
            # verify if we have a valid buffer_id, if yes avoid to send both
            # flow_mod & packet_out
            if msg.buffer_id != ofproto.OFP_NO_BUFFER:
                self.add_flow(datapath, 1, match, actions, msg.buffer_id)
                return
            else:
                self.add_flow(datapath, 1, match, actions)

        data = None
        if msg.buffer_id == ofproto.OFP_NO_BUFFER:
            data = msg.data

        out = parser.OFPPacketOut(datapath=datapath, buffer_id=msg.buffer_id,
                                  in_port=in_port, actions=actions, data=data)
        datapath.send_msg(out)


    ## Add flow method
    def add_flow(self, datapath, priority, match, actions, buffer_id=None):
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        inst = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS,
                                             actions)]
        if buffer_id:
            mod = parser.OFPFlowMod(datapath=datapath, buffer_id=buffer_id,
                                    priority=priority, match=match,
                                    instructions=inst)
        else:
            mod = parser.OFPFlowMod(datapath=datapath, priority=priority,
                                    match=match, instructions=inst)
        datapath.send_msg(mod)

