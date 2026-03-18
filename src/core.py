"""
Mystical Prediction - 核心模块
定义所有预测系统的基础类、数据模型、通用工具
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Tuple, Optional, Any
from enum import Enum
import json
from pathlib import Path


# ==================== 枚举定义 ====================

class Element(Enum):
    """五行枚举"""
    WOOD = "木"
    FIRE = "火"
    EARTH = "土"
    METAL = "金"
    WATER = "水"
    
    def __str__(self):
        return self.value


class Yin_Yang(Enum):
    """阴阳枚举"""
    YIN = "阴"
    YANG = "阳"
    
    def __str__(self):
        return self.value


# ==================== 数据模型 ====================

@dataclass
class BirthInfo:
    """
    出生信息模型
    包含公历日期、时间、地点、性别等基本信息
    """
    year: int
    month: int
    day: int
    hour: int
    minute: int = 0
    place: str = "未知"
    gender: str = "未知"
    lunar_year: Optional[int] = None  # 农历年份（若已知）
    lunar_month: Optional[int] = None  # 农历月份
    lunar_day: Optional[int] = None    # 农历日期
    is_leap_month: bool = False        # 是否农历闰月
    
    def to_datetime(self) -> datetime:
        """转换为Python datetime对象"""
        return datetime(self.year, self.month, self.day, self.hour, self.minute)
    
    def __str__(self):
        return f"{self.year}年{self.month}月{self.day}日 {self.hour}:{self.minute:02d} 出生于{self.place}"


@dataclass
class PredictionResult:
    """
    统一的预测结果结构
    所有预测系统都返回这个格式
    """
    system_name: str                    # 预测系统名称
    system_name_cn: str                 # 系统中文名
    key_info: Dict[str, Any]           # 核心计算数据
    analysis: str                       # 深度解读文本
    suggestions: List[str]              # 可操作建议（3-5条）
    confidence: float                   # 可信度评分(0-1)
    tags: List[str] = field(default_factory=list)  # 标签
    timestamp: datetime = field(default_factory=datetime.now)
    
    def to_dict(self) -> Dict:
        """转换为字典"""
        return {
            "system_name": self.system_name,
            "system_name_cn": self.system_name_cn,
            "key_info": self.key_info,
            "analysis": self.analysis,
            "suggestions": self.suggestions,
            "confidence": self.confidence,
            "tags": self.tags,
            "timestamp": self.timestamp.isoformat()
        }
    
    def to_json(self) -> str:
        """转换为JSON字符串"""
        return json.dumps(self.to_dict(), ensure_ascii=False, indent=2)


@dataclass
class ComprehensiveReport:
    """综合预测报告"""
    birth_info: BirthInfo
    results: Dict[str, PredictionResult]
    generated_at: datetime = field(default_factory=datetime.now)
    summary: str = ""
    
    def to_markdown(self) -> str:
        """转换为Markdown格式报告"""
        md = f"""
# 🔮 {self.birth_info.place} 的七维预测报告

**出生信息**: {self.birth_info}  
**生成时间**: {self.generated_at.strftime('%Y年%m月%d日 %H:%M')}

---

"""
        for system_name, result in self.results.items():
            md += f"""
## {result.system_name_cn}

**可信度**: {'★' * int(result.confidence * 5)}{'☆' * (5 - int(result.confidence * 5))}

{result.analysis}

### 建议
"""
            for i, suggestion in enumerate(result.suggestions, 1):
                md += f"- {suggestion}\n"
            md += "\n---\n\n"
        
        if self.summary:
            md += f"""
## 综合分析

{self.summary}

"""
        
        md += """
---

**免责声明**: 本报告仅供参考，最终决策权在用户自己手中。
"""
        return md.strip()


# ==================== 知识库加载器 ====================

class KnowledgeBase:
    """知识库管理器"""
    
    def __init__(self, data_dir: str = "data"):
        self.data_dir = Path(data_dir)
        self.cache: Dict[str, Dict] = {}
    
    def load(self, filename: str) -> Dict:
        """加载知识库JSON文件"""
        if filename in self.cache:
            return self.cache[filename]
        
        filepath = self.data_dir / filename
        if not filepath.exists():
            return {"error": f"File not found: {filename}"}
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.cache[filename] = data
                return data
        except Exception as e:
            return {"error": str(e)}
    
    def get_item(self, filename: str, *keys) -> Any:
        """获取知识库中的具体项"""
        data = self.load(filename)
        result = data
        for key in keys:
            if isinstance(result, dict) and key in result:
                result = result[key]
            else:
                return None
        return result


# ==================== 基础预测器抽象类 ====================

class BaseDiviner:
    """
    所有预测系统的基类
    定义统一的预测流程：计算 → 映射 → 解读 → 建议
    """
    
    system_name: str = "BaseDiviner"
    system_name_cn: str = "基础预测器"
    
    def __init__(self, birth_info: BirthInfo, kb_filename: Optional[str] = None):
        self.birth_info = birth_info
        self.birth_datetime = birth_info.to_datetime()
        self.kb = KnowledgeBase() if kb_filename else None
        self.kb_data = self.kb.load(kb_filename) if kb_filename else {}
    
    def predict(self) -> PredictionResult:
        """
        执行预测 - 模板方法模式
        定义统一的预测流程
        """
        try:
            # 第一步：计算核心数据
            calculated_data = self._calculate()
            
            # 第二步：映射到含义
            mapped_meanings = self._map_meanings(calculated_data)
            
            # 第三步：生成深度解读
            analysis_text = self._interpret(mapped_meanings)
            
            # 第四步：生成建议
            suggestions = self._generate_suggestions(mapped_meanings)
            
            # 第五步：评估可信度
            confidence = self._assess_confidence(calculated_data)
            
            return PredictionResult(
                system_name=self.__class__.__name__,
                system_name_cn=self.system_name_cn,
                key_info=calculated_data,
                analysis=analysis_text,
                suggestions=suggestions,
                confidence=confidence,
                tags=self._generate_tags(mapped_meanings)
            )
        
        except Exception as e:
            return PredictionResult(
                system_name=self.__class__.__name__,
                system_name_cn=self.system_name_cn,
                key_info={"error": str(e)},
                analysis=f"预测过程出错: {str(e)}",
                suggestions=["请检查输入的出生信息是否正确"],
                confidence=0.0
            )
    
    # 模板方法 - 子类必须实现
    def _calculate(self) -> Dict:
        """第一步：计算核心数据"""
        raise NotImplementedError(f"{self.__class__.__name__} 未实现 _calculate 方法")
    
    def _map_meanings(self, data: Dict) -> Dict:
        """第二步：映射含义"""
        raise NotImplementedError(f"{self.__class__.__name__} 未实现 _map_meanings 方法")
    
    def _interpret(self, meanings: Dict) -> str:
        """第三步：生成解读"""
        raise NotImplementedError(f"{self.__class__.__name__} 未实现 _interpret 方法")
    
    def _generate_suggestions(self, meanings: Dict) -> List[str]:
        """第四步：生成建议"""
        raise NotImplementedError(f"{self.__class__.__name__} 未实现 _generate_suggestions 方法")
    
    def _assess_confidence(self, data: Dict) -> float:
        """第五步：评估可信度 (默认0.85)"""
        return 0.85
    
    def _generate_tags(self, meanings: Dict) -> List[str]:
        """生成标签（可选）"""
        return []


# ==================== 工具函数 ====================

def lunar_to_solar(lunar_year: int, lunar_month: int, lunar_day: int, 
                   is_leap: bool = False) -> Tuple[int, int, int]:
    """
    农历转公历
    需要调用专业库（ephem或lunarcalendar）
    """
    # TODO: 实现农历转公历算法
    pass


def solar_to_lunar(year: int, month: int, day: int) -> Tuple[int, int, int]:
    """
    公历转农历
    需要调用专业库
    """
    # TODO: 实现公历转农历算法
    pass


def get_zodiac_sign(month: int, day: int) -> str:
    """获取西方星座"""
    zodiac = [
        "摩羯座", "水瓶座", "双鱼座", "白羊座", "金牛座", "双子座",
        "巨蟹座", "狮子座", "处女座", "天秤座", "天蝎座", "射手座"
    ]
    days = [20, 19, 21, 20, 21, 21, 23, 23, 23, 23, 22, 22]
    
    if month == 1:
        return zodiac[0] if day >= 20 else zodiac[11]
    elif month == 12:
        return zodiac[11] if day <= 21 else zodiac[0]
    else:
        return zodiac[month] if day >= days[month - 1] else zodiac[month - 1]


def element_compatibility(element1: Element, element2: Element) -> str:
    """判断两个五行的相生相克关系"""
    relations = {
        (Element.WOOD, Element.FIRE): "相生",
        (Element.FIRE, Element.EARTH): "相生",
        (Element.EARTH, Element.METAL): "相生",
        (Element.METAL, Element.WATER): "相生",
        (Element.WATER, Element.WOOD): "相生",
        # 相克
        (Element.WOOD, Element.EARTH): "相克",
        (Element.EARTH, Element.WATER): "相克",
        (Element.WATER, Element.FIRE): "相克",
        (Element.FIRE, Element.METAL): "相克",
        (Element.METAL, Element.WOOD): "相克",
    }
    
    key = (element1, element2)
    if key in relations:
        return relations[key]
    elif (element2, element1) in relations:
        return relations[(element2, element1)]
    else:
        return "无关系"


if __name__ == "__main__":
    # 测试
    birth = BirthInfo(1990, 3, 18, 14, 30, "湖南岳阳", "女")
    print(f"出生信息: {birth}")
    print(f"出生时间: {birth.to_datetime()}")
    
    # 测试西方星座
    zodiac = get_zodiac_sign(3, 18)
    print(f"星座: {zodiac}")
    
    # 测试五行相生相克
    print(element_compatibility(Element.WOOD, Element.FIRE))
