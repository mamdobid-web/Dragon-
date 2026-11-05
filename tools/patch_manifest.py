"""Patch AndroidManifest.xml: set app label to a plain string and raise targetSdkVersion.
usage: python3 patch_manifest.py <in.xml> <out.xml> "<label>" <targetSdk>"""
import sys,os,struct; sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from axml import AXML
src,dst,label,target=sys.argv[1],sys.argv[2],sys.argv[3],int(sys.argv[4])
a=AXML(open(src,'rb').read()); idx=a.add_string(label)
patches=[]
for name,attrs in a.elements():
    for x in attrs:
        if name=='application' and x['name']=='label': patches.append((x['pos'],'label'))
        if name=='uses-sdk' and x['name']=='targetSdkVersion': patches.append((x['pos'],'target'))
out=bytearray(a.build()); delta=len(out)-len(a.d)
for pos,kind in patches:
    q=pos+delta   # attributes are after the string pool, so they shift by delta
    if kind=='label':
        struct.pack_into('<i',out,q+8,idx); out[q+15]=0x03; struct.pack_into('<I',out,q+16,idx)
    else:
        struct.pack_into('<I',out,q+16,target)
open(dst,'wb').write(out)
b=AXML(bytes(out))
for n,at in b.elements():
    if n in('application','uses-sdk'): print(n,[(x['name'],x['raw'] or x['value']) for x in at if x['name'] in('label','targetSdkVersion','minSdkVersion')])
