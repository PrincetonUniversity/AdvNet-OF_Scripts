#!/bin/bash
 
# FileName: pktgen.conf.1-1-flow.sh
# modprobe pktgen
 
function pgset() {
    local result
 
    echo $1 > $PGDEV
 
    result=`cat $PGDEV | fgrep "Result: OK:"`
    if [ "$result" = "" ]; then
         cat $PGDEV | grep Result:
    fi
}
 
function pg() {
    echo inject > $PGDEV
    cat $PGDEV
}
 
# Config Start Here -----------------------------------------------------------
 
# thread config
# Each CPU has own thread. Please modify veth0 to any ethX you want to use in your experiment setup. Most likely, eth1 (assuming that eth0 is for openflow control, eth1 for flow inject, and eth2 for flow receiving, eth2 is in a different namesapce to avoid OS bypass).
 
PGDEV=/proc/net/pktgen/kpktgend_0
  echo "Removing all devices"
 pgset "rem_device_all"
  echo "Adding veth0"
 pgset "add_device veth0"

# device config
# delay 0 means maximum speed.
 
CLONE_SKB="clone_skb 0"
# NIC adds 4 bytes CRC
PKT_SIZE="pkt_size 60"
 
# COUNT 0 means forever
#COUNT="count 0"
COUNT="count 0"
DELAY="delay 0"  #nano sec

PGDEV=/proc/net/pktgen/veth0
  echo "Configuring $PGDEV"
 pgset "$COUNT"
 pgset "$CLONE_SKB"
 pgset "$PKT_SIZE"
 pgset "$DELAY"

# Random address within the
# min-max range
# pgset "flag IPDST_RND"
pgset "src_min 10.0.0.1"
pgset "src_max 10.0.0.1"
#flow probe method 1
#pgset "dst_min 192.168.56.0"
pgset "dst_min 192.168.59.255"
pgset "dst_max 192.168.59.255"
# 8k Concurrent flows at 4 pkts
pgset "flows 1024"
pgset "flowlen 1"

# Time to run
PGDEV=/proc/net/pktgen/pgctrl
 
 echo "Running... ctrl^C to stop"
 pgset "start"
 echo "Done"
