import socket

from delphin.codecs import simplemrs, mrx
from delphin.codecs import mrsprolog

from xml.etree import ElementTree as ET
import re

def parsePlugs(plugs):
    mapped = {}
    r = "plug\((h\d+) (h\d+)\)"
    res = re.findall(r, plugs)
    return res


class UtoolConnection:
    
    def __init__(self, hostname = "127.0.0.1", port = 2802):
        self.hostname = hostname
        self.port = port

    def solve0(self, domgraph, inputcodec, outputcodec):
        ret = []

        msg = f'''
        <utool cmd="solve" output-codec="{outputcodec}">
          <usr codec="{inputcodec}" string="{domgraph}"/>
         </utool>
        '''

        self._connect()
        self.f.write(msg)
        self.f.flush()
        self.sock.shutdown(1)

        result = self.f.read()
        element = ET.XML(result)

        if element.tag == "error":
            raise Exception("Error: " + element.attrib["explanation"])
        elif element.tag == "result":
            for subelement in element:
                if subelement.tag == "solution":
                    ret.append(subelement.attrib["string"])
            self._close()
            
        return ret
    

    def solve(self, m):
        def aux(solution):
            scopes = m.scopes()            
            root = list(set(scopes[1].keys()) - set([s[1] for s in solution]))[0]
            return dict(root = root, plugs = {v[0] : v[1] for v in solution})

        m.icons.clear()
        pl = mrsprolog.encode(m, indent=True)
        solutions = self.solve0(pl, "mrs-prolog", "plugging-oz")
        return [aux(parsePlugs(r)) for r in solutions]

    
    def solvable0(self, domgraph, inputcodec = "mrs-prolog"):

        msg = f'''
        <utool cmd="solvable">
          <usr codec="{inputcodec}" string="{domgraph}"/>
         </utool>
        '''
        
        self._connect()
        self.f.write(msg)
        self.f.flush()
        self.sock.shutdown(1)

        result = self.f.read()
        element = ET.XML(result)
        data = {}

        if element.tag == "error":
            raise Exception(f"Error: {element.attrib['explanation']}")
        elif element.tag == "result":
            self._close()
            return element.attrib

    def solvable(self, m):
        m.icons.clear()
        pl = mrsprolog.encode(m, indent=True)
        
        return self.solvable0(pl, inputcodec = "mrs-prolog")
        
        
    def _connect(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setblocking(True)
        self.sock.connect((self.hostname, self.port))
        self.f = self.sock.makefile(mode='rw')
        
    def _close(self):
        self.sock.close()



