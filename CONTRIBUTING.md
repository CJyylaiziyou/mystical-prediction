# 贡献指南 Contributing Guide

感谢你对 Mystical Prediction 项目的兴趣！

## 如何贡献

### 报告 Bug
- 在 Issues 页面提交 Bug 报告
- 请描述复现步骤、预期行为和实际行为

### 提交 Pull Request
1. Fork 本仓库
2. 创建你的特性分支：`git checkout -b feature/your-feature`
3. 提交你的修改：`git commit -m 'feat: add some feature'`
4. 推送到分支：`git push origin feature/your-feature`
5. 提交 Pull Request

### 知识库优化
- 知识库文件位于 `data/` 目录
- 直接编辑对应的 JSON 文件即可
- 请确保 JSON 格式正确

### 添加新预测系统
继承 `BaseDiviner` 类并实现以下方法：
- `_calculate()`: 核心计算逻辑
- `_map_meanings()`: 含义映射
- `_interpret()`: 生成解读文本
- `_generate_suggestions()`: 生成建议

## 代码规范
- 遵循 PEP 8 代码风格
- 所有公开方法必须有文档字符串
- 新功能需要配套测试

## 联系方式
- 提交 Issue 进行讨论
- GitHub: [@CJyylaiziyou](https://github.com/CJyylaiziyou)
