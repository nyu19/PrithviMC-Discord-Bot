from mctools import PINGClient


ping = PINGClient('vote.prithvimc.tk',25566)
data = ping.get_stats()

print(data)