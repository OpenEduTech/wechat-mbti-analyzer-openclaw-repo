# WeChat MBTI Analyzer for OpenClaw

## 中文简介

`wechat-mbti-analyzer-openclaw-repo` 是一个面向 OpenClaw 的可复用工作流仓库，用于导出微信聊天记录，并将其整理为中文 MBTI 风格的人格分析、关系分析与团队协作报告。

它支持：

- 单聊人格分析
- 合伙人 / 工作搭档分析
- 家庭 / 亲密关系分析
- 群聊工作模式分析
- 时间切片聊天分析

## English Overview

`wechat-mbti-analyzer-openclaw-repo` is a reusable OpenClaw workflow for exporting WeChat chats and turning them into Chinese MBTI-style personality, relationship, and team-workflow reports.

It supports:

- one-to-one chat analysis
- founder or work-partner analysis
- family or intimate relationship analysis
- group workflow analysis
- time-sliced chat analysis

## 重要前置条件 / Important Prerequisite

这个仓库**不会自动为用户安装** `wechat-cli`。  
This repository does **not** install `wechat-cli` automatically for the user.

在使用本仓库任何脚本之前，用户必须先：
Before using any script in this repo, the user must first:

1. 安装 `wechat-cli` / install `wechat-cli`
2. 完成 `wechat-cli init` / initialize `wechat-cli`
3. 确认本地微信数据可访问 / make sure local WeChat data can be accessed

官方项目 / Official project:

- https://github.com/freestylefly/wechat-cli

## 安装前置 / Installation Prerequisites

### Windows

请确保：
Make sure the machine has:

- 已安装并登录微信 / WeChat installed and logged in
- 可用的 Python / Python available
- 已安装并可调用的 `wechat-cli` / `wechat-cli` installed and accessible

检查 `wechat-cli` 是否可用：
Check whether `wechat-cli` is available:

```powershell
wechat-cli --help
```

如果已经安装但不在 `PATH` 中，请使用完整路径。  
If `wechat-cli` is installed but not in `PATH`, use its full path.

安装完成后先初始化：
After installation, initialize it:

```powershell
wechat-cli init
```

### macOS

请确保：
Make sure the machine has:

- 已安装并登录微信 / WeChat installed and logged in
- 可用的 Python 3 / Python 3 available
- 已安装并可调用的 `wechat-cli` / `wechat-cli` installed and accessible

检查 `wechat-cli` 是否可用：
Check whether `wechat-cli` is available:

```bash
wechat-cli --help
```

初始化：
Initialize it:

```bash
wechat-cli init
```

## 运行本仓库前先验证 / Verify Before Running This Repo

建议先确认以下命令能正常运行：
Verify these commands work first:

```bash
wechat-cli sessions
```

或 / or:

```bash
wechat-cli contacts --query "<name>"
```

如果这些命令失败，本仓库工作流也会失败。  
If these commands fail, the workflow in this repo will also fail.

## 这个仓库做什么 / What This Repo Does

本仓库默认假设 `wechat-cli` 已经可以正常工作，然后在其上增加一层更高阶的分析流程：
This repo assumes `wechat-cli` is already working, then adds a higher-level workflow on top:

1. 导出目标聊天 / export the target chat
2. 生成聊天文本与元数据 / generate transcript artifacts and metadata
3. 生成正式报告模板 / generate a report template
4. 生成中文正式报告初稿 / generate a Chinese formal report draft
5. 提供适合 OpenClaw 的提示词与示例 / provide reusable prompts and examples for OpenClaw

## 跨平台入口 / Cross-Platform Entry Points

### Windows

生成报告初稿 / Draft report:

```powershell
python .\scripts\wechat_mbti_common.py draft --chat-name "<chat name>"
```

或 / or:

```cmd
.\scripts\generate_chinese_report_draft.cmd --chat-name "<chat name>"
```

### macOS

生成报告初稿 / Draft report:

```bash
python3 ./scripts/wechat_mbti_common.py draft --chat-name "<chat name>"
```

或 / or:

```bash
bash ./scripts/generate_chinese_report_draft.sh --chat-name "<chat name>"
```

## 命令变体 / Command Variants

仅导出 / Export only:

```bash
python3 ./scripts/wechat_mbti_common.py export --chat-name "<chat name>"
```

仅生成模板 / Template only:

```bash
python3 ./scripts/wechat_mbti_common.py template --chat-name "<chat name>"
```

生成报告初稿 / Draft report:

```bash
python3 ./scripts/wechat_mbti_common.py draft --chat-name "<chat name>"
```

时间切片 / Optional time slicing:

```bash
python3 ./scripts/wechat_mbti_common.py draft --chat-name "<chat name>" --start-time "2026-04-01" --end-time "2026-04-09 23:59:59"
```

## 推荐的 OpenClaw 任务描述 / Recommended OpenClaw Prompt

Use the workflow files in this repository to export the WeChat chat "<chat name>" and generate a Chinese MBTI and collaboration report draft. First export the transcript, then inspect speaker patterns, then write a formal Chinese report. Keep MBTI as a behavior-based inference, not a diagnosis.

## 输出文件 / Output Files

一次成功运行通常会生成：
A successful run typically generates:

- `all-messages.txt`
- `metadata.json`
- `mbti-analysis-prompt.md`
- `formal-report-template.md`
- `formal-report-draft.md`

## 仓库主要文件 / Repository Files

- `SYSTEM_PROMPT.md`
  OpenClaw system prompt

- `TASK_TEMPLATES.md`
  reusable OpenClaw task templates

- `examples/`
  ready-to-paste OpenClaw task examples

- `scripts/`
  export and report-generation scripts

- `references/`
  report structure references

## 示例任务 / Examples

可直接复制的 OpenClaw 任务示例在 `examples/`：
Ready-to-paste OpenClaw task examples are in `examples/`:

- `examples/single-chat-mbti.txt`
- `examples/founder-collaboration-report.txt`
- `examples/family-relationship-report.txt`
- `examples/group-workflow-report.txt`
- `examples/time-sliced-report.txt`

## 说明 / Notes

- 本仓库中的 MBTI 属于基于行为模式的推断，不是正式心理测评。
- 工作聊天往往会放大角色行为。
- 家庭或亲密关系聊天可能会放大短期压力状态。
- 群聊分析应先看工作模式和角色分工，再看 MBTI。

- MBTI in this repo is a behavior-based inference, not a formal diagnosis.
- Work chats may overrepresent role behavior.
- Family or intimate chats may overrepresent temporary stress.
- Group chats should be analyzed for workflow and role split before typing members.
