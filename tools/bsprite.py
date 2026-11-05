import struct
FMT={0x8888:4,0x4444:2,0x1555:2,0x0565:2}
def find_image_block(e):
    """Locate pixel-format block; return dict or None."""
    for i in range(6,len(e)-12):
        f=struct.unpack_from('<H',e,i)[0]
        if f not in FMT: continue
        enc=struct.unpack_from('<H',e,i+2)[0]
        unk,npal,ncol=e[i+4],e[i+5],e[i+6]
        if ncol==0: ncol=256
        p=i+7; pals=[]
        bpc=FMT[f]
        if p+npal*ncol*bpc+8>len(e) or npal==0: continue
        for k in range(npal):
            pals.append([struct.unpack_from('<I' if bpc==4 else '<H',e,p+(j*bpc))[0] for j in range(ncol)]); p+=ncol*bpc
        return dict(at=i,fmt=f,enc=enc,unk=unk,npal=npal,ncol=ncol,pals=pals,data=p)
    return None
def to_rgba(f,c):
    if f==0x8888: return ((c>>16)&255,(c>>8)&255,c&255,(c>>24)&255)
    if f==0x4444: return (((c>>8)&15)*17,((c>>4)&15)*17,(c&15)*17,((c>>12)&15)*17)
    if f==0x1555: return (((c>>10)&31)*255//31,((c>>5)&31)*255//31,(c&31)*255//31,255 if c>>15 else 0)
    if f==0x0565:
        r,g,b=((c>>11)&31)*255//31,((c>>5)&63)*255//63,(c&31)*255//31
        return (r,g,b,0 if (r,g,b)==(255,0,255) else 255)
def rle(d,enc,n):
    out=[];i=0
    if enc==0x27F1:  # I127RLE
        while len(out)<n and i<len(d):
            c=d[i];i+=1
            if c>127: out+= [d[i]]*(c-128); i+=1
            else: out.append(c)
    elif enc==0x5602:  # I256 raw indices
        out=list(d[:n]); i=n
    elif enc==0x1600:  # I16: 2 px per byte
        for b in d:
            out+=[b>>4,b&15]
            i+=1
            if len(out)>=n: break
    elif enc==0x64F0:  # I64RLE
        while len(out)<n and i<len(d):
            c=d[i];i+=1
            out+= [c&63]*((c>>6)+1)
    else: return None,0
    return out[:n],i
