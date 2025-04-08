import random

import toffee_test
from picker_out_instruncache import DUTInstrUncache

from env import InstrUncacheBundle
from env import InstrUncacheEnv

import toffee

"""
Test cases
"""

#@toffee_test.testcase
#async def test_random(adder_env):
#    for _ in range(1000):
#        a = random.randint(0, 2**64 - 1)
#        b = random.randint(0, 2**64 - 1)
#        cin = random.randint(0, 1)
#        await adder_env.add_agent.exec_add(a, b, cin)
#
#
#@toffee_test.testcase
#async def test_boundary(adder_env):
#    for cin in [0, 1]:
#        for a in [0, 2**64 - 1]:
#            for b in [0, 2**64 - 1]:
#                await adder_env.add_agent.exec_add(a, b, cin)

"""
Coverage definition
"""

#import toffee.funcov as fc
#from toffee.funcov import CovGroup
#
#
#def adder_cover_point(adder):
#    g = CovGroup("Adder addition function")
#
#    g.add_cover_point(adder.io_cout, {"io_cout is 0": fc.Eq(0)}, name="Cout is 0")
#    g.add_cover_point(adder.io_cout, {"io_cout is 1": fc.Eq(1)}, name="Cout is 1")
#    g.add_cover_point(adder.io_cin, {"io_cin is 0": fc.Eq(0)}, name="Cin is 0")
#    g.add_cover_point(adder.io_cin, {"io_cin is 1": fc.Eq(1)}, name="Cin is 1")
#    g.add_cover_point(adder.io_a, {"a > 0": fc.Gt(0)}, name="signal a set")
#    g.add_cover_point(adder.io_b, {"b > 0": fc.Gt(0)}, name="signal b set")
#    g.add_cover_point(adder.io_sum, {"sum > 0": fc.Gt(0)}, name="signal sum set")
#    g.add_cover_point(
#        (toffee.Delayer(adder.io_cout, 1), adder.io_cout),
#        {
#            "io_cout 1 -> 0": lambda signal: signal[0].value == 1
#            and signal[1].value == 0
#        },
#        name="Cout 1 -> 0",
#    )
#
#    return g


#@toffee_test.testcase
#async def test_reset(instruncache_env):
#    print ('reset', instruncache_env.instruncache_agent.bundle.reset)
#    io_req_ready = await instruncache_env.instruncache_agent.exec_reset()
##    print ('io_req_ready', instruncache_env.instruncache_bundle.io_req_ready)
##    print ('io_resp_valid', instruncache_env.instruncache_bundle.io_resp_valid)
##    print ('x io_req_ready', io_req_ready)
#    print ('io_req_ready', instruncache_env.instruncache_agent.bundle.io_req_ready)
#    print ('auto_client_out_a_bits_address', instruncache_env.instruncache_agent.bundle.auto_client_out_a_bits_address)
#




"""
Initialize before each test
"""



#@toffee_test.fixture
#async def instruncache_env(toffee_request: toffee_test.ToffeeRequest):
#    toffee.setup_logging(toffee.WARNING)
#    dut = toffee_request.create_dut(DUTInstrUncache, "clock")
##    toffee_request.add_cov_groups(adder_cover_point(dut))
#    toffee.start_clock(dut)
##    return AdderEnv(AdderBundle.from_prefix("io_").bind(dut))
#    #return InstrUncacheEnv(InstrUncacheBundle.from_regex(".*").bind(dut))
#    instruncache_bundle = InstrUncacheBundle()
#    instruncache_bundle.bind(dut)
#    return InstrUncacheEnv(instruncache_bundle)




from toffee import *

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


#class InstrUncacheAgent(Agent):
#    @driver_method()
#    async def exec_reset(self):
##        self.bundle.a.value = a
##        self.bundle.b.value = b
##        self.bundle.cin.value = cin
#        self.bundle.reset = 1
#        await self.bundle.step()
#        await self.bundle.step()
#        print ('!!!! reset', self.bundle.reset)
#        await self.bundle.step()
#        await self.bundle.step()
#        await self.bundle.step()
#        self.bundle.reset = 0
#        self.bundle.auto_client_out_a_ready = 1
#
#        print ('!!!!', self.bundle.io_req_ready.value)
#        print ('!!!!', self.bundle.auto_client_out_a_bits_address.value)
#        return self.bundle.io_req_ready


@toffee_test.testcase
async def test_instruncache_smoke(toffee_request: toffee_test.ToffeeRequest):

    toffee.setup_logging(toffee.WARNING)
    instruncache = toffee_request.create_dut(DUTInstrUncache, "clock")
    toffee.start_clock(instruncache)

    instruncache_bundle = InstrUncacheBundle()
    instruncache_bundle.bind(instruncache)


    # Simulate L2 already ready
    instruncache_bundle.auto_client_out_a_ready.value = 1


    #
    # reset dut
    #

    #instruncache_bundle['reset'].value = 1
    instruncache_bundle.reset.value = 1
    await instruncache_bundle.step(10)
    instruncache_bundle.reset.value = 0
    await instruncache_bundle.step(1)

    assert 1 == instruncache_bundle.io_req_ready.value


    #
    # Simulate IFU sends a request
    #

    instruncache_bundle.io_req_bits_addr.value= 0xF0000000;
    instruncache_bundle.io_req_valid.value = 1;

    await instruncache_bundle.step(1)

    # pull io_req_valid low after seeing io_req_ready high for one cycle
    instruncache_bundle.io_req_valid.value = 0;

    await instruncache_bundle.step(1)


    # InstrUncache should be busy now
    assert 0 == instruncache_bundle.io_req_ready.value

    # InstrUncache should send out request to L2
    assert 0xF0000000 == instruncache_bundle.auto_client_out_a_bits_address.value
    assert 1 == instruncache_bundle.auto_client_out_a_valid.value

    # after seeing auto_client_out_a_valid high for once cycle, L2 should turn to busy
    instruncache_bundle.auto_client_out_a_ready.value = 0

    await instruncache_bundle.step(1)


    #
    # Simulate L2 takes the request and sends back data
    #


    # L2 may take variable cycles to get back the data
    await instruncache_bundle.step(5)

    instruncache_bundle.auto_client_out_d_valid.value = 1
    instruncache_bundle.auto_client_out_d_bits_source.value = 0
    instruncache_bundle.auto_client_out_d_bits_corrupt.value = 0
    instruncache_bundle.auto_client_out_d_bits_data.value = 0xAAAAAAAABBBBBBBB
   
    # _data with _valid last for one cycle
    await instruncache_bundle.step(1)
    instruncache_bundle.auto_client_out_d_valid.value = 0
    instruncache_bundle.auto_client_out_d_bits_source.value = 0
    instruncache_bundle.auto_client_out_d_bits_corrupt.value = 0
    instruncache_bundle.auto_client_out_d_bits_data.value = 0

    # L2 ready to take another request
    instruncache_bundle.auto_client_out_a_ready.value = 1



    #
    # Test InstrUncache return data to IFU the requester
    #

    # Needs one cycle for the data to go through InstrUncache, registering
    await instruncache_bundle.step(1)

    assert 1 == instruncache_bundle.io_resp_valid.value
    assert 0 == instruncache_bundle.io_resp_bits_corrupt.value
    assert 0xBBBBBBBB == instruncache_bundle.io_resp_bits_data.value



    #print ('reset', instruncache_bundle.reset)
    #print ('io_req_ready', instruncache_bundle.io_req_ready.value)
    #print ('auto_client_out_a_bits_address', instruncache_bundle.auto_client_out_a_bits_address)


async def _request_data(instruncache_bundle, req_addr, \
                        l2_resp_source, l2_resp_corrupt, l2_resp_data):

    # Simulate L2 already ready
    instruncache_bundle.auto_client_out_a_ready.value = 1


    #
    # reset dut
    #

    #instruncache_bundle['reset'].value = 1
    instruncache_bundle.reset.value = 1
    await instruncache_bundle.step(10)
    instruncache_bundle.reset.value = 0
    await instruncache_bundle.step(1)

    assert 1 == instruncache_bundle.io_req_ready.value


    #
    # Simulate IFU sends a request
    #

    instruncache_bundle.io_req_bits_addr.value= req_addr;
    instruncache_bundle.io_req_valid.value = 1;

    await instruncache_bundle.step(1)

    # pull io_req_valid low after seeing io_req_ready high for one cycle
    instruncache_bundle.io_req_valid.value = 0;

    await instruncache_bundle.step(1)


    # InstrUncache should be busy now
    assert 0 == instruncache_bundle.io_req_ready.value

    # InstrUncache should send out request to L2
    assert 0xF0000000 == instruncache_bundle.auto_client_out_a_bits_address.value
    assert 1 == instruncache_bundle.auto_client_out_a_valid.value

    # after seeing auto_client_out_a_valid high for once cycle, L2 should turn to busy
    instruncache_bundle.auto_client_out_a_ready.value = 0

    await instruncache_bundle.step(1)


    #
    # Simulate L2 takes the request and sends back data
    #


    # L2 may take variable cycles to get back the data
    await instruncache_bundle.step(5)

    instruncache_bundle.auto_client_out_d_valid.value = 1
    instruncache_bundle.auto_client_out_d_bits_source.value = l2_resp_source
    instruncache_bundle.auto_client_out_d_bits_corrupt.value = l2_resp_corrupt
    instruncache_bundle.auto_client_out_d_bits_data.value = l2_resp_data
   
    # _data with _valid last for one cycle
    await instruncache_bundle.step(1)
    instruncache_bundle.auto_client_out_d_valid.value = 0
    instruncache_bundle.auto_client_out_d_bits_source.value = 0
    instruncache_bundle.auto_client_out_d_bits_corrupt.value = 0
    instruncache_bundle.auto_client_out_d_bits_data.value = 0

    # L2 ready to take another request
    instruncache_bundle.auto_client_out_a_ready.value = 1



    #
    # Test InstrUncache return data to IFU the requester
    #

    # Needs one cycle for the data to go through InstrUncache, registering
    await instruncache_bundle.step(1)

    #assert 1 == instruncache_bundle.io_resp_valid.value
    #assert 0 == instruncache_bundle.io_resp_bits_corrupt.value
    #assert 0xBBBBBBBB == instruncache_bundle.io_resp_bits_data.value
    return instruncache_bundle.io_resp_valid.value, \
            instruncache_bundle.io_resp_bits_corrupt.value, \
            instruncache_bundle.io_resp_bits_data.value



#
#  0xF0000006 case is questionable
#  should define whats normal behavior
#

@toffee_test.testcase
async def test_instruncache_addr_alignment(toffee_request: toffee_test.ToffeeRequest):

    toffee.setup_logging(toffee.WARNING)
    instruncache = toffee_request.create_dut(DUTInstrUncache, "clock")
    toffee.start_clock(instruncache)

    instruncache_bundle = InstrUncacheBundle()
    instruncache_bundle.bind(instruncache)

    # subtest 0
    io_resp_valid, \
    io_resp_bits_corrupt, \
    io_resp_bits_data = await _request_data(instruncache_bundle, 0xF0000002, 0, 0, 0xAAAAAAAABBBBBBBB)

    assert 1 == io_resp_valid
    assert 0 == io_resp_bits_corrupt
    assert 0xAAAABBBB == io_resp_bits_data

    # subtest 1
    io_resp_valid, \
    io_resp_bits_corrupt, \
    io_resp_bits_data = await _request_data(instruncache_bundle, 0xF0000004, 0, 0, 0xAAAAAAAABBBBBBBB)

    assert 1 == io_resp_valid
    assert 0 == io_resp_bits_corrupt
    assert 0xAAAAAAAA == io_resp_bits_data

    # subtest 2
    io_resp_valid, \
    io_resp_bits_corrupt, \
    io_resp_bits_data = await _request_data(instruncache_bundle, 0xF0000006, 0, 0, 0xAAAAAAAABBBBBBBB)

    assert 1 == io_resp_valid
    assert 0 == io_resp_bits_corrupt
    assert 0x0000AAAA == io_resp_bits_data


#
#  InstrUncache does not handle addr misalignment
#  simpley ignore the address bit 0
#
@toffee_test.testcase
async def test_instruncache_addr_misalign(toffee_request: toffee_test.ToffeeRequest):

    toffee.setup_logging(toffee.WARNING)
    instruncache = toffee_request.create_dut(DUTInstrUncache, "clock")
    toffee.start_clock(instruncache)

    instruncache_bundle = InstrUncacheBundle()
    instruncache_bundle.bind(instruncache)

    # subtest 0
    io_resp_valid, \
    io_resp_bits_corrupt, \
    io_resp_bits_data = await _request_data(instruncache_bundle, 0xF0000001, 0, 0, 0xAAAAAAAABBBBBBBB)

    assert 1 == io_resp_valid
    assert 0 == io_resp_bits_corrupt
    assert 0xBBBBBBBB == io_resp_bits_data


@toffee_test.testcase
async def test_instruncache_l2_resp_corrupt(toffee_request: toffee_test.ToffeeRequest):

    toffee.setup_logging(toffee.WARNING)
    instruncache = toffee_request.create_dut(DUTInstrUncache, "clock")
    toffee.start_clock(instruncache)

    instruncache_bundle = InstrUncacheBundle()
    instruncache_bundle.bind(instruncache)

    # subtest 0
    io_resp_valid, \
    io_resp_bits_corrupt, \
    io_resp_bits_data = await _request_data(instruncache_bundle, 0xF0000001, 0, 1, 0xAAAAAAAABBBBBBBB)

    assert 1 == io_resp_valid
    assert 1 == io_resp_bits_corrupt
    #assert 0xBBBBBBBB == io_resp_bits_data
