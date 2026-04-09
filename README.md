# ChatMessage MBTI Analyzer for OpenClaw

## 中文版

### 项目简介

`chatmessage-mbti-analyzer-openclaw-repo` 是一个面向 OpenClaw 的可复用工作流仓库，用于导出和分析聊天消息，并将其整理为中文 MBTI 风格的人格分析、关系分析与团队协作报告。

当前支持的数据来源：

- 微信聊天记录
- 飞书单聊与群聊消息

适用场景包括：

- 单聊人格分析
- 合伙人 / 工作搭档分析
- 家庭 / 亲密关系分析
- 群聊工作模式分析
- 时间切片聊天分析
- 多消息源的协作关系分析

### 重要前置条件

这个仓库不会自动帮用户安装消息导出 CLI。

在使用本仓库之前，请先按数据来源准备对应工具：

1. 如果分析微信聊天，请先安装并初始化 `wechat-cli`
2. 如果分析飞书聊天，请先安装并登录 `lark-cli`
3. 确认本地或账号侧已经具备访问聊天数据的权限

相关项目：

- 微信 CLI: https://github.com/freestylefly/wechat-cli
- 飞书 / Lark CLI: 请参考飞书开放平台或 Lark CLI 官方安装说明

### 微信使用前置

#### Windows

请确保：

- 已安装并登录微信
- 可用的 Python
- 已安装并可调用的 `wechat-cli`

检查：

```powershell
wechat-cli --help
wechat-cli init
wechat-cli sessions
```

#### macOS

请确保：

- 已安装并登录微信
- 可用的 Python 3
- 已安装并可调用的 `wechat-cli`

检查：

```bash
wechat-cli --help
wechat-cli init
wechat-cli sessions
```

### 飞书使用前置

请确保：

- 已安装并登录 `lark-cli`
- 已完成 CLI 初始化
- 当前账号具备访问飞书消息接口的权限

检查：

```bash
lark-cli auth status
```

如需直接访问消息接口，可再验证：

```bash
lark-cli api GET /open-apis/im/v1/chats
```

### 这个仓库做什么

本仓库在消息导出 CLI 之上增加了一层更高阶的分析流程：

1. 导出目标聊天或群聊
2. 生成统一的聊天文本与元数据
3. 生成正式报告模板
4. 生成中文正式报告初稿
5. 提供适合 OpenClaw 的系统提示词、任务模板和示例
6. 可选地通过飞书 CLI 把报告发布到飞书文档或发送通知

### 微信流水线

生成微信报告初稿：

```bash
python3 ./scripts/wechat_mbti_common.py draft --chat-name "<chat name>"
```

Windows:

```powershell
python .\scripts\wechat_mbti_common.py draft --chat-name "<chat name>"
```

### 飞书流水线

生成飞书聊天报告初稿：

```bash
python3 ./scripts/feishu_chat_pipeline.py draft --chat-id "<chat-id>" --chat-name "<chat name>"
```

如果明确是群聊：

```bash
python3 ./scripts/feishu_chat_pipeline.py draft --chat-id "<chat-id>" --chat-name "<group name>" --chat-type group
```

Windows:

```powershell
python .\scripts\feishu_chat_pipeline.py draft --chat-id "<chat-id>" --chat-name "<chat name>"
```

### 飞书发布能力

本仓库还支持把生成好的 Markdown 报告发布到飞书文档，或者向飞书聊天发送通知。

发布文档：

```bash
python3 ./scripts/publish_to_feishu.py doc --file ./exports/wechat-mbti/<run>/formal-report-draft.md --title "MBTI Report"
```

发送通知：

```bash
python3 ./scripts/publish_to_feishu.py notify --chat-id "<chat-id>" --text "The MBTI report has been generated."
```

### 输出文件

一次成功运行通常会生成：

- `all-messages.txt`
- `metadata.json`
- `mbti-analysis-prompt.md`
- `formal-report-template.md`
- `formal-report-draft.md`

### 仓库主要文件

- `SYSTEM_PROMPT.md`
  OpenClaw 系统提示词

- `TASK_TEMPLATES.md`
  可复用的 OpenClaw 任务模板

- `examples/`
  可直接复制的 OpenClaw 任务示例

- `scripts/`
  导出、分析、发布脚本

- `references/`
  报告结构参考资料

- `FEISHU_CLI.md`
  飞书 CLI 接入说明

### 说明

- 本仓库中的 MBTI 属于基于行为模式的推断，不是正式心理测评。
- 工作聊天往往会放大角色行为。
- 家庭或亲密关系聊天可能会放大短期压力状态。
- 群聊分析应先看工作模式和角色分工，再看 MBTI。
- 不同消息源的数据结构不同，但最终会统一整理为可分析文本。

---

## English

### Overview

`chatmessage-mbti-analyzer-openclaw-repo` is a reusable OpenClaw workflow for exporting and analyzing chat messages, then turning them into Chinese MBTI-style personality, relationship, and team-workflow reports.

Currently supported message sources:

- WeChat chat history
- Feishu / Lark direct chats and group chats

Typical use cases:

- one-to-one personality analysis
- founder or work-partner analysis
- family or intimate relationship analysis
- group workflow analysis
- time-sliced chat analysis
- multi-source collaboration analysis

### Important Prerequisite

This repository does not automatically install the source CLI tools.

Before using this repo, prepare the source-specific CLI first:

1. install and initialize `wechat-cli` for WeChat analysis
2. install and log in to `lark-cli` for Feishu analysis
3. make sure the current device or account can access the target chat data

Related projects:

- WeChat CLI: https://github.com/freestylefly/wechat-cli
- Feishu / Lark CLI: follow the official Feishu or Lark CLI installation guide

### WeChat Prerequisites

#### Windows

Make sure the machine has:

- WeChat installed and logged in
- Python available
- `wechat-cli` installed and accessible

Check:

```powershell
wechat-cli --help
wechat-cli init
wechat-cli sessions
```

#### macOS

Make sure the machine has:

- WeChat installed and logged in
- Python 3 available
- `wechat-cli` installed and accessible

Check:

```bash
wechat-cli --help
wechat-cli init
wechat-cli sessions
```

### Feishu Prerequisites

Make sure the machine has:

- `lark-cli` installed and logged in
- CLI initialization completed
- account permissions for Feishu message APIs

Check:

```bash
lark-cli auth status
```

Optional API verification:

```bash
lark-cli api GET /open-apis/im/v1/chats
```

### What This Repo Does

This repository adds a higher-level analysis workflow on top of message export CLIs:

1. export the target chat or group
2. generate normalized transcript text and metadata
3. generate a formal report template
4. generate a Chinese formal report draft
5. provide OpenClaw system prompts, task templates, and examples
6. optionally publish the final report back to Feishu Docs or send Feishu notifications

### WeChat Pipeline

Generate a WeChat report draft:

```bash
python3 ./scripts/wechat_mbti_common.py draft --chat-name "<chat name>"
```

Windows:

```powershell
python .\scripts\wechat_mbti_common.py draft --chat-name "<chat name>"
```

### Feishu Pipeline

Generate a Feishu chat report draft:

```bash
python3 ./scripts/feishu_chat_pipeline.py draft --chat-id "<chat-id>" --chat-name "<chat name>"
```

If the target is definitely a group:

```bash
python3 ./scripts/feishu_chat_pipeline.py draft --chat-id "<chat-id>" --chat-name "<group name>" --chat-type group
```

Windows:

```powershell
python .\scripts\feishu_chat_pipeline.py draft --chat-id "<chat-id>" --chat-name "<chat name>"
```

### Feishu Delivery Workflow

This repo can also publish generated Markdown reports to Feishu Docs or send Feishu notifications.

Publish a document:

```bash
python3 ./scripts/publish_to_feishu.py doc --file ./exports/wechat-mbti/<run>/formal-report-draft.md --title "MBTI Report"
```

Send a notification:

```bash
python3 ./scripts/publish_to_feishu.py notify --chat-id "<chat-id>" --text "The MBTI report has been generated."
```

### Output Files

A successful run typically generates:

- `all-messages.txt`
- `metadata.json`
- `mbti-analysis-prompt.md`
- `formal-report-template.md`
- `formal-report-draft.md`

### Repository Files

- `SYSTEM_PROMPT.md`
  OpenClaw system prompt

- `TASK_TEMPLATES.md`
  reusable OpenClaw task templates

- `examples/`
  ready-to-paste OpenClaw task examples

- `scripts/`
  export, analysis, and delivery scripts

- `references/`
  report structure references

- `FEISHU_CLI.md`
  Feishu CLI integration notes

### Notes

- MBTI in this repo is a behavior-based inference, not a formal diagnosis.
- Work chats may overrepresent role behavior.
- Family or intimate chats may overrepresent temporary stress.
- Group chats should be analyzed for workflow and role split before typing members.
- Different message sources have different schemas, but this repo normalizes them into a shared analysis format.
