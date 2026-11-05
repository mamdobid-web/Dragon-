"""Minimal Android binary XML (AXML) reader/editor for AndroidManifest.xml."""
import struct
class AXML:
    def __init__(self,data):
        self.d=bytearray(data); i=8; self.sp=None
        while i<len(self.d):
            t,hs,sz=struct.unpack_from('<HHI',self.d,i)
            if t==0x0001 and self.sp is None: self.sp=(i,sz); self._read_pool(i)
            i+=sz
    def _read_pool(self,i):
        d=self.d; n,ns,flags,ss,so=struct.unpack_from('<IIIII',d,i+8); self.utf8=bool(flags&0x100); self.strs=[]
        for k in range(n):
            o=i+ss+struct.unpack_from('<I',d,i+28+4*k)[0]
            if self.utf8:
                o+=1 if d[o]<0x80 else 2
                l=d[o]; o+=1
                if l&0x80: l=((l&0x7f)<<8)|d[o]; o+=1
                self.strs.append(d[o:o+l].decode('utf8'))
            else:
                l=struct.unpack_from('<H',d,o)[0]; o+=2
                if l&0x8000: l=((l&0x7fff)<<16)|struct.unpack_from('<H',d,o)[0]; o+=2
                self.strs.append(d[o:o+2*l].decode('utf-16le'))
        self.n_styles=ns
    def elements(self):
        i=8
        while i<len(self.d):
            t,hs,sz=struct.unpack_from('<HHI',self.d,i)
            if t==0x0102:
                name=self.strs[struct.unpack_from('<I',self.d,i+20)[0]]
                ac=struct.unpack_from('<H',self.d,i+28)[0]; attrs=[]
                for a in range(ac):
                    q=i+36+20*a; ni=struct.unpack_from('<I',self.d,q+4)[0]; raw=struct.unpack_from('<i',self.d,q+8)[0]
                    typ=self.d[q+15]; val=struct.unpack_from('<I',self.d,q+16)[0]
                    attrs.append(dict(name=self.strs[ni],raw=self.strs[raw] if raw>=0 else None,type=typ,value=val,pos=q))
                yield name,attrs
            i+=sz
    def add_string(self,s):
        self.strs.append(s); return len(self.strs)-1
    def build(self):
        """Rebuild string pool (UTF-16, no styles) and return new bytes."""
        assert self.n_styles==0
        i,sz=self.sp; data=b''; offs=[]
        for s in self.strs:
            offs.append(len(data)); u=s.encode('utf-16le'); data+=struct.pack('<H',len(u)//2)+u+b'\0\0'
        while len(data)%4: data+=b'\0'
        n=len(self.strs); hdr=28; ss=hdr+4*n
        chunk=struct.pack('<HHIIIIII',1,28,ss+len(data),n,0,0,ss,0)+b''.join(struct.pack('<I',o) for o in offs)+data
        out=self.d[:i]+chunk+self.d[i+sz:]
        struct.pack_into('<I',out,4,len(out)); return bytes(out)
