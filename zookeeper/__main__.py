import sys
from . import zookeeper
from .__version__ import __version__
import logging

def _cli():
    from optparse import OptionParser
    usage=  f"usage:\t%prog [settings]\n"\
            f"backend - VISA backend\n"\
            f"Welcome to zookeeper, version {__version__}\n"
    parser = OptionParser(usage, version="%prog " + __version__)
    
    parser.add_option("-b", "--backend", action="store", type="string",
                      dest="backend", default=zookeeper.backend,
                      help=f"VISA backend. Defaults to `{zookeeper.backend}' ")
    
    (opt, remaining_args) = parser.parse_args()
    
    if opt.backend is not None:
        zookeeper.backend = opt.backend
    
    if len(remaining_args) != 0:
        print("Usage: python -m zookeeper [settings] \npython -m zookeeper -h for help")
        sys.exit(1)
    
    # setup logger    
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
    
    zookeeper.main()
    sys.exit(0)
        
if __name__ == '__main__':
    # setup logger here
    _cli()







