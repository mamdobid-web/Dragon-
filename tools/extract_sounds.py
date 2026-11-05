"""Extract OGG sounds from pack 3: python3 extract_sounds.py <assets/800x480> <out_dir>"""
import sys,os; sys.path.insert(0,os.path.dirname(os.path.abspath(__file__))); import packlib as P
P.d=sys.argv[1]; os.makedirs(sys.argv[2],exist_ok=True); n=0
for k,e in enumerate(P.parse(P.load('3'))):
    if e[1:5]==b'OggS': open(os.path.join(sys.argv[2],f'snd{k:03d}.ogg'),'wb').write(e[1:]); n+=1
print('ogg',n)
