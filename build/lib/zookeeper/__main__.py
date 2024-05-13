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
    
    parser.add_option("-c", "--config", action="store", type="string",
                    dest="configfile", default=zookeeper.configfile,
                    help=f"Config file name. Must be placed in project root directory.\
                            Defaults to `{zookeeper.configfile}' ")

    (opt, remaining_args) = parser.parse_args()
    
    if opt.backend is not None:
        zookeeper.backend = opt.backend
    if opt.configfile is not None:
        zookeeper.configfile = opt.configfile

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







