ps aux | grep -ie pox.py | awk '{print $2}' | xargs kill -9
ps aux | grep -ie tcpdump | awk '{print $2}' | xargs kill -9
ps aux | grep -ie hping | awk '{print $2}' | xargs kill -9
ps aux | grep -ie simplesniffer | awk '{print $2}' | xargs kill -9

