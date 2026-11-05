"""Generic Gameloft GLLib pack reader: u16 count, count x u32 start offsets, then entries (1 flag byte + payload).
Large packs are split into 2,000,000-byte chunks: N, N.1, N.2 ..."""
import sys,struct,os,collections
d=None
def load(n):
    data=open(os.path.join(d,n),'rb').read(); i=1
    while os.path.exists(os.path.join(d,f"{n}.{i}")):
        data+=open(os.path.join(d,f"{n}.{i}"),'rb').read(); i+=1
    return data
def parse(data):
    if len(data)<6: return None
    c=struct.unpack_from('<H',data,0)[0]
    if 2+4*c>len(data): return None
    offs=list(struct.unpack_from(f'<{c}I',data,2))
    if not offs or offs[0]!=2+4*c: return None
    ends=offs[1:]+[len(data)]
    return [data[a:b] for a,b in zip(offs,ends)]
def kind(b):
    if b[:8]==b'\x89PNG\r\n\x1a\n': return 'png'
    if b[:4]==b'OggS': return 'ogg'
    if b[:4]==b'RIFF': return 'wav'
    if b[:3]==b'ID3' or b[:2]==b'\xff\xfb': return 'mp3'
    if b[:4]==b'MThd': return 'mid'
    return 'raw:'+b[:4].hex()
