print(open(".tmp",'r').read())

tmp = str(int(open(".tmp",'r').read())+1)
print(open(".tmp",'w').write(tmp))
print(open(".tmp",'r').read())
print(open(".tmp",'r').read())
print(open(".tmp",'r').read())


