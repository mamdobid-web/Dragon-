"""Parse the module/frame/animation tables of a GLLib BSprite (layout seen with flags 0x004185b1).

  u16 0x05DF, u32 flags, u32 (unknown)
  u16 nModules  x { u8 type, u16 x, u16 y, u16 w, u16 h }        rects inside the image
  u16 nFModules x { u8 module, s16 ox, s16 oy, u8 flags }         flags: bit0 flip-x, bit1 flip-y, bit2 rot90
  u16 (unknown), u16 nFrames x { u8 nFModules, u16 firstFModule, u8 (unknown) }
  nFrames x { s16 x, s16 y, u16 w, u16 h }                        frame bounding rects
  u16 nAFrames  x { u8 frame, u8 time, s8 ox, s8 oy, u8 flags }
  u16 nAnims    x { u8 nAFrames, u16 firstAFrame }
  ... image block (see bs2.py)
"""
import struct
def parse(e,img_at):
    p=10
    def u16():
        nonlocal p; v=struct.unpack_from('<H',e,p)[0]; p+=2; return v
    n=u16(); modules=[struct.unpack_from('<BHHHH',e,p+9*i)[1:] for i in range(n)]; p+=9*n
    n=u16(); fmods=[struct.unpack_from('<BhhB',e,p+6*i) for i in range(n)]; p+=6*n
    u16(); n=u16(); frames=[]
    for i in range(n):
        c,s=struct.unpack_from('<BH',e,p); p+=4; frames.append(fmods[s:s+c])
    rects=[struct.unpack_from('<hhHH',e,p+8*i) for i in range(n)]; p+=8*n
    n=u16(); aframes=[struct.unpack_from('<BBbbB',e,p+5*i) for i in range(n)]; p+=5*n
    n=u16(); anims=[]
    for i in range(n):
        c,s=struct.unpack_from('<BH',e,p); p+=3; anims.append(aframes[s:s+c])
    if p!=img_at: raise ValueError(f'layout mismatch: ended at {p:#x}, image block at {img_at:#x}')
    return dict(modules=modules,frames=frames,rects=rects,anims=anims)
