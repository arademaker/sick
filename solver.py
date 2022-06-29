from delphin import ace
from delphin.codecs import simplemrs, mrx
from delphin.codecs import mrsprolog
import sys, os
from delphin import tsql, itsdb
import utoolclient

root = "data"
profiles = ["sentences-aa","sentences-ab","sentences-ac","sentences-ad"]
utool = utoolclient.UtoolConnection()

for p in profiles:
    ignore = None
    ts = itsdb.TestSuite(f'{root}/{p}')
    print(f"> Loading {p}")
    rows = tsql.select('i-id readings result-id i-input mrs', ts)
    print(f"> Loaded {p}")
    for r in rows:
        if r[0] == ignore:
            continue
        mrs = simplemrs.decode(r[4])
        try:
            s = utool.solvable(mrs)['count']
        except Exception as e:
            ignore = r[0]
            print(f"> [{r[0]}] {r[3]} ({r[2]}/{r[1]} readings)\n {e}")
        else:
            ignore = None
