"""
Mystical Prediction 完整使用示例
演示如何使用各个预测系统
"""

from src.core import BirthInfo
from src.bazi import BaziCalculator
# from src.ziwei import ZiweiCalculator
# from src.iching import IChingCalculator
# from src.engine import SageDivination


def example_bazi():
    """八字四柱预测示例"""
    print("=" * 60)
    print("八字四柱预测示例")
    print("=" * 60)
    
    # 创建出生信息
    birth_info = BirthInfo(
        year=1990,
        month=3,
        day=18,
        hour=14,
        minute=30,
        place="湖南岳阳",
        gender="女"
    )
    
    print(f"\n出生信息: {birth_info}\n")
    
    # 执行预测
    bazi = BaziCalculator(birth_info)
    result = bazi.predict()
    
    # 输出结果
    print(f"系统: {result.system_name_cn}")
    print(f"可信度: {'★' * int(result.confidence * 5)}{'☆' * (5 - int(result.confidence * 5))}")
    print(f"标签: {', '.join(result.tags)}")
    print(f"\n【核心数据】")
    print(f"日干: {result.key_info.get('day_master')}")
    print(f"五行配置: {result.key_info.get('five_elements')}")
    print(f"五行平衡度: {result.key_info.get('balance_status')}")
    
    print(f"\n【深度解读】")
    print(result.analysis)
    
    print(f"\n【建议】")
    for i, suggestion in enumerate(result.suggestions, 1):
        print(f"{i}. {suggestion}")
    
    print("\n" + "=" * 60)


def example_json_export():
    """导出为JSON示例"""
    print("=" * 60)
    print("JSON导出示例")
    print("=" * 60)
    
    birth_info = BirthInfo(1990, 3, 18, 14, 30, "湖南岳阳", "女")
    bazi = BaziCalculator(birth_info)
    result = bazi.predict()
    
    json_data = result.to_json()
    print(json_data)
    
    print("\n" + "=" * 60)


def example_batch_prediction():
    """批量预测示例"""
    print("=" * 60)
    print("批量预测示例")
    print("=" * 60)
    
    # 定义多个出生信息
    birth_infos = [
        BirthInfo(1990, 3, 18, 14, 30, "湖南岳阳", "女"),
        BirthInfo(1988, 5, 12, 9, 15, "深圳", "男"),
        BirthInfo(1992, 10, 25, 16, 45, "北京", "女"),
    ]
    
    results = []
    for birth_info in birth_infos:
        print(f"\n预测: {birth_info}")
        bazi = BaziCalculator(birth_info)
        result = bazi.predict()
        results.append(result)
        
        print(f"  日干: {result.key_info.get('day_master')}")
        print(f"  五行平衡: {result.key_info.get('balance_status')}")
        print(f"  可信度: {result.confidence:.2%}")
    
    print("\n" + "=" * 60)
    return results


def example_comprehensive_report():
    """综合报告示例（当实现了多个系统后）"""
    print("=" * 60)
    print("综合预测报告示例")
    print("=" * 60)
    
    birth_info = BirthInfo(1990, 3, 18, 14, 30, "湖南岳阳", "女")
    
    # 当实现了完整的SageDivination时，可以这样使用：
    # sage = SageDivination(birth_info)
    # results = sage.predict_all()
    # report = sage.generate_comprehensive_report()
    # print(report)
    
    # 目前先演示单系统
    bazi = BaziCalculator(birth_info)
    result = bazi.predict()
    
    report = f"""
╔══════════════════════════════════════════╗
║     {birth_info.place}的七维预测报告      ║
╚══════════════════════════════════════════╝

👤 出生信息
├─ 时间: {birth_info.year}年{birth_info.month}月{birth_info.day}日 {birth_info.hour}:{birth_info.minute:02d}
├─ 地点: {birth_info.place}
└─ 性别: {birth_info.gender}

📊 八字四柱分析
├─ 日干: {result.key_info.get('day_master')}
├─ 五行平衡: {result.key_info.get('balance_status')}
├─ 可信度: {'★' * int(result.confidence * 5)}{'☆' * (5 - int(result.confidence * 5))}
└─ 标签: {', '.join(result.tags)}

📖 深度解读
{result.analysis}

💡 建议
"""
    
    for i, suggestion in enumerate(result.suggestions, 1):
        report += f"({i}) {suggestion}\n"
    
    report += f"""
═══════════════════════════════════════════

⚖️ 免责声明
本报告仅供参考，最终决策权在用户自己手中。
传统预测系统具有主观性，请理性对待预测结果。
"""
    
    print(report)


def example_direct_usage():
    """最简单的直接使用方式"""
    print("=" * 60)
    print("最简单的直接使用示例")
    print("=" * 60)
    
    # 一行代码创建出生信息
    birth = BirthInfo(1990, 3, 18, 14, 30)
    
    # 一行代码执行预测
    result = BaziCalculator(birth).predict()
    
    # 直接获取结果
    print(result.analysis)


if __name__ == "__main__":
    # 运行所有示例
    
    # 1. 最简单的示例
    print("\n")
    example_direct_usage()
    
    # 2. 八字详细示例
    print("\n")
    example_bazi()
    
    # 3. JSON导出
    print("\n")
    example_json_export()
    
    # 4. 批量预测
    print("\n")
    example_batch_prediction()
    
    # 5. 综合报告
    print("\n")
    example_comprehensive_report()