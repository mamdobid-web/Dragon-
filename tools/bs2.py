import struct
FMT={0x8888:4,0x4444:2,0x1555:2,0x0565:2}
def parse(e):
    for i in range(6,len(e)-12):
        f=struct.unpack_from('<H',e,i)[0]
        if f not in FMT: continue
        enc=struct.unpack_from('<H',e,i+2)[0]; nimg=e[i+4]; p=i+5; bpc=FMT[f]; sets=[]
        try:
            for _ in range(nimg):
                npal,ncol=e[p],e[p+1] or 256; p+=2
                pals=[[struct.unpack_from('<I' if bpc==4 else '<H',e,p+ncol*bpc*k+j*bpc)[0] for j in range(ncol)] for k in range(npal)]
                p+=npal*ncol*bpc; sets.append(pals)
            imgs=[]
            for _ in range(nimg):
                w,h,sz=struct.unpack_from('<HHI',e,p); p+=8
                if p+sz>len(e) or w*h==0 or w>4096 or h>4096: raise ValueError
                imgs.append((w,h,e[p:p+sz])); p+=sz
        except Exception: continue
        if p==len(e): return dict(fmt=f,enc=enc,sets=sets,imgs=imgs,at=i)
    return None
