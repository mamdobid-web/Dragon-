"""zipalign replacement: rewrite APK so STORED entries start on 4-byte boundaries (.so on 4096).
usage: python3 align_apk.py <in.apk> <out.apk>"""
import sys,zipfile
zi=zipfile.ZipFile(sys.argv[1]); zo=zipfile.ZipFile(sys.argv[2],'w')
for info in zi.infolist():
    data=zi.read(info.filename)
    ni=zipfile.ZipInfo(info.filename,info.date_time); ni.compress_type=info.compress_type; ni.external_attr=info.external_attr
    if ni.compress_type==zipfile.ZIP_STORED:
        al=4096 if info.filename.endswith('.so') else 4
        start=zo.fp.tell()+30+len(ni.filename.encode())
        pad=(-start)%al
        if pad and pad<4: pad+=al
        if pad: ni.extra=b'\xff\xff'+(pad-4).to_bytes(2,'little')+b'\0'*(pad-4)
    zo.writestr(ni,data)
zo.close()
print('aligned')
