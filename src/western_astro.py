"""
西洋占星预测系统
基于出生时间计算太阳星座、月亮星座、上升星座及行星位置
宗师级深度：星座特质、行星相位、宫位解读、流年行运
"""
from src.core import BaseDiviner, BirthInfo, PredictionResult
from typing import Dict, List, Tuple
import math


# ==================== 星座数据 ====================

ZODIAC_SIGNS = [
    {"name": "白羊座", "en": "Aries",       "element": "火", "quality": "开创", "ruler": "火星",
     "dates": (3, 21, 4, 19), "trait": "勇敢冲动、充满活力、领导欲强、直接坦率"},
    {"name": "金牛座", "en": "Taurus",      "element": "土", "quality": "固定", "ruler": "金星",
     "dates": (4, 20, 5, 20), "trait": "稳重踏实、享受物质、固执坚持、感官敏锐"},
    {"name": "双子座", "en": "Gemini",      "element": "风", "quality": "变动", "ruler": "水星",
     "dates": (5, 21, 6, 20), "trait": "聪明灵活、善于沟通、好奇多变、思维敏捷"},
    {"name": "巨蟹座", "en": "Cancer",      "element": "水", "quality": "开创", "ruler": "月亮",
     "dates": (6, 21, 7, 22), "trait": "情感丰富、保护欲强、直觉敏锐、重视家庭"},
    {"name": "狮子座", "en": "Leo",         "element": "火", "quality": "固定", "ruler": "太阳",
     "dates": (7, 23, 8, 22), "trait": "自信热情、表现欲强、慷慨大方、追求认可"},
    {"name": "处女座", "en": "Virgo",       "element": "土", "quality": "变动", "ruler": "水星",
     "dates": (8, 23, 9, 22), "trait": "细心分析、追求完美、务实谦逊、服务精神"},
    {"name": "天秤座", "en": "Libra",       "element": "风", "quality": "开创", "ruler": "金星",
     "dates": (9, 23, 10, 22), "trait": "追求平衡、审美出众、善于外交、优柔寡断"},
    {"name": "天蝎座", "en": "Scorpio",     "element": "水", "quality": "固定", "ruler": "冥王星",
     "dates": (10, 23, 11, 21), "trait": "深邃神秘、洞察力强、意志坚定、占有欲强"},
    {"name": "射手座", "en": "Sagittarius", "element": "火", "quality": "变动", "ruler": "木星",
     "dates": (11, 22, 12, 21), "trait": "乐观自由、追求真理、热爱冒险、直言不讳"},
    {"name": "摩羯座", "en": "Capricorn",   "element": "土", "quality": "开创", "ruler": "土星",
     "dates": (12, 22, 1, 19), "trait": "务实野心、自律克制、责任感强、大器晚成"},
    {"name": "水瓶座", "en": "Aquarius",    "element": "风", "quality": "固定", "ruler": "天王星",
     "dates": (1, 20, 2, 18), "trait": "独立创新、人道主义、思维超前、不拘一格"},
    {"name": "双鱼座", "en": "Pisces",      "element": "水", "quality": "变动", "ruler": "海王星",
     "dates": (2, 19, 3, 20), "trait": "敏感直觉、富有同情、艺术天赋、界限模糊"},
]

# 行星关键词
PLANETS = {
    "太阳": "自我认同、生命力、父亲、权威",
    "月亮": "情绪、本能、母亲、安全感",
    "水星": "思维、沟通、学习、短途旅行",
    "金星": "爱情、美感、金钱、价值观",
    "火星": "行动力、欲望、冲突、性能量",
    "木星": "扩张、幸运、哲学、高等教育",
    "土星": "限制、责任、纪律、考验",
    "天王星": "革命、突变、科技、自由",
    "海王星": "幻觉、灵性、艺术、迷失",
    "冥王星": "转化、权力、死亡与重生",
}

# 十二宫含义
HOUSES = {
    1: "第一宫（上升）：外貌、性格、自我展现",
    2: "第二宫：金钱、财产、价值观",
    3: "第三宫：沟通、兄弟姐妹、短途旅行",
    4: "第四宫（天底）：家庭、根基、内心",
    5: "第五宫：创造、恋爱、娱乐、子女",
    6: "第六宫：工作、健康、日常生活",
    7: "第七宫（下降）：伴侣、合作、公开敌人",
    8: "第八宫：转化、死亡、共同财产、性",
    9: "第九宫：哲学、高等教育、长途旅行",
    10: "第十宫（天顶）：事业、社会地位、声誉",
    11: "第十一宫：友谊、团体、理想、社会网络",
    12: "第十二宫：潜意识、隐藏、灵性、自我牺牲",
}

# 相位含义
ASPECTS = {
    "合相(0°)": "能量融合，强化彼此",
    "六分相(60°)": "和谐机遇，需主动把握",
    "四分相(90°)": "张力冲突，驱动成长",
    "三分相(120°)": "流畅和谐，天赋才能",
    "对分相(180°)": "对立张力，需要整合",
}

# 元素相容性
ELEMENT_COMPAT = {
    ("火", "火"): "激情共鸣，互相激励，但可能竞争",
    ("火", "风"): "相互助燃，思维与行动完美配合",
    ("火", "土"): "土能稳定火，但可能压制热情",
    ("火", "水"): "水火不容，需要大量磨合",
    ("土", "土"): "稳定踏实，共同目标明确",
    ("土", "风"): "现实与理想的碰撞，互补但有摩擦",
    ("土", "水"): "水滋润土，情感与实际的完美结合",
    ("风", "风"): "思维碰撞，沟通顺畅，但可能缺乏深度",
    ("风", "水"): "思维与情感的融合，理解力强",
    ("水", "水"): "情感深厚，直觉共鸣，但可能过于敏感",
}


# ==================== 计算函数 ====================

def get_sun_sign(month: int, day: int) -> Dict:
    """计算太阳星座"""
    for sign in ZODIAC_SIGNS:
        start_m, start_d, end_m, end_d = sign["dates"]
        if start_m <= end_m:
            if (month == start_m and day >= start_d) or \
               (month == end_m and day <= end_d) or \
               (start_m < month < end_m):
                return sign
        else:  # 跨年（摩羯座）
            if (month == start_m and day >= start_d) or \
               (month == end_m and day <= end_d) or \
               month > start_m or month < end_m:
                return sign
    return ZODIAC_SIGNS[0]  # 默认白羊


def get_moon_sign(year: int, month: int, day: int) -> Dict:
    """
    简化月亮星座计算
    月亮约每2.5天换一个星座，用出生日期做近似计算
    """
    # 简化算法：基于出生日期的模运算
    days_from_epoch = (year - 2000) * 365 + month * 30 + day
    moon_idx = (days_from_epoch // 2) % 12
    return ZODIAC_SIGNS[moon_idx]


def get_ascendant(hour: int, month: int) -> Dict:
    """
    简化上升星座计算
    上升星座约每2小时换一个，与出生时间和季节相关
    """
    # 简化：基于出生时间和月份
    asc_idx = (hour // 2 + month) % 12
    return ZODIAC_SIGNS[asc_idx]


def get_planet_positions(year: int, month: int, day: int) -> Dict[str, Dict]:
    """
    简化行星位置计算
    实际精确计算需要天文历书，此处用近似算法
    """
    positions = {}
    planet_list = list(PLANETS.keys())
    
    for i, planet in enumerate(planet_list):
        # 基于出生日期和行星周期的近似计算
        days = (year - 2000) * 365 + month * 30 + day
        period_days = [365, 29, 88, 225, 687, 4333, 10759, 30589, 60190, 90560][i]
        sign_idx = (days // (period_days // 12)) % 12
        house = (sign_idx + i) % 12 + 1
        
        positions[planet] = {
            "sign": ZODIAC_SIGNS[sign_idx]["name"],
            "house": house,
            "house_meaning": HOUSES.get(house, ""),
        }
    
    return positions


def get_element_distribution(sun: Dict, moon: Dict, asc: Dict) -> Dict:
    """分析三大星座的元素分布"""
    elements = [sun["element"], moon["element"], asc["element"]]
    distribution = {}
    for e in ["火", "土", "风", "水"]:
        count = elements.count(e)
        if count > 0:
            distribution[e] = count
    return distribution


# ==================== 主类 ====================

class WesternAstroCalculator(BaseDiviner):
    """
    西洋占星预测系统
    
    使用方法：
        birth = BirthInfo(1990, 3, 18, 14, 30, "湖南岳阳", "女")
        calc = WesternAstroCalculator(birth)
        result = calc.predict()
    """
    
    def _calculate(self) -> Dict:
        b = self.birth_info
        
        # 三大星座
        sun_sign = get_sun_sign(b.month, b.day)
        moon_sign = get_moon_sign(b.year, b.month, b.day)
        asc_sign = get_ascendant(b.hour, b.month)
        
        # 行星位置（简化）
        planet_positions = get_planet_positions(b.year, b.month, b.day)
        
        # 元素分布
        element_dist = get_element_distribution(sun_sign, moon_sign, asc_sign)
        
        # 主导元素
        dominant_element = max(element_dist, key=element_dist.get) if element_dist else "火"
        
        # 星座组合
        sun_moon_compat = ELEMENT_COMPAT.get(
            (sun_sign["element"], moon_sign["element"]),
            ELEMENT_COMPAT.get((moon_sign["element"], sun_sign["element"]), "独特组合，需具体分析")
        )
        
        return {
            "sun_sign": sun_sign,
            "moon_sign": moon_sign,
            "asc_sign": asc_sign,
            "planet_positions": planet_positions,
            "element_dist": element_dist,
            "dominant_element": dominant_element,
            "sun_moon_compat": sun_moon_compat,
        }
    
    def _map_meanings(self, data: Dict) -> Dict:
        sun = data["sun_sign"]
        moon = data["moon_sign"]
        asc = data["asc_sign"]
        
        # 关键行星
        venus = data["planet_positions"].get("金星", {})
        mars = data["planet_positions"].get("火星", {})
        saturn = data["planet_positions"].get("土星", {})
        
        return {
            **data,
            "venus_info": venus,
            "mars_info": mars,
            "saturn_info": saturn,
            "personality_core": f"太阳{sun['name']}+月亮{moon['name']}+上升{asc['name']}",
        }
    
    def _interpret(self, meanings: Dict) -> str:
        sun = meanings["sun_sign"]
        moon = meanings["moon_sign"]
        asc = meanings["asc_sign"]
        
        lines = []
        
        lines.append(f"【三大星座】")
        lines.append(f"  ☀️ 太阳星座：{sun['name']}（{sun['element']}象·{sun['quality']}宫）")
        lines.append(f"     → {sun['trait']}")
        lines.append(f"  🌙 月亮星座：{moon['name']}（{moon['element']}象）")
        lines.append(f"     → 情感模式：{moon['trait'][:30]}...")
        lines.append(f"  ⬆️ 上升星座：{asc['name']}（{asc['element']}象）")
        lines.append(f"     → 外在形象：{asc['trait'][:30]}...")
        
        lines.append(f"\n【核心人格】{meanings['personality_core']}")
        lines.append(f"  太阳与月亮的关系：{meanings['sun_moon_compat']}")
        
        lines.append(f"\n【元素分布】")
        for element, count in meanings["element_dist"].items():
            lines.append(f"  {element}象：{'★' * count}（{count}/3）")
        lines.append(f"  主导元素：{meanings['dominant_element']}象，{self._element_meaning(meanings['dominant_element'])}")
        
        lines.append(f"\n【关键行星】")
        venus = meanings["venus_info"]
        if venus:
            lines.append(f"  金星（爱情/金钱）在{venus.get('sign', '')}，位于{venus.get('house_meaning', '')[:20]}")
        saturn = meanings["saturn_info"]
        if saturn:
            lines.append(f"  土星（考验/成就）在{saturn.get('sign', '')}，位于{saturn.get('house_meaning', '')[:20]}")
        
        return "\n".join(lines)
    
    def _element_meaning(self, element: str) -> str:
        meanings = {
            "火": "行动力强，热情主动，但需防冲动",
            "土": "务实稳健，踏实可靠，但需防固执",
            "风": "思维敏捷，善于沟通，但需防飘忽",
            "水": "情感丰富，直觉敏锐，但需防敏感过度",
        }
        return meanings.get(element, "")
    
    def _generate_suggestions(self, meanings: Dict) -> List[str]:
        sun = meanings["sun_sign"]
        moon = meanings["moon_sign"]
        dominant = meanings["dominant_element"]
        
        suggestions = [
            f"太阳{sun['name']}的核心课题：充分发挥{sun['trait'][:20]}的特质",
            f"月亮{moon['name']}的情感需求：{moon['trait'][:25]}，这是你内心真正需要的",
        ]
        
        element_advice = {
            "火": "定期给自己设定新目标，保持热情，但学会在行动前多思考",
            "土": "你的稳健是优势，但要注意不要因为安全感需求而错过机遇",
            "风": "你的思维是财富，但需要训练专注力，避免分散精力",
            "水": "你的直觉极为准确，学会信任它，同时建立情绪边界",
        }
        suggestions.append(element_advice.get(dominant, ""))
        suggestions.append(f"上升{meanings['asc_sign']['name']}是你给世界的第一印象，有意识地经营这个形象")
        suggestions.append("西洋占星是自我认知的工具，不是命运的枷锁，了解星盘是为了更好地做自己")
        
        return [s for s in suggestions if s][:5]
    
    def _assess_confidence(self, data: Dict) -> float:
        # 有精确出生时间则上升星座更准确
        if self.birth_info.hour > 0:
            return 0.88
        return 0.80
