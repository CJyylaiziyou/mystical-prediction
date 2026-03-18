"""
Mystical Prediction — 宗师级多维预测引擎 v1.0
集成7大传统预测智慧体系
"""

__version__ = "1.0.0"
__author__ = "CJyylaiziyou"

from src.core import BirthInfo, PredictionResult, Element
from src.bazi import BaziCalculator
from src.ziwei import ZiweiCalculator
from src.western_astro import WesternAstroCalculator
from src.tarot import TarotReader
from src.iching import IChingCalculator
from src.meihua import MeihuaCalculator
from src.qimen import QimenCalculator
from src.engine import SageDivination

__all__ = [
    "BirthInfo", "PredictionResult", "Element",
    "BaziCalculator", "ZiweiCalculator", "WesternAstroCalculator",
    "TarotReader", "IChingCalculator", "MeihuaCalculator",
    "QimenCalculator", "SageDivination",
]
