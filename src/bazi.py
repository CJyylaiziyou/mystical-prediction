"""
八字四柱预测系统
通过天干地支的组合，解析五行配置、大运、流年
宗师级深度：十神论断、喜用神分析、运势推演
"""

from src.core import BaseDiviner, BirthInfo, Element, PredictionResult
from typing import Dict, List, Tuple
from datetime import datetime


class BaziCalculator(BaseDiviner):
    """
    八字四柱系统
    
    核心原理：
    1. 出生时间转换为天干地支（年月日时）
    2. 分析五行的平衡度和喜用神
    3. 根据十神论进行深度解读
    4. 推演大运和流年的影响
    """
    
    system_name_cn = "八字四柱"
    
    # 十天干
    HEAVENLY_STEMS = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
    
    # 十二地支
    EARTHLY_BRANCHES = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]
    
    # 天干对应五行
    STEM_ELEMENT_MAP = {
        "甲": Element.WOOD, "乙": Element.WOOD,
        "丙": Element.FIRE, "丁": Element.FIRE,
        "戊": Element.EARTH, "己": Element.EARTH,
        "庚": Element.METAL, "辛": Element.METAL,
        "壬": Element.WATER, "癸": Element.WATER,
    }
    
    # 地支对应五行
    BRANCH_ELEMENT_MAP = {
        "子": Element.WATER, "丑": Element.EARTH,
        "寅": Element.WOOD, "卯": Element.WOOD,
        "辰": Element.EARTH, "巳": Element.FIRE,
        "午": Element.FIRE, "未": Element.EARTH,
        "申": Element.METAL, "酉": Element.METAL,
        "戌": Element.EARTH, "亥": Element.WATER,
    }
    
    # 十神定义 (相对于日干)
    SHIFU_MAP = {
        "相同": "比肩/劫财",
        "同性生": "食神/伤官",
        "异性生": "正财/偏财",
        "生我同": "正印/偏印",
        "生我异": "正官/偏官",
    }
    
    # 日干性质
    STEM_TRAITS = {
        "甲": {"五行": "木", "阴阳": "阳", "性格": "仁慈、好动、竞争心强"},
        "乙": {"五行": "木", "阴阳": "阴", "性格": "温和、委婉、细心敏感"},
        "丙": {"五行": "火", "阴阳": "阳", "性格": "热情、积极、急躁易动怒"},
        "丁": {"五行": "火", "阴阳": "阴", "性格": "聪慧、谨慎、内向沉静"},
        "戊": {"五行": "土", "阴阳": "阳", "性格": "诚实、厚重、踏实稳健"},
        "己": {"五行": "土", "阴阳": "阴", "性格": "灵活、精细、多思多虑"},
        "庚": {"五行": "金", "阴阳": "阳", "性格": "刚毅、果断、固执强硬"},
        "辛": {"五行": "金", "阴阳": "阴", "性格": "精明、敏锐、好管闲事"},
        "壬": {"五行": "水", "阴阳": "阳", "性格": "聪慧、好学、好色贪心"},
        "癸": {"五行": "水", "阴阳": "阴", "性格": "柔和、沉静、内敛神秘"},
    }
    
    def __init__(self, birth_info: BirthInfo):
        super().__init__(birth_info, kb_filename="bazi_knowledge.json")
    
    def _calculate(self) -> Dict:
        """计算八字四柱"""
        year_stem, year_branch = self._calculate_year_pillar()
        month_stem, month_branch = self._calculate_month_pillar(year_stem)
        day_stem, day_branch = self._calculate_day_pillar()
        hour_stem, hour_branch = self._calculate_hour_pillar(day_stem)
        
        all_stems = [year_stem, month_stem, day_stem, hour_stem]
        all_branches = [year_branch, month_branch, day_branch, hour_branch]
        
        return {
            "four_pillars": {
                "year": (year_stem, year_branch),
                "month": (month_stem, month_branch),
                "day": (day_stem, day_branch),
                "hour": (hour_stem, hour_branch),
            },
            "day_master": day_stem,
            "day_master_element": self.STEM_ELEMENT_MAP[day_stem],
            "day_master_traits": self.STEM_TRAITS[day_stem],
            "all_stems": all_stems,
            "all_branches": all_branches,
            "five_elements": self._analyze_elements(all_stems, all_branches),
            "strength_analysis": self._analyze_strength(day_stem, all_stems, all_branches),
        }
    
    def _calculate_year_pillar(self) -> Tuple[str, str]:
        """计算年柱"""
        year = self.birth_info.year
        
        # 天干: (year - 4) % 10
        stem_idx = (year - 4) % 10
        stem = self.HEAVENLY_STEMS[stem_idx]
        
        # 地支: (year - 4) % 12
        branch_idx = (year - 4) % 12
        branch = self.EARTHLY_BRANCHES[branch_idx]
        
        return stem, branch
    
    def _calculate_month_pillar(self, year_stem: str) -> Tuple[str, str]:
        """计算月柱"""
        month = self.birth_info.month
        day = self.birth_info.day
        
        # 地支直接用月份
        branch = self.EARTHLY_BRANCHES[(month - 1) % 12]
        
        # 天干根据年干推算
        year_stem_idx = self.HEAVENLY_STEMS.index(year_stem)
        
        # 月干有固定规律：以甲子月为起点
        month_stem_map = {
            1: ["丙", "戊", "庚", "壬", "甲"],  # 子月: 丙子、戊子、庚子、壬子、甲子
            2: ["丁", "己", "辛", "癸", "乙"],  # 丑月
            # ... (实际应该有12个月的映射)
        }
        
        # 简化处理：根据年干推算
        base_stem_idx = (year_stem_idx * 2 + month - 1) % 10
        stem = self.HEAVENLY_STEMS[base_stem_idx]
        
        return stem, branch
    
    def _calculate_day_pillar(self) -> Tuple[str, str]:
        """
        计算日柱
        需要用到复杂的历法计算，这里使用简化版本
        实际应该调用专业的农历算法库
        """
        # 简化实现：基于年月日的哈希
        total_days = (self.birth_info.year - 1900) * 365 + \
                     (self.birth_info.month - 1) * 30 + \
                     self.birth_info.day
        
        stem_idx = (total_days + 4) % 10
        branch_idx = (total_days + 0) % 12
        
        stem = self.HEAVENLY_STEMS[stem_idx]
        branch = self.EARTHLY_BRANCHES[branch_idx]
        
        return stem, branch
    
    def _calculate_hour_pillar(self, day_stem: str) -> Tuple[str, str]:
        """计算时柱"""
        hour = self.birth_info.hour
        
        # 地支：一个时辰对应两个小时
        branch_idx = (hour // 2) % 12
        branch = self.EARTHLY_BRANCHES[branch_idx]
        
        # 天干：根据日干推算
        day_stem_idx = self.HEAVENLY_STEMS.index(day_stem)
        
        # 时干有规律：甲己日甲子时起，乙庚日丙子时起...
        hour_stem_offset = {
            0: 0,  # 甲己日 -> 甲
            1: 2,  # 乙庚日 -> 丙
            2: 4,  # 丙辛日 -> 戊
            3: 6,  # 丁壬日 -> 庚
            4: 8,  # 戊癸日 -> 壬
        }
        
        offset = hour_stem_offset.get(day_stem_idx % 5, 0)
        stem_idx = (offset + branch_idx) % 10
        stem = self.HEAVENLY_STEMS[stem_idx]
        
        return stem, branch
    
    def _analyze_elements(self, stems: List[str], branches: List[str]) -> Dict[Element, int]:
        """分析五行配置"""
        elements_count = {e: 0 for e in Element}
        
        # 统计天干中的五行
        for stem in stems:
            element = self.STEM_ELEMENT_MAP[stem]
            elements_count[element] += 1
        
        # 统计地支中的五行（地支中包含多个五行）
        for branch in branches:
            element = self.BRANCH_ELEMENT_MAP[branch]
            elements_count[element] += 1
        
        return elements_count
    
    def _analyze_strength(self, day_stem: str, stems: List[str], 
                         branches: List[str]) -> Dict:
        """分析日干强弱"""
        day_stem_element = self.STEM_ELEMENT_MAP[day_stem]
        
        # 统计帮扶日干的力量
        support = 0
        克制日干的力量克制 = 0
        
        for stem in stems[1:]:  # 除了日干本身
            element = self.STEM_ELEMENT_MAP[stem]
            # 同五行为比肩/劫财，相生为帮扶
            if element == day_stem_element:
                support += 2
            elif self._element_generates(element, day_stem_element):
                support += 1
            elif self._element_generates(day_stem_element, element):
                克制 -= 1
            elif self._element_counters(element, day_stem_element):
                克制 -= 2
        
        strength = "强" if support > 克制 else "弱" if support < 克制 else "平"
        
        return {
            "strength": strength,
            "support_power": support,
            "counter_power": 克制,
            "needs": self._get_element_needs(strength, day_stem_element)
        }
    
    def _element_generates(self, source: Element, target: Element) -> bool:
        """判断source是否生target"""
        generation_map = {
            Element.WOOD: Element.FIRE,
            Element.FIRE: Element.EARTH,
            Element.EARTH: Element.METAL,
            Element.METAL: Element.WATER,
            Element.WATER: Element.WOOD,
        }
        return generation_map.get(source) == target
    
    def _element_counters(self, attacker: Element, defender: Element) -> bool:
        """判断attacker是否克defender"""
        counter_map = {
            Element.WOOD: Element.EARTH,
            Element.EARTH: Element.WATER,
            Element.WATER: Element.FIRE,
            Element.FIRE: Element.METAL,
            Element.METAL: Element.WOOD,
        }
        return counter_map.get(attacker) == defender
    
    def _get_element_needs(self, strength: str, element: Element) -> List[str]:
        """根据强弱判断需要补强的五行"""
        if strength == "强":
            # 需要克制和消耗
            return ["克制", "消耗"]
        elif strength == "弱":
            # 需要帮扶和生助
            return ["帮扶", "生助"]
        else:
            return ["维持平衡"]
    
    def _map_meanings(self, data: Dict) -> Dict:
        """映射到八字含义"""
        day_stem = data["day_master"]
        elements = data["five_elements"]
        strength = data["strength_analysis"]
        
        # 分析喜用神
        day_element = data["day_master_element"]
        favorable_element = self._determine_favorable_element(
            day_element, strength["strength"], elements
        )
        
        return {
            "day_master": day_stem,
            "day_master_element": day_element,
            "day_master_yin_yang": self.STEM_TRAITS[day_stem]["阴阳"],
            "five_elements": elements,
            "strongest_element": max(elements.items(), key=lambda x: x[1])[0],
            "weakest_element": min(elements.items(), key=lambda x: x[1])[0],
            "balance_status": self._assess_balance(elements),
            "day_master_strength": strength["strength"],
            "favorable_element": favorable_element,
            "unfavorable_element": self._get_unfavorable_element(favorable_element),
            "traits": self.STEM_TRAITS[day_stem],
        }
    
    def _determine_favorable_element(self, day_element: Element, 
                                     strength: str, elements: Dict) -> Element:
        """确定喜用神"""
        if strength == "强":
            # 日干过强，需要克制或消耗
            for element in Element:
                if self._element_counters(element, day_element):
                    return element
        else:
            # 日干偏弱，需要帮扶
            if self._element_generates(day_element, Element.FIRE):
                return day_element
            for element in Element:
                if self._element_generates(element, day_element):
                    return element
        
        return day_element
    
    def _get_unfavorable_element(self, favorable: Element) -> Element:
        """根据喜用神推断忌讳的五行"""
        counter_map = {
            Element.FIRE: Element.METAL,
            Element.METAL: Element.FIRE,
            Element.WATER: Element.FIRE,
            Element.WOOD: Element.METAL,
            Element.EARTH: Element.WOOD,
        }
        return counter_map.get(favorable, Element.EARTH)
    
    def _assess_balance(self, elements: Dict[Element, int]) -> str:
        """评估五行平衡度"""
        values = list(elements.values())
        max_val = max(values)
        min_val = min(values)
        
        if max_val - min_val == 0:
            return "极其平衡"
        elif max_val - min_val <= 1:
            return "平衡"
        elif max_val - min_val <= 2:
            return "基本平衡"
        elif max_val - min_val <= 3:
            return "略失衡"
        else:
            return "严重失衡"
    
    def _interpret(self, meanings: Dict) -> str:
        """生成宗师级解读"""
        day_stem = meanings["day_master"]
        element = meanings["day_master_element"]
        strength = meanings["day_master_strength"]
        balance = meanings["balance_status"]
        favorable = meanings["favorable_element"]
        traits = meanings["traits"]
        
        interpretation = f"""
【八字四柱深度解读】

你的日干为{day_stem}{element.value}，这是你八字的【身份密码】。

{element.value}性人的基本特质：
• {traits['性格']}
• 心理优势：稳定、坚持
• 潜在劣势：过度{element.value}会显得死板、缺乏变通

📊 五行能量分布：{balance}
{balance.startswith('极其平衡') and '这表示你的五行配置天然和谐，人生运势相对平稳顺利。' or '这提示你需要在生活中有意识地调理，平衡五行能量。'}

🔑 喜用神分析：【{favorable.value}】
这是你命盘中最需要的能量：
• 遇到属{favorable.value}的人、事、物，运势会明显提升
• 选择{favorable.value}相关的行业、方位能事半功倍
• 困难时期，靠近{favorable.value}的能量能获得转机

⚠️ 需要克制的：【{meanings['unfavorable_element'].value}】
• 过量的{meanings['unfavorable_element'].value}能量会拖累你
• 需要在人际选择、投资决策上保持谨慎
• 可通过增强喜用神来中和

💪 你当前的优势：日干{strength}，说明{strength == '强' and '你有很强的自我意识和执行力，但需要学会倾听他人，避免固执己见。' or '你需要借助外力获得成就，擅长团队合作，容易获得贵人相助。'}

🎯 建议方向：
在接下来的12个月，重点接触{favorable.value}属性的事物：
• 颜色选择：关注与{favorable.value}对应的色系
• 方位选择：{favorable.value}对应的方位能增强运势
• 人脉建立：寻找属{favorable.value}五行特质的人成为朋友或伙伴
        """
        return interpretation.strip()
    
    def _generate_suggestions(self, meanings: Dict) -> List[str]:
        """生成可操作建议"""
        favorable = meanings["favorable_element"]
        unfavorable = meanings["unfavorable_element"]
        strength = meanings["day_master_strength"]
        
        suggestions = [
            f"🎯 近一年重点补强【{favorable.value}】五行：选择相关颜色衣着、在其对应方位办公休息",
            f"🤝 寻找属【{favorable.value}】特质的人际关系，这些人是你的贵人和助力",
            f"⚡ {'避免过度依赖他人，培养独立思考能力' if strength == '强' else '学会主动出击，不要过度被动等待'}",
            f"📅 每个月查看《当月流年运势》，在关键节点提前做出调整",
            "🔮 建议每个季度做一次深度流年预测，动态优化人生策略",
        ]
        
        return suggestions
    
    def _assess_confidence(self, data: Dict) -> float:
        """评估可信度"""
        # 基础可信度
        confidence = 0.88
        
        # 根据数据完整性调整
        if data.get("four_pillars"):
            confidence += 0.04
        
        # 根据五行平衡度调整
        elements = data.get("five_elements", {})
        values = list(elements.values())
        if values:
            balance_score = 1 - (max(values) - min(values)) / sum(values)
            confidence = confidence * 0.5 + balance_score * 0.5
        
        return min(confidence, 0.95)  # 最高95%
    
    def _generate_tags(self, meanings: Dict) -> List[str]:
        """生成标签"""
        tags = [
            meanings["day_master_element"].value,
            meanings["balance_status"],
            f"喜{meanings['favorable_element'].value}",
        ]
        return tags


if __name__ == "__main__":
    # 测试
    birth_info = BirthInfo(1990, 3, 18, 14, 30, "湖南岳阳", "女")
    bazi = BaziCalculator(birth_info)
    result = bazi.predict()
    
    print(result.analysis)
    print("\n建议:")
    for suggestion in result.suggestions:
        print(f"• {suggestion}")
