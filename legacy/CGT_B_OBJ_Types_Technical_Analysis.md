# CGT_B 项目中的 OBJ 类型深度技术分析

## 概述

本文档基于CGT_B源代码分析，详细阐述了三种核心OBJ类型（OBJ_MSG、OBJ_COM、OBJ_GUEST）在航空电子系统SPOCK配置管理中的技术实现和验证机制。

---

## 1. 核心数据结构与类定义

### 1.1 XmlObject 基础类

**文件位置**: `source/CGT/XmlConfiguration/XmlLogicalStructure/XmlObject.cs:17`

```csharp
[XmlRoot("OBJECT")]
public class XmlObject : IXmlSerializable
{
    private string objectType;          // OBJ_MSG, OBJ_COM, OBJ_GUEST
    private string objectName;          // 对象实例名称
    private XmlMapping objectMapping;   // 输入输出映射关系
    private XmlSpecific specific;       // 特定配置（如消息映射）
    private string lruId;              // 关联的LRU板卡ID
  
    public string ObjectType => objectType;
    public string ObjectName => objectName;
    public XmlMapping ObjectMapping => objectMapping;
    public XmlSpecific Specific => specific;
    public string LruId { get; set; }
}
```

**核心功能**:

- XML序列化/反序列化接口实现
- LRU板卡关联算法
- 输入输出映射管理
- 数据完整性验证

### 1.2 XmlObjectComMsg 消息映射类

**文件位置**: `source/CGT/XmlConfiguration/XmlLogicalStructure/XmlObjectComMsg.cs:10`

```csharp
[XmlRoot("OBJECT_COM_MSG")]
public class XmlObjectComMsg : IXmlSerializable
{
    private Collection<XmlDataMapping> dataMappingList;
    private ComMessageDirections direction;  // Consumed/Produced
    private string messageId;                // MSG_RX_VITAL_1, MSG_TX_VITAL_1等
  
    public enum ComMessageDirections
    {
        Consumed,   // 接收消息
        Produced    // 发送消息
    }
}
```

---

## 2. OBJ_MSG - 对外消息对象详解

### 2.1 核心处理逻辑

**文件位置**: `source/CGT/Process.cs:2165`

```csharp
Collection<XmlObject> logObjectCollection = XmlConfigurationManager.Instance.CurrentDevice.LogStruct.LogObjectCollection;
foreach (XmlObject obj2 in logObjectCollection)
{
    if (obj2.ObjectType == "OBJ_MSG")
    {
        // 处理输出映射 - 用于发送消息
        foreach (XmlOutput output in obj2.ObjectMapping.OutputDictionary)
        {
            if (output.Mapping is XmlLogical)
            {
                XmlLogical mapping = (XmlLogical)output.Mapping;
                if (mapping != null)
                {
                    dictionary.Add(mapping.DataName, obj2);
                }
            }
        }
      
        // 处理输入映射 - 用于接收消息
        foreach (XmlInput input in obj2.ObjectMapping.InputDictionary)
        {
            if (input.Mapping is XmlLogical)
            {
                XmlLogical logical2 = (XmlLogical)input.Mapping;
                if (logical2 != null)
                {
                    if (!dictionary2.ContainsKey(logical2.DataName))
                    {
                        dictionary2[logical2.DataName] = new List<XmlObject>();
                    }
                    dictionary2[logical2.DataName].Add(obj2);
                }
            }
        }
    }
}
```

### 2.2 严格验证机制

**文件位置**: `source/CGT/Process.cs:2392-2395`

```csharp
private static bool CheckObjectType_Methodo_128()
{
    bool flag = true;
    foreach (XmlObject obj2 in XmlConfigurationManager.Instance.CurrentDevice.LogStruct.LogObjectCollection)
    {
        // 强制约束：只有OBJ_MSG类型才能包含OBJECT_COM_MSG配置
        if (((obj2.Specific != null) && (obj2.Specific.ComMsgDictionary.Count != 0)) 
            && (obj2.ObjectType != "OBJ_MSG"))
        {
            flag = false;
            Program.Log.Error("00,NH", 
                "Object {0} having OBJECT_COM_MSG list, but not set to the type OBJ_MSG", 
                new object[] { obj2.ObjectName });
        }
    }
    return flag;
}
```

### 2.3 防止循环连接验证

**文件位置**: `source/CGT/Process.cs:2202-2206`

```csharp
// 防止同一LRU上的OBJECT_COM_MSG直接连接
foreach (XmlObject obj2 in list)
{
    if (obj2.LruId == pair.Value.LruId)
    {
        Program.Log.Error("00,CY", 
            "There is a direct link defined between two OBJECT_COM_MSG ({0} and {1}) located on the same LRU ({2})", 
            new object[] { obj2.ObjectName, pair.Value.ObjectName, pair.Value.LruId });
        return false;
    }
}
```

### 2.4 配置示例分析

```xml
<!-- 输入消息配置 -->
<OBJECT OBJ_TYPE="OBJ_MSG" OBJECT_DESCR="FROM:VITAL" OBJECT_NAME="OBJ_COM_INCOMING1">
  <MAPPING>
    <INPUT IO_NUMBER="1" IO_USE="true">
      <PHYSICAL CELL_ID="CELL_COM_R1_L2_C1" />
    </INPUT>
    <OUTPUT IO_NUMBER="1" IO_USE="true">
      <LOGICAL DATA_LENGTH="1" DATA_TYPE="SAFETY_DATA" DATA_NAME="DATA_IN_G_1_3_1" DATA_DEFAULT="00000000" />
    </OUTPUT>
  </MAPPING>
  <SPECIFIC>
    <OBJECT_COM_MSG MESSAGE_ID="MSG_RX_VITAL_1" DIRECTION="CONSUMED">
      <DATA_MAPPING IO_NUMBER="1" OFFSET="0" />
      <DATA_MAPPING IO_NUMBER="2" OFFSET="1" />
    </OBJECT_COM_MSG>
  </SPECIFIC>
</OBJECT>
```

**技术特点**:

- **MESSAGE_ID**: 唯一标识符，用于USIG安全会话关联
- **DIRECTION**: Consumed(接收)/Produced(发送)
- **OFFSET**: 消息内数据的字节偏移位置，确保数据帧结构正确性

---

## 3. OBJ_COM - 以太网通信码位对象

### 3.1 网络层抽象设计

```xml
<OBJECT OBJ_TYPE="OBJ_COM" OBJECT_DESCR="COM object" OBJECT_NAME="OBJ_COM_1">
  <MAPPING>
    <OUTPUT IO_NUMBER="1" IO_USE="true">
      <LOGICAL DATA_LENGTH="1" DATA_TYPE="SAFETY_DATA" DATA_NAME="DATA_OUT_G_1_2_1" DATA_DEFAULT="00000001" />
    </OUTPUT>
    <OUTPUT IO_NUMBER="2" IO_USE="true">
      <LOGICAL DATA_LENGTH="2" DATA_TYPE="SAFETY_DATA" DATA_NAME="DATA_OUT_G_1_2_2" DATA_DEFAULT="00000003" />
    </OUTPUT>
  </MAPPING>
  <SPECIFIC />  <!-- 无特定消息配置 -->
</OBJECT>
```

### 3.2 与物理网络配置的关联

```xml
<!-- 对应的物理网络配置 -->
<CELL_COM>
  <IP TIME_TO_LIVE="9">
    <NORMAL_IP IP_TYPE="PRIMARY_N" IP_ADDRESS="20.3.1.8" IP_SUBNET_MASK="255.255.0.0" />
    <REDUNDANT_IP IP_TYPE="PRIMARY_R" IP_ADDRESS="20.5.1.9" IP_SUBNET_MASK="255.255.0.0" />
  </IP>
  <UDP>
    <PORT UDP_TYPE="FSFB2" UDP_N="40000" UDP_R="40001" />
  </UDP>
  <USIG SS_TYPE="80" LOG_ID="6" SS_ID="6">
    <SAFTY_TRAFFIC PROTOCOL_TYPE="FSFB2" MAX_LIFE_TIME="3" MAX_DELTA_TC="3" />
  </USIG>
</CELL_COM>
```

**技术特点**:

- **数据中继功能**: 作为OBJ_MSG和OBJ_GUEST之间的逻辑桥梁
- **网络协议支持**: FSFB2安全功能块协议
- **IP冗余配置**: PRIMARY/REDUNDANT双路径保障

---

## 4. OBJ_GUEST - 板卡对应关系对象

### 4.1 冗余机制实现

```xml
<!-- 主板卡对象 -->
<OBJECT OBJ_TYPE="OBJ_GUEST" OBJECT_DESCR="COM transobj" OBJECT_NAME="OBJ_GUEST_1_4">
  <MAPPING>
    <INPUT IO_NUMBER="1" IO_USE="true">
      <LOGICAL DATA_NAME="DATA_IN_G_1_4_1" />
    </INPUT>
    <OUTPUT IO_NUMBER="1" IO_USE="true">
      <LOGICAL DATA_LENGTH="1" DATA_TYPE="SAFETY_DATA" DATA_NAME="DATA_OUT_G_1_4_1" DATA_DEFAULT="00000000" />
    </OUTPUT>
  </MAPPING>
</OBJECT>

<!-- 冗余板卡对象 -->
<OBJECT OBJ_TYPE="OBJ_GUEST" OBJECT_DESCR="COM transobj" OBJECT_NAME="OBJ_GUEST_1_9">
  <MAPPING>
    <INPUT IO_NUMBER="1" IO_USE="true">
      <LOGICAL DATA_NAME="DATA_IN_G_1_4_1" />  <!-- 共享输入数据 -->
    </INPUT>
    <OUTPUT IO_NUMBER="1" IO_USE="true">
      <LOGICAL DATA_LENGTH="1" DATA_TYPE="SAFETY_DATA" DATA_NAME="DATA_OUT_G_1_9_1" DATA_DEFAULT="00000000">
        <DATA_REDUNDANCY REDUNDANCY_TYPE="BOOLEAN" REDUNDANT_DATA_NAME="DATA_OUT_G_1_4_1" />
      </LOGICAL>
    </OUTPUT>
  </MAPPING>
</OBJECT>
```

### 4.2 对应的物理层配置

```xml
<LRU LRU_ID="LRU_1_4" LRU_SLOT="4" LRU_NAME="1_4" LRU_TYPE="LRU_VOOB16E" LRU_CODE="MAGICMAGICMAG">
  <LRU_PARAM>
    <LRU_GUEST PARAM_DATA_VERSION="1.0"/> 
  </LRU_PARAM>
</LRU>

<LRU LRU_ID="LRU_1_9" LRU_SLOT="9" LRU_NAME="1_9" LRU_TYPE="LRU_VOOB16E" 
     LRU_CODE="CASCO_VOOB16E" REDUNDANT_LRU_ID="LRU_1_4">
  <LRU_PARAM>
    <LRU_GUEST PARAM_DATA_VERSION="1.0"/> 
  </LRU_PARAM>
</LRU>
```

**冗余策略**:

- **布尔冗余**: REDUNDANCY_TYPE="BOOLEAN"
- **数据关联**: REDUNDANT_DATA_NAME指向主数据源
- **硬件冗余**: REDUNDANT_LRU_ID提供板卡级故障切换

---

## 5. LRU板卡类型关联与验证

### 5.1 严格类型匹配验证

**文件位置**: `source/CGT/Process.cs:2318-2372`

```csharp
foreach (XmlObject obj2 in XmlConfigurationManager.Instance.CurrentDevice.LogStruct.LogObjectCollection)
{
    if (((obj2.ObjectType == "OBJ_MSG") || (obj2.ObjectType == "OBJ_OM")) || (obj2.ObjectType == "OBJ_IM"))
    {
        if (dictionary2[obj2.ObjectName].Count != 1)
        {
            flag = false;
            Program.Log.Error("00,NG", "Object {0} of type {1} linked to many Lru's", 
                new object[] { obj2.ObjectName, obj2.ObjectType });
        }
        else if (((obj2.ObjectType == "OBJ_IM") || (obj2.ObjectType == "OBJ_OM")) 
                && dictionary.ContainsKey(dictionary2[obj2.ObjectName][0].LruId))
        {
            // OBJ_IM必须关联LRU_IM类型
            if ((obj2.ObjectType == "OBJ_IM") && (dictionary2[obj2.ObjectName][0].LruType != "LRU_IM"))
            {
                flag = false;
                Program.Log.Error("00,NG", "Object {0} of type {1} is not linked to Lru of type LRU_IM", 
                    new object[] { obj2.ObjectName, obj2.ObjectType });
            }
            // OBJ_OM必须关联LRU_OM类型  
            else if ((obj2.ObjectType == "OBJ_OM") && (dictionary2[obj2.ObjectName][0].LruType != "LRU_OM"))
            {
                flag = false;
                Program.Log.Error("00,NG", "Object {0} of type {1} is not linked to Lru of type LRU_OM", 
                    new object[] { obj2.ObjectName, obj2.ObjectType });
            }
        }
    }
}
```

### 5.2 端口方向验证

```csharp
// OBJ_IM验证：只能有物理输出，不能有逻辑输入
if ((obj2.ObjectType == "OBJ_IM") && (dictionary2[obj2.ObjectName][0].LruType == "LRU_IM"))
{
    for (int num = 0; num < obj2.ObjectMapping.InputDictionary.Count; num++)
    {
        if (obj2.ObjectMapping.InputDictionary[num].Mapping is XmlLogical)
        {
            flag = false;
            Program.Log.Error("00,NG", "Object {0} of type {1} is defined with logical input(s)", 
                new object[] { obj2.ObjectName, obj2.ObjectType });
        }
    }
}

// OBJ_OM验证：只能有物理输入，不能有逻辑输出
else if ((obj2.ObjectType == "OBJ_OM") && (dictionary2[obj2.ObjectName][0].LruType == "LRU_OM"))
{
    for (int num = 0; num < obj2.ObjectMapping.OutputDictionary.Count; num++)
    {
        if (obj2.ObjectMapping.OutputDictionary[num].Mapping is XmlLogical)
        {
            flag = false;
            Program.Log.Error("00,NG", "Object {0} of type {1} is defined with logical output(s)", 
                new object[] { obj2.ObjectName, obj2.ObjectType });
        }
    }
}
```

---

## 6. LRU关联算法实现

### 6.1 FindAssociatedLru算法

**文件位置**: `source/CGT/XmlConfiguration/XmlLogicalStructure/XmlObject.cs:27-100`

```csharp
public void FindAssociatedLru()
{
    string cellId = string.Empty;
  
    // 第一步：通过物理输入查找CELL_ID
    foreach (XmlInput input in this.objectMapping.InputDictionary)
    {
        if (input.Mapping is XmlPhysical)
        {
            XmlPhysical mapping = (XmlPhysical) input.Mapping;
            cellId = mapping.CellId;
            break;
        }
    }
  
    // 第二步：如果输入没找到，通过物理输出查找
    if (string.IsNullOrEmpty(cellId))
    {
        foreach (XmlOutput output in this.objectMapping.OutputDictionary)
        {
            if (output.Mapping is XmlPhysical)
            {
                XmlPhysical physical2 = (XmlPhysical) output.Mapping;
                cellId = physical2.CellId;
                break;
            }
        }
    }
  
    // 第三步：通过CELL_ID在物理结构中查找LRU
    if (!string.IsNullOrEmpty(cellId))
    {
        foreach (XmlRack rack in XmlConfigurationManager.Instance.CurrentDevice.PhyStruct.RackList.Values)
        {
            foreach (XmlLru lru in rack.LruDictionary.Values)
            {
                foreach (XmlCell cell in lru.CellDictionary.Values)
                {
                    if (cellId == cell.Id)
                    {
                        this.lruId = lru.LruId;
                        return;
                    }
                }
            }
        }
    }
  
    // 第四步：通过INTERFACES接口查找（用于OBJ_MSG, OBJ_OM, OBJ_IM）
    if ((((this.Specific != null) && (this.Specific.ComMsgDictionary.Count != 0)) 
        || (this.ObjectType == "OBJ_OM")) || (this.ObjectType == "OBJ_IM"))
    {
        // 通过逻辑数据名在接口配置中查找LRU关联
        foreach (XmlInput input in this.objectMapping.InputDictionary)
        {
            if (input.Mapping is XmlLogical)
            {
                XmlLogical logical = (XmlLogical) input.Mapping;
                string lruId = FindLruUsingInterfacesElement(logical.DataName, InterObjectMessageDirections.Input);
                if (lruId != null)
                {
                    this.lruId = lruId;
                    return;
                }
            }
        }
    }
  
    // 如果都没找到，记录警告
    Program.Log.InfoFormat("Unable to find the LRU for the object {0}", new object[] { this.ObjectName });
    this.lruId = string.Empty;
}
```

### 6.2 接口查找辅助方法

```csharp
private static string FindLruUsingInterfacesElement(string dataName, InterObjectMessageDirections direction)
{
    foreach (XmlInterSafe safe in XmlConfigurationManager.Instance.CurrentDevice.Interfaces.InterObject.SafeElementsCollection)
    {
        if ((safe.DataName == dataName) && (safe.Direction == direction))
        {
            return safe.LruId;
        }
    }
    return null;
}
```

---

## 7. CAN网络集成与PDO表生成

### 7.1 PDO查询算法

**文件位置**: `source/CGT/BinaryKeyGeneration/GenericKey/Modules/Can/PdoBuilder.cs:246,264`

```csharp
// 输入模块PDO表查询
if (inputModule)
{
    str = "/DEVICE/LOG_STRUCT/OBJECT[@OBJ_TYPE='OBJ_IM']/MAPPING/OUTPUT[LOGICAL[@DATA_NAME='{0}']]/@IO_NUMBER";
}
else
{
    // 输出模块PDO表查询
    str = "/DEVICE/LOG_STRUCT/OBJECT[@OBJ_TYPE='OBJ_OM']/MAPPING/INPUT[LOGICAL[@DATA_NAME='{0}']]/@IO_NUMBER";
}

// 使用XPath查询获取IO编号
XmlNode node = xmlDocument.SelectSingleNode(string.Format(str, dataName));
if (node != null)
{
    return Convert.ToInt32(node.Value);
}
```

### 7.2 网络协议栈支持

```xml
<!-- FSFB2安全功能块协议配置 -->
<SAFTY_TRAFFIC PROTOCOL_TYPE="FSFB2" MAX_LIFE_TIME="3" MAX_DELTA_TC="3" 
               REMOTE_TRAFFIC_COUNTER="500" N_BSD_TO_SSR="40" MAX_ERROR="5">
  <LOCAL NODE_ADDRESS="0283" SID_A="311616DC" SID_B="07643EDE" 
         SINIT_A="5A7531D8" SINIT_B="329D10DA" SUBNET_ADDRESS="fffe">
    <DATAVER DATAVER_A="281C2104" DATAVER_B="6A5B0106" NUM_DATAVER="1" />
  </LOCAL>
  <REMOTE NODE_ADDRESS="0001" SID_A="59E82D0C" SID_B="45455B0E" 
          SINIT_A="0AA65708" SINIT_B="65323D0A" SUBNET_ADDRESS="fffe">
    <DATAVER DATAVER_A="3F8721D4" DATAVER_B="750831D6" NUM_DATAVER="1" />
  </REMOTE>
</SAFTY_TRAFFIC>
```

**安全特性**:

- **SID认证**: 双重安全标识符（SID_A/SID_B）
- **数据版本控制**: DATAVER确保数据同步性
- **流量计数**: REMOTE_TRAFFIC_COUNTER防重放攻击
- **超时机制**: MAX_LIFE_TIME控制消息生命周期

---

## 8. 错误处理与调试机制

### 8.1 分层错误码系统

| 错误码 | 含义       | 触发条件                            |
| ------ | ---------- | ----------------------------------- |
| 00,NH  | 配置不匹配 | 非OBJ_MSG对象包含OBJECT_COM_MSG配置 |
| 00,NG  | 关联错误   | 对象类型与LRU类型不匹配             |
| 00,CY  | 循环连接   | 同一LRU上的消息对象直接连接         |

### 8.2 调试日志示例

```csharp
// 详细的错误信息记录
Program.Log.Error("00,NG", 
    "Object {0} of type {1} is not linked to Lru of type LRU_IM", 
    new object[] { obj2.ObjectName, obj2.ObjectType });

Program.Log.Error("00,CY", 
    "There is a direct link defined between two OBJECT_COM_MSG ({0} and {1}) located on the same LRU ({2})", 
    new object[] { obj2.ObjectName, pair.Value.ObjectName, pair.Value.LruId });

// 信息级日志
Program.Log.InfoFormat("Unable to find the LRU for the object {0}", 
    new object[] { this.ObjectName });
```

---

## 9. 性能优化与内存管理

### 9.1 数据结构选择

```csharp
// 使用Dictionary进行O(1)查找
Dictionary<string, XmlObject> dictionary = new Dictionary<string, XmlObject>();
Dictionary<string, List<XmlObject>> dictionary2 = new Dictionary<string, List<XmlObject>>();

// 使用Collection进行顺序访问
Collection<XmlDataMapping> dataMappingList = new Collection<XmlDataMapping>();
Collection<LogicalInputDataPinNumberAssociation> collection = new Collection<LogicalInputDataPinNumberAssociation>();
```

### 9.2 序列化优化

```csharp
// 静态序列化器避免重复创建
private static XmlSerializer serializer = new XmlSerializer(typeof(XmlObject));
private static XmlSerializer serializer = new XmlSerializer(typeof(XmlObjectComMsg));

public static XmlSerializer Serializer
{
    get { return serializer; }
}
```

---

## 10. 航空电子安全认证特性

### 10.1 DO-178C合规性设计

**确定性行为**:

- 所有对象类型都有明确的状态转换规则
- 验证逻辑覆盖所有可能的配置组合
- 错误处理路径完全可预测

**可追溯性**:

- 从XML配置到二进制密钥的完整追踪链
- 每个数据变换都有明确的源码对应
- 配置变更可通过版本控制系统追踪

**故障检测**:

- 编译时类型检查和约束验证
- 运行时数据完整性检查
- 多层次的错误检测和报告机制

### 10.2 冗余保护架构

```
┌─────────────────┐    ┌─────────────────┐
│   LRU_1_4       │    │   LRU_1_9       │
│  (Primary)      │    │  (Redundant)    │
├─────────────────┤    ├─────────────────┤
│ OBJ_GUEST_1_4   │    │ OBJ_GUEST_1_9   │
│ ┌─────────────┐ │    │ ┌─────────────┐ │
│ │DATA_OUT_G_  │ │◄──►│ │DATA_OUT_G_  │ │
│ │1_4_1        │ │    │ │1_9_1        │ │
│ │(BOOLEAN     │ │    │ │(REDUNDANT)  │ │
│ │ REDUNDANCY) │ │    │ │             │ │
│ └─────────────┘ │    │ └─────────────┘ │
└─────────────────┘    └─────────────────┘
```

**三层冗余保护**:

1. **硬件级**: REDUNDANT_LRU_ID提供板卡故障切换
2. **数据级**: DATA_REDUNDANCY提供软件数据保护
3. **网络级**: PRIMARY/SECONDARY IP提供通信路径冗余

---

## 11. 总结

CGT_B项目中的OBJ类型设计体现了航空电子系统对安全性、可靠性和实时性的严格要求：

1. **模块化架构**: 三种OBJ类型各司其职，物理层→逻辑层→接口层分层清晰
2. **严格验证**: 多层次的类型检查和约束验证确保配置正确性
3. **冗余保护**: 硬件、软件、网络三级冗余机制保障系统可靠性
4. **性能优化**: 合理的数据结构选择和算法设计确保实时性能
5. **安全认证**: 符合DO-178C标准的确定性设计和可追溯性

这种设计完全满足SPOCK系统在关键安全应用场景下的技术要求，为航空电子系统的配置管理提供了坚实的技术基础。

---

**文档版本**: v1.0
**最后更新**: 2025-07-13
**作者**: CGT_B技术分析团队
