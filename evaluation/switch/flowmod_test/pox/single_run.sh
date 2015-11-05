#/bin/bash
ps aux | grep -ie pktgen.conf | awk '{print $2}' | xargs kill -9
ps aux | grep -ie pox.py | awk '{print $2}' | xargs kill -9
ps aux | grep -ie sniffer | awk '{print $2}' | xargs kill -9
sleep 2

# Run test. $1 is add/mod, $2 is number of flows.
app='pox.samples.l2_joon_'$1' --rate='$2' --nflows='$3' --inport='$4' --outport='$5
echo $app

./pox.py $app
sleep 40

# Clean up
ps aux | grep -ie pktgen.conf | awk '{print $2}' | xargs kill -9
ps aux | grep -ie pox.py | awk '{print $2}' | xargs kill -9
ps aux | grep -ie sniffer | awk '{print $2}' | xargs kill -9

# Produce outputs
python parse_control.py
