import sys,struct
d=open(sys.argv[1],'rb').read()
def uleb(p):
    r=s=0
    while True:
        b=d[p];p+=1;r|=(b&0x7f)<<s;s+=7
        if b<0x80: return r,p
n,off=struct.unpack_from('<II',d,0x38)
out=[]
for i in range(n):
    so=struct.unpack_from('<I',d,off+4*i)[0]
    l,p=uleb(so); e=d.index(b'\0',p)
    out.append(d[p:e].decode('utf8','replace'))
tn,to=struct.unpack_from('<II',d,0x40)
types=[out[struct.unpack_from('<I',d,to+4*i)[0]] for i in range(tn)]
cn,co=struct.unpack_from('<II',d,0x60)
classes=[types[struct.unpack_from('<I',d,co+32*i)[0]] for i in range(cn)]
open(sys.argv[2]+'/strings.txt','w').write('\n'.join(out))
open(sys.argv[2]+'/classes.txt','w').write('\n'.join(classes))
print(len(out),'strings',len(classes),'classes')
