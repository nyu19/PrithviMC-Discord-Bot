import re
from mctools import QUERYClient,PINGClient
IP = 'vote.prithvimctk'

ping = PINGClient(IP,timeout=1)
# query = QUERYClient('140.238.228.116',25566,timeout=5)
data = ping.get_stats()
data.pop('favicon')
data.pop('description')

# ansi = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
# result = ansi.sub('', data['description'])#.replace('  ','')

print(data)

# print(query.get_full_stats())



# ping.stop()
# query.stop()

