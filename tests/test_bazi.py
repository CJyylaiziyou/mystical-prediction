"""
八字四柱系统基础测试
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.core import BirthInfo
from src.bazi import BaziCalculator


def test_bazi_basic():
    """测试基础八字计算"""
    birth = BirthInfo(year=1990, month=3, day=18, hour=14, minute=30, gender="女")
    calc = BaziCalculator(birth)
    result = calc.predict()
    assert result is not None
    assert result.analysis != ""
    print("✅ 基础八字计算测试通过")


def test_bazi_year_pillar():
    """测试年柱计算"""
    birth = BirthInfo(year=1989, month=4, day=3, hour=2, minute=52, gender="女")
    calc = BaziCalculator(birth)
    result = calc.predict()
    assert "己" in result.key_info.get("year_pillar", "")
    print("✅ 年柱计算测试通过")


if __name__ == "__main__":
    test_bazi_basic()
    test_bazi_year_pillar()
    print("\n所有测试通过！")
