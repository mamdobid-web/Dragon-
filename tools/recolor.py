"""Hue-shift every palette of the dragon sprite pack in place (same byte size).
usage: python3 recolor.py <assets/WxH dir> <pack> <degrees>"""
import sys,os,struct,colorsys
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
import packlib as P, bs2
src,pk,deg=sys.argv[1],sys.argv[2],float(sys.argv[3])
P.d=src
chunks=[pk]; i=1
while os.path.exists(os.path.join(src,f'{pk}.{i}')): chunks.append(f'{pk}.{i}'); i+=1
sizes=[os.path.getsize(os.path.join(src,c)) for c in chunks]
data=bytearray(b''.join(open(os.path.join(src,c),'rb').read() for c in chunks))
c=struct.unpack_from('<H',data,0)[0]; offs=list(struct.unpack_from(f'<{c}I',data,2))
ends=offs[1:]+[len(data)]
def shift(r,g,b):
    h,l,s=colorsys.rgb_to_hls(r/255,g/255,b/255); r,g,b=colorsys.hls_to_rgb((h+deg/360)%1,l,s)
    return round(r*255),round(g*255),round(b*255)
nspr=ncol=0
for a,b in zip(offs,ends):
    e=bytes(data[a+1:b])
    if e[:2]!=b'\xdf\x05': continue
    r=bs2.parse(e)
    if not r or r['fmt'] not in (0x8888,0x4444): continue
    bpc=4 if r['fmt']==0x8888 else 2
    p=a+1+r['at']+5
    for _ in r['sets']:
        npal,nc=data[p],data[p+1] or 256; p+=2
        for k in range(npal*nc):
            q=p+k*bpc
            if bpc==4:
                v=struct.unpack_from('<I',data,q)[0]; A=v>>24
                if A==0: continue
                R,G,B=shift((v>>16)&255,(v>>8)&255,v&255)
                struct.pack_into('<I',data,q,(A<<24)|(R<<16)|(G<<8)|B)
            else:
                v=struct.unpack_from('<H',data,q)[0]; A=v>>12
                if A==0: continue
                R,G,B=shift(((v>>8)&15)*17,((v>>4)&15)*17,(v&15)*17)
                struct.pack_into('<H',data,q,(A<<12)|((R//17)<<8)|((G//17)<<4)|(B//17))
            ncol+=1
        p+=npal*nc*bpc
    nspr+=1
o=0
for ch,sz in zip(chunks,sizes):
    open(os.path.join(src,ch),'wb').write(data[o:o+sz]); o+=sz
print(f'recoloured {nspr} sprites, {ncol} colours, pack {pk} in {src}')
