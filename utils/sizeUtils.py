import math
def converter(byte:int):
    if byte == 0:
       return "0B"
    size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    i = int(math.floor(math.log(byte, 1024)))
    p = math.pow(1024, i)
    s = round(byte / p, 2)
    return str(s) + " " + size_name[i]
    
def mbconverter(Mbyte:int):
    byte = Mbyte
    if byte == 0:
       return "0MB"
    size_name = ("MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    i = int(math.floor(math.log(byte, 1024)))
    p = math.pow(1024, i)
    s = round(byte / p, 2)
    return str(s) + " " + size_name[i]