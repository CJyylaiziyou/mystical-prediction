"""
梅花易数预测系统
邵康节所创，以数字演化卦象，体用生克断事
宗师级深度：先天八卦数、五行生克、动爻变卦、万物类象
"""
from src.core import BaseDiviner, BirthInfo, PredictionResult
from typing import Dict, List, Tuple
from datetime import datetime


# ==================== 先天八卦数 ====================

# 先天八卦数（乾1兑2离3震4巽5坎6艮7坤8）
XIANTIAN_NUM = {
    1: "乾", 2: "兑", 3: "离", 4: "震",
    5: "巽", 6: "坎", 7: "艮", 8: "坤",
}

BAGUA_ELEMENT = {
    "乾": "金", "兑": "金", "离": "火", "震": "木",
    "巽": "木", "坎": "水", "艮": "土", "坤": "土",
}

BAGUA_NATURE = {
    "乾": "天", "兑": "泽", "离": "火", "震": "雷",
    "巽": "风", "坎": "水", "艮": "山", "坤": "地",
}

BAGUA_TRAIT = {
    "乾": "刚健、领导、父、君、金属、圆形",
    "兑": "喜悦、口舌、少女、金属、缺口",
    "离": "光明、文书、中女、火、眼睛",
    "震": "震动、长男、木、车、雷声",
    "巽": "顺从、长女、木、风、绳索",
    "坎": "险陷、中男、水、耳朵、盗贼",
    "艮": "止、少男、土、山、手、犬",
    "坤": "顺、母、土、腹、布匹、众人",
}

# 五行生克
WUXING_SHENG = {"木": "火", "火": "土", "土": "金", "金": "水", "水": "木"}
WUXING_KE = {"木": "土", "火": "金", "土": "水", "金": "木", "水": "火"}

# 64卦卦名（简化，按先天数组合）
HEXAGRAM_NAMES = {
    (1, 1): "乾", (1, 2): "履", (1, 3): "同人", (1, 4): "无妄",
    (1, 5): "姤",  (1, 6): "讼",  (1, 7): "遁",   (1, 8): "否",
    (2, 1): "夬",  (2, 2): "兑",  (2, 3): "睽",   (2, 4): "归妹",
    (2, 5): "大过",(2, 6): "困",  (2, 7): "咸",   (2, 8): "萃",
    (3, 1): "大有",(3, 2): "革",  (3, 3): "离",   (3, 4): "丰",
    (3, 5): "鼎",  (3, 6): "未济",(3, 7): "旅",   (3, 8): "晋",
    (4, 1): "大壮",(4, 2): "随",  (4, 3): "噬嗑", (4, 4): "震",
    (4, 5): "益",  (4, 6): "解",  (4, 7): "小过", (4, 8): "豫",
    (5, 1): "小畜",(5, 2): "中孚",(5, 3): "家人", (5, 4): "益",
    (5, 5): "巽",  (5, 6): "涣",  (5, 7): "渐",   (5, 8): "观",
    (6, 1): "需",  (6, 2): "节",  (6, 3): "既济", (6, 4): "屯",
    (6, 5): "井",  (6, 6): "坎",  (6, 7): "蹇",   (6, 8): "比",
    (7, 1): "大畜",(7, 2): "损",  (7, 3): "贲",   (7, 4): "颐",
    (7, 5): "蛊",  (7, 6): "蒙",  (7, 7): "艮",   (7, 8): "剥",
    (8, 1): "泰",  (8, 2): "临",  (8, 3): "明夷", (8, 4): "复",
    (8, 5): "升",  (8, 6): "师",  (8, 7): "谦",   (8, 8): "坤",
}

# 卦象吉凶参考
GUA_JIXIONG = {
    "乾": "大吉", "坤": "中吉", "泰": "大吉", "否": "凶",
    "既济": "吉", "未济": "需努力", "坎": "险", "离": "吉",
    "震": "动", "艮": "止", "损": "小损", "益": "大益",
    "丰": "盛极", "旅": "漂泊", "困": "困难", "井": "稳定",
}


# ==================== 起卦方法 ====================

def qi_gua_by_number(num1: int, num2: int, num3: int = None) -> Dict:
    """
    数字起卦（最常用）
    上卦 = num1 % 8，下卦 = num2 % 8，动爻 = num3 % 6（若无num3则用num1+num2）
    """
    shang_num = num1 % 8 if num1 % 8 != 0 else 8
    xia_num = num2 % 8 if num2 % 8 != 0 else 8
    
    if num3 is not None:
        dong_yao = num3 % 6 if num3 % 6 != 0 else 6
    else:
        dong_yao = (num1 + num2) % 6 if (num1 + num2) % 6 != 0 else 6
    
    return {
        "shang_num": shang_num,
        "xia_num": xia_num,
        "dong_yao": dong_yao,
        "shang_gua": XIANTIAN_NUM[shang_num],
        "xia_gua": XIANTIAN_NUM[xia_num],
    }


def qi_gua_by_time(dt: datetime = None) -> Dict:
    """
    时间起卦：年月日时数相加
    """
    if dt is None:
        dt = datetime.now()
    
    year_num = dt.year % 100 if dt.year % 100 != 0 else 100
    month_num = dt.month
    day_num = dt.day
    hour_num = dt.hour // 2 + 1  # 时辰数（子=1）
    
    total = year_num + month_num + day_num
    shang_num = total % 8 if total % 8 != 0 else 8
    xia_num = (total + hour_num) % 8 if (total + hour_num) % 8 != 0 else 8
    dong_yao = (total + hour_num) % 6 if (total + hour_num) % 6 != 0 else 6
    
    return {
        "shang_num": shang_num,
        "xia_num": xia_num,
        "dong_yao": dong_yao,
        "shang_gua": XIANTIAN_NUM[shang_num],
        "xia_gua": XIANTIAN_NUM[xia_num],
    }


def get_bian_gua_meihua(shang_gua: str, xia_gua: str, dong_yao: int) -> str:
    """计算变卦"""
    shang_num = [k for k, v in XIANTIAN_NUM.items() if v == shang_gua][0]
    xia_num = [k for k, v in XIANTIAN_NUM.items() if v == xia_gua][0]
    
    if dong_yao <= 3:
        # 动爻在下卦，下卦变
        new_xia_num = (xia_num % 8) + 1 if xia_num < 8 else 1
        new_xia_gua = XIANTIAN_NUM[new_xia_num]
        return HEXAGRAM_NAMES.get((shang_num, new_xia_num), f"{shang_gua}变")
    else:
        # 动爻在上卦，上卦变
        new_shang_num = (shang_num % 8) + 1 if shang_num < 8 else 1
        return HEXAGRAM_NAMES.get((new_shang_num, xia_num), f"变{xia_gua}")


def analyze_ti_yong(shang_gua: str, xia_gua: str, dong_yao: int) -> Dict:
    """
    体用分析
    动爻在上卦：下卦为体，上卦为用
    动爻在下卦：上卦为体，下卦为用
    """
    if dong_yao <= 3:
        ti_gua = shang_gua  # 上卦为体
        yong_gua = xia_gua  # 下卦为用
    else:
        ti_gua = xia_gua    # 下卦为体
        yong_gua = shang_gua # 上卦为用
    
    ti_element = BAGUA_ELEMENT[ti_gua]
    yong_element = BAGUA_ELEMENT[yong_gua]
    
    # 体用关系
    if WUXING_SHENG.get(yong_element) == ti_element:
        relation = "用生体（大吉，得到帮助）"
        jixiong = "大吉"
    elif WUXING_SHENG.get(ti_element) == yong_element:
        relation = "体生用（小吉，有所付出）"
        jixiong = "小吉"
    elif WUXING_KE.get(yong_element) == ti_element:
        relation = "用克体（凶，受到阻碍）"
        jixiong = "凶"
    elif WUXING_KE.get(ti_element) == yong_element:
        relation = "体克用（吉，主动有力）"
        jixiong = "吉"
    else:
        relation = "体用比和（平稳，同类相助）"
        jixiong = "平"
    
    return {
        "ti_gua": ti_gua,
        "yong_gua": yong_gua,
        "ti_element": ti_element,
        "yong_element": yong_element,
        "relation": relation,
        "jixiong": jixiong,
    }


# ==================== 主类 ====================

class MeihuaCalculator(BaseDiviner):
    """
    梅花易数预测系统
    
    使用方法：
        birth = BirthInfo(1990, 3, 18, 14, 30)
        calc = MeihuaCalculator(birth, num1=3, num2=7, question="这件事能成吗？")
        result = calc.predict()
    """
    
    def __init__(self, birth_info: BirthInfo, num1: int = None, num2: int = None,
                 num3: int = None, question: str = ""):
        super().__init__(birth_info)
        self.num1 = num1
        self.num2 = num2
        self.num3 = num3
        self.question = question
    
    def _calculate(self) -> Dict:
        b = self.birth_info
        
        # 起卦
        if self.num1 and self.num2:
            gua_info = qi_gua_by_number(self.num1, self.num2, self.num3)
        else:
            # 用出生时间起卦
            from datetime import datetime
            dt = datetime(b.year, b.month, b.day, b.hour, b.minute)
            gua_info = qi_gua_by_time(dt)
        
        shang_gua = gua_info["shang_gua"]
        xia_gua = gua_info["xia_gua"]
        dong_yao = gua_info["dong_yao"]
        
        # 本卦名
        ben_gua_name = HEXAGRAM_NAMES.get(
            (gua_info["shang_num"], gua_info["xia_num"]),
            f"{shang_gua}{xia_gua}"
        )
        
        # 变卦
        bian_gua_name = get_bian_gua_meihua(shang_gua, xia_gua, dong_yao)
        
        # 体用分析
        ti_yong = analyze_ti_yong(shang_gua, xia_gua, dong_yao)
        
        # 万物类象
        shang_xiang = BAGUA_TRAIT.get(shang_gua, "")
        xia_xiang = BAGUA_TRAIT.get(xia_gua, "")
        
        return {
            "shang_gua": shang_gua,
            "xia_gua": xia_gua,
            "dong_yao": dong_yao,
            "ben_gua_name": ben_gua_name,
            "bian_gua_name": bian_gua_name,
            "ti_yong": ti_yong,
            "shang_xiang": shang_xiang,
            "xia_xiang": xia_xiang,
            "question": self.question,
            "gua_jixiong": GUA_JIXIONG.get(ben_gua_name, "需综合分析"),
        }
    
    def _map_meanings(self, data: Dict) -> Dict:
        return data
    
    def _interpret(self, meanings: Dict) -> str:
        lines = []
        
        if meanings["question"]:
            lines.append(f"【所问】{meanings['question']}")
        
        lines.append(f"\n【本卦】{meanings['shang_gua']}上{meanings['xia_gua']}下 → {meanings['ben_gua_name']}卦")
        lines.append(f"  参考吉凶：{meanings['gua_jixiong']}")
        
        lines.append(f"\n【万物类象】")
        lines.append(f"  上卦{meanings['shang_gua']}（{BAGUA_NATURE[meanings['shang_gua']]}）：{meanings['shang_xiang']}")
        lines.append(f"  下卦{meanings['xia_gua']}（{BAGUA_NATURE[meanings['xia_gua']]}）：{meanings['xia_xiang']}")
        
        ti_yong = meanings["ti_yong"]
        lines.append(f"\n【体用分析】（第{meanings['dong_yao']}爻动）")
        lines.append(f"  体卦：{ti_yong['ti_gua']}（{ti_yong['ti_element']}）")
        lines.append(f"  用卦：{ti_yong['yong_gua']}（{ti_yong['yong_element']}）")
        lines.append(f"  关系：{ti_yong['relation']}")
        
        lines.append(f"\n【变卦】{meanings['bian_gua_name']}卦（事情发展趋势）")
        
        lines.append(f"\n【断语】")
        jixiong = ti_yong["jixiong"]
        if jixiong in ["大吉", "吉", "小吉"]:
            lines.append(f"体用{ti_yong['relation']}，整体向{jixiong}，所问之事可期。")
            lines.append(f"顺势而为，把握{BAGUA_TRAIT.get(ti_yong['ti_gua'], '')[:10]}之象，事可成。")
        elif jixiong == "凶":
            lines.append(f"体用{ti_yong['relation']}，当前时机不利，宜暂缓行动。")
            lines.append(f"待{meanings['bian_gua_name']}卦之象显现，再做决断。")
        else:
            lines.append(f"体用比和，事情平稳推进，无大吉亦无大凶，稳健为上。")
        
        return "\n".join(lines)
    
    def _generate_suggestions(self, meanings: Dict) -> List[str]:
        ti_yong = meanings["ti_yong"]
        jixiong = ti_yong["jixiong"]
        
        suggestions = []
        
        if jixiong in ["大吉", "吉"]:
            suggestions.append("时机有利，可大胆推进，主动出击")
            suggestions.append(f"善用{BAGUA_TRAIT.get(ti_yong['ti_gua'], '')[:15]}的特质，是当前优势")
        elif jixiong == "小吉":
            suggestions.append("小步推进，循序渐进，避免冒进")
            suggestions.append("有所付出才有所得，不要期望不劳而获")
        elif jixiong == "凶":
            suggestions.append("当前不宜主动出击，以守为攻")
            suggestions.append("寻求外部支援，借力打力")
        else:
            suggestions.append("维持现状，稳健经营，不急于求变")
        
        suggestions.append(f"变卦{meanings['bian_gua_name']}是最终走向，可作为行动目标参考")
        suggestions.append("梅花易数重在当下时机，同一问题不同时间起卦结果不同，需把握'时'的概念")
        
        return suggestions[:5]
    
    def _assess_confidence(self, data: Dict) -> float:
        return 0.82
