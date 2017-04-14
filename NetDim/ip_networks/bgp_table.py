# NetDim (contact@netdim.fr)

from miscellaneous.network_functions import compute_network
from pythonic_tkinter.preconfigured_widgets import *
from operator import itemgetter

class BGPTable(CustomTopLevel):
    def __init__(self, node, view):
        super().__init__() 
        self.cs = view
        self.ST = ScrolledText(self)
        self.wm_attributes('-topmost', True)

        codes = '''
BGP table version is 6, local router ID is {ip}
Status codes: s suppressed, d damped, h history, * valid, > best, i - internal,
              r RIB-failure, S Stale, m multipath, b backup-path, x best-external, f RT-Filter, a additional-path
Origin codes: i - IGP, e - EGP, ? - incomplete
RPKI validation codes: V valid, I invalid, N Not found\n'''\
                                            .format(ip=node.ipaddress)
        
        self.ST.insert('insert', codes)
        
        if node.default_route:
            gateway = 'Gateway of last resort is {gw} to network 0.0.0.0\n\n'\
                                        .format(gw=node.default_route)
        else:
            gateway = 'Gateway of last resort is not set\n\n'
        self.ST.insert('insert', gateway)
                
        for sntw, routes in node.bgpt.items():
            if len(routes) - 1:
                for idx, route in enumerate(routes):
                    weight, nh, source, AS_path = route
                    rtype = 'N*' + ' '*8
                    if not idx:
                        line = '{rtype} {sntw} {nh}  0  {weight} {path}\n'\
                                        .format(
                                                rtype = rtype, 
                                                sntw = sntw, 
                                                nh = nh,
                                                weight = weight,
                                                path = ''.join(map(str, AS_path))
                                                )
                    else:
                        spaces = ' '*(len(rtype) + len(sntw))
                        line = '{spaces} {nh}  0  {weight} {path}\n'\
                                        .format(
                                                spaces = spaces,
                                                nh = nh,
                                                weight = weight,
                                                path = ''.join(map(str, AS_path))
                                                )
            else:
                route ,= routes
                weight, nh, source, AS_path = route
                rtype = 'N*' + ' '*8
                line = '{rtype} {sntw} {nh}  0  {weight} {path}\n'\
                                .format(
                                        rtype = rtype, 
                                        sntw = sntw, 
                                        nh = nh,
                                        weight = weight,
                                        path = ' '.join(map(str, AS_path))
                                        )
                self.ST.insert('insert', line)
                                        
        self.ST.pack(fill='both', expand='yes')