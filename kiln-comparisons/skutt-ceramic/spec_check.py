import json,re,html,sys
REF={ # Skutt catalog 2023 / model pages: (phase,volts)->(amps,watts,cone,tempF); cuft; tea bowls
'818':(2.6,12,{('1','240'):(26.7,6400,10,2350),('1','208'):(26.7,5550,10,2350)}),
'818-3':(2.3,12,{('1','240'):(26.7,6400,10,2350),('1','208'):(26.7,5550,10,2350)}),
'818-30A-3':(2.3,12,{('1','240'):(21.7,5200,8,2300),('1','208'):(24.0,4990,8,2300)}),
'822':(3.2,15,{('1','240'):(33.4,8000,10,2350),('1','208'):(38.5,8000,10,2350)}),
'822-3':(2.9,15,{('1','240'):(33.4,8000,10,2350),('1','208'):(38.5,8000,10,2350)}),
'1018':(4.6,26,{('1','240'):(39.4,9460,10,2350),('1','208'):(40.0,8320,10,2350)}),
'1018-3':(4.2,26,{('1','240'):(39.4,9460,10,2350),('1','208'):(40.0,8320,10,2350)}),
'1022':(5.7,32,{('1','240'):(48,11520,10,2350),('1','208'):(48,9984,10,2350),('3','240'):(34.6,11520,10,2350),('3','208'):(34.6,9984,10,2350)}),
'1022-3':(5.25,32,{('1','240'):(48,11520,10,2350),('1','208'):(48,9984,10,2350),('3','240'):(34.6,11520,10,2350),('3','208'):(34.6,9984,10,2350)}),
'1027':(7.0,38,{('1','240'):(48,11520,10,2350),('1','208'):(48,9984,6,2250),('3','240'):(29.3,11520,10,2350),('3','208'):(31.7,11000,10,2350)}),
'1027-3':(6.4,38,{('1','240'):(48,11520,10,2350),('1','208'):(48,9984,10,2350),('3','240'):(29.3,11520,10,2350),('3','208'):(31.7,11000,10,2350)}),
'1218-3':(6.6,42,{('1','240'):(48,11520,10,2350),('1','208'):(48,9984,10,2350),('3','240'):(29.3,11520,10,2350),('3','208'):(29.5,9984,10,2350)}),
'1222-3':(8.1,46,{('1','240'):(48,11520,10,2350),('1','208'):(48,9984,8,2300),('3','240'):(34.6,11520,10,2350),('3','208'):(40,11520,10,2350)}),
'1227-3':(9.9,50,{('1','240'):(48,11520,8,2300),('1','208'):(48,9984,5,2185),('3','240'):(29.3,11520,8,2300),('3','208'):(31.7,11000,8,2300)}),
'1227-3PK':(9.9,50,{('1','240'):(60,14300,10,2350),('1','208'):(69,14300,10,2350),('3','240'):(40,14300,10,2350),('3','208'):(46.7,14300,10,2350)}),
'1231-3PK':(11.6,54,{('1','240'):(72,17300,10,2350),('1','208'):(80,16640,10,2350),('3','240'):(44.5,17300,10,2350),('3','208'):(51.5,17300,10,2350)}),
'1627-3PK':(18.5,99,{('3','240'):(66,23600,10,2350),('3','208'):(76,23600,10,2350)}),
'1627-3PK-LF':(18.5,99,{('1','240'):(68,16300,1,2100),('1','208'):(69,14300,1,2100),('3','240'):(46,16300,1,2100),('3','208'):(47,14300,1,2100)}),
'714':(1.4,None,{('1','120/208-240'):(20,3600,8,2300)}),
'GT':(1.1,None,{('1','240'):(17,4000,10,2350),('1','208'):(20,4000,10,2350)}),
}
def key_from_title(t):
    if 'GlazeTech' in t: return 'GT'
    if 'Low Fire' in t or 'LF' in t.split(): return '1627-3PK-LF'
    m=re.search(r'KMT?\s?(\d{3,4})(-30A)?(-3)?(PK)?',t)
    if not m: return None
    k=m.group(1)+('-30A' if m.group(2) else '')+('-3' if m.group(3) else '')+('PK' if m.group(4) else '')
    k=k.replace('1627-3PK','1627-3PK')
    if k in ('1218','1222','1227','1231','1627'): k+='-3'
    if k.endswith('-3PK') or k in REF: return k
    if k+'PK' in REF: return k+'PK'
    return k if k in REF else None
def cells(f): return [html.unescape(re.sub(r'<[^>]+>','',c)).strip() for c in re.findall(r'<t[dh][^>]*>(.*?)</t[dh]>',f,re.S)]
def num(s):
    try: return float(s)
    except: return None
def check(p):
    s=(p['specs'] or {}).get('value') or ''
    base=key_from_title(p['title'])
    out=[]
    m=re.search(r'<table class="ceramic-specs">(.*?)</table>',s,re.S)
    if m and base:
        for r in [cells(tr) for tr in re.findall(r'<tr>(.*?)</tr>',m.group(1),re.S)][1:]:
            if len(r)<10: out.append(f'short row {r}'); continue
            k=base
            if '30A' in r[0]: k='818-30A-3'
            if base.startswith('1627'): k='1627-3PK' if 'Cone 10' in r[5] else '1627-3PK-LF'
            cf,tb,rows=REF[k]
            ph,v=r[1],r[2]
            key=(ph or '?',v)
            if ph=='' : out.append(f'{r[0]}: blank phase (volts {v}, amps {r[3]})')
            exp=rows.get(key)
            if exp is None:
                # maybe volts wrong: find a ref row with same phase+amps+watts
                cand=[kk for kk,vv in rows.items() if kk[0]==(ph or kk[0]) and num(r[3])==vv[0] and num(r[4])==vv[1]]
                out.append(f'{r[0]} row ({ph},{v},{r[3]}A,{r[4]}W): no Skutt row; matches {cand}')
                continue
            a,w,c,t=exp
            if num(r[3])!=a: out.append(f'{r[0]} {key}: amps {r[3]} -> {a}')
            if num(r[4])!=w: out.append(f'{r[0]} {key}: watts {r[4]} -> {w}')
            mc=re.search(r'Cone\s*(\d+)\s*,\s*(\d+)',r[5])
            if not mc or int(mc.group(1))!=c or int(mc.group(2))!=t: out.append(f'{r[0]} {key}: temp "{r[5]}" -> Cone {c}, {t} F')
            if num(r[6])!=cf: out.append(f'{r[0]} {key}: cuft {r[6]} -> {cf}')
    c2=re.search(r'<table class="capacity">(.*?)</table>',s,re.S)
    if c2 and base:
        cf,tb,_=REF['1627-3PK' if base.startswith('1627') else ('818-3' if base=='818-30A-3' else base)] if (base in REF or base.startswith('1627')) else (None,None,None)
        for r in [cells(tr) for tr in re.findall(r'<tr>(.*?)</tr>',c2.group(1),re.S)][1:]:
            if len(r)>=4 and cf and num(r[3])!=cf: out.append(f'capacity table {r} -> cuft {cf}')
            if len(r)>=5 and tb and num(r[4])!=tb: out.append(f'capacity table tea bowls {r[4]} -> {tb}')
    return base,out
if __name__=='__main__':
    d=json.load(open(sys.argv[1]))
    for p in d['data']['collection']['products']['nodes']:
        base,out=check(p)
        if out or '--all' in sys.argv:
            print(f"{p['status'][:3]} {p['title'][:75]} [{base}] {p['handle']}")
            for o in out: print('     ',o)
