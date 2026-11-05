"""Rebuild an APK from the original, replacing files from a modified tree.
usage: python3 build_apk.py <original.apk> <modified_dir> <out_unsigned.apk>
Drops the old signature (META-INF) and keeps each entry's compression method."""
import sys,os,zipfile
orig,moddir,out=sys.argv[1:4]
zi=zipfile.ZipFile(orig); zo=zipfile.ZipFile(out,'w'); changed=0
for info in zi.infolist():
    if info.filename.startswith('META-INF/'): continue
    data=zi.read(info.filename)
    p=os.path.join(moddir,info.filename)
    if os.path.isfile(p):
        new=open(p,'rb').read()
        if new!=data: data=new; changed+=1
    ni=zipfile.ZipInfo(info.filename,info.date_time); ni.compress_type=info.compress_type; ni.external_attr=info.external_attr
    zo.writestr(ni,data)
zo.close(); print('changed entries:',changed)
