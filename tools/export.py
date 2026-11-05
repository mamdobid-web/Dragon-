import sys,os,zlib,struct,json,collections
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
import packlib as P, bs2, decode as D, bsprite as B
src,out=sys.argv[1],sys.argv[2]; P.d=src
def png(path,w,h,rgba):
    raw=b''.join(b'\0'+bytes(rgba[y*w*4:(y+1)*w*4]) for y in range(h))
    def ch(t,b): return struct.pack('>I',len(b))+t+b+struct.pack('>I',zlib.crc32(t+b)&0xffffffff)
    open(path,'wb').write(b'\x89PNG\r\n\x1a\n'+ch(b'IHDR',struct.pack('>IIBBBBB',w,h,8,6,0,0,0))+ch(b'IDAT',zlib.compress(raw,6))+ch(b'IEND',b''))
stats=collections.Counter(); index=[]
for pk in ['2','5','8','9','12']:
    os.makedirs(f'{out}/sprites/pack{pk}',exist_ok=True)
    for k,e in enumerate(P.parse(P.load(pk))):
        e=e[1:]
        if e[:2]!=b'\xdf\x05': continue
        r=bs2.parse(e)
        for ii,((w,h,d),pals) in enumerate(zip(r['imgs'],r['sets'])):
            n=w*h; idx,used=D.indices(r['enc'],d,n,len(pals[0]))
            if idx is None or len(idx)!=n: stats['fail']+=1; continue
            alpha=None
            if r['enc']>>12==0xA:
                alpha,_=D.alpha_fe(d[used:],n)
                if len(alpha)!=n: alpha=None; stats['alpha_fail']+=1
            for pi,pal in enumerate(pals if len(pals)<=12 else pals[:12]):
                cols=[B.to_rgba(r['fmt'],c) for c in pal]
                buf=bytearray(n*4)
                for j,ci in enumerate(idx):
                    c=cols[ci] if ci<len(cols) else (0,0,0,0)
                    a=c[3] if alpha is None else alpha[j]
                    buf[j*4:j*4+4]=bytes((c[0],c[1],c[2],a))
                name=f'pack{pk}/s{k:03d}' + (f'_img{ii}' if len(r['imgs'])>1 else '') + (f'_pal{pi}' if len(pals)>1 else '')+'.png'
                png(f'{out}/sprites/{name}',w,h,buf); stats['png']+=1
                index.append(dict(file=name,w=w,h=h,palettes=len(pals),enc=hex(r['enc'])))
            stats['ok']+=1
json.dump(index,open(f'{out}/sprites/index.json','w'),indent=0)
print(dict(stats))
