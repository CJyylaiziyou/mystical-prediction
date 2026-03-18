"""
统一预测引擎
整合7大预测体系，生成综合报告
"""
from src.core import BirthInfo, PredictionResult
from src.bazi import BaziCalculator
from src.ziwei import ZiweiCalculator
from src.western_astro import WesternAstroCalculator
from src.tarot import TarotReader
from src.iching import IChingCalculator
from src.meihua import MeihuaCalculator
from src.qimen import QimenCalculator
from typing import Dict, List, Optional
from datetime import datetime


class SageDivination:
    """
    宗师级多维预测引擎
    
    使用方法：
        birth = BirthInfo(1990, 3, 18, 14, 30, "湖南岳阳", "女")
        sage = SageDivination(birth)
        report = sage.generate_comprehensive_report()
        print(report)
    """
    
    def __init__(self, birth_info: BirthInfo):
        self.birth_info = birth_info
        self.results: Dict[str, PredictionResult] = {}
    
    def predict_bazi(self) -> PredictionResult:
        calc = BaziCalculator(self.birth_info)
        result = calc.predict()
        self.results["bazi"] = result
        return result
    
    def predict_ziwei(self) -> PredictionResult:
        calc = ZiweiCalculator(self.birth_info)
        result = calc.predict()
        self.results["ziwei"] = result
        return result
    
    def predict_western_astro(self) -> PredictionResult:
        calc = WesternAstroCalculator(self.birth_info)
        result = calc.predict()
        self.results["western_astro"] = result
        return result
    
    def predict_tarot(self, spread: str = "三张", question: str = "") -> PredictionResult:
        reader = TarotReader(self.birth_info, spread=spread, question=question)
        result = reader.predict()
        self.results["tarot"] = result
        return result
    
    def predict_iching(self, question: str = "") -> PredictionResult:
        calc = IChingCalculator(self.birth_info, question=question)
        result = calc.predict()
        self.results["iching"] = result
        return result
    
    def predict_meihua(self, num1: int = None, num2: int = None, question: str = "") -> PredictionResult:
        calc = MeihuaCalculator(self.birth_info, num1=num1, num2=num2, question=question)
        result = calc.predict()
        self.results["meihua"] = result
        return result
    
    def predict_qimen(self, question: str = "") -> PredictionResult:
        calc = QimenCalculator(self.birth_info, question=question)
        result = calc.predict()
        self.results["qimen"] = result
        return result
    
    def predict_all(self, question: str = "") -> Dict[str, PredictionResult]:
        """运行所有预测系统"""
        self.predict_bazi()
        self.predict_ziwei()
        self.predict_western_astro()
        self.predict_tarot(question=question)
        self.predict_iching(question=question)
        self.predict_meihua(question=question)
        self.predict_qimen(question=question)
        return self.results
    
    def generate_comprehensive_report(self, question: str = "") -> str:
        """生成综合报告"""
        if not self.results:
            self.predict_all(question=question)
        
        b = self.birth_info
        lines = []
        
        lines.append("=" * 60)
        lines.append("✨ Mystical Prediction — 多维命运综合报告")
        lines.append("=" * 60)
        lines.append(f"被测者：{b.gender} | 出生：{b.year}年{b.month}月{b.day}日 {b.hour:02d}:{b.minute:02d}")
        lines.append(f"出生地：{b.place}")
        lines.append(f"报告生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}")
        lines.append("")
        
        system_order = [
            ("bazi", "📊 八字四柱"),
            ("ziwei", "🌟 紫微斗数"),
            ("western_astro", "♈ 西洋占星"),
            ("tarot", "🃏 塔罗牌"),
            ("iching", "☯️ 易经六十四卦"),
            ("meihua", "🌸 梅花易数"),
            ("qimen", "🧭 奇门遁甲"),
        ]
        
        for key, title in system_order:
            result = self.results.get(key)
            if result:
                lines.append(f"\n{'─' * 50}")
                lines.append(f"{title}")
                lines.append(f"可信度：{'★' * int(result.confidence * 5)}")
                lines.append("")
                lines.append(result.analysis)
                lines.append("")
                lines.append("【建议】")
                for i, suggestion in enumerate(result.suggestions, 1):
                    lines.append(f"  {i}. {suggestion}")
        
        lines.append(f"\n{'=' * 60}")
        lines.append("【综合结论】")
        lines.append(self._synthesize_conclusion())
        lines.append("")
        lines.append("⚠️ 免责声明：本报告仅供参考，不构成任何人生决策的唯一依据。")
        lines.append("=" * 60)
        
        return "\n".join(lines)
    
    def _synthesize_conclusion(self) -> str:
        """综合多系统结论"""
        conclusions = []
        
        if "bazi" in self.results:
            bazi = self.results["bazi"]
            conclusions.append(f"八字：{bazi.analysis[:50]}...")
        
        if "ziwei" in self.results:
            ziwei = self.results["ziwei"]
            conclusions.append(f"紫微：{ziwei.analysis[:50]}...")
        
        if conclusions:
            return "综合各预测体系，" + "；".join(conclusions[:2]) + "。多系统共同指向的方向，可信度更高。"
        
        return "请先运行 predict_all() 获取各系统预测结果。"
