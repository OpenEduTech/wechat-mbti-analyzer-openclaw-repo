---
name: wechat-mbti-analyzer
description: Export WeChat personal or group chats with wechat-cli, organize transcript artifacts, and write Chinese MBTI-style personality, collaboration, and team-workflow reports. Use when Codex or another local agent needs to analyze WeChat conversations, compare interpersonal styles, infer likely MBTI tendencies from chat behavior, summarize team working patterns, or produce formal Chinese reports for one person, two people, or a small work group.
---

# WeChat MBTI Analyzer

## Overview

Use this skill to turn local WeChat chats into reusable analysis artifacts and formal Chinese reports.

This skill is best for:

- one-to-one personality and interaction analysis
- founder or cofounder collaboration analysis
- small-group workflow analysis
- side-by-side role comparison across multiple chats

Do not present MBTI as a clinical truth. Frame it as a behavior-based inference from chat records.

## Workflow

### 1. Confirm the chat target

Use `wechat-cli contacts --query "<name>"` when the exact chat name is uncertain.

For groups, prefer the exact group name from `wechat-cli sessions`.

If a contact nickname does not match the actual chat object, switch to the real chat name before exporting.

### 2. Export the full chat

On Windows, you can use the bundled PowerShell script:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\export_chat.ps1 -ChatName "<chat name>"
```

For cross-platform use in OpenClaw or plain terminals, prefer the Python entry point:

```bash
python3 ./scripts/wechat_mbti_common.py export --chat-name "<chat name>"
```

On Windows:

```powershell
python .\scripts\wechat_mbti_common.py export --chat-name "<chat name>"
```

The export step writes:

- merged transcript text
- paged raw JSON
- metadata
- a reusable MBTI analysis prompt

### 3. Generate a formal report template in one step

PowerShell:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\generate_report_template.ps1 -ChatName "<chat name>"
```

Cross-platform:

```bash
python3 ./scripts/wechat_mbti_common.py template --chat-name "<chat name>"
```

This wrapper:

- exports the chat when needed
- detects whether the target is closer to a one-to-one chat or a group chat
- computes lightweight speaker statistics
- writes a formal Chinese report template skeleton

### 4. Generate a Chinese formal draft in one step

PowerShell:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\generate_chinese_report_draft.ps1 -ChatName "<chat name>"
```

Cross-platform:

```bash
python3 ./scripts/wechat_mbti_common.py draft --chat-name "<chat name>"
```

Optional time slicing:

```bash
python3 ./scripts/wechat_mbti_common.py draft --chat-name "<chat name>" --start-time "2026-01-01" --end-time "2026-04-09 23:59:59"
```

This wrapper:

- exports the chat when needed
- creates the formal report template
- detects whether the chat is closer to a one-to-one chat or a group chat
- writes `formal-report-draft.md` as a Chinese first draft with sample stats and sections already filled
- leaves only the final MBTI type calls and evidence polishing for refinement

### 5. Inspect speaker structure before inferring type

For one-to-one chats, quickly check:

- message volume by speaker
- recurring topics
- how each person reacts under stress
- who initiates, who filters, who reassures, who pushes

For groups, quickly check:

- top speakers by volume
- who defines goals
- who translates goals into execution
- who provides external signals
- who mostly implements

Do not infer type from one isolated message. Look for repeated patterns.

### 6. Write the report in Chinese

Default report sections:

1. Analysis scope and caveats
2. Executive summary
3. Personality reading for each subject
4. Dimension-by-dimension MBTI reasoning
5. Interaction or workflow pattern
6. Risks and blind spots
7. Practical recommendations

Use the report patterns in `references/report-patterns.md`.

### 7. Match report style to chat type

Use these defaults:

- personal contact: emphasize personality, communication style, and relationship dynamics
- founder or work partner: emphasize decision style, conflict pattern, complementarity, and role boundaries
- work group: emphasize operating model, implicit hierarchy, role split, bottlenecks, and team risks

### 8. State uncertainty clearly

Always mention that:

- MBTI is an inference, not a diagnosis
- work chat may overrepresent role behavior
- intimate chat may overrepresent stress and family context
- group chat may underrepresent private reasoning

## Heuristics

### Likely ENTJ signals

- repeatedly sets goals, cadence, or milestones
- pushes responsibility and output ownership
- reframes single problems as system or strategy problems
- becomes more controlling and structured under pressure

### Likely INTJ signals

- compressed wording with high judgment density
- filters options quickly
- emphasizes strategic fit and selectivity
- contributes fewer messages but often higher-level directional ones

### Likely ESTJ signals

- strong focus on process, versions, rules, format, deadlines, and external correctness
- turns discussion into documents, tasks, or operational closure
- highly sensitive to execution hygiene and realism

### Likely ESFJ signals

- recurring care reminders, coordination, relational maintenance, and practical support
- values respect, companionship, and visible mutual responsibility
- stabilizes people and daily life more than abstract strategy

### Likely ENTP signals

- jumps across product, technology, pricing, and positioning with ease
- tests alternatives quickly
- often reframes the same issue from multiple angles
- strong idea-bridge role between technical and business language

### Likely ISTP signals

- talks less, does more
- provides concrete fixes, tests, versions, and implementation notes
- rarely drives the whole room but often resolves local obstacles

## Output Rules

- Write final reports in Chinese unless the user asks otherwise.
- Use concrete evidence lines from the transcript when available.
- Prefer phrases like `更像` and `更接近于` over absolute claims.
- Separate `work-mode personality` from `relationship-mode personality` when needed.
- For group analysis, focus first on working model and roles, then on MBTI.

## Resources

- Use `scripts/wechat_mbti_common.py` for the cross-platform OpenClaw workflow.
- Use `scripts/export_chat.ps1` for the Windows PowerShell export workflow.
- Use `scripts/generate_report_template.ps1` when the user wants a one-click report skeleton on Windows.
- Use `scripts/generate_chinese_report_draft.ps1` when the user wants a one-click Chinese first draft on Windows.
- Use `OPENCLAW.md` when packaging this workflow for OpenClaw.
- Use `references/report-patterns.md` for report structure and wording patterns.
