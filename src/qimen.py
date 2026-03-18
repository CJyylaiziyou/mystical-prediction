"""
奇门遁甲预测系统
时家奇门，按时辰排盘，九宫八门九星十神，方位吉凶断事
宗师级深度：三奇六仪、八门吉凶、九星旺衰、方位趋避
"""
from src.core import BaseDiviner, BirthInfo, PredictionResult
from typing import Dict, List, Tuple
from datetime import datetime


# ==================== 基础数据 ====================

# 九宫方位
JIUGONG = {
    1: "坎宫（北）", 2: "坤宫（西南）", 3: "震宫（东）",
    4: "巽宫（东南）", 5: "中宫", 6: "乾宫（西北）",
    7: "兑宫（西）", 8: "艮宫（东北）", 9: "离宫（南）",
}

# 八门吉凶
BA_MEN = {
    "开门": {"jixiong": "大吉", "domain": "出行、开业、求职、谈判"},
    "休门": {"jixiong": "吉",   "domain": "休息、养生、隐居、保守"},
    "生门": {"jixiong": "大吉", "domain": "求财、经商、农业、生育"},
    "伤门": {"jixiong": "凶",   "domain": "出行受阻、争斗、伤病"},
    "杜门": {"jixiong": "凶",   "domain": "闭塞、隐藏、逃跑、埋伏"},
    "景门": {"jixiong": "小吉", "domain": "文书、考试、婚姻、火灾"},
    "死门": {"jixiong": "大凶", "domain": "丧葬、疾病、绝境"},
    "惊门": {"jixiong": "凶",   "domain": "惊恐、官司、口舌是非"},
}

# 九星吉凶
JIU_XING = {
    "天蓬": {"jixiong": "凶", "element": "水", "trait": "盗贼、奸邪、险阻"},
    "天芮": {"jixiong": "凶", "element": "土", "trait": "疾病、死亡、小人"},
    "天冲": {"jixiong": "吉", "element": "木", "trait": "勇猛、行动、震动"},
    "天辅": {"jixiong": "吉", "element": "木", "trait": "文书、贵人、辅助"},
    "天禽": {"jixiong": "吉", "element": "土", "trait": "中正、稳定、帝王"},
    "天心": {"jixiong": "吉", "element": "金", "trait": "医药、智慧、谋略"},
    "天柱": {"jixiong": "凶", "element": "金", "trait": "破坏、口舌、折断"},
    "天任": {"jixiong": "吉", "element": "土", "trait": "稳重、仁厚、承载"},
    "天英": {"jixiong": "凶", "element": "火", "trait": "虚名、文采、虚伪"},
}

# 三奇六仪
SAN_QI = ["乙", "丙", "丁"]  # 三奇（天奇、地奇、人奇）
LIU_YI = ["戊", "己", "庚", "辛", "壬", "癸"]  # 六仪

# 天干五行
TIANGAN_ELEMENT = {
    "甲": "木", "乙": "木", "丙": "火", "丁": "火",
    "戊": "土", "己": "土", "庚": "金", "辛": "金",
    "壬": "水", "癸": "水",
}

# 吉方建议
LUCKY_DIRECTIONS = {
    "开门": "西北方（乾宫）",
    "休门": "北方（坎宫）",
    "生门": "东北方（艮宫）",
    "景门": "南方（离宫）",
}


# ==================== 排盘计算 ====================

def get_shichen(hour: int) -> Tuple[int, str]:
    """获取时辰序号和名称"""
    shichen_names = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]
    idx = hour // 2
    return idx, shichen_names[idx]


def get_ju_number(year: int, month: int, day: int, hour: int) -> Tuple[int, str]:
    """
    计算局数（阳遁/阴遁）
    简化算法：根据月份判断阴阳遁，根据日时计算局数
    """
    # 冬至到夏至为阳遁（11月-次年4月），夏至到冬至为阴遁
    if month in [11, 12, 1, 2, 3, 4]:
        dun_type = "阳遁"
        ju = (day + hour // 2) % 9 + 1
    else:
        dun_type = "阴遁"
        ju = 9 - (day + hour // 2) % 9
        if ju == 0:
            ju = 9
    
    return ju, dun_type


def arrange_jiugong(ju: int, dun_type: str) -> Dict[int, Dict]:
    """
    排九宫（简化版）
    阳遁顺布，阴遁逆布
    """
    # 八门在九宫中的分布（按局数偏移）
    men_list = list(BA_MEN.keys())
    xing_list = list(JIU_XING.keys())
    
    gong_info = {}
    for gong_num in range(1, 10):
        if gong_num == 5:
            # 中宫
            gong_info[gong_num] = {
                "gong": JIUGONG[gong_num],
                "men": "中宫无门",
                "xing": xing_list[(ju + gong_num) % 9],
                "gan": "戊",
            }
            continue
        
        if dun_type == "阳遁":
            men_idx = (ju + gong_num - 2) % 8
            xing_idx = (ju + gong_num - 1) % 9
        else:
            men_idx = (8 - ju + gong_num) % 8
            xing_idx = (9 - ju + gong_num) % 9
        
        gan_idx = (ju + gong_num) % 10
        gan_list = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
        
        gong_info[gong_num] = {
            "gong": JIUGONG[gong_num],
            "men": men_list[men_idx],
            "xing": xing_list[xing_idx % 9],
            "gan": gan_list[gan_idx % 10],
        }
    
    return gong_info


def find_lucky_gong(gong_info: Dict) -> List[Dict]:
    """找出吉方"""
    lucky = []
    for gong_num, info in gong_info.items():
        men = info.get("men", "")
        xing = info.get("xing", "")
        
        men_ji = BA_MEN.get(men, {}).get("jixiong", "")
        xing_ji = JIU_XING.get(xing, {}).get("jixiong", "")
        
        if men_ji in ["大吉", "吉"] and xing_ji in ["大吉", "吉"]:
            lucky.append({
                "gong": info["gong"],
                "men": men,
                "xing": xing,
                "level": "上吉",
            })
        elif men_ji in ["大吉", "吉"] or xing_ji in ["大吉", "吉"]:
            lucky.append({
                "gong": info["gong"],
                "men": men,
                "xing": xing,
                "level": "次吉",
            })
    
    return lucky[:3]  # 返回前三吉方


# ==================== 主类 ====================

class QimenCalculator(BaseDiviner):
    """
    奇门遁甲预测系统
    
    使用方法：
        birth = BirthInfo(1990, 3, 18, 14, 30)
        calc = QimenCalculator(birth, question="出行方向如何选择？")
        result = calc.predict()
    """
    
    def __init__(self, birth_info: BirthInfo, question: str = ""):
        super().__init__(birth_info)
        self.question = question
    
    def _calculate(self) -> Dict:
        b = self.birth_info
        
        # 时辰
        shichen_idx, shichen_name = get_shichen(b.hour)
        
        # 局数
        ju, dun_type = get_ju_number(b.year, b.month, b.day, b.hour)
        
        # 排九宫
        gong_info = arrange_jiugong(ju, dun_type)
        
        # 找吉方
        lucky_gongs = find_lucky_gong(gong_info)
        
        # 值符值使（当值的星和门）
        zhifu_gong = ju  # 值符在本局宫位
        zhifu_info = gong_info.get(zhifu_gong, {})
        
        return {
            "ju": ju,
            "dun_type": dun_type,
            "shichen": shichen_name,
            "gong_info": gong_info,
            "lucky_gongs": lucky_gongs,
            "zhifu": zhifu_info,
            "question": self.question,
        }
    
    def _map_meanings(self, data: Dict) -> Dict:
        return data
    
    def _interpret(self, meanings: Dict) -> str:
        lines = []
        
        if meanings["question"]:
            lines.append(f"【所问】{meanings['question']}")
        
        lines.append(f"\n【时家奇门盘】{meanings['dun_type']}第{meanings['ju']}局 · {meanings['shichen']}时")
        
        lines.append(f"\n【九宫概览】")
        for gong_num in [4, 9, 2, 3, 5, 7, 8, 1, 6]:  # 按方位顺序
            info = meanings["gong_info"].get(gong_num, {})
            men = info.get("men", "")
            xing = info.get("xing", "")
            men_ji = BA_MEN.get(men, {}).get("jixiong", "")
            lines.append(f"  {info.get('gong', '')}：{men}（{men_ji}）+ {xing}")
        
        lines.append(f"\n【吉方推荐】")
        lucky = meanings["lucky_gongs"]
        if lucky:
            for i, lg in enumerate(lucky, 1):
                men_domain = BA_MEN.get(lg["men"], {}).get("domain", "")
                lines.append(f"  第{i}吉方：{lg['gong']}（{lg['level']}）")
                lines.append(f"    {lg['men']}+{lg['xing']}，适合：{men_domain[:20]}")
        else:
            lines.append("  当前时辰吉方不明显，宜守不宜动")
        
        lines.append(f"\n【断语】")
        if lucky:
            best = lucky[0]
            lines.append(f"当前{meanings['dun_type']}第{meanings['ju']}局，{best['gong']}为最吉之方。")
            men_domain = BA_MEN.get(best["men"], {}).get("domain", "")
            lines.append(f"{best['men']}主{men_domain}，{best['xing']}星辅之，此方向行事事半功倍。")
        else:
            lines.append(f"当前时辰吉门不显，宜静待时机，不宜轻举妄动。")
        
        return "\n".join(lines)
    
    def _generate_suggestions(self, meanings: Dict) -> List[str]:
        lucky = meanings["lucky_gongs"]
        suggestions = []
        
        if lucky:
            best = lucky[0]
            men_domain = BA_MEN.get(best["men"], {}).get("domain", "")
            suggestions.append(f"最佳方位：{best['gong']}，适合{men_domain[:15]}等事宜")
            suggestions.append(f"出行、谈判、求财可选择朝向{best['gong']}方向")
        
        suggestions.append(f"当前{meanings['dun_type']}，顺应时势，不逆势而行")
        suggestions.append("奇门遁甲重在'时机'与'方位'，同一事在不同时辰的吉凶方位不同")
        suggestions.append("重大决策建议结合八字、紫微斗数综合判断，单一体系仅供参考")
        
        return suggestions[:5]
    
    def _assess_confidence(self, data: Dict) -> float:
        return 0.80
