"""
易经64卦预测系统
支持时间起卦、数字起卦，含互卦、变卦、体用分析
宗师级深度：卦象象意、爻辞解读、体用生克断事
"""
from src.core import BaseDiviner, BirthInfo, PredictionResult
from typing import Dict, List, Tuple
import hashlib


# ==================== 八卦基础 ====================

BAGUA = {
    "乾": {"binary": "111", "element": "金", "nature": "天", "trait": "刚健、领导、创造"},
    "兑": {"binary": "110", "element": "金", "nature": "泽", "trait": "喜悦、口才、交流"},
    "离": {"binary": "101", "element": "火", "nature": "火", "trait": "光明、文明、附丽"},
    "震": {"binary": "100", "element": "木", "nature": "雷", "trait": "动、奋发、长子"},
    "巽": {"binary": "011", "element": "木", "nature": "风", "trait": "顺、渗透、长女"},
    "坎": {"binary": "010", "element": "水", "nature": "水", "trait": "险、智慧、中男"},
    "艮": {"binary": "001", "element": "土", "nature": "山", "trait": "止、稳重、少男"},
    "坤": {"binary": "000", "element": "土", "nature": "地", "trait": "顺、承载、母"},
}

# 64卦（上卦+下卦 -> 卦名）
HEXAGRAMS_64 = {
    ("乾", "乾"): {"name": "乾", "num": 1,  "meaning": "元亨利贞，自强不息，天行健，君子以自强不息"},
    ("坤", "坤"): {"name": "坤", "num": 2,  "meaning": "厚德载物，顺势而为，地势坤，君子以厚德载物"},
    ("坎", "震"): {"name": "屯", "num": 3,  "meaning": "万事开头难，初创艰辛，坚持必有收获"},
    ("艮", "坎"): {"name": "蒙", "num": 4,  "meaning": "启蒙教化，虚心求学，蒙以养正"},
    ("乾", "坎"): {"name": "需", "num": 5,  "meaning": "等待时机，养精蓄锐，时机未到宜等待"},
    ("坎", "乾"): {"name": "讼", "num": 6,  "meaning": "争讼不利，以和为贵，避免正面冲突"},
    ("坎", "坤"): {"name": "师", "num": 7,  "meaning": "统帅之道，以德服人，团队协作"},
    ("坤", "坎"): {"name": "比", "num": 8,  "meaning": "亲比团结，寻求合作，广结善缘"},
    ("乾", "巽"): {"name": "小畜", "num": 9,  "meaning": "小有积蓄，循序渐进，积少成多"},
    ("兑", "乾"): {"name": "履", "num": 10, "meaning": "谨慎行事，礼义当先，步步为营"},
    ("乾", "坤"): {"name": "泰", "num": 11, "meaning": "天地交泰，万事亨通，把握良机"},
    ("坤", "乾"): {"name": "否", "num": 12, "meaning": "否极泰来，暂时受阻，静待转机"},
    ("乾", "离"): {"name": "同人", "num": 13, "meaning": "志同道合，广泛合作，开诚布公"},
    ("离", "乾"): {"name": "大有", "num": 14, "meaning": "大有所获，丰收之象，把握当下"},
    ("艮", "坤"): {"name": "谦", "num": 15, "meaning": "谦虚谨慎，低调行事，谦受益满招损"},
    ("坤", "震"): {"name": "豫", "num": 16, "meaning": "豫悦顺动，顺势而为，提前准备"},
    ("兑", "震"): {"name": "随", "num": 17, "meaning": "随机应变，顺应时势，灵活处事"},
    ("巽", "艮"): {"name": "蛊", "num": 18, "meaning": "整治弊端，改革创新，拨乱反正"},
    ("兑", "坤"): {"name": "临", "num": 19, "meaning": "临近成功，把握机遇，积极进取"},
    ("坤", "巽"): {"name": "观", "num": 20, "meaning": "观察审视，冷静分析，以观待变"},
    ("离", "震"): {"name": "噬嗑", "num": 21, "meaning": "排除障碍，刚毅果断，解决问题"},
    ("震", "离"): {"name": "贲", "num": 22, "meaning": "文饰修美，注重形象，内外兼修"},
    ("艮", "坤"): {"name": "剥", "num": 23, "meaning": "剥落衰退，顺势保存，静待复苏"},
    ("坤", "震"): {"name": "复", "num": 24, "meaning": "否极泰来，回归正道，重新出发"},
    ("乾", "震"): {"name": "无妄", "num": 25, "meaning": "顺天应人，真实无妄，脚踏实地"},
    ("震", "乾"): {"name": "大畜", "num": 26, "meaning": "积累蓄势，厚积薄发，大器晚成"},
    ("艮", "震"): {"name": "颐", "num": 27, "meaning": "养生养德，谨慎言行，自养养人"},
    ("兑", "巽"): {"name": "大过", "num": 28, "meaning": "过犹不及，独立担当，非常之时"},
    ("坎", "坎"): {"name": "坎", "num": 29, "meaning": "重重险阻，坚守正道，险中求生"},
    ("离", "离"): {"name": "离", "num": 30, "meaning": "光明附丽，文明昌盛，依附正道"},
    ("兑", "艮"): {"name": "咸", "num": 31, "meaning": "感应相通，男女相悦，以诚感人"},
    ("震", "巽"): {"name": "恒", "num": 32, "meaning": "恒久坚持，持之以恒，始终如一"},
    ("乾", "艮"): {"name": "遁", "num": 33, "meaning": "适时退隐，以退为进，保存实力"},
    ("震", "乾"): {"name": "大壮", "num": 34, "meaning": "阳刚壮盛，正大光明，勿恃强凌弱"},
    ("离", "坤"): {"name": "晋", "num": 35, "meaning": "晋升进步，光明前途，积极进取"},
    ("坤", "离"): {"name": "明夷", "num": 36, "meaning": "光明受损，韬光养晦，忍辱负重"},
    ("巽", "离"): {"name": "家人", "num": 37, "meaning": "家庭和睦，各守本分，齐家治国"},
    ("离", "兑"): {"name": "睽", "num": 38, "meaning": "对立分歧，求同存异，化解矛盾"},
    ("坎", "艮"): {"name": "蹇", "num": 39, "meaning": "行路艰难，寻求援助，迂回前进"},
    ("震", "坎"): {"name": "解", "num": 40, "meaning": "解除困难，宽大为怀，化险为夷"},
    ("艮", "兑"): {"name": "损", "num": 41, "meaning": "损下益上，适当舍弃，损有余补不足"},
    ("巽", "震"): {"name": "益", "num": 42, "meaning": "损上益下，利人利己，积极行动"},
    ("乾", "兑"): {"name": "夬", "num": 43, "meaning": "决断果断，公开处理，以正胜邪"},
    ("巽", "乾"): {"name": "姤", "num": 44, "meaning": "意外相遇，防范小人，不可轻信"},
    ("坤", "兑"): {"name": "萃", "num": 45, "meaning": "聚集汇合，凝聚力量，团结一致"},
    ("巽", "坤"): {"name": "升", "num": 46, "meaning": "循序渐进，稳步上升，积累晋升"},
    ("兑", "坎"): {"name": "困", "num": 47, "meaning": "困境之中，守正不变，困而后通"},
    ("坎", "巽"): {"name": "井", "num": 48, "meaning": "取之不尽，养民利民，改革更新"},
    ("兑", "离"): {"name": "革", "num": 49, "meaning": "变革创新，顺应时代，除旧布新"},
    ("离", "巽"): {"name": "鼎", "num": 50, "meaning": "鼎新革故，稳固根基，培育人才"},
    ("震", "震"): {"name": "震", "num": 51, "meaning": "雷霆震动，临危不惧，修身自省"},
    ("艮", "艮"): {"name": "艮", "num": 52, "meaning": "适时止步，知止而止，静思内省"},
    ("巽", "艮"): {"name": "渐", "num": 53, "meaning": "循序渐进，按部就班，水到渠成"},
    ("震", "兑"): {"name": "归妹", "num": 54, "meaning": "归宿之道，顺从礼义，婚姻慎重"},
    ("离", "震"): {"name": "丰", "num": 55, "meaning": "丰盛鼎盛，居安思危，盛极必衰"},
    ("巽", "离"): {"name": "旅", "num": 56, "meaning": "旅途漂泊，谨慎处世，客居他乡"},
    ("巽", "巽"): {"name": "巽", "num": 57, "meaning": "顺从渗透，柔顺谦逊，潜移默化"},
    ("兑", "兑"): {"name": "兑", "num": 58, "meaning": "喜悦和谐，以诚待人，口才出众"},
    ("坎", "巽"): {"name": "涣", "num": 59, "meaning": "涣散离析，凝聚人心，化解危机"},
    ("兑", "坎"): {"name": "节", "num": 60, "meaning": "节制有度，适可而止，量入为出"},
    ("巽", "兑"): {"name": "中孚", "num": 61, "meaning": "诚信为本，以诚感人，内外一致"},
    ("震", "艮"): {"name": "小过", "num": 62, "meaning": "小有过失，谨慎行事，不可大动"},
    ("坎", "离"): {"name": "既济", "num": 63, "meaning": "大功告成，居安思危，防微杜渐"},
    ("离", "坎"): {"name": "未济", "num": 64, "meaning": "尚未完成，继续努力，前途光明"},
}

BAGUA_LIST = list(BAGUA.keys())


# ==================== 起卦方法 ====================

def time_gua(year: int, month: int, day: int, hour: int) -> Tuple[str, str, int]:
    """
    时间起卦：年月日时数相加
    上卦 = (年+月+日) % 8，下卦 = (年+月+日+时) % 8，动爻 = (年+月+日+时) % 6
    """
    total = year % 100 + month + day
    shang_idx = total % 8
    xia_idx = (total + hour) % 8
    dong_yao = (total + hour) % 6 + 1
    
    shang_gua = BAGUA_LIST[shang_idx]
    xia_gua = BAGUA_LIST[xia_idx]
    
    return shang_gua, xia_gua, dong_yao


def number_gua(num1: int, num2: int) -> Tuple[str, str, int]:
    """
    数字起卦：两个数字
    上卦 = num1 % 8，下卦 = num2 % 8，动爻 = (num1+num2) % 6
    """
    shang_idx = num1 % 8 if num1 % 8 != 0 else 8
    xia_idx = num2 % 8 if num2 % 8 != 0 else 8
    dong_yao = (num1 + num2) % 6 + 1
    
    shang_gua = BAGUA_LIST[(shang_idx - 1) % 8]
    xia_gua = BAGUA_LIST[(xia_idx - 1) % 8]
    
    return shang_gua, xia_gua, dong_yao


def get_bian_gua(shang: str, xia: str, dong_yao: int) -> Tuple[str, str]:
    """
    计算变卦：动爻变阴阳，得到变卦
    """
    shang_bin = list(BAGUA[shang]["binary"])
    xia_bin = list(BAGUA[xia]["binary"])
    
    # 动爻位置（1-6，从下往上）
    if dong_yao <= 3:
        # 在下卦
        pos = dong_yao - 1
        xia_bin[2 - pos] = "0" if xia_bin[2 - pos] == "1" else "1"
    else:
        # 在上卦
        pos = dong_yao - 4
        shang_bin[2 - pos] = "0" if shang_bin[2 - pos] == "1" else "1"
    
    # 找变卦对应的卦名
    new_shang_bin = "".join(shang_bin)
    new_xia_bin = "".join(xia_bin)
    
    new_shang = next((k for k, v in BAGUA.items() if v["binary"] == new_shang_bin), shang)
    new_xia = next((k for k, v in BAGUA.items() if v["binary"] == new_xia_bin), xia)
    
    return new_shang, new_xia


def get_hu_gua(shang: str, xia: str) -> Tuple[str, str]:
    """
    计算互卦：取2-4爻为下互卦，3-5爻为上互卦
    """
    shang_bin = BAGUA[shang]["binary"]
    xia_bin = BAGUA[xia]["binary"]
    full_bin = xia_bin + shang_bin  # 从下到上
    
    hu_xia_bin = full_bin[1:4]  # 2-4爻
    hu_shang_bin = full_bin[2:5]  # 3-5爻
    
    hu_xia = next((k for k, v in BAGUA.items() if v["binary"] == hu_xia_bin), xia)
    hu_shang = next((k for k, v in BAGUA.items() if v["binary"] == hu_shang_bin), shang)
    
    return hu_shang, hu_xia


# ==================== 主类 ====================

class IChingCalculator(BaseDiviner):
    """
    易经64卦预测系统
    
    使用方法：
        birth = BirthInfo(1990, 3, 18, 14, 30)
        calc = IChingCalculator(birth, question="事业发展如何？")
        result = calc.predict()
    """
    
    def __init__(self, birth_info: BirthInfo, question: str = "", method: str = "time"):
        super().__init__(birth_info)
        self.question = question
        self.method = method  # "time" 或 "number"
    
    def _calculate(self) -> Dict:
        b = self.birth_info
        
        # 起卦
        shang_gua, xia_gua, dong_yao = time_gua(b.year, b.month, b.day, b.hour)
        
        # 本卦
        ben_gua = HEXAGRAMS_64.get((shang_gua, xia_gua), {
            "name": f"{shang_gua}{xia_gua}",
            "num": 0,
            "meaning": "卦象待解"
        })
        
        # 互卦
        hu_shang, hu_xia = get_hu_gua(shang_gua, xia_gua)
        hu_gua = HEXAGRAMS_64.get((hu_shang, hu_xia), {"name": f"{hu_shang}{hu_xia}", "meaning": ""})
        
        # 变卦
        bian_shang, bian_xia = get_bian_gua(shang_gua, xia_gua, dong_yao)
        bian_gua = HEXAGRAMS_64.get((bian_shang, bian_xia), {"name": f"{bian_shang}{bian_xia}", "meaning": ""})
        
        # 体用卦（下卦为体，上卦为用）
        ti_gua_name = xia_gua
        yong_gua_name = shang_gua
        ti_element = BAGUA[ti_gua_name]["element"]
        yong_element = BAGUA[yong_gua_name]["element"]
        
        # 五行生克
        sheng_ke = self._check_element_relation(ti_element, yong_element)
        
        return {
            "shang_gua": shang_gua,
            "xia_gua": xia_gua,
            "ben_gua": ben_gua,
            "dong_yao": dong_yao,
            "hu_gua": hu_gua,
            "bian_gua": bian_gua,
            "ti_gua": {"name": ti_gua_name, "element": ti_element, "trait": BAGUA[ti_gua_name]["trait"]},
            "yong_gua": {"name": yong_gua_name, "element": yong_element, "trait": BAGUA[yong_gua_name]["trait"]},
            "sheng_ke": sheng_ke,
            "question": self.question,
        }
    
    def _check_element_relation(self, ti: str, yong: str) -> str:
        """判断体用五行关系"""
        sheng = {"木": "火", "火": "土", "土": "金", "金": "水", "水": "木"}
        ke = {"木": "土", "火": "金", "土": "水", "金": "木", "水": "火"}
        
        if sheng.get(yong) == ti:
            return "用生体（大吉）"
        elif sheng.get(ti) == yong:
            return "体生用（小吉，有所付出）"
        elif ke.get(yong) == ti:
            return "用克体（凶，需防外来阻碍）"
        elif ke.get(ti) == yong:
            return "体克用（吉，主动有力）"
        else:
            return "体用比和（平稳）"
    
    def _map_meanings(self, data: Dict) -> Dict:
        return data
    
    def _interpret(self, meanings: Dict) -> str:
        ben_gua = meanings["ben_gua"]
        hu_gua = meanings["hu_gua"]
        bian_gua = meanings["bian_gua"]
        ti = meanings["ti_gua"]
        yong = meanings["yong_gua"]
        sheng_ke = meanings["sheng_ke"]
        question = meanings["question"]
        
        lines = []
        
        if question:
            lines.append(f"【所问之事】{question}")
        
        lines.append(f"【本卦】第{ben_gua.get('num', '')}卦 · {ben_gua.get('name', '')}卦")
        lines.append(f"  {ben_gua.get('meaning', '')}")
        
        lines.append(f"\n【体用分析】")
        lines.append(f"  体卦（{ti['name']}·{ti['element']}）：{ti['trait']}")
        lines.append(f"  用卦（{yong['name']}·{yong['element']}）：{yong['trait']}")
        lines.append(f"  体用关系：{sheng_ke}")
        
        lines.append(f"\n【互卦】{hu_gua.get('name', '')}卦（事情内部发展趋势）")
        lines.append(f"  {hu_gua.get('meaning', '')}")
        
        lines.append(f"\n【变卦】{bian_gua.get('name', '')}卦（第{meanings['dong_yao']}爻动，事情最终走向）")
        lines.append(f"  {bian_gua.get('meaning', '')}")
        
        lines.append(f"\n【综合断语】")
        if "吉" in sheng_ke:
            lines.append(f"整体卦象偏吉，{ben_gua.get('name', '')}卦提示：{ben_gua.get('meaning', '')[:30]}。")
            lines.append(f"顺势而为，把握时机，事情朝{bian_gua.get('name', '')}卦方向发展。")
        else:
            lines.append(f"卦象提示需谨慎，{ben_gua.get('name', '')}卦警示：{ben_gua.get('meaning', '')[:30]}。")
            lines.append(f"宜静不宜动，等待{bian_gua.get('name', '')}卦所示的转机。")
        
        return "\n".join(lines)
    
    def _generate_suggestions(self, meanings: Dict) -> List[str]:
        sheng_ke = meanings["sheng_ke"]
        ben_gua = meanings["ben_gua"]
        
        suggestions = [
            f"本卦核心启示：{ben_gua.get('meaning', '')[:40]}",
        ]
        
        if "大吉" in sheng_ke or "体克用" in sheng_ke:
            suggestions.append("时机有利，可积极推进，主动出击")
            suggestions.append("把握当下窗口期，不宜拖延")
        elif "凶" in sheng_ke:
            suggestions.append("当前时机不佳，宜守不宜攻，静待变化")
            suggestions.append("注意防范外部阻力，低调行事")
        else:
            suggestions.append("平稳推进，按部就班，不急不躁")
        
        suggestions.append("易经重在'时'与'位'，同一卦在不同时机结论不同，需结合实际情况判断")
        suggestions.append("变卦揭示最终走向，可作为行动参考的终点目标")
        
        return suggestions[:5]
