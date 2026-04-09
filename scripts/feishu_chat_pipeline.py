import argparse
import json
import os
import re
import subprocess
import sys
from collections import Counter
from datetime import datetime
from pathlib import Path
from shutil import which
from urllib.parse import urlencode


def get_default_output_root():
    if sys.platform == "darwin":
        return Path.home() / "feishu-mbti-exports"
    if os.name == "nt":
        return Path("D:/code_folder/exports/feishu-mbti")
    return Path.cwd() / "exports" / "feishu-mbti"


DEFAULT_OUTPUT_ROOT = get_default_output_root()


def find_lark_cli():
    candidates = [
        "lark-cli",
        "feishu-cli",
        str(Path.home() / ".npm-global/bin/lark-cli"),
        str(Path.home() / ".local/bin/lark-cli"),
        "/opt/homebrew/bin/lark-cli",
        "/usr/local/bin/lark-cli",
    ]
    for candidate in candidates:
        if os.path.basename(candidate) == candidate:
            resolved = which(candidate)
            if resolved:
                return resolved
        elif Path(candidate).exists():
            return candidate
    return None


def run_lark_cli(args):
    cli = find_lark_cli()
    if not cli:
        raise RuntimeError(
            "Could not find lark-cli. Install it first, then run `lark-cli config init` and `lark-cli auth login --recommend`."
        )

    completed = subprocess.run(
        [cli, *args],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding="utf-8",
    )
    if completed.returncode != 0:
        raise RuntimeError(completed.stderr.strip() or completed.stdout.strip())
    return completed


def sanitize_name(value):
    return "".join("_" if ch in '<>:"/\\|?*' else ch for ch in value)


def parse_time(value):
    if not value:
        return ""
    try:
        ivalue = int(str(value))
    except ValueError:
        return str(value)

    if ivalue > 10_000_000_000:
        ivalue = ivalue / 1000
    return datetime.fromtimestamp(ivalue).strftime("%Y-%m-%d %H:%M:%S")


def parse_message_content(message):
    message_type = message.get("msg_type") or message.get("message_type") or "unknown"
    body = message.get("body") or {}
    raw_content = body.get("content") or message.get("content") or ""

    content_obj = None
    if isinstance(raw_content, str):
        try:
            content_obj = json.loads(raw_content)
        except Exception:
            content_obj = {"text": raw_content}
    elif isinstance(raw_content, dict):
        content_obj = raw_content
    else:
        content_obj = {}

    if message_type == "text":
        return content_obj.get("text") or str(raw_content)

    if message_type == "post":
        parts = []
        for locale in content_obj.values():
            rows = locale.get("content", []) if isinstance(locale, dict) else []
            for row in rows:
                for item in row:
                    text = item.get("text")
                    if text:
                        parts.append(text)
        return " ".join(parts) or "[post]"

    if message_type == "file":
        return "[file]"
    if message_type == "image":
        return "[image]"
    if message_type == "audio":
        return "[audio]"
    if message_type == "media":
        return "[media]"
    if message_type == "sticker":
        return "[sticker]"
    if message_type == "interactive":
        return "[card]"
    if message_type == "share_chat":
        return "[shared chat]"
    if message_type == "share_user":
        return "[shared user]"
    if message_type == "location":
        return "[location]"

    text = content_obj.get("text") or str(raw_content)
    return text[:500] if text else f"[{message_type}]"


def parse_sender_name(message):
    sender = message.get("sender") or {}
    sender_keys = [
        "name",
        "sender_name",
    ]
    for key in sender_keys:
        if sender.get(key):
            return sender[key]

    sender_id = sender.get("sender_id") or {}
    for key in ("user_id", "union_id", "open_id"):
        if sender_id.get(key):
            return sender_id[key]

    return "unknown"


def format_transcript_line(message):
    timestamp = parse_time(message.get("create_time") or message.get("update_time"))
    sender = parse_sender_name(message)
    content = parse_message_content(message).replace("\n", " ").strip()
    return f"[{timestamp}] {sender}: {content}"


def get_messages_page(chat_id, page_size, page_token=None, start_time=None, end_time=None):
    params = {
        "container_id_type": "chat",
        "container_id": chat_id,
        "page_size": page_size,
    }
    if page_token:
        params["page_token"] = page_token
    if start_time:
        params["start_time"] = start_time
    if end_time:
        params["end_time"] = end_time

    path = "/open-apis/im/v1/messages?" + urlencode(params)
    completed = run_lark_cli(["api", "GET", path])
    return json.loads(completed.stdout)


def export_feishu_chat(chat_id, chat_name, output_root, page_size, start_time, end_time):
    run_dir = output_root / f"{sanitize_name(chat_name)}-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
    run_dir.mkdir(parents=True, exist_ok=True)

    all_items = []
    all_lines = []
    page_index = 0
    page_token = None

    while True:
        page = get_messages_page(chat_id, page_size, page_token=page_token, start_time=start_time, end_time=end_time)
        page_path = run_dir / f"history-page-{page_index:04d}.json"
        page_path.write_text(json.dumps(page, ensure_ascii=False, indent=2), encoding="utf-8")

        data = page.get("data") or {}
        items = data.get("items") or []
        all_items.extend(items)
        all_lines.extend(format_transcript_line(item) for item in items)

        print(f"Fetched page {page_index} with {len(items)} messages")

        if not data.get("has_more"):
            break
        page_index += 1
        page_token = data.get("page_token")
        if not page_token:
            break

    messages_path = run_dir / "all-messages.txt"
    messages_path.write_text("\n".join(all_lines), encoding="utf-8")

    metadata = {
        "source": "feishu",
        "exported_at": datetime.now().isoformat(timespec="seconds"),
        "chat_id": chat_id,
        "chat_name": chat_name,
        "output_dir": str(run_dir),
        "page_size": page_size,
        "message_count": len(all_lines),
        "start_time": start_time,
        "end_time": end_time,
    }
    metadata_path = run_dir / "metadata.json"
    metadata_path.write_text(json.dumps(metadata, ensure_ascii=False, indent=2), encoding="utf-8")

    prompt_path = run_dir / "mbti-analysis-prompt.md"
    prompt_path.write_text(
        "\n".join(
            [
                "# MBTI Analysis Prompt",
                "",
                "Use the attached transcript file all-messages.txt to analyze the people in the Feishu conversation.",
                "",
                f"- Chat name: {chat_name}",
                f"- Chat id: {chat_id}",
                "",
                "Requirements:",
                "",
                "1. Infer likely MBTI tendencies as behavior-based inference, not diagnosis.",
                "2. Analyze E/I, S/N, T/F, J/P.",
                "3. Cite repeated wording, behavior, and interaction patterns.",
                "4. Give one most likely type and two backup candidates.",
                "5. Analyze interaction structure, conflict pattern, and complementarity.",
            ]
        ),
        encoding="utf-8",
    )

    return {
        "run_dir": run_dir,
        "messages_path": messages_path,
        "metadata_path": metadata_path,
        "prompt_path": prompt_path,
        "message_count": len(all_lines),
    }


def read_metadata(path):
    return json.loads(path.read_text(encoding="utf-8"))


def get_transcript_lines(path):
    return path.read_text(encoding="utf-8").splitlines()


def get_speaker_stats(lines):
    counter = Counter()
    for line in lines:
        match = re.match(r"^\[[^\]]+\] ([^:]+):", line)
        if match:
            counter[match.group(1).strip()] += 1
    return sorted(counter.items(), key=lambda item: item[1], reverse=True)


def get_speaker_samples(lines, speaker, limit=3):
    pattern = re.compile(r"^\[[^\]]+\] ([^:]+):\s*(.*)$")
    samples = []
    for line in lines:
        match = pattern.match(line)
        if match and match.group(1).strip() == speaker:
            content = match.group(2).strip()
            if content:
                samples.append(content)
        if len(samples) >= limit:
            break
    return samples


def detect_group_chat(chat_type, speaker_stats):
    if chat_type == "group":
        return True
    if chat_type == "personal":
        return False
    return len(speaker_stats) > 2


def get_time_range_text(metadata):
    if metadata.get("start_time") or metadata.get("end_time"):
        return f"{metadata.get('start_time') or ''} ~ {metadata.get('end_time') or ''}".strip()
    return "full export"


def build_personal_template(chat_name, metadata, speaker_stats, transcript_path):
    speaker_lines = [f"- {name}: {count} messages" for name, count in speaker_stats]
    return "\n".join(
        [
            "# Formal Feishu MBTI and Relationship Report",
            "",
            "Write the final prose in Chinese.",
            "",
            "## Scope",
            "",
            f"- Transcript: `{transcript_path}`",
            f"- Chat target: {chat_name}",
            f"- Exported at: {metadata.get('exported_at')}",
            f"- Message count: {metadata.get('message_count')}",
            f"- Time range: {get_time_range_text(metadata)}",
            "",
            "## Speaker Stats",
            "",
            *speaker_lines,
            "",
            "## Executive Summary",
            "",
            "- Most likely MBTI type for the other person:",
            "- Backup types:",
            "- Core interaction pattern:",
            "- Main complementarity:",
            "- Main conflict risk:",
        ]
    )


def build_group_template(chat_name, metadata, speaker_stats, transcript_path):
    speaker_lines = [f"- {name}: {count} messages" for name, count in speaker_stats[:10]]
    member_sections = []
    for name, _count in speaker_stats[:8]:
        member_sections.extend(
            [
                f"## Member: {name}",
                "",
                "### Most Likely Type",
                "",
                "### Backup Types",
                "",
                "### Functional Role",
                "",
                "### Key Evidence",
                "",
            ]
        )
    return "\n".join(
        [
            "# Formal Feishu Group Workflow and MBTI Report",
            "",
            "Write the final prose in Chinese.",
            "",
            "## Scope",
            "",
            f"- Transcript: `{transcript_path}`",
            f"- Group name: {chat_name}",
            f"- Exported at: {metadata.get('exported_at')}",
            f"- Message count: {metadata.get('message_count')}",
            f"- Time range: {get_time_range_text(metadata)}",
            "",
            "## Core Speaker Stats",
            "",
            *speaker_lines,
            "",
            "## Executive Summary",
            "",
            "- What kind of work group is this:",
            "- Who is the core driver:",
            "- What are the main layers or roles:",
            "- Main team strength:",
            "- Main structural risk:",
            "",
            "## Group Working Model",
            "",
            "### Operating Logic",
            "",
            "### Hidden Hierarchy and Role Split",
            "",
            "### Sources of Efficiency",
            "",
            "### Bottlenecks",
            "",
            *member_sections,
        ]
    )


def build_personal_draft(chat_name, metadata, speaker_stats, lines, transcript_path):
    speaker_summary = [f"- {name}: {count}" for name, count in speaker_stats]
    if len(speaker_stats) > 1:
        sample_speaker = speaker_stats[1][0] if speaker_stats[0][0] == "me" else speaker_stats[0][0]
    elif speaker_stats:
        sample_speaker = speaker_stats[0][0]
    else:
        sample_speaker = chat_name
    sample_bullets = [f"- {sample}" for sample in get_speaker_samples(lines, sample_speaker, 3)] or ["- Add transcript evidence here."]
    return "\n".join(
        [
            "# 性格与互动关系分析报告",
            "",
            "## 一、分析范围与方法说明",
            "",
            "本报告基于以下飞书聊天导出文件进行分析：",
            "",
            f"- `{transcript_path}`",
            "",
            "这是一份基于聊天行为的 MBTI 倾向分析，不是正式心理测评。",
            "",
            "样本信息：",
            "",
            f"- 聊天对象：{chat_name}",
            f"- 导出时间：{metadata.get('exported_at')}",
            f"- 消息总数：{metadata.get('message_count')}",
            f"- 时间范围：{get_time_range_text(metadata)}",
            "",
            "发言量分布：",
            "",
            *speaker_summary,
            "",
            "## 二、结论摘要",
            "",
            "从这份飞书聊天记录看，双方的互动并不是完全对称的，而是存在比较稳定的角色分化。",
            "- 一方更像推动者或节奏定义者",
            "- 另一方更像承接者、回应者或稳定器",
            "- 双方在压力下的表达方式很可能不同",
            "",
            "## 三、MBTI 倾向初步分析",
            "",
            "建议先从四个维度核对：",
            "",
            "- E / I：更外放还是更内收",
            "- S / N：更偏具体现实还是更偏抽象趋势",
            "- T / F：更偏标准和判断还是更偏关系和感受",
            "- J / P：更偏结构、节奏和闭环还是更偏随机应对",
            "",
            "- 最可能类型：待补充",
            "- 备选类型：待补充",
            "",
            "## 四、互动模式初稿",
            "",
            "- 可以重点分析谁在定义目标、谁在接住细节",
            "- 可以分析双方谁更重视效率与结果，谁更重视体验与关系",
            "- 可以分析双方在压力时是更倾向加大控制，还是更倾向表达感受",
            "",
            "## 五、可直接引用的原始表达",
            "",
            *sample_bullets,
        ]
    )


def build_group_draft(chat_name, metadata, speaker_stats, lines, transcript_path):
    speaker_summary = [f"- {name}: {count}" for name, count in speaker_stats]
    member_sections = []
    for name, count in speaker_stats[:6]:
        samples = get_speaker_samples(lines, name, 2) or ["Add transcript evidence here."]
        member_sections.extend(
            [
                f"## 成员：{name}",
                "",
                f"- 发言量：{count}",
                "- 群内角色初判：待补充",
                "- 最可能 MBTI：待补充",
                "- 备选类型：待补充",
                "- 代表性表达候选：",
                *[f"  - {sample}" for sample in samples],
                "",
            ]
        )
    return "\n".join(
        [
            "# 工作群工作模式与成员 MBTI 分析报告",
            "",
            "## 一、分析范围与方法说明",
            "",
            "本报告基于以下飞书群聊导出文件进行分析：",
            "",
            f"- `{transcript_path}`",
            "",
            "这是一份基于工作对话的 MBTI 倾向和协作模式分析，不是正式心理测评。",
            "",
            f"- 群名：{chat_name}",
            f"- 导出时间：{metadata.get('exported_at')}",
            f"- 消息总数：{metadata.get('message_count')}",
            f"- 时间范围：{get_time_range_text(metadata)}",
            f"- 发言人数：{len(speaker_stats)}",
            "",
            "发言量分布：",
            "",
            *speaker_summary,
            "",
            "## 二、结论摘要",
            "",
            "这个飞书群更像一个围绕核心任务运转的小型作战群，而不是平均分布式讨论群。",
            "- 头部发言者很可能承担了更多方向、节奏或评审责任",
            "- 中间层成员更可能承接方案、流程、版本或交付",
            "- 低频成员可能负责局部输入、执行或外部信息补充",
            "",
            "## 三、群组工作模式初判",
            "",
            "- 核对谁在定义目标、截止时间和优先级",
            "- 核对谁在把目标翻译成文档、方案、产品或交付",
            "- 核对谁在提供外部机会、商业判断或行业信号",
            "",
            "## 四、成员逐一分析",
            "",
            *member_sections,
        ]
    )


def get_latest_export_dir(output_root, chat_name):
    matches = sorted(output_root.glob(f"{sanitize_name(chat_name)}-*"), key=lambda p: p.stat().st_mtime, reverse=True)
    if not matches:
        raise RuntimeError(f"Could not locate an existing export directory for {chat_name}")
    return matches[0]


def write_template(chat_name, chat_type, run_dir):
    metadata = read_metadata(run_dir / "metadata.json")
    transcript_path = run_dir / "all-messages.txt"
    lines = get_transcript_lines(transcript_path)
    speaker_stats = get_speaker_stats(lines)
    report_path = run_dir / "formal-report-template.md"
    report = build_group_template(chat_name, metadata, speaker_stats, transcript_path) if detect_group_chat(chat_type, speaker_stats) else build_personal_template(chat_name, metadata, speaker_stats, transcript_path)
    report_path.write_text(report, encoding="utf-8")
    return report_path


def write_draft(chat_name, chat_type, run_dir):
    metadata = read_metadata(run_dir / "metadata.json")
    transcript_path = run_dir / "all-messages.txt"
    lines = get_transcript_lines(transcript_path)
    speaker_stats = get_speaker_stats(lines)
    draft_path = run_dir / "formal-report-draft.md"
    draft = build_group_draft(chat_name, metadata, speaker_stats, lines, transcript_path) if detect_group_chat(chat_type, speaker_stats) else build_personal_draft(chat_name, metadata, speaker_stats, lines, transcript_path)
    draft_path.write_text(draft, encoding="utf-8")
    return draft_path


def build_parser():
    parser = argparse.ArgumentParser(description="Export Feishu chat history and generate MBTI-style reports.")
    subparsers = parser.add_subparsers(dest="command", required=True)
    for command in ("export", "template", "draft"):
        sub = subparsers.add_parser(command)
        sub.add_argument("--chat-id", required=True)
        sub.add_argument("--chat-name", required=True)
        sub.add_argument("--chat-type", choices=("auto", "personal", "group"), default="auto")
        sub.add_argument("--output-root", default=str(DEFAULT_OUTPUT_ROOT))
        sub.add_argument("--page-size", type=int, default=50)
        sub.add_argument("--start-time")
        sub.add_argument("--end-time")
        if command in ("template", "draft"):
            sub.add_argument("--skip-export", action="store_true")
    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()
    output_root = Path(args.output_root)
    output_root.mkdir(parents=True, exist_ok=True)

    if args.command == "export":
        result = export_feishu_chat(args.chat_id, args.chat_name, output_root, args.page_size, args.start_time, args.end_time)
        print("")
        print("Feishu export complete.")
        print(f"Output directory: {result['run_dir']}")
        print(f"Messages exported: {result['message_count']}")
        print(f"Merged text: {result['messages_path']}")
        print(f"Prompt file: {result['prompt_path']}")
        return 0

    run_dir = get_latest_export_dir(output_root, args.chat_name) if args.skip_export else export_feishu_chat(args.chat_id, args.chat_name, output_root, args.page_size, args.start_time, args.end_time)["run_dir"]

    if args.command == "template":
        report_path = write_template(args.chat_name, args.chat_type, run_dir)
        print("")
        print("Feishu report template complete.")
        print(f"Output directory: {run_dir}")
        print(f"Report template: {report_path}")
        return 0

    if args.command == "draft":
        write_template(args.chat_name, args.chat_type, run_dir)
        draft_path = write_draft(args.chat_name, args.chat_type, run_dir)
        print("")
        print("Feishu report draft complete.")
        print(f"Output directory: {run_dir}")
        print(f"Report draft: {draft_path}")
        return 0

    return 1


if __name__ == "__main__":
    sys.exit(main())
