import sys,os,struct,json; sys.path.insert(0,os.path.dirname(os.path.abspath(__file__))); import packlib as P
P.d=sys.argv[1]; out={}
for t,e in enumerate(P.parse(P.load(sys.argv[2]))):
    if not e: continue
    e=e[2:]; n=struct.unpack_from("<I",e,0)[0]; ends=struct.unpack_from(f'<{n}I',e,4); base=4+4*n; s=0; L=[]
    for x in ends: L.append(e[base+s:base+x].decode('utf8','replace')); s=x
    out[t]=L
json.dump(out,open(sys.argv[3],'w'),ensure_ascii=False,indent=1)
for t,L in out.items(): print(t,len(L),' | '.join(L[:6])[:150])
