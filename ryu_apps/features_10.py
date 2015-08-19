################################################################
# Ryu Application:
#   App for fetching attached switch's features and capabilities
#  - Author: Joon Kim (joonk@princeton.edu)
################################################################

################################################################
#                         Apache License
#                   Version 2.0, January 2004
#                http://www.apache.org/licenses/
#
#TERMS AND CONDITIONS FOR USE, REPRODUCTION, AND DISTRIBUTION
#
#1. Definitions.
#
#  "License" shall mean the terms and conditions for use, reproduction,
#  and distribution as defined by Sections 1 through 9 of this document.
#
#  "Licensor" shall mean the copyright owner or entity authorized by
#  the copyright owner that is granting the License.
#
#  "Legal Entity" shall mean the union of the acting entity and all
#  other entities that control, are controlled by, or are under common
#  control with that entity. For the purposes of this definition,
#  "control" means (i) the power, direct or indirect, to cause the
#  direction or management of such entity, whether by contract or
#  otherwise, or (ii) ownership of fifty percent (50%) or more of the
#  outstanding shares, or (iii) beneficial ownership of such entity.
#
#  "You" (or "Your") shall mean an individual or Legal Entity
#  exercising permissions granted by this License.
#
#  "Source" form shall mean the preferred form for making modifications,
#  including but not limited to software source code, documentation
#  source, and configuration files.
#
#  "Object" form shall mean any form resulting from mechanical
#  transformation or translation of a Source form, including but
#  not limited to compiled object code, generated documentation,
#  and conversions to other media types.
#
#  "Work" shall mean the work of authorship, whether in Source or
#  Object form, made available under the License, as indicated by a
#  copyright notice that is included in or attached to the work
#  (an example is provided in the Appendix below).
#
#  "Derivative Works" shall mean any work, whether in Source or Object
#  form, that is based on (or derived from) the Work and for which the
#  editorial revisions, annotations, elaborations, or other modifications
#  represent, as a whole, an original work of authorship. For the purposes
#  of this License, Derivative Works shall not include works that remain
#  separable from, or merely link (or bind by name) to the interfaces of,
#  the Work and Derivative Works thereof.
#
#  "Contribution" shall mean any work of authorship, including
#  the original version of the Work and any modifications or additions
#  to that Work or Derivative Works thereof, that is intentionally
#  submitted to Licensor for inclusion in the Work by the copyright owner
#  or by an individual or Legal Entity authorized to submit on behalf of
#  the copyright owner. For the purposes of this definition, "submitted"
#  means any form of electronic, verbal, or written communication sent
#  to the Licensor or its representatives, including but not limited to
#  communication on electronic mailing lists, source code control systems,
#  and issue tracking systems that are managed by, or on behalf of, the
#  Licensor for the purpose of discussing and improving the Work, but
#  excluding communication that is conspicuously marked or otherwise
#  designated in writing by the copyright owner as "Not a Contribution."
#
#  "Contributor" shall mean Licensor and any individual or Legal Entity
#  on behalf of whom a Contribution has been received by Licensor and
#  subsequently incorporated within the Work.
#
#  2. Grant of Copyright License. Subject to the terms and conditions of
#  this License, each Contributor hereby grants to You a perpetual,
#  worldwide, non-exclusive, no-charge, royalty-free, irrevocable
#  copyright license to reproduce, prepare Derivative Works of,
#  publicly display, publicly perform, sublicense, and distribute the
#  Work and such Derivative Works in Source or Object form.
#
#  3. Grant of Patent License. Subject to the terms and conditions of
#  this License, each Contributor hereby grants to You a perpetual,
#  worldwide, non-exclusive, no-charge, royalty-free, irrevocable
#  (except as stated in this section) patent license to make, have made,
#  use, offer to sell, sell, import, and otherwise transfer the Work,
#  where such license applies only to those patent claims licensable
#  by such Contributor that are necessarily infringed by their
#  Contribution(s) alone or by combination of their Contribution(s)
#  with the Work to which such Contribution(s) was submitted. If You
#  institute patent litigation against any entity (including a cross-claim or
#  counterclaim in a lawsuit) alleging that the Work or a Contribution
#  incorporated within the Work constitutes direct
#  or contributory patent infringement, then any patent licenses
#  granted to You under this License for that Work shall terminate
#  as of the date such litigation is filed.
#
#  4. Redistribution. You may reproduce and distribute copies of the
#  Work or Derivative Works thereof in any medium, with or without
#  modifications, and in Source or Object form, provided that You
#  meet the following conditions:
#
#  (a) You must give any other recipients of the Work or
#  Derivative Works a copy of this License; and
#
#  (b) You must cause any modified files to carry prominent notices
#  stating that You changed the files; and
#
#  (c) You must retain, in the Source form of any Derivative Works
#  that You distribute, all copyright, patent, trademark, and
#  attribution notices from the Source form of the Work,
#  excluding those notices that do not pertain to any part of
#  the Derivative Works; and
#
#  (d) If the Work includes a "NOTICE" text file as part of its
#  distribution, then any Derivative Works that You distribute must
#  include a readable copy of the attribution notices contained
#  within such NOTICE file, excluding those notices that do not
#  pertain to any part of the Derivative Works, in at least one
#  of the following places: within a NOTICE text file distributed
#  as part of the Derivative Works; within the Source form or
#  documentation, if provided along with the Derivative Works; or,
#  within a display generated by the Derivative Works, if and
#  wherever such third-party notices normally appear. The contents
#  of the NOTICE file are for informational purposes only and
#  do not modify the License. You may add Your own attribution
#  notices within Derivative Works that You distribute, alongside
#  or as an addendum to the NOTICE text from the Work, provided
#  that such additional attribution notices cannot be construed
#  as modifying the License.
#
#  You may add Your own copyright statement to Your modifications and
#  may provide additional or different license terms and conditions
#  for use, reproduction, or distribution of Your modifications, or
#  for any such Derivative Works as a whole, provided Your use,
#  reproduction, and distribution of the Work otherwise complies with
#  the conditions stated in this License.
#
#  5. Submission of Contributions. Unless You explicitly state otherwise,
#  any Contribution intentionally submitted for inclusion in the Work
#  by You to the Licensor shall be under the terms and conditions of
#  this License, without any additional terms or conditions.
#  Notwithstanding the above, nothing herein shall supersede or modify
#  the terms of any separate license agreement you may have executed
#  with Licensor regarding such Contributions.
#
#  6. Trademarks. This License does not grant permission to use the trade
#  names, trademarks, service marks, or product names of the Licensor,
#  except as required for reasonable and customary use in describing the
#  origin of the Work and reproducing the content of the NOTICE file.
#
#  7. Disclaimer of Warranty. Unless required by applicable law or
#  agreed to in writing, Licensor provides the Work (and each
#  Contributor provides its Contributions) on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
#  implied, including, without limitation, any warranties or conditions
#  of TITLE, NON-INFRINGEMENT, MERCHANTABILITY, or FITNESS FOR A
#  PARTICULAR PURPOSE. You are solely responsible for determining the
#  appropriateness of using or redistributing the Work and assume any
#  risks associated with Your exercise of permissions under this License.
#
#  8. Limitation of Liability. In no event and under no legal theory,
#  whether in tort (including negligence), contract, or otherwise,
#  unless required by applicable law (such as deliberate and grossly
#  negligent acts) or agreed to in writing, shall any Contributor be
#  liable to You for damages, including any direct, indirect, special,
#  incidental, or consequential damages of any character arising as a
#  result of this License or out of the use or inability to use the
#  Work (including but not limited to damages for loss of goodwill,
#  work stoppage, computer failure or malfunction, or any and all
#  other commercial damages or losses), even if such Contributor
#  has been advised of the possibility of such damages.
#
#  9. Accepting Warranty or Additional Liability. While redistributing
#  the Work or Derivative Works thereof, You may choose to offer,
#  and charge a fee for, acceptance of support, warranty, indemnity,
#  or other liability obligations and/or rights consistent with this
#  License. However, in accepting such obligations, You may act only
#  on Your own behalf and on Your sole responsibility, not on behalf
#  of any other Contributor, and only if You agree to indemnify,
#  defend, and hold each Contributor harmless for any liability
#  incurred by, or claims asserted against, such Contributor by reason
#  of your accepting any such warranty or additional liability.
#
#  END OF TERMS AND CONDITIONS
#
#  APPENDIX: How to apply the Apache License to your work.
#
#  To apply the Apache License to your work, attach the following
#  boilerplate notice, with the fields enclosed by brackets "{}"
#  replaced with your own identifying information. (Don't include
#  the brackets!)  The text should be enclosed in the appropriate
#  comment syntax for the file format. We also recommend that a
#  file or class name and description of purpose be included on the
#  same "printed page" as the copyright notice for easier
#  identification within third-party archives.
#
#  Copyright 2015 Hyojoon Kim. Princeton University.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#  http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
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

