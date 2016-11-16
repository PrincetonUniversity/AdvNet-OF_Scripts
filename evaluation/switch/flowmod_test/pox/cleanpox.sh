ps aux | grep -ie pox.py | awk '{print $2}' | xargs kill -9

