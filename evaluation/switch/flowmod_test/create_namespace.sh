#/bin/bash

# Add namespaces
sudo ip netns add sender
sudo ip netns add receiver

# Add interface to each namespace
sudo ip link set em3 netns sender
sudo ip link set em4 netns receiver

# Make interface up
sudo ip netns exec sender ifconfig em3 0
sudo ip netns exec sender ifconfig em3 up
sudo ip netns exec receiver ifconfig em4 0
sudo ip netns exec receiver ifconfig em4 up


