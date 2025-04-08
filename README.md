# InstrUncache

## 测试目标

InstrUncache模块用于Frontend中获取非缓存指令。例如某一地址对应TLB查询结果为Non-cacheable，IFU发送请求到InstrUncache模块。

`````verilog
module InstrUncache(
  input         clock,
  input         reset,
  input         auto\_client\_out\_a\_ready,
  output        auto\_client\_out\_a\_valid,
  output [47:0] auto\_client\_out\_a\_bits\_address,
  input         auto\_client\_out\_d\_valid,
  input         auto\_client\_out\_d\_bits\_source,
  input  [63:0] auto\_client\_out\_d\_bits\_data,
  input         auto\_client\_out\_d\_bits\_corrupt,
  output        io\_req\_ready,
  input         io\_req\_valid,
  input  [47:0] io\_req\_bits\_addr,
  output        io\_resp\_valid,
  output [31:0] io\_resp\_bits\_data,
  output        io\_resp\_bits\_corrupt
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
async def \_request\_data(instruncache\_bundle, req\_addr, \
                        l2\_resp\_source, l2\_resp\_corrupt, l2\_resp\_data):
`````
instruncache\_bundle:

    创建时钟，绑定待测试模块信号。


`````python
@toffee\_test.testcase
async def test\_instruncache\_addr\_alignment(toffee\_request: toffee\_test.ToffeeRequest):

    toffee.setup\_logging(toffee.WARNING)
    instruncache = toffee\_request.create\_dut(DUTInstrUncache, "clock")
    toffee.start\_clock(instruncache)

    instruncache\_bundle = InstrUncacheBundle()
    instruncache\_bundle.bind(instruncache)

`````

req\_addr:

    IFU向InstrUncache请求数据的地址


l2\_resp\_source, l2\_resp\_corrupt, l2\_resp\_data

    模拟L2返回数据


示例：

`````python
    io\_resp\_valid, \
    io\_resp\_bits\_corrupt, \
    io\_resp\_bits\_data = await \_request\_data(instruncache\_bundle, 0xF0000002, 0, 0, 0xAAAAAAAABBBBBBBB)

    assert 1 == io\_resp\_valid
    assert 0 == io\_resp\_bits\_corrupt
    assert 0xAAAABBBB == io\_resp\_bits\_data
`````

## 用例说明

#### 测试用例1  test\_instruncache\_smoke

|步骤|操作内容|预期结果|覆盖功能点|
|0|reset dut|assert |-|
|0|reset dut                         |assert io\_req\_ready == 1                              |-|

|1|IFU发出读数据请求, 地址0xF0000000 |assert auto\_client\_out\_a\_bits\_address == 0xF0000000     |-|
| |                                  |assert auto\_client\_out\_a\_valid == 1                     |-|
|2|模拟L2返回数据                    |set auto\_client\_out\_d\_bits\_data = 0xAAAAAAAABBBBBBBB    |-|
|3|检测InstrUncache是否正确返回数据  |assert io\_resp\_valid == 1                               |-|
| |                                  |assert io\_resp\_bits\_corrupt == 0                        |-|
| |


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

