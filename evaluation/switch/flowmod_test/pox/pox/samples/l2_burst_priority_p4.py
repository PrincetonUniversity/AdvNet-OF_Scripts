# Copyright 2011 James McCauley
#
# This file is part of POX.
#
# POX is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# POX is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with POX.  If not, see <http://www.gnu.org/licenses/>.

"""
An L2 learning switch.

It is derived from one written live for an SDN crash course.
It is somwhat similar to NOX's pyswitch in that it installs
exact-match rules for each flow.
"""
from __future__ import division
from random import randrange
from pox.core import core
import pox.openflow.libopenflow_01 as of
from pox.lib.util import dpid_to_str
from pox.lib.util import str_to_bool
import sys, os, commands, time
from pox.lib.util import dpidToStr


log = core.getLogger()
#-------------------------------define flow rate----------
flow_rate = 50
interval = 1/flow_rate
print 'current flow modification rate is:', flow_rate
global burst
burst = {}
# We don't want to flood immediately when a switch connects.
# Can be overriden on commandline.
_flood_delay = 0

class LearningSwitch (object):
  """
  The learning switch "brain" associated with a single OpenFlow switch.

  When we see a packet, we'd like to output it on a port which will
  eventually lead to the destination.  To accomplish this, we build a
  table that maps addresses to ports.

  We populate the table by observing traffic.  When we see a packet
  from some source coming from some port, we know that source is out
  that port.

  When we want to forward traffic, we look up the desintation in our
  table.  If we don't know the port, we simply send the message out
  all ports except the one it came in on.  (In the presence of loops,
  this is bad!).

  In short, our algorithm looks like this:

  For each packet from the switch:
  1) Use source address and switch port to update address/port table
  2) Is transparent = False and either Ethertype is LLDP or the packet's
     destination address is a Bridge Filtered address?
     Yes:
        2a) Drop packet -- don't forward link-local traffic (LLDP, 802.1x)
            DONE
  3) Is destination multicast?
     Yes:
        3a) Flood the packet
            DONE
  4) Port for destination address in our address/port table?
     No:
        4a) Flood the packet
            DONE
  5) Is output port the same as input port?
     Yes:
        5a) Drop packet and similar ones for a while
  6) Install flow table entry in the switch so that this
     flow goes out the appopriate port
     6a) Send the packet out appropriate port
  """
  def __init__ (self, connection, transparent):
    # Switch we'll be adding L2 learning switch capabilities to
    self.connection = connection
    self.transparent = transparent
    # Our table
    self.macToPort = {}
    # We want to hear PacketIn messages, so we listen
    # to the connection
    connection.addListeners(self)

    # We just use this to know when to log a helpful message
    self.hold_down_expired = _flood_delay == 0
    #-----------------------
    msg = of.ofp_flow_mod(command=of.OFPFC_DELETE)

    # iterate over all connected switches and delete all their flows
    connection.send(msg)
    print "INFO: Clearing all flows..."
    #for BCM switch only
    msg = of.ofp_flow_mod()
    msg.priority = 1
    msg.match.dl_type = 0x800
    msg.match.in_port = 1
    msg.match.nw_src = '10.0.0.1'
    msg.idle_timeout = 0
    msg.hard_timeout = 0
    #msg.actions.append(of.ofp_action_output(port = 1))
    self.connection.send(msg)
    print 'INFO: add a default rule... (BCM only)'


    for k in xrange(1,301):#the number of rules to install
       #insert first
       msg = of.ofp_flow_mod()
       #msg.match = of.ofp_match.from_packet(packet, event.port)
       #msg.priority = 20000 + randrange(1000)
       #msg.priority = 2000
       if k >= 1 and k <= 100:
	  msg.priority = 1000
       if k >= 101 and k <= 200:
	  msg.priority = 2000
       if k >= 201 and k <= 300:
	  msg.priority = 3000
       msg.match.dl_type = 0x800
       i = int(k / 256) + 56
       j = k % 256
       dst = '193.168.' + str(i) + '.' + str(j)
       #msg.match.in_port = 1
       #msg.match.nw_src = '10.0.0.1'
       msg.match.nw_dst = dst
       #print 'INFO',dst, time.time()
       msg.idle_timeout = 0
       msg.hard_timeout = 0
       msg.actions.append(of.ofp_action_output(port = 10))
       #msg.data = event.ofp # 6a
       self.connection.send(msg)
       time.sleep(0.1)
    #-------------------------
    # (note that flow_mods match all flows by default)
    os.system('./simplesniffer eth2 200&')
    os.system('sudo bash ../pktgen/pktgen.conf.1-1-flow-dist.sh &')
    time.sleep(5)
    y = 0
    print 'INFO: starting sending flow mod...'
    for k in xrange(1,201):#the number of rules to install
       #insert first
       msg = of.ofp_flow_mod()
       #msg.match = of.ofp_match.from_packet(packet, event.port)
       #msg.priority = 20000 + randrange(1000)
       msg.priority = 4000
       msg.match.dl_type = 0x800
       i = int(k / 256) + 56
       j = k % 256
       dst = '192.168.' + str(i) + '.' + str(j)
       #msg.match.in_port = 1
       #msg.match.nw_src = '10.0.0.1'
       msg.match.nw_dst = dst
       #print 'INFO',dst, time.time()
       msg.idle_timeout = 0
       msg.hard_timeout = 0
       msg.actions.append(of.ofp_action_output(port = 5))
       #msg.data = event.ofp # 6a
       self.connection.send(msg)
       #print 'DATA: 10.0.0.1', dst, '%f' %time.time()
       #print 'DATA: 10.0.0.1', dst, '%f' %time.time()
       burst[dst] = time.time()
       #time.sleep(interval)
    print 'INFO: flow mod measure finished...'
    #write file
    w = open('poxout1','w')
    for d in burst:
    	w.write('src: 10.0.0.1 dst: %s sec: %f usec: %f\n' %(d, int(burst[d]), (burst[d] - int(burst[d])) * 1000000 ))
    w.close()
    os.system('sudo bash cleanpox.sh') #self destrory
  def _handle_PacketIn (self, event):
    """
    Handle packet in messages from the switch to implement above algorithm.
    """

    packet = event.parsed
    #print 'PACKET_IN:', event.port, packet.next.dstip,'%f' % time.time()

  def _handle_flowstats_received (event):
   stats = flow_stats_to_list(event.stats)
   print "FlowStatsReceived from %s: %s" % (dpidToStr(event.connection.dpid), stats)
  
class l2_learning (object):
  """
  Waits for OpenFlow switches to connect and makes them learning switches.
  """
  def __init__ (self, transparent):
    core.openflow.addListeners(self)
    self.transparent = transparent

  def _handle_ConnectionUp (self, event):
    log.debug("Connection %s" % (event.connection,))
    LearningSwitch(event.connection, self.transparent)


def launch (transparent=False, hold_down=_flood_delay):
  """
  Starts an L2 learning switch.
  """
  try:
    global _flood_delay
    _flood_delay = int(str(hold_down), 10)
    assert _flood_delay >= 0
  except:
    raise RuntimeError("Expected hold-down to be a number")

  core.registerNew(l2_learning, str_to_bool(transparent))
