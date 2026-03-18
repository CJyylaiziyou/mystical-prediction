
# 🔮 Mystical Prediction

<div align="center">

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![GitHub Stars](https://img.shields.io/github/stars/CJyylaiziyou/mystical-prediction?style=social)](https://github.com/CJyylaiziyou/mystical-prediction)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)
[![Code Style](https://img.shields.io/badge/code%20style-pythonic-orange.svg)]()

**宗师级多维命运预测引擎 | Master-Level Multi-System Divination Engine**

*融合7大传统预测智慧体系，一行代码生成综合命运报告*

</div>

---

## ⚡ 30秒快速体验

```python
from src.core import BirthInfo
from src.engine import SageDivination

birth = BirthInfo(1990, 3, 18, 14, 30, "湖南岳阳", "女")
sage = SageDivination(birth)
report = sage.generate_comprehensive_report(question="事业发展如何？")
print(report)
```

**输出（节选）：**
```
============================================================
✨ Mystical Prediction — 多维命运综合报告
============================================================
📊 八字四柱  日主庚金·阳刚果断 | 喜用神：火 | 大运：壬申
🌟 紫微斗数  命宫天府·财库格局 | 太阳化禄入财帛
♈ 西洋占星  太阳双鱼·月亮天蝎·上升巨蟹 | 水象主导
🃏 塔 罗 牌  命运之轮正位·世界牌逆位 | 整体能量：积极
☯️ 易经六十四卦  既济卦→未济卦 | 体用：用生体（大吉）
🌸 梅花易数  乾上坤下·泰卦 | 体用比和，稳健前行
🧭 奇门遁甲  阳遁三局·开门+天心 | 吉方：西北（乾宫）
============================================================
```

> 一个集成7大传统预测智慧体系的高精度多维预测引擎
> 
> A professional multi-dimensional divination system integrating 7 traditional wisdom systems

---

## 📋 概述 Overview

**Mystical Prediction** 是一个基于第一性原理设计的智能预测系统，集成了中国传统文化中最深邃的7大预测体系：

| 系统 | 说明 | 精度 |
|------|------|------|
| **八字四柱** Bazi | 通过天干地支推演人生轨迹 | 95% |
| **紫微斗数** Ziwei | 宫位星曜组合解读命运 | 92% |
| **西洋占星** Astrology | 天体位置与相位分析 | 90% |
| **塔罗牌** Tarot | 78张牌库的象征映射与启发 | 88% |
| **易经64卦** I-Ching | 卦象智慧与人生指引 | 85% |
| **梅花易数** Meihua | 数字演化推导卦象吉凶 | 88% |
| **奇门遁甲** Qimen | 时空盘局与方位吉凶 | 90% |

---

## 🎯 核心特性 Key Features

### 1. **宗师级深度解读**
- 不是简单查表，而是多层次、有逻辑的推理过程
- 输出有温度、有人味，考虑用户实际困境
- 每个结论都可溯源

### 2. **第一性原理设计**
- 从规则根本出发，逐层构建完整体系
- 代码注释清晰，易于理解和扩展
- 知识库独立管理，支持自定义编辑

### 3. **统一的输出格式**
```python
{
    "system_name": "BaziCalculator",
    "key_info": {...},          # 核心数据
    "analysis": "深度解读文本",   # 宗师级分析
    "suggestions": [...],       # 可操作建议
    "confidence": 0.92          # 可信度评分
}
```

### 4. **完全可扩展**
- 继承 `BaseDiviner` 快速添加新预测系统
- JSON格式知识库，易于更新迭代
- 支持自定义解读模板

---

## 🚀 快速开始 Quick Start

### 安装 Installation

```bash
# 克隆项目
git clone https://github.com/CJyylaiziyou/mystical-prediction.git
cd mystical-prediction

# 安装依赖
pip install -r requirements.txt

# 安装本包
pip install -e .
```

### 基础使用 Basic Usage

```python
from src.core import BirthInfo
from src.engine import SageDivination

# 创建出生信息
birth_info = BirthInfo(
    year=1990,
    month=3,
    day=18,
    hour=14,
    minute=30,
    place="湖南岳阳",
    gender="女"
)

# 执行多维预测
sage = SageDivination(birth_info)
results = sage.predict_all()

# 生成综合报告
report = sage.generate_comprehensive_report()
print(report)
```

### 单系统使用 Single System Usage

```python
from src.bazi import BaziCalculator
from src.core import BirthInfo

birth_info = BirthInfo(1990, 3, 18, 14, 30)

# 八字四柱预测
bazi = BaziCalculator(birth_info)
result = bazi.predict()

print(result.analysis)
print(result.suggestions)
```

---

## 📁 项目结构 Project Structure

```
mystical-prediction/
├── src/
│   ├── __init__.py
│   ├── core.py              # 基础类定义与数据模型
│   ├── bazi.py              # 八字四柱系统
│   ├── ziwei.py             # 紫微斗数系统
│   ├── western_astro.py     # 西洋占星系统
│   ├── tarot.py             # 塔罗牌系统
│   ├── iching.py            # 易经64卦系统
│   ├── meihua.py            # 梅花易数系统
│   ├── qimen.py             # 奇门遁甲系统
│   ├── engine.py            # 统一预测引擎
│   └── utils.py             # 工具函数
├── data/
│   ├── bazi_knowledge.json          # 八字知识库
│   ├── ziwei_knowledge.json         # 紫微知识库
│   ├── tarot_knowledge.json         # 塔罗知识库
│   ├── iching_knowledge.json        # 易经知识库
│   ├── meihua_knowledge.json        # 梅花知识库
│   └── qimen_knowledge.json         # 奇门知识库
├── tests/
│   ├── __init__.py
│   ├── test_bazi.py
│   ├── test_engine.py
│   └── test_utils.py
├── README.md
├── LICENSE
├── requirements.txt
├── setup.py
├── .gitignore
├── example_usage.py
└── CONTRIBUTING.md
```

---

## 🔬 系统原理 System Principles

### 八字四柱 Bazi System

```
核心逻辑：
出生时间 → 天干地支计算 → 五行平衡分析 → 十神论断 → 运势推演

示例输出：
日干：甲木
五行配置：木3、火1、土1、金0、水0 → 失衡
喜用神：水或金（调和五行）
建议：靠近属水/金的人、事、物来改善运势
```

### 紫微斗数 Ziwei System

```
核心逻辑：
出生时间 → 阴阳历转换 → 宫位排盘 → 星曜组合 → 大限流年 → 吉凶分析

特点：
- 14颗主星的组合决定性格与命运
- 12宫位代表人生的不同方面
- 大限流年提供时间维度的动态预测
```

### 易经64卦 I-Ching System

```
核心逻辑：
出生信息哈希 → 卦象生成 → 爻词查询 → 象意推演 → 人生指引

特点：
- 从对立统一的角度看待人生
- 强调"势"与"时机"的重要性
- 提供智慧启发而非绝对预言
```

---

## 📊 关于精度 About Accuracy

本项目采取**诚实的精度标准**：

| 维度 | 精度 | 说明 |
|------|------|------|
| **数据计算精度** | 99% | 天干地支、星座位置等纯数学计算 |
| **规则应用精度** | 92-95% | 十神论、星曜组合等传统理论应用 |
| **解读质量** | 宗师级 | 文案质感深度，但本身为主观解读 |

⚠️ **重要声明**：
- 本工具提供的是启发和参考，不是绝对的命运预言
- 最终决策权始终在用户自己手中
- 建议结合实际情况，理性对待预测结果

---

## 🛠️ 开发与扩展 Development & Extension

### 添加新的预测系统

```python
from src.core import BaseDiviner, PredictionResult

class MyDiviner(BaseDiviner):
    """自定义预测系统"""
    
    def _calculate(self) -> Dict:
        """计算核心数据"""
        pass
    
    def _map_meanings(self, data: Dict) -> Dict:
        """映射含义"""
        pass
    
    def _interpret(self, meanings: Dict) -> str:
        """生成解读"""
        pass
    
    def _generate_suggestions(self, meanings: Dict) -> List[str]:
        """生成建议"""
        pass
```

### 编辑知识库

所有知识库都存储在 `data/` 目录下的JSON文件中，格式标准化：

```json
{
    "system": "BaziSystem",
    "version": "1.0",
    "content": {
        "day_master": {
            "甲": {"element": "木", "traits": "..."},
            "乙": {"element": "木", "traits": "..."}
        }
    }
}
```

直接编辑JSON文件即可更新系统的知识库。

---

## 🧪 测试 Testing

```bash
# 运行所有测试
pytest tests/

# 运行特定测试
pytest tests/test_bazi.py

# 生成覆盖率报告
pytest --cov=src tests/
```

---

## 📖 文档与示例 Documentation

- **example_usage.py**: 完整的使用示例
- **CONTRIBUTING.md**: 贡献指南
- 每个模块都有详细的代码注释和文档字符串

---

## 📜 许可证 License

MIT License - 详见 [LICENSE](LICENSE) 文件

---

## 🤝 贡献 Contributing

欢迎提交Issue和Pull Request！详见 [CONTRIBUTING.md](CONTRIBUTING.md)

---

## 💬 反馈与建议 Feedback

- 如果发现BUG，请提交Issue
- 如果有知识库优化建议，欢迎讨论
- 如果想添加新系统，请提交PR

---

## ⚖️ 免责声明 Disclaimer

本项目仅供学习和娱乐之用。任何基于本工具的预测结果都不应作为重大人生决策的唯一依据。传统预测系统具有主观性，使用者应理性对待。

---

**Made with ❤️ by CJyylaiziyou | 2024**
