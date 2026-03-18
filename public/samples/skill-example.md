# Skill 示例

这是一个 Claude Code Skill 的示例文件。

## 文件位置

- 用户级：`~/.claude/skills/<skill-name>/SKILL.md`
- 项目级：`.claude/skills/<skill-name>/SKILL.md`

## 示例 Skill 文件

### 1. 代码审查 Skill

```yaml
---
name: code-review
description: 对代码变更进行全面审查。使用 /code-review 在提交前审查更改。
disable-model-invocation: true
---

对当前工作目录中的代码变更进行全面审查。

请检查以下方面：

1. **代码质量**
   - 代码是否清晰易懂？
   - 变量和函数命名是否恰当？
   - 是否遵循项目的编码规范？

2. **潜在问题**
   - 是否有明显的 bug？
   - 是否有性能问题？
   - 是否有安全风险？

3. **测试覆盖**
   - 新功能是否有对应的测试？
   - 测试是否充分？

4. **文档**
   - 公共 API 是否有适当的注释？
   - 复杂的逻辑是否有解释？

请按优先级列出发现的问题，并提供具体的改进建议。
```

### 2. 部署 Skill

```yaml
---
name: deploy
description: 执行部署流程。使用 /deploy [环境] 部署到指定环境。
---

部署流程：

1. **预部署检查**
   - 运行测试套件：`npm test`
   - 检查代码质量：`npm run lint`
   - 确认所有更改已提交

2. **构建**
   - 清理旧的构建文件
   - 运行构建：`npm run build`
   - 验证构建输出

3. **部署**
   - 根据环境变量确定目标环境
   - 执行部署命令
   - 验证部署成功

4. **后部署验证**
   - 检查关键功能是否正常
   - 监控错误日志

支持的环境：staging, production
```

### 3. API 文档 Skill

```yaml
---
name: api-docs
description: 生成 API 文档。使用 /api-docs 更新 API 文档。
---

生成项目的 API 文档：

1. 扫描 `src/api/` 目录中的所有路由文件
2. 提取接口定义和注释
3. 生成 OpenAPI/Swagger 规范
4. 更新 `docs/api.md` 文件

输出格式应包括：
- 端点 URL
- HTTP 方法
- 请求参数
- 响应格式
- 错误代码
- 示例请求/响应
```

### 4. 重构助手 Skill

```yaml
---
name: refactor
description: 帮助重构代码。使用 /refactor <文件路径> 开始重构。
---

帮助用户安全地重构代码：

1. **分析阶段**
   - 读取目标文件
   - 理解代码结构和依赖关系
   - 识别潜在风险

2. **规划阶段**
   - 与用户讨论重构策略
   - 制定详细的重构计划
   - 识别需要修改的相关文件

3. **执行阶段**
   - 按步骤执行重构
   - 每步完成后运行测试
   - 确保代码始终可工作

4. **验证阶段**
   - 运行完整测试套件
   - 检查代码质量
   - 确认功能完整性

始终遵循的原则：
- 小步快跑，频繁验证
- 保持代码可工作
- 添加必要的测试
```

## Skill Frontmatter 参考

| 字段 | 类型 | 说明 |
|------|------|------|
| `name` | string | Skill 名称，用于 `/command` |
| `description` | string | 描述，帮助 Claude 了解何时使用 |
| `disable-model-invocation` | boolean | 设为 true 时，只有用户能调用 |
| `skills` | array | 启动时预加载的其他 skill |
| `tools` | array | 限制可用的工具 |
| `model` | string | 指定使用的模型 |
