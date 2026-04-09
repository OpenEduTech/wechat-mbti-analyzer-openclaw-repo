# WeChat MBTI Analyzer for OpenClaw

`wechat-mbti-analyzer-openclaw-repo` is a reusable OpenClaw workflow for exporting WeChat chats and turning them into Chinese MBTI-style personality, relationship, and team-workflow reports.

It supports:

- one-to-one chat analysis
- founder or work-partner analysis
- family or intimate relationship analysis
- group workflow analysis
- time-sliced chat analysis

## Important Prerequisite

This repository does **not** install `wechat-cli` for the user automatically.

Before using any script in this repo, the user must first:

1. install `wechat-cli`
2. initialize `wechat-cli`
3. make sure local WeChat data can be accessed

Official project:

- https://github.com/freestylefly/wechat-cli

## Installation Prerequisites

### Windows

Make sure the machine has:

- WeChat installed and logged in
- Python available
- `wechat-cli` installed and accessible

Check whether `wechat-cli` is available:

```powershell
wechat-cli --help
```

If `wechat-cli` is installed but not in `PATH`, use its full path.

After installation, initialize it:

```powershell
wechat-cli init
```

### macOS

Make sure the machine has:

- WeChat installed and logged in
- Python 3 available
- `wechat-cli` installed and accessible

Check whether `wechat-cli` is available:

```bash
wechat-cli --help
```

Initialize it:

```bash
wechat-cli init
```

## Before Running This Repo

The user should verify these commands work first:

```bash
wechat-cli sessions
```

or:

```bash
wechat-cli contacts --query "<name>"
```

If these fail, the workflow in this repo will also fail.

## What This Repo Does

This repo assumes `wechat-cli` is already working, then adds a higher-level workflow on top:

1. export the target chat
2. generate transcript artifacts
3. generate a report template
4. generate a Chinese formal report draft
5. provide reusable prompts and examples for OpenClaw

## Cross-Platform Entry Points

### Windows

Draft report:

```powershell
python .\scripts\wechat_mbti_common.py draft --chat-name "<chat name>"
```

or:

```cmd
.\scripts\generate_chinese_report_draft.cmd --chat-name "<chat name>"
```

### macOS

Draft report:

```bash
python3 ./scripts/wechat_mbti_common.py draft --chat-name "<chat name>"
```

or:

```bash
bash ./scripts/generate_chinese_report_draft.sh --chat-name "<chat name>"
```

## Command Variants

Export only:

```bash
python3 ./scripts/wechat_mbti_common.py export --chat-name "<chat name>"
```

Template only:

```bash
python3 ./scripts/wechat_mbti_common.py template --chat-name "<chat name>"
```

Draft report:

```bash
python3 ./scripts/wechat_mbti_common.py draft --chat-name "<chat name>"
```

Optional time slicing:

```bash
python3 ./scripts/wechat_mbti_common.py draft --chat-name "<chat name>" --start-time "2026-04-01" --end-time "2026-04-09 23:59:59"
```

## Recommended OpenClaw Prompt

Use the workflow files in this repository to export the WeChat chat "<chat name>" and generate a Chinese MBTI and collaboration report draft. First export the transcript, then inspect speaker patterns, then write a formal Chinese report. Keep MBTI as a behavior-based inference, not a diagnosis.

## Output Files

A successful run typically generates:

- `all-messages.txt`
- `metadata.json`
- `mbti-analysis-prompt.md`
- `formal-report-template.md`
- `formal-report-draft.md`

## Repository Files

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

## Examples

Ready-to-paste OpenClaw task examples are in `examples/`:

- `examples/single-chat-mbti.txt`
- `examples/founder-collaboration-report.txt`
- `examples/family-relationship-report.txt`
- `examples/group-workflow-report.txt`
- `examples/time-sliced-report.txt`

## Notes

- MBTI in this repo is a behavior-based inference, not a formal diagnosis.
- Work chats may overrepresent role behavior.
- Family or intimate chats may overrepresent temporary stress.
- Group chats should be analyzed for workflow and role split before typing members.
