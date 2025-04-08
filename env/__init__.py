from .agent import InstrUncacheAgent
from .agent import InstrUncacheBundle
#from .refmodel import AdderModelWithDriverHook
#from .refmodel import AdderModelWithMonitorHook
#from .refmodel import AdderModelWithPort
from toffee import *


class InstrUncacheEnv(Env):
    def __init__(self, instruncache_bundle):
        super().__init__()
        self.instruncache_agent = InstrUncacheAgent(instruncache_bundle)
#        self.instruncache_bundle = instruncache_bundle

#        self.attach(AdderModelWithDriverHook())
#        self.attach(AdderModelWithMonitorHook())
#        self.attach(AdderModelWithPort())
