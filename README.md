# WeChat MBTI Analyzer for OpenClaw

Use this folder as an OpenClaw reusable workflow for:

- exporting WeChat personal chats
- exporting WeChat group chats
- generating Chinese MBTI-style report templates
- generating Chinese formal report drafts

## What OpenClaw Should Do

1. Confirm the exact chat target with `wechat-cli contacts --query "<name>"` or `wechat-cli sessions`.
2. Export the full transcript.
3. Read `all-messages.txt` and `metadata.json`.
4. Infer likely MBTI tendencies as behavior-based guesses, not formal diagnosis.
5. Write the final report in Chinese.

## Cross-Platform Entry Points

### Windows

```powershell
python .\scripts\wechat_mbti_common.py draft --chat-name "<chat name>"
```

or:

```cmd
.\scripts\generate_chinese_report_draft.cmd --chat-name "<chat name>"
```

### macOS

```bash
python3 ./scripts/wechat_mbti_common.py draft --chat-name "<chat name>"
```

or:

```bash
bash ./scripts/generate_chinese_report_draft.sh --chat-name "<chat name>"
```

## Recommended OpenClaw Prompt

Use this workflow folder to export the WeChat chat "<chat name>" and generate a Chinese MBTI and collaboration report draft. First export the transcript, then inspect speaker patterns, then write a formal Chinese report. Keep MBTI as a behavior-based inference, not a diagnosis.

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

## Output Files

- `all-messages.txt`
- `metadata.json`
- `mbti-analysis-prompt.md`
- `formal-report-template.md`
- `formal-report-draft.md`

## Examples

Ready-to-paste OpenClaw task examples are in `examples/`:

- `examples/single-chat-mbti.txt`
- `examples/founder-collaboration-report.txt`
- `examples/family-relationship-report.txt`
- `examples/group-workflow-report.txt`
- `examples/time-sliced-report.txt`
