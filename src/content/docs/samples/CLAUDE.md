# 项目 CLAUDE.md 示例

这是一个 CLAUDE.md 文件示例，展示了如何为项目配置 Claude Code 的持久上下文。

## 项目概述

这是一个 [技术栈] 项目，使用 [主要框架/库]。

## 编码规范

### 代码风格
- 使用 2 个空格缩进
- 使用单引号而非双引号
- 最大行长度 100 字符

### 命名约定
- 文件：kebab-case（如 `my-component.ts`）
- 类：PascalCase（如 `MyClass`）
- 函数/变量：camelCase（如 `myFunction`）
- 常量：UPPER_SNAKE_CASE（如 `MAX_COUNT`）

## 常用命令

### 开发
```bash
# 启动开发服务器
npm run dev

# 运行测试
npm test

# 构建项目
npm run build

# 运行 lint
npm run lint
```

### 数据库
```bash
# 迁移数据库
npm run db:migrate

# 重置数据库
npm run db:reset
```

## 项目结构

```
src/
├── components/    # UI 组件
├── lib/          # 工具函数
├── hooks/        # React hooks
├── types/        # TypeScript 类型
└── api/          # API 路由
```

## 重要规则

1. **提交前必须运行测试**：`npm test`
2. **不要提交 .env 文件**：确保敏感信息不会被泄露
3. **使用类型安全**：所有新代码必须使用 TypeScript
4. **遵循已有模式**：在添加新功能时，参考现有代码的风格

## 依赖管理

- 使用 `npm` 而非 `yarn`
- 添加新依赖前需要团队讨论
- 优先使用已经存在的依赖

## 测试策略

- 单元测试：`*.test.ts` 文件
- 集成测试：`*.spec.ts` 文件
- 测试覆盖率目标：80%

## Git 工作流

1. 从 `main` 分支创建功能分支
2. 提交前运行 `npm test` 和 `npm run lint`
3. 使用描述性的提交信息
4. 通过 Pull Request 合并代码
5. 需要至少 1 个代码审查

---

## 可以导入的其他文件

你可以使用 `@` 语法导入其他文件：
- @README.md
- @docs/architecture.md
- @docs/api-guide.md
