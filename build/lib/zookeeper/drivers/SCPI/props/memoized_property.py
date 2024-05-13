from functools import wraps, partial

#def memoized_property(fget):
#    """
#    Only calls getter on first access
#    """
#    @wraps(fget)
#    def fget_memoized(self):
#        if not hasattr(self, attr_name)

class Attribute(property):
    def __init__(self, limits=(None, None), step=None):
        if len(limits) != 2 or limits[0] >= limits[-1] \
            or type(limits) is not tuple:
            raise AttributeError("limits: bad usage")
        else:
            self.__limits = limits
        
        if step <= 0:
            raise AttributeError("step: bad usage")
        else:
            self.__step = step
        
    def __call__(self, func):
        self.__func = func
        return self.wrapper
    
    def wrapper(self, *args, **kwargs):
        # check limits
        # if     


class Instrument(object):
    def __init__(self, num=0):
        self.__num = num
    
    @Attribute(limits=(1, 10))
    def num(self):
        return self.__num