"""GLLib data tables (pack 10 and similar).
entry = u8 flag, u32 0, u16 nCols, u16 nRows, u8 colType[nCols] (1=u8, 2=s16, 4=s32), u8 0x48, then rows (row-major).
usage: python3 tables.py <assets/WxH> <pack> <out_dir>  -> one CSV per table"""
import sys,os,struct,csv
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__))); import packlib as P
FMT={1:'B',2:'h',4:'i'}
def parse(e):
    if len(e)<9: return None
    nc,nr=struct.unpack_from('<HH',e,5)
    if nc==0: return []
    types=list(e[9:9+nc]); p=9+nc
    if p>=len(e) or e[p]!=0x48 or any(t not in FMT for t in types): return None
    p+=1; rows=[]; rf='<'+''.join(FMT[t] for t in types); rs=struct.calcsize(rf)
    for r in range(nr): rows.append(struct.unpack_from(rf,e,p)); p+=rs
    return dict(types=types,rows=rows,end=p,size=len(e))
if __name__=='__main__':
    P.d=sys.argv[1]; out=sys.argv[3]; os.makedirs(out,exist_ok=True)
    for k,e in enumerate(P.parse(P.load(sys.argv[2]))):
        t=parse(e)
        if not t: print(k,'empty/other'); continue
        with open(os.path.join(out,f't{k:02d}.csv'),'w',newline='') as f: csv.writer(f).writerows(t['rows'])
        print(f"{k:2} cols={len(t['types']):2} rows={len(t['rows']):3} {'OK' if t['end']==t['size'] else 'size mismatch %d/%d'%(t['end'],t['size'])}")
