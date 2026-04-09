# Feishu CLI Integration

This repository can optionally integrate with Feishu / Lark CLI as a delivery layer.

Current Feishu integration in this repo is designed for:

- exporting Feishu chat or group message history for analysis
- publishing generated markdown reports to Feishu Docs
- sending a follow-up notification message to a Feishu chat

It now supports two roles:

1. using `wechat-cli` as the WeChat export source
2. using `lark-cli` as the Feishu chat export source

## Install Feishu CLI

Please follow the official Feishu / Lark CLI installation guide first.

Typical flow:

```bash
npm install -g @larksuite/cli
```

Then initialize and log in:

```bash
lark-cli config init
lark-cli auth login --recommend
```

Check status:

```bash
lark-cli auth status
```

If you want to export Feishu chat history, also verify raw API access works:

```bash
lark-cli api GET /open-apis/im/v1/chats
```

## Export Feishu Chat History and Generate a Report

Use the dedicated Feishu pipeline:

```bash
python3 ./scripts/feishu_chat_pipeline.py draft --chat-id "<chat-id>" --chat-name "<chat name>"
```

Windows:

```powershell
python .\scripts\feishu_chat_pipeline.py draft --chat-id "<chat-id>" --chat-name "<chat name>"
```

If the target is a group, you can force group mode:

```bash
python3 ./scripts/feishu_chat_pipeline.py draft --chat-id "<chat-id>" --chat-name "<group name>" --chat-type group
```

Export only:

```bash
python3 ./scripts/feishu_chat_pipeline.py export --chat-id "<chat-id>" --chat-name "<chat name>"
```

Template only:

```bash
python3 ./scripts/feishu_chat_pipeline.py template --chat-id "<chat-id>" --chat-name "<chat name>" --skip-export
```

## Publish a Report to Feishu Docs

```bash
python3 ./scripts/publish_to_feishu.py doc --file ./exports/wechat-mbti/<run>/formal-report-draft.md --title "MBTI Report"
```

Windows:

```powershell
python .\scripts\publish_to_feishu.py doc --file .\exports\wechat-mbti\<run>\formal-report-draft.md --title "MBTI Report"
```

## Send a Notification Message

```bash
python3 ./scripts/publish_to_feishu.py notify --chat-id "<chat-id>" --text "The MBTI report has been generated and published."
```

## Recommended Usage Pattern

### WeChat source mode

1. Use `wechat-cli` to export the WeChat chat.
2. Use this repo to generate `formal-report-draft.md`.
3. Use `publish_to_feishu.py doc` to publish the report into Feishu Docs.
4. Optionally use `publish_to_feishu.py notify` to send the document link or summary into a Feishu chat.

### Feishu source mode

1. Use `feishu_chat_pipeline.py` with `lark-cli` to export the Feishu chat or group history.
2. Generate `formal-report-draft.md`.
3. Optionally publish the report back into Feishu Docs.
4. Optionally send a follow-up notification into a Feishu chat.
