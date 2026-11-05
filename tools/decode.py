import math
def i127(d,n):
    o=[];i=0
    while i<len(d) and len(o)<n:
        c=d[i];i+=1
        if c>127: o+=[d[i]]*(c-128);i+=1
        else:o.append(c)
    return o,i
def i256(d,n):
    o=[];i=0
    while i<len(d) and len(o)<n:
        c=d[i];i+=1
        if c>127: k=c-128;o+=list(d[i:i+k]);i+=k
        else: o+=[d[i]]*c;i+=1
    return o,i
def i64(d,n,ncol):
    cb=max(1,math.ceil(math.log2(ncol)));m=(1<<cb)-1;o=[];i=0
    while i<len(d) and len(o)<n:
        c=d[i];i+=1;o+=[c&m]*((c>>cb)+1)
    return o,i
def indices(enc,d,n,ncol):
    if enc==0x27F1 or enc==0xA127: return i127(d,n)
    if enc==0x56F2 or enc==0xA256: return i256(d,n)
    if enc==0x64F0 or enc==0xA640: return i64(d,n,ncol)
    if enc==0x5602: return list(d[:n]),n
    return None,0
def alpha_fe(d,n):
    o=[];i=0
    while i<len(d) and len(o)<n:
        c=d[i];i+=1
        if c==0xFE: o+=[d[i+1]]*d[i];i+=2
        else:o.append(c)
    return o,i
