
from delphin import itsdb
from delphin import ace
from delphin import commands

src_path = 'golden'
tgt_path = 'p'

commands.mkprof(tgt_path, source=src_path)
src_ts = itsdb.TestSuite(src_path)
tgt_ts = itsdb.TestSuite(tgt_path)
with ace.ACEGenerator('erg.dat') as cpu:
    tgt_ts.process(cpu, source=src_ts)
