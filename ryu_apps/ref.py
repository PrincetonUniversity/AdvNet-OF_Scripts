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

from ryu.lib import ofctl_v1_3
from ryu.ofproto import ofproto_v1_0
from ryu.ofproto import ofproto_v1_3

inst_str_list = ["GOTO table","Write metadata","Write actions", \
                 "Apply actions", "Clear actions", "Meter table"]

action_map = {ofproto_v1_3.OFPAT_OUTPUT: "Output to switch port",
   ofproto_v1_3.OFPAT_COPY_TTL_OUT: "Copy TTL 'outwards' from next-to-outermost to outermost",
   ofproto_v1_3.OFPAT_COPY_TTL_IN: "Copy TTL 'inwards' from outermost to next-to-outermost",
   ofproto_v1_3.OFPAT_SET_MPLS_TTL: "MPLS TTL",
   ofproto_v1_3.OFPAT_DEC_MPLS_TTL: "Decrement MPLS TTL",
   ofproto_v1_3.OFPAT_PUSH_VLAN :   "Push a new VLAN tag",
   ofproto_v1_3.OFPAT_POP_VLAN  :   "Pop the outer VLAN tag",
   ofproto_v1_3.OFPAT_PUSH_MPLS :   "Push a new MPLS tag",
   ofproto_v1_3.OFPAT_POP_MPLS  :   "Pop the outer MPLS tag",
   ofproto_v1_3.OFPAT_SET_QUEUE :   "Set queue id when outputting to a port",
   ofproto_v1_3.OFPAT_GROUP :       "Apply group",
   ofproto_v1_3.OFPAT_SET_NW_TTL:   "Set IP TTL",
   ofproto_v1_3.OFPAT_DEC_NW_TTL:   "Decrement IP TTL",
   ofproto_v1_3.OFPAT_SET_FIELD :   "Set a header field using OXM TLV format",
   ofproto_v1_3.OFPAT_PUSH_PBB :    "Push a new PBB service tag (I-TAG)",
   ofproto_v1_3.OFPAT_POP_PBB  :    "Pop the outer PBB service tag (I-TAG)",
   ofproto_v1_3.OFPAT_EXPERIMENTER : "Experimenter"
}


match_map = {
    ofproto_v1_3.OFPXMT_OFB_IN_PORT : "Switch input port",
    ofproto_v1_3.OFPXMT_OFB_IN_PHY_PORT   : "Switch physical input port",
    ofproto_v1_3.OFPXMT_OFB_METADATA      : "Metadata passed between tables",
    ofproto_v1_3.OFPXMT_OFB_ETH_DST       : "Ethernet destination address",
    ofproto_v1_3.OFPXMT_OFB_ETH_SRC       : "Ethernet source address",
    ofproto_v1_3.OFPXMT_OFB_ETH_TYPE      : "Ethernet frame type",
    ofproto_v1_3.OFPXMT_OFB_VLAN_VID      : "VLAN id",
    ofproto_v1_3.OFPXMT_OFB_VLAN_PCP      : "VLAN priority",
    ofproto_v1_3.OFPXMT_OFB_IP_DSCP       : "IP DSCP (6 bits in ToS field)",
    ofproto_v1_3.OFPXMT_OFB_IP_ECN        : "IP ECN (2 bits in ToS field)",
    ofproto_v1_3.OFPXMT_OFB_IP_PROTO      : "IP protocol",
    ofproto_v1_3.OFPXMT_OFB_IPV4_SRC      : "IPv4 source address",
    ofproto_v1_3.OFPXMT_OFB_IPV4_DST      : "IPv4 destination address",
    ofproto_v1_3.OFPXMT_OFB_TCP_SRC       : "TCP source port",
    ofproto_v1_3.OFPXMT_OFB_TCP_DST       : "TCP destination port",
    ofproto_v1_3.OFPXMT_OFB_UDP_SRC       : "UDP source port",
    ofproto_v1_3.OFPXMT_OFB_UDP_DST       : "UDP destination port",
    ofproto_v1_3.OFPXMT_OFB_SCTP_SRC      : "SCTP source port",
    ofproto_v1_3.OFPXMT_OFB_SCTP_DST      : "SCTP destination port",
    ofproto_v1_3.OFPXMT_OFB_ICMPV4_TYPE   : "ICMP type",
    ofproto_v1_3.OFPXMT_OFB_ICMPV4_CODE   : "ICMP code",
    ofproto_v1_3.OFPXMT_OFB_ARP_OP        : "ARP opcode",
    ofproto_v1_3.OFPXMT_OFB_ARP_SPA       : "ARP source IPv4 address",
    ofproto_v1_3.OFPXMT_OFB_ARP_TPA       : "ARP target IPv4 address",
    ofproto_v1_3.OFPXMT_OFB_ARP_SHA       : "ARP source hardware address",
    ofproto_v1_3.OFPXMT_OFB_ARP_THA       : "ARP target hardware address",
    ofproto_v1_3.OFPXMT_OFB_IPV6_SRC      : "IPv6 source address",
    ofproto_v1_3.OFPXMT_OFB_IPV6_DST      : "IPv6 destination address",
    ofproto_v1_3.OFPXMT_OFB_IPV6_FLABEL   : "IPv6 Flow Label ",
    ofproto_v1_3.OFPXMT_OFB_ICMPV6_TYPE   : "ICMPv6 type",
    ofproto_v1_3.OFPXMT_OFB_ICMPV6_CODE   : "ICMPv6 code",
    ofproto_v1_3.OFPXMT_OFB_IPV6_ND_TARGET: "Target address for ND",
    ofproto_v1_3.OFPXMT_OFB_IPV6_ND_SLL   : "Source link-layer for ND",
    ofproto_v1_3.OFPXMT_OFB_IPV6_ND_TLL   : "Target link-layer for ND",
    ofproto_v1_3.OFPXMT_OFB_MPLS_LABEL    : "MPLS label",
    ofproto_v1_3.OFPXMT_OFB_MPLS_TC       : "MPLS TC",
    ofproto_v1_3.OFPXMT_OFB_MPLS_BOS      : "MPLS BoS bit",
    ofproto_v1_3.OFPXMT_OFB_PBB_ISID      : "PBB I-SID",
    ofproto_v1_3.OFPXMT_OFB_TUNNEL_ID     : "Logical Port Metadata",
    ofproto_v1_3.OFPXMT_OFB_IPV6_EXTHDR   : "IPv6 Extension Header pseudo-field"
}



action_map_v10 = {
   ofproto_v1_0.OFPAT_OUTPUT         :" Output to switch port",
   ofproto_v1_0.OFPAT_SET_VLAN_VID  :" Set the 802.1q VLAN id",
   ofproto_v1_0.OFPAT_SET_VLAN_PCP  :" Set the 802.1q priority",
   ofproto_v1_0.OFPAT_STRIP_VLAN   :" Strip the 802.1q header",
   ofproto_v1_0.OFPAT_SET_DL_SRC   :" Set ethernet source address",
   ofproto_v1_0.OFPAT_SET_DL_DST   :" Set ethernet destination address",
   ofproto_v1_0.OFPAT_SET_NW_SRC   :" Set IP source address",
   ofproto_v1_0.OFPAT_SET_NW_DST   :" Set IP destination address",
   ofproto_v1_0.OFPAT_SET_NW_TOS   :" Set IP ToS (DSCP field, 6 bits)",
   ofproto_v1_0.OFPAT_SET_TP_SRC   :" Set TCP/UDP source port",
   ofproto_v1_0.OFPAT_SET_TP_DST   :" Set TCP/UDP destination port",
   ofproto_v1_0.OFPAT_ENQUEUE   :" Output to queue",
   ofproto_v1_0.OFPAT_VENDOR: " Vendor. 0xffff"
}


