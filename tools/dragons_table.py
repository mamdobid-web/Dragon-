"""Summarise the dragon species table (pack 10, table 2) into a readable CSV.
Column meanings are inferred from the data; see README for confidence.
usage: python3 dragons_table.py <tables_dir> <texts_EN.json> <out.csv>"""
import sys,csv,json
R=[list(map(int,r)) for r in csv.reader(open(sys.argv[1]+'/t02.csv'))]
N=json.load(open(sys.argv[2]))['1']
with open(sys.argv[3],'w',newline='') as f:
    w=csv.writer(f); w.writerow(['id','name','currency','price','time_seconds','gold_per_min_L1','gold_per_min_L10','gold_per_min_L40'])
    for i,r in enumerate(R):
        if i and r[0]==0 and r[11]==0: continue  # empty placeholder rows
        per=lambda lv: round(60000/r[20+lv],1) if r[20+lv] else 0
        w.writerow([r[0],N[r[1]] if r[1]<len(N) else r[1],'gems' if r[10] else 'gold',r[11],r[16],per(1),per(10),per(40)])
print(len(R),'dragons')
