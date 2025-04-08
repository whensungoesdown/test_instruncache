from toffee import *


#class AdderBundle(Bundle):
#    a, b, cin, sum, cout = Signals(5)
#
#
#class AdderAgent(Agent):
#    @driver_method()
#    async def exec_add(self, a, b, cin):
#        self.bundle.a.value = a
#        self.bundle.b.value = b
#        self.bundle.cin.value = cin
#        await self.bundle.step()
#        return self.bundle.sum.value, self.bundle.cout.value
#
#    @monitor_method()
#    async def monitor_once(self):
#        return self.bundle.as_dict()


class InstrUncacheBundle(Bundle):
        
    clock, \
    reset, \
    auto_client_out_a_ready, \
    auto_client_out_a_valid, \
    auto_client_out_a_bits_address, \
    auto_client_out_d_valid, \
    auto_client_out_d_bits_source, \
    auto_client_out_d_bits_data, \
    auto_client_out_d_bits_corrupt, \
    io_req_ready, \
    io_req_valid, \
    io_req_bits_addr, \
    io_resp_valid, \
    io_resp_bits_data, \
    io_resp_bits_corrupt = Signals(15)


class InstrUncacheAgent(Agent):
    @driver_method()
    async def exec_reset(self):
#        self.bundle.a.value = a
#        self.bundle.b.value = b
#        self.bundle.cin.value = cin
        self.bundle.reset = 1
        await self.bundle.step()
        await self.bundle.step()
        print ('!!!! reset', self.bundle.reset)
        await self.bundle.step()
        await self.bundle.step()
        await self.bundle.step()
        self.bundle.reset = 0
        self.bundle.auto_client_out_a_ready = 1

        print ('!!!!', self.bundle.io_req_ready)
        print ('!!!!', self.bundle.auto_client_out_a_bits_address)
        return self.bundle.io_req_ready

#    @monitor_method()
#    async def monitor_once(self):
#        return self.bundle.as_dict()
