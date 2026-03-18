"""
塔罗牌预测系统
78张完整牌库（22大阿卡纳 + 56小阿卡纳），支持多种牌阵
宗师级深度：正逆位牌义、牌阵综合解读、实际生活映射
"""
from src.core import BaseDiviner, BirthInfo, PredictionResult
from typing import Dict, List, Optional
import random
import hashlib


# ==================== 牌库 ====================

MAJOR_ARCANA = [
    {"id": 0,  "name": "愚者",     "en": "The Fool",         "upright": "新开始、冒险、纯真、自由精神", "reversed": "鲁莽、逃避、冒失、不负责任"},
    {"id": 1,  "name": "魔术师",   "en": "The Magician",     "upright": "意志力、技能、专注、创造力",   "reversed": "操纵、欺骗、技能浪费、缺乏专注"},
    {"id": 2,  "name": "女祭司",   "en": "The High Priestess","upright": "直觉、神秘、内在知识、潜意识", "reversed": "隐藏秘密、压抑直觉、表面知识"},
    {"id": 3,  "name": "女皇",     "en": "The Empress",      "upright": "丰盛、母性、创造、自然美",     "reversed": "依赖、创造力受阻、过度保护"},
    {"id": 4,  "name": "皇帝",     "en": "The Emperor",      "upright": "权威、结构、稳定、父性",       "reversed": "专制、控制欲、缺乏灵活"},
    {"id": 5,  "name": "教皇",     "en": "The Hierophant",   "upright": "传统、信仰、精神指引、规范",   "reversed": "叛逆、打破传统、个人信仰"},
    {"id": 6,  "name": "恋人",     "en": "The Lovers",       "upright": "爱情、选择、价值观、和谐",     "reversed": "失衡、价值观冲突、错误选择"},
    {"id": 7,  "name": "战车",     "en": "The Chariot",      "upright": "意志力、胜利、控制、决心",     "reversed": "失控、侵略性、缺乏方向"},
    {"id": 8,  "name": "力量",     "en": "Strength",         "upright": "内在力量、勇气、耐心、同情",   "reversed": "软弱、自我怀疑、缺乏自信"},
    {"id": 9,  "name": "隐士",     "en": "The Hermit",       "upright": "内省、独处、指引、寻求真相",   "reversed": "孤立、拒绝帮助、迷失"},
    {"id": 10, "name": "命运之轮", "en": "Wheel of Fortune", "upright": "命运、转折、机遇、循环",       "reversed": "坏运气、抗拒变化、命运失控"},
    {"id": 11, "name": "正义",     "en": "Justice",          "upright": "公正、真相、因果、平衡",       "reversed": "不公正、逃避责任、不诚实"},
    {"id": 12, "name": "倒吊人",   "en": "The Hanged Man",   "upright": "暂停、放手、新视角、牺牲",     "reversed": "拖延、抗拒、无谓牺牲"},
    {"id": 13, "name": "死神",     "en": "Death",            "upright": "结束、转变、过渡、放手",       "reversed": "抗拒变化、停滞、无法放手"},
    {"id": 14, "name": "节制",     "en": "Temperance",       "upright": "平衡、耐心、调和、目标感",     "reversed": "失衡、过度、缺乏长远规划"},
    {"id": 15, "name": "恶魔",     "en": "The Devil",        "upright": "束缚、物质主义、阴暗面、执念", "reversed": "解脱、摆脱束缚、重获自由"},
    {"id": 16, "name": "塔",       "en": "The Tower",        "upright": "突变、混乱、启示、打破旧结构", "reversed": "避免灾难、延迟崩溃、内部动荡"},
    {"id": 17, "name": "星星",     "en": "The Star",         "upright": "希望、灵感、平静、更新",       "reversed": "绝望、失去信念、失去方向"},
    {"id": 18, "name": "月亮",     "en": "The Moon",         "upright": "幻觉、恐惧、潜意识、混乱",     "reversed": "释放恐惧、压抑情绪、混乱减少"},
    {"id": 19, "name": "太阳",     "en": "The Sun",          "upright": "成功、快乐、活力、清晰",       "reversed": "短暂的悲观、延迟成功"},
    {"id": 20, "name": "审判",     "en": "Judgement",        "upright": "反思、重生、内在召唤、宽恕",   "reversed": "自我怀疑、拒绝改变、错失机会"},
    {"id": 21, "name": "世界",     "en": "The World",        "upright": "完成、整合、成就、旅行",       "reversed": "未完成、延迟、缺乏完结感"},
]

# 小阿卡纳（权杖/圣杯/宝剑/星币各14张，此处用代表性牌）
SUITS = {
    "权杖": {"element": "火", "domain": "事业、激情、创造力、行动"},
    "圣杯": {"element": "水", "domain": "情感、关系、直觉、梦想"},
    "宝剑": {"element": "风", "domain": "思维、冲突、真相、挑战"},
    "星币": {"element": "土", "domain": "物质、金钱、工作、实际"},
}

COURT_CARDS = ["侍从", "骑士", "王后", "国王"]
PIP_MEANINGS = {
    1: "新开始、潜力、种子", 2: "平衡、选择、合作",
    3: "创造、合作、成长", 4: "稳定、休息、巩固",
    5: "冲突、挑战、变化", 6: "和谐、给予、回忆",
    7: "评估、策略、防御", 8: "行动、进展、技能",
    9: "接近完成、智慧、独立", 10: "完成、结束、过渡",
}


def build_minor_arcana() -> List[Dict]:
    """构建56张小阿卡纳"""
    cards = []
    for suit, info in SUITS.items():
        # A到10
        for num in range(1, 11):
            num_name = "A" if num == 1 else str(num)
            cards.append({
                "name": f"{suit}{num_name}",
                "suit": suit,
                "number": num,
                "element": info["element"],
                "upright": f"{suit}牌组{num_name}：{PIP_MEANINGS.get(num, '')}，{info['domain']}方面有所显现",
                "reversed": f"{suit}牌组{num_name}逆位：{info['domain']}方面遇阻，需要重新审视",
            })
        # 宫廷牌
        for court in COURT_CARDS:
            cards.append({
                "name": f"{suit}{court}",
                "suit": suit,
                "number": 11 + COURT_CARDS.index(court),
                "element": info["element"],
                "upright": f"{suit}{court}：{info['domain']}领域中成熟稳健的能量或人物",
                "reversed": f"{suit}{court}逆位：{info['domain']}领域中能量受阻或人物的负面特质",
            })
    return cards


ALL_CARDS = MAJOR_ARCANA + build_minor_arcana()

# 牌阵定义
SPREADS = {
    "单张": {"positions": ["当前状况"], "desc": "快速洞察当下"},
    "三张": {"positions": ["过去", "现在", "未来"], "desc": "时间线解读"},
    "凯尔特十字": {
        "positions": ["当前状况", "挑战/阻碍", "遥远过去", "近期过去", "可能结果", "近期未来", "自身态度", "外部影响", "希望与恐惧", "最终结果"],
        "desc": "最全面的综合解读"
    },
    "爱情三角": {"positions": ["你的感受", "对方感受", "关系走向"], "desc": "感情专项解读"},
    "是否": {"positions": ["支持的力量", "阻碍的力量", "建议"], "desc": "决策参考"},
}


# ==================== 主类 ====================

class TarotReader(BaseDiviner):
    """
    塔罗牌预测系统
    
    使用方法：
        birth = BirthInfo(1990, 3, 18, 14, 30)
        reader = TarotReader(birth, spread="三张", question="感情走向如何？")
        result = reader.predict()
    """
    
    def __init__(self, birth_info: BirthInfo, spread: str = "三张", question: str = ""):
        super().__init__(birth_info)
        self.spread = spread if spread in SPREADS else "三张"
        self.question = question
    
    def _draw_cards(self) -> List[Dict]:
        """根据出生信息生成确定性随机抽牌（可重复）"""
        seed_str = f"{self.birth_info.year}{self.birth_info.month}{self.birth_info.day}{self.question}"
        seed = int(hashlib.md5(seed_str.encode()).hexdigest(), 16) % (2**32)
        rng = random.Random(seed)
        
        spread_info = SPREADS[self.spread]
        n = len(spread_info["positions"])
        
        cards = rng.sample(ALL_CARDS, n)
        # 随机正逆位
        drawn = []
        for card in cards:
            is_reversed = rng.random() > 0.65  # 约35%逆位
            drawn.append({**card, "is_rev": is_reversed})
        return drawn
    
    def _calculate(self) -> Dict:
        drawn_cards = self._draw_cards()
        spread_info = SPREADS[self.spread]
        
        card_readings = []
        for i, (card, position) in enumerate(zip(drawn_cards, spread_info["positions"])):
            is_rev = card["is_rev"]
            meaning = card.get("reversed", "") if is_rev else card.get("upright", "")
            
            card_readings.append({
                "position": position,
                "card_name": card["name"],
                "is_reversed": is_rev,
                "orientation": "逆位" if is_rev else "正位",
                "meaning": meaning,
            })
        
        return {
            "spread": self.spread,
            "question": self.question,
            "card_readings": card_readings,
            "spread_desc": spread_info["desc"],
        }
    
    def _map_meanings(self, data: Dict) -> Dict:
        card_readings = data["card_readings"]
        
        # 统计正逆位比例
        reversed_count = sum(1 for c in card_readings if c["is_reversed"])
        total = len(card_readings)
        
        # 主要能量
        major_cards = [c for c in card_readings if any(
            m["name"] == c["card_name"] for m in MAJOR_ARCANA
        )]
        
        energy_tone = "积极向上" if reversed_count < total / 2 else "需要内省调整"
        
        return {
            "card_readings": card_readings,
            "energy_tone": energy_tone,
            "major_cards": major_cards,
            "reversed_ratio": f"{reversed_count}/{total}",
            "question": data["question"],
        }
    
    def _interpret(self, meanings: Dict) -> str:
        card_readings = meanings["card_readings"]
        energy_tone = meanings["energy_tone"]
        question = meanings["question"]
        
        lines = []
        
        if question:
            lines.append(f"【问题】{question}")
        
        lines.append(f"【整体能量】{energy_tone}，牌阵呈现{meanings['reversed_ratio']}逆位。")
        lines.append("")
        
        for reading in card_readings:
            lines.append(f"【{reading['position']}】{reading['card_name']}（{reading['orientation']}）")
            lines.append(f"  → {reading['meaning']}")
        
        lines.append("")
        
        # 综合解读
        if len(card_readings) >= 3:
            first = card_readings[0]["card_name"]
            last = card_readings[-1]["card_name"]
            lines.append(f"【综合解读】从{first}到{last}，牌阵揭示了一个从{card_readings[0]['position']}到{card_readings[-1]['position']}的完整叙事。")
            lines.append("塔罗不是命运的判决，而是当下能量的镜像——你看到的，正是你内心深处已知的答案。")
        
        return "\n".join(lines)
    
    def _generate_suggestions(self, meanings: Dict) -> List[str]:
        card_readings = meanings["card_readings"]
        suggestions = []
        
        # 基于牌义生成建议
        for reading in card_readings[:3]:
            if not reading["is_reversed"]:
                suggestions.append(f"{reading['position']}方面：{reading['card_name']}正位提示你顺势而为，{reading['meaning'][:20]}...")
            else:
                suggestions.append(f"{reading['position']}方面：{reading['card_name']}逆位提醒你需要调整，{reading['meaning'][:20]}...")
        
        suggestions.append("塔罗解读仅供参考，最终决策权在你自己手中")
        suggestions.append("建议在平静状态下重新抽牌，情绪稳定时的解读更准确")
        
        return suggestions[:5]
    
    def _assess_confidence(self, data: Dict) -> float:
        return 0.75  # 塔罗主观性较强
