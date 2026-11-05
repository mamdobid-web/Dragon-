"""Readers for the layout packs (verified byte-exact).

pack 7  - island maps. Each map = a 7-byte header {u8 flag, u16 w, u16 h, u16 0} followed by
          layer entries of w*h bytes (one byte per cell): a tile layer and a 0-3 terrain/zone layer.
pack 16 - part compositions (one entry per dragon species + 1 empty):
          u8 flag, u8 0, u16 a, u16 b, u8 index,
          then groups: 0x01 {u16 groupId, u16 param}
                       followed by 0x02 {s16 x, s16 y, u16 sprite, u16 frame, u8 flags} records.
"""
import struct
def map_header(e):
    if len(e)==7: return struct.unpack_from('<HH',e,1)
def comp(e):
    p=1; head=struct.unpack_from('<BHHB',e,p); p+=6; groups=[]
    while p<len(e):
        t=e[p]
        if t==1: gid,par=struct.unpack_from('<HH',e,p+1); groups.append(dict(id=gid,param=par,parts=[])); p+=5
        elif t==2:
            if not groups: raise ValueError('part before group')
            groups[-1]['parts'].append(struct.unpack_from('<hhHHB',e,p+1)); p+=10
        else: raise ValueError(f'unknown tag {t:#x} at {p}')
    return dict(head=head,groups=groups)
