ps aux | grep -ie pktgen.conf | awk '{print $2}' | sudo xargs kill -9
ps aux | grep -ie pox.py | awk '{print $2}' | sudo xargs kill -9
ps aux | grep -ie sniffer | awk '{print $2}' | sudo xargs kill -9


