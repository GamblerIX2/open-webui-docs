---
sidebar_position: 10
title: "代码审查"
---

# 🔍 自动化代码审查

让 AI 审查 pull request、分支差异或文件，获得详细的代码审查报告——包括安全漏洞、性能问题、风格违调和改进建议。

> **你：** $Code Reviewer <br/>
> 审查 `feature/auth-refactor` 分支相对于 `main` 的变更。

## AI 的工作流程

1. 运行 `git diff main..feature/auth-refactor` 查看所有变更
2. 在完整上下文中读取每个修改的文件（不仅仅是 diff——它理解周围代码）
3. 对发现进行分类：安全、性能、正确性、风格、文档
4. 按优先级排列问题：严重到小细节
5. 提出带代码片段的具体修复建议
6. 保存结构化审查报告

{/* TODO: Screenshot — Chat showing the AI reviewing a branch diff. The response lists findings organized by severity: "🔴 Critical: SQL injection in user_query() — use parameterized queries. 🟡 Warning: N+1 query in get_orders(). 🔵 Suggestion: Extract validation logic into a helper." */}

{/* TODO: Screenshot — The generated review report in the file browser: a markdown file with sections for each file reviewed, findings with line numbers, and suggested fixes with code blocks. */}

## 技能内容

将下面的内容复制到**工作区 → 技能 → 创建**：

```markdown
---
name: code-reviewer
description: Reviews code changes for security, performance, correctness, and style issues
---

## Code Review

When asked to review code:

1. **Get the diff**: Use `git diff`, `git log`, or read the specified files to understand what changed
2. **Read full context**: Don't just look at changed lines — read the entire file to understand the surrounding logic, imports, and how the changes fit in
3. **Check for these categories**:
   - **Security**: SQL injection, XSS, hardcoded credentials, missing auth checks, unsafe deserialization, path traversal
   - **Correctness**: Logic errors, off-by-one bugs, unhandled edge cases, race conditions, missing error handling
   - **Performance**: N+1 queries, unnecessary loops, missing indexes, large memory allocations, blocking calls in async code
   - **Style & maintainability**: Inconsistent naming, overly complex functions, missing docstrings, dead code, magic numbers
   - **Testing**: Missing test coverage for new code paths, edge cases not tested
4. **Prioritize findings**:
   - 🔴 Critical: Must fix before merge (security, data loss, crashes)
   - 🟡 Warning: Should fix (performance, correctness edge cases)
   - 🔵 Suggestion: Nice to have (style, refactoring opportunities)
   - 💬 Nitpick: Optional (naming preferences, formatting)
5. **For each finding**:
   - Cite the exact file and line number
   - Explain WHY it's a problem (not just what's wrong)
   - Provide a concrete fix with a code snippet
6. **Write a summary**: Overall assessment, number of findings by severity, recommendation (approve / request changes)

Be thorough but fair. Acknowledge good patterns and well-written code, not just problems.
```
