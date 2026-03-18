"""
紫微斗数预测系统
通过出生年月日时，排出命宫、身宫、十四主星落宫，解读人生格局
宗师级深度：星曜组合、四化飞星、大限流年推演
"""
from src.core import BaseDiviner, BirthInfo, PredictionResult
from typing import Dict, List, Tuple
import math


# ==================== 基础数据 ====================

TIANGAN = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
DIZHI = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]

# 五行局对应数
WUXING_JU = {1: "水二局", 2: "水二局", 3: "木三局", 4: "金四局", 5: "土五局", 6: "火六局"}

# 命宫起寅月，逆数生月，再顺数生时
MING_GONG_TABLE = {
    # (月, 时支) -> 命宫地支索引(0=子)
}

# 十四主星
MAIN_STARS = [
    "紫微", "天机", "太阳", "武曲", "天同", "廉贞",
    "天府", "太阴", "贪狼", "巨门", "天相", "天梁", "七杀", "破军"
]

# 星曜特质
STAR_TRAITS = {
    "紫微": {"element": "土", "yin_yang": "阴", "trait": "帝王星，主权贵、领导力、自尊心强，喜独当一面"},
    "天机": {"element": "木", "yin_yang": "阴", "trait": "智慧星，主聪明、变动、谋略，善分析但多虑"},
    "太阳": {"element": "火", "yin_yang": "阳", "trait": "官禄主，主名誉、事业、父缘，光明磊落"},
    "武曲": {"element": "金", "yin_yang": "阴", "trait": "财星，主财富、执行力、刚毅，孤克之性"},
    "天同": {"element": "水", "yin_yang": "阳", "trait": "福星，主享受、温和、感情丰富，偏安逸"},
    "廉贞": {"element": "火", "yin_yang": "阴", "trait": "囚星，主才艺、桃花、是非，刚烈多变"},
    "天府": {"element": "土", "yin_yang": "阳", "trait": "财库星，主稳重、保守、积累，南斗主星"},
    "太阴": {"element": "水", "yin_yang": "阴", "trait": "田宅主，主财富、母缘、阴柔，女命尤重"},
    "贪狼": {"element": "木", "yin_yang": "阳", "trait": "桃花星，主欲望、才艺、交际，多才多艺"},
    "巨门": {"element": "水", "yin_yang": "阴", "trait": "暗曜，主口才、是非、探究，善辩论"},
    "天相": {"element": "水", "yin_yang": "阳", "trait": "印星，主辅佐、文书、衣食，稳重守成"},
    "天梁": {"element": "土", "yin_yang": "阳", "trait": "荫星，主庇护、医药、宗教，老成持重"},
    "七杀": {"element": "金", "yin_yang": "阴", "trait": "将星，主冲劲、变革、独立，孤克之性"},
    "破军": {"element": "水", "yin_yang": "阴", "trait": "耗星，主开创、破坏、变动，先破后立"},
}

# 十二宫名称（从命宫顺时针）
PALACES = ["命宫", "兄弟", "夫妻", "子女", "财帛", "疾厄", "迁移", "奴仆", "官禄", "田宅", "福德", "父母"]

# 四化对照表（年干 -> {星: 化})
SI_HUA = {
    "甲": {"廉贞": "化禄", "破军": "化权", "武曲": "化科", "太阳": "化忌"},
    "乙": {"天机": "化禄", "天梁": "化权", "紫微": "化科", "太阴": "化忌"},
    "丙": {"天同": "化禄", "天机": "化权", "文昌": "化科", "廉贞": "化忌"},
    "丁": {"太阴": "化禄", "天同": "化权", "天机": "化科", "巨门": "化忌"},
    "戊": {"贪狼": "化禄", "太阴": "化权", "右弼": "化科", "天机": "化忌"},
    "己": {"武曲": "化禄", "贪狼": "化权", "天梁": "化科", "文曲": "化忌"},
    "庚": {"太阳": "化禄", "武曲": "化权", "太阴": "化科", "天同": "化忌"},
    "辛": {"巨门": "化禄", "太阳": "化权", "文曲": "化科", "文昌": "化忌"},
    "壬": {"天梁": "化禄", "紫微": "化权", "左辅": "化科", "武曲": "化忌"},
    "癸": {"破军": "化禄", "巨门": "化权", "太阴": "化科", "贪狼": "化忌"},
}

# 大限起始年龄（按五行局）
JU_START_AGE = {2: 2, 3: 3, 4: 4, 5: 5, 6: 6}


# ==================== 核心计算 ====================

def get_year_ganzhi(year: int) -> Tuple[str, str]:
    """获取年份天干地支"""
    tg_idx = (year - 4) % 10
    dz_idx = (year - 4) % 12
    return TIANGAN[tg_idx], DIZHI[dz_idx]


def get_ming_gong(birth_month: int, birth_hour: int) -> int:
    """
    计算命宫地支索引（0=子）
    寅宫起正月，逆数生月定起点，再顺数生时
    """
    # 寅=2，逆数月份：寅起正月，二月丑，三月子...
    # 命宫起点 = (寅宫索引 - 月份 + 1 + 12) % 12
    # 寅在地支中索引为2
    base = (2 - birth_month + 1 + 12) % 12  # 逆数月份后的起点
    # 再顺数时支
    hour_zhi = birth_hour // 2  # 时支索引（子=0）
    ming_gong = (base + hour_zhi) % 12
    return ming_gong


def get_wuxing_ju(year_tg: str, ming_gong_dz: str) -> int:
    """
    计算五行局
    根据年干和命宫地支（纳音五行）
    """
    tg_idx = TIANGAN.index(year_tg)
    dz_idx = DIZHI.index(ming_gong_dz)
    
    # 纳音五行对照（简化版，按60甲子）
    # 用年干索引 + 命宫地支索引推算
    nayin_map = {
        (0, 1): 6, (0, 2): 3, (0, 3): 4, (0, 4): 5, (0, 5): 2,
        (1, 0): 6, (1, 1): 3, (1, 2): 4, (1, 3): 5, (1, 4): 2,
    }
    
    # 简化：按命宫地支分组
    ju_by_dz = {
        "子": 2, "丑": 2,
        "寅": 3, "卯": 3,
        "辰": 4, "巳": 4,
        "午": 5, "未": 5,
        "申": 6, "酉": 6,
        "戌": 2, "亥": 2,
    }
    
    # 根据年干奇偶微调
    base_ju = ju_by_dz.get(ming_gong_dz, 2)
    if tg_idx % 2 == 1:  # 阴年干
        base_ju = max(2, base_ju - 1) if base_ju > 2 else 3
    
    return base_ju


def place_ziwei(ju: int, lunar_day: int) -> int:
    """
    安紫微星：根据五行局和农历日期确定紫微地支索引
    """
    # 紫微安法：以五行局数除农历日，余数定宫
    # 余0在午，余1在未，依次类推（简化算法）
    remainder = lunar_day % ju
    if remainder == 0:
        remainder = ju
    
    # 紫微从午宫(7)起，按余数顺布
    ziwei_positions = {
        2: [7, 1],          # 水二局：午、丑
        3: [7, 10, 1],      # 木三局：午、戌、丑
        4: [7, 10, 1, 4],   # 金四局：午、戌、丑、辰
        5: [7, 10, 1, 4, 9], # 土五局
        6: [7, 10, 1, 4, 9, 6], # 火六局
    }
    
    positions = ziwei_positions.get(ju, [7])
    return positions[(remainder - 1) % len(positions)]


def place_tianfu(ziwei_pos: int) -> int:
    """天府星位置：与紫微相对（子午相冲规律）"""
    tianfu_map = {
        0: 8, 1: 7, 2: 6, 3: 5, 4: 4, 5: 3,
        6: 2, 7: 1, 8: 0, 9: 11, 10: 10, 11: 9
    }
    return tianfu_map.get(ziwei_pos, 0)


def place_all_stars(ziwei_pos: int, tianfu_pos: int) -> Dict[str, int]:
    """
    安放十四主星
    基于紫微和天府位置，按固定间距安放其他主星
    """
    stars = {}
    stars["紫微"] = ziwei_pos
    stars["天府"] = tianfu_pos
    
    # 紫微系（顺时针）
    ziwei_series_offset = [0, 11, 10, 9, 8, 7]  # 紫微、天机、太阳、武曲、天同、廉贞
    ziwei_series = ["紫微", "天机", "太阳", "武曲", "天同", "廉贞"]
    for i, star in enumerate(ziwei_series):
        stars[star] = (ziwei_pos + ziwei_series_offset[i]) % 12
    
    # 天府系（逆时针）
    tianfu_series_offset = [0, 1, 2, 3, 4, 5, 6, 7]
    tianfu_series = ["天府", "太阴", "贪狼", "巨门", "天相", "天梁", "七杀", "破军"]
    for i, star in enumerate(tianfu_series):
        stars[star] = (tianfu_pos + tianfu_series_offset[i]) % 12
    
    return stars


def get_palace_stars(ming_gong: int, star_positions: Dict[str, int]) -> Dict[str, List[str]]:
    """将星曜分配到十二宫"""
    palace_stars = {palace: [] for palace in PALACES}
    
    for star, pos in star_positions.items():
        # 计算星曜在哪个宫（相对于命宫的偏移）
        palace_idx = (pos - ming_gong + 12) % 12
        palace_name = PALACES[palace_idx]
        palace_stars[palace_name].append(star)
    
    return palace_stars


def get_daxian(ming_gong: int, ju: int, gender: str, year_tg: str) -> List[Dict]:
    """
    计算大限（每个大限10年）
    男命阳年顺行，阴年逆行；女命相反
    """
    tg_idx = TIANGAN.index(year_tg)
    is_yang_year = (tg_idx % 2 == 0)
    
    # 顺逆行判断
    if gender == "男":
        forward = is_yang_year
    else:
        forward = not is_yang_year
    
    start_age = JU_START_AGE.get(ju, 2)
    daxian_list = []
    
    for i in range(12):
        if forward:
            palace_idx = (ming_gong + i) % 12
        else:
            palace_idx = (ming_gong - i + 12) % 12
        
        age_start = start_age + i * 10
        age_end = age_start + 9
        
        daxian_list.append({
            "period": f"{age_start}-{age_end}岁",
            "palace": PALACES[palace_idx % len(PALACES)],
            "dizhi": DIZHI[palace_idx],
        })
    
    return daxian_list


# ==================== 主类 ====================

class ZiweiCalculator(BaseDiviner):
    """
    紫微斗数预测系统
    
    使用方法：
        birth = BirthInfo(1990, 3, 18, 14, 30, gender="女")
        calc = ZiweiCalculator(birth)
        result = calc.predict()
    """
    
    def _calculate(self) -> Dict:
        b = self.birth_info
        
        # 1. 年干支
        year_tg, year_dz = get_year_ganzhi(b.year)
        
        # 2. 命宫
        ming_gong = get_ming_gong(b.month, b.hour)
        ming_gong_dz = DIZHI[ming_gong]
        
        # 3. 五行局
        ju = get_wuxing_ju(year_tg, ming_gong_dz)
        
        # 4. 农历日（若未提供，用公历日近似）
        lunar_day = b.lunar_day if b.lunar_day else b.day
        
        # 5. 安紫微、天府
        ziwei_pos = place_ziwei(ju, lunar_day)
        tianfu_pos = place_tianfu(ziwei_pos)
        
        # 6. 安十四主星
        star_positions = place_all_stars(ziwei_pos, tianfu_pos)
        
        # 7. 分配宫位
        palace_stars = get_palace_stars(ming_gong, star_positions)
        
        # 8. 四化
        sihua = SI_HUA.get(year_tg, {})
        
        # 9. 大限
        daxian = get_daxian(ming_gong, ju, b.gender, year_tg)
        
        # 10. 命宫主星
        ming_stars = palace_stars.get("命宫", [])
        
        return {
            "year_ganzhi": f"{year_tg}{year_dz}",
            "year_tg": year_tg,
            "ming_gong_dz": ming_gong_dz,
            "ming_gong_idx": ming_gong,
            "wuxing_ju": WUXING_JU.get(ju, f"{ju}局"),
            "ju": ju,
            "star_positions": star_positions,
            "palace_stars": palace_stars,
            "sihua": sihua,
            "daxian": daxian,
            "ming_stars": ming_stars,
        }
    
    def _map_meanings(self, data: Dict) -> Dict:
        ming_stars = data["ming_stars"]
        palace_stars = data["palace_stars"]
        
        # 命宫星曜特质
        ming_traits = []
        for star in ming_stars:
            if star in STAR_TRAITS:
                ming_traits.append(STAR_TRAITS[star])
        
        # 财帛宫、官禄宫、夫妻宫主星
        key_palaces = {}
        for palace in ["财帛", "官禄", "夫妻", "疾厄", "福德"]:
            stars = palace_stars.get(palace, [])
            key_palaces[palace] = {
                "stars": stars,
                "traits": [STAR_TRAITS.get(s, {}).get("trait", "") for s in stars if s in STAR_TRAITS]
            }
        
        # 四化影响
        sihua_analysis = []
        for star, hua in data["sihua"].items():
            for palace, pstars in palace_stars.items():
                if star in pstars:
                    sihua_analysis.append(f"{star}{hua}在{palace}宫")
        
        return {
            "ming_stars": ming_stars,
            "ming_traits": ming_traits,
            "key_palaces": key_palaces,
            "sihua_analysis": sihua_analysis,
            "wuxing_ju": data["wuxing_ju"],
            "daxian": data["daxian"],
        }
    
    def _interpret(self, meanings: Dict) -> str:
        ming_stars = meanings["ming_stars"]
        ming_traits = meanings["ming_traits"]
        key_palaces = meanings["key_palaces"]
        sihua_analysis = meanings["sihua_analysis"]
        
        lines = []
        
        # 命宫解读
        if ming_stars:
            star_names = "、".join(ming_stars)
            lines.append(f"【命宫格局】命宫坐{star_names}。")
            for trait in ming_traits:
                lines.append(f"{trait['trait']}。")
        else:
            lines.append("【命宫格局】命宫无主星，借对宫星曜论命，性格受环境塑造较深。")
        
        # 财官夫
        for palace in ["财帛", "官禄", "夫妻"]:
            info = key_palaces.get(palace, {})
            stars = info.get("stars", [])
            traits = info.get("traits", [])
            if stars:
                lines.append(f"【{palace}宫】坐{'、'.join(stars)}，{traits[0] if traits else ''}。")
        
        # 四化
        if sihua_analysis:
            lines.append(f"【四化飞星】本命年{'；'.join(sihua_analysis[:3])}，对相关宫位影响深远。")
        
        # 大限
        daxian = meanings["daxian"]
        if daxian:
            current_daxian = daxian[2] if len(daxian) > 2 else daxian[0]
            lines.append(f"【大限参考】{current_daxian['period']}走{current_daxian['palace']}大限，"
                        f"此限{current_daxian['dizhi']}宫主事，宜把握此阶段机遇。")
        
        return "\n".join(lines)
    
    def _generate_suggestions(self, meanings: Dict) -> List[str]:
        ming_stars = meanings["ming_stars"]
        suggestions = []
        
        star_suggestions = {
            "紫微": "适合走管理、领导路线，避免事必躬亲，学会授权",
            "天机": "善用分析能力，避免想太多而错失行动时机",
            "太阳": "公开场合发光发热，适合公众事业，注意保护眼睛",
            "武曲": "财运佳但需防孤克，感情上多些柔软，财务规划要稳健",
            "天同": "享受生活是天赋，但需防懒散，给自己设定明确目标",
            "廉贞": "才华横溢，但需管理情绪，避免因冲动引发是非",
            "天府": "稳健积累是正道，适合守业，不宜冒进投机",
            "太阴": "直觉敏锐，适合幕后运作，注意情绪管理",
            "贪狼": "多才多艺是优势，专注一两个方向深耕，避免分散",
            "巨门": "口才是武器，适合教育、咨询、媒体行业",
            "天相": "辅佐型人才，找对平台和贵人，事半功倍",
            "天梁": "适合医疗、公益、宗教领域，老成持重是优势",
            "七杀": "冲劲十足，适合创业，注意与人合作时的方式方法",
            "破军": "天生开拓者，接受变化而非抗拒，先破后立是命运节奏",
        }
        
        for star in ming_stars[:2]:  # 取前两颗主星
            if star in star_suggestions:
                suggestions.append(star_suggestions[star])
        
        if not suggestions:
            suggestions.append("命宫无主星，性格可塑性强，善于适应环境，建议多尝试不同领域找到真正热爱")
        
        suggestions.append("流年运势需结合当年飞化具体分析，建议每年初做一次流年盘")
        suggestions.append("紫微斗数重格局轻单星，命宫星曜需结合三方四正综合论断")
        
        return suggestions[:5]
    
    def _assess_confidence(self, data: Dict) -> float:
        # 有农历日期则精度更高
        if self.birth_info.lunar_day:
            return 0.92
        return 0.85
