# 数据来源说明

## 原始数据

原始数据来自GitHub仓库：
https://github.com/jr198868/Machine_Learning_Nonpoint_Source_Pollution

数据位置：`Machine_Learning_Nonpoint_Source_Pollution/data/`

## 数据类型

### 1. 水质径流数据 (water_runoff_sample)
- **Total_Nitrogen/** - 总氮数据
- **Total_Phosphorus/** - 总磷数据
- **Ammoniacal_Nitrogen/** - 氨氮数据
- **Nitrate_Nitrogen/** - 硝态氮数据
- **Dissolved_Phosphorus/** - 溶解性磷数据
- **Particulate_Phosphorus/** - 颗粒态磷数据

### 2. 淋溶数据 (water_leaching_sample)
- 30cm和60cm深度的水质淋溶数据

### 3. 气象数据 (weather_data)
- 温度、降水量、风速等气象因子

## 注意事项

由于原始数据较大，本项目使用符号链接或直接引用原始仓库中的数据。
如需完整数据，请克隆原始仓库：

```bash
git clone https://github.com/jr198868/Machine_Learning_Nonpoint_Source_Pollution.git
```

## 数据格式

水质数据包含以下列：
- 日期相关列（Year, Month, Day）
- 营养元素列（NPK, PK, NK, CK, OF - 代表不同施肥处理）
- 气象因子列（Dew Point Temperature, Visibility, Wind Speed, Precipitation等）
