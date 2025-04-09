# InstrUncache

## 测试目标

InstrUncache模块用于Frontend中获取非缓存指令。例如某一地址对应TLB查询结果为Non-cacheable，IFU发送请求到InstrUncache模块。

`````verilog
module InstrUncache(
  input         clock,
  input         reset,
  input         auto_client_out_a_ready,
  output        auto_client_out_a_valid,
  output [47:0] auto_client_out_a_bits_address,
  input         auto_client_out_d_valid,
  input         auto_client_out_d_bits_source,
  input  [63:0] auto_client_out_d_bits_data,
  input         auto_client_out_d_bits_corrupt,
  output        io_req_ready,
  input         io_req_valid,
  input  [47:0] io_req_bits_addr,
  output        io_resp_valid,
  output [31:0] io_resp_bits_data,
  output        io_resp_bits_corrupt
);
`````

测试方法：模拟IFU向InstrUncache发出读数据请求。InstrUncache收到后向L2缓存接口发读数据请求。模拟L2返回数据，检测InstrUncache返回给IFU的数据是否正确。

## 测试环境

Ubuntu 24.04, 测试环境依赖g++, python3，verilator，xspcomm，picker，pytest，toffee，toffee-test。

## 功能检测


|序号|所属模块|功能描述|检查点描述|检查标识|检查项|

|0|InstrUncache|检测InstrUncache基本功能，模拟IFU向InstrUncache发送读数据请求以及L2返回数据，检测InstrUncache返回给IFU的数据是否正确。|-|-|-|

|-|-|-|-|-|-|


## 验证接口

`````python
async def _request_data(instruncache_bundle, req_addr, \
                        l2_resp_source, l2_resp_corrupt, l2_resp_data):
`````
instruncache\_bundle:

    创建时钟，绑定待测试模块信号。


`````python
@toffee_test.testcase
async def test_instruncache_addr_alignment(toffee_request: toffee_test.ToffeeRequest):

    toffee.setup_logging(toffee.WARNING)
    instruncache = toffee_request.create_dut(DUTInstrUncache, "clock")
    toffee.start_clock(instruncache)

    instruncache_bundle = InstrUncacheBundle()
    instruncache_bundle.bind(instruncache)

`````

req\_addr:

    IFU向InstrUncache请求数据的地址


l2\_resp\_source, l2\_resp\_corrupt, l2\_resp\_data

    模拟L2返回数据


示例：

`````python
    io_resp_valid, \
    io_resp_bits_corrupt, \
    io_resp_bits_data = await _request_data(instruncache_bundle, 0xF0000002, 0, 0, 0xAAAAAAAABBBBBBBB)

    assert 1 == io_resp_valid
    assert 0 == io_resp_bits_corrupt
    assert 0xAAAABBBB == io_resp_bits_data
`````

## 用例说明

#### 测试用例1  test\_instruncache\_smoke

测试步骤

##### 1. reset

拉高reset信号10个时钟周期，再恢复reset到0。

检测

`````python
    assert 1 == instruncache_bundle.io_req_ready.value
`````

值为1表示设备重置，可以接受请求。


##### 2. 模拟IFU发出读数据请求, addr = 0xF0000000

InstrUncache收到IFU的请求后，转向L2请求数据。

检测L2请求是否正确发出

`````python
    assert 0xF0000000 == instruncache_bundle.auto_client_out_a_bits_address.value
    assert 1 == instruncache_bundle.auto_client_out_a_valid.value
`````

##### 3. 模拟L2返回数据

设置

`````python
    instruncache_bundle.auto_client_out_d_valid.value = 1
    instruncache_bundle.auto_client_out_d_bits_source.value = 0
    instruncache_bundle.auto_client_out_d_bits_corrupt.value = 0
    instruncache_bundle.auto_client_out_d_bits_data.value = 0xAAAAAAAABBBBBBBB
`````

##### 4. 检测InstrUncache是否向IFU返回数据

IFU向InstrUncache请求的数据是32位宽，InstrUncache向L2请求的数据是64位宽。
所以InstrUncache要根据数据地址对数据做相应处理，截取32位。

检测

`````python
    assert 1 == instruncache_bundle.io_resp_valid.value
    assert 0 == instruncache_bundle.io_resp_bits_corrupt.value
    assert 0xBBBBBBBB == instruncache_bundle.io_resp_bits_data.value
`````


#### 测试用例2

|步骤|操作内容|预期结果|覆盖功能点|
|x|x|x|x|
|-|-|-|-|


## 目录结构

<对本模块的目录结构进行描述>


## 检测列表


- [ ] 本文档符合指定[模板]()要求
- [ ] Env提供的API不包含任何DUT引脚和时序信息
- [ ] Env的API保持稳定（共有[ X ]个）
- [ ] Env中对所支持的RTL版本（支持版本[ X ]）进行了检查
- [ ] 功能点（共有[ X ]个）与[设计文档]()一致
- [ ] 检查点（共有[ X ]个）覆盖所有功能点
- [ ] 检查点的输入不依赖任何DUT引脚，仅依赖Env的标准API
- [ ] 所有测试用例（共有[ X ]个）都对功能检查点进行了反标
- [ ] 所有测试用例都是通过 assert 进行的结果判断
- [ ] 所有DUT或对应wrapper都是通过fixture创建
- [ ] 在上述fixture中对RTL版本进行了检查
- [ ] 创建DUT或对应wrapper的fixture进行了功能和代码行覆盖率统计
- [ ] 设置代码行覆盖率时对过滤需求进行了检查

