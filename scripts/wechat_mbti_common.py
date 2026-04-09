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


def get_default_output_root():
    if sys.platform == "darwin":
        return Path.home() / "wechat-mbti-exports"
    if os.name == "nt":
        return Path("D:/code_folder/exports/wechat-mbti")
    return Path.cwd() / "exports" / "wechat-mbti"


DEFAULT_OUTPUT_ROOT = get_default_output_root()


def ensure_utf8_env():
    env = os.environ.copy()
    env["PYTHONUTF8"] = "1"
    return env


def find_wechat_cli():
    candidates = [
        "wechat-cli",
        str(Path.home() / "AppData/Roaming/Python/Python314/Scripts/wechat-cli.exe"),
        str(Path.home() / ".local/bin/wechat-cli"),
        "/opt/homebrew/bin/wechat-cli",
        "/usr/local/bin/wechat-cli",
    ]
    for candidate in candidates:
        if os.path.basename(candidate) == candidate:
            resolved = which(candidate)
            if resolved:
                return resolved
        elif Path(candidate).exists():
            return candidate
    return "wechat-cli"


def run_wechat_cli(args, check=True, allow_nonzero=False):
    completed = subprocess.run(
        [find_wechat_cli(), *args],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding="utf-8",
        env=ensure_utf8_env(),
    )
    if check and completed.returncode != 0 and not allow_nonzero:
        raise RuntimeError(f"wechat-cli failed: {' '.join(args)}\n{completed.stderr.strip()}")
    return completed


def sanitize_name(value):
    return "".join("_" if ch in '<>:"/\\|?*' else ch for ch in value)


def get_history_page(chat_name, limit, offset, start_time, end_time, include_media_paths):
    args = ["history", chat_name, "--limit", str(limit), "--offset", str(offset), "--format", "json"]
    if start_time:
        args.extend(["--start-time", start_time])
    if end_time:
        args.extend(["--end-time", end_time])
    if include_media_paths:
        args.append("--media")
    return json.loads(run_wechat_cli(args).stdout)


def export_chat(chat_name, output_root, page_size, start_time, end_time, include_media_paths):
    run_dir = output_root / f"{sanitize_name(chat_name)}-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
    run_dir.mkdir(parents=True, exist_ok=True)

    all_messages = []
    page_index = 0
    offset = 0

    while True:
        page = get_history_page(chat_name, page_size, offset, start_time, end_time, include_media_paths)
        page_path = run_dir / f"history-page-{page_index:04d}.json"
        page_path.write_text(json.dumps(page, ensure_ascii=False, indent=2), encoding="utf-8")
        messages = page.get("messages", [])
        all_messages.extend(str(message) for message in messages)
        print(f"Fetched page {page_index} with {len(messages)} messages")
        if len(messages) < page_size:
            break
        page_index += 1
        offset += page_size

    messages_path = run_dir / "all-messages.txt"
    messages_path.write_text("\n".join(all_messages), encoding="utf-8")

    metadata = {
        "exported_at": datetime.now().isoformat(timespec="seconds"),
        "chat_name": chat_name,
        "output_dir": str(run_dir),
        "page_size": page_size,
        "message_count": len(all_messages),
        "start_time": start_time,
        "end_time": end_time,
        "include_media_paths": include_media_paths,
    }
    metadata_path = run_dir / "metadata.json"
    metadata_path.write_text(json.dumps(metadata, ensure_ascii=False, indent=2), encoding="utf-8")

    prompt_path = run_dir / "mbti-analysis-prompt.md"
    prompt_path.write_text(
        "\n".join(
            [
                "# MBTI Analysis Prompt",
                "",
                "Use the attached chat transcript file all-messages.txt to analyze the people in the conversation.",
                "",
                "- Person A: me",
                f"- Person B: {chat_name}",
                "",
                "Requirements:",
                "",
                "1. Infer each person's MBTI tendency, but explicitly state that this is only a behavior-based inference, not a formal assessment.",
                "2. Analyze all four dimensions for each person: E/I, S/N, T/F, J/P.",
                "3. Cite concrete wording, patterns, or repeated behaviors from the chat as evidence.",
                "4. Give one most likely MBTI type and two backup candidates for each person.",
                "5. Analyze the interaction pattern between the people.",
                "6. End with a confidence note about uncertainty and sample bias.",
            ]
        ),
        encoding="utf-8",
    )

    return {
        "run_dir": run_dir,
        "messages_path": messages_path,
        "metadata_path": metadata_path,
        "prompt_path": prompt_path,
        "message_count": len(all_messages),
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


def detect_group_chat(chat_name, speaker_stats):
    if "群" in chat_name:
        return True
    if len(speaker_stats) > 2:
        return True
    try:
        completed = run_wechat_cli(["members", chat_name], check=False, allow_nonzero=True)
        return completed.returncode == 0 and bool(completed.stdout.strip())
    except Exception:
        return False


def get_time_range_text(metadata):
    if metadata.get("start_time") or metadata.get("end_time"):
        return f"{metadata.get('start_time') or ''} ~ {metadata.get('end_time') or ''}".strip()
    return "全量导出"


def build_personal_template(chat_name, metadata, speaker_stats, transcript_path):
    speaker_lines = [f"- {name}: {count} messages" for name, count in speaker_stats]
    return "\n".join(
        [
            "# Formal MBTI and Relationship Report",
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
            "# Formal Group Workflow and MBTI Report",
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
    speaker_summary = [f"- {name}：{count} 条" for name, count in speaker_stats]
    if len(speaker_stats) > 1 and speaker_stats[0][0] == "me":
        sample_speaker = speaker_stats[1][0]
    elif speaker_stats:
        sample_speaker = speaker_stats[0][0]
    else:
        sample_speaker = chat_name
    sample_bullets = [f"- {sample}" for sample in get_speaker_samples(lines, sample_speaker, 3)] or ["- 待从聊天原文中补充代表性表达"]
    return "\n".join(
        [
            "# 性格与互动关系分析报告",
            "",
            "## 一、分析范围与方法说明",
            "",
            "本报告基于以下聊天导出文件进行分析：",
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
            "从这份聊天记录看，双方的互动并不是完全对称的，而是存在比较稳定的角色分化。",
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
            "",
            "## 六、定稿待补项",
            "",
            "- 补充最可能 MBTI 与两个备选类型",
            "- 补充 2 到 4 条代表性证据",
            "- 补充双方的互补点、冲突点和关系建议",
            "",
            "## 七、最终结论",
            "",
            "这份初稿已经生成了中文正式报告的基本结构、样本信息和论证入口，下一步只需要结合原始聊天记录补足证据与类型判断即可。",
        ]
    )


def build_group_draft(chat_name, metadata, speaker_stats, lines, transcript_path):
    speaker_summary = [f"- {name}：{count} 条" for name, count in speaker_stats]
    member_sections = []
    for name, count in speaker_stats[:6]:
        samples = get_speaker_samples(lines, name, 2) or ["待补充"]
        member_sections.extend(
            [
                f"## 成员：{name}",
                "",
                f"- 发言量：{count} 条",
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
            "本报告基于以下群聊导出文件进行分析：",
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
            "这个群更像一个围绕核心任务运转的小型作战群，而不是平均分布式讨论群。",
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
            "## 五、团队优势",
            "",
            "- 目标集中度可能较高",
            "- 角色分层很可能已经自然形成",
            "- 只要中间层承接稳定，推进效率通常不会低",
            "",
            "## 六、团队风险",
            "",
            "- 过度依赖少数核心发言者",
            "- 承接层强，但不一定天然承担顶层设计",
            "- 执行层如果缺少 owner，容易出现等指令现象",
            "",
            "## 七、定稿待补项",
            "",
            "- 为每位成员补充 MBTI 初判与备选类型",
            "- 为每位成员补充 2 到 4 条代表性证据",
            "- 补充群内隐性层级、分工与瓶颈判断",
        ]
    )


def get_latest_export_dir(output_root, chat_name):
    matches = sorted(output_root.glob(f"{sanitize_name(chat_name)}-*"), key=lambda p: p.stat().st_mtime, reverse=True)
    if not matches:
        raise RuntimeError(f"Could not locate an existing export directory for {chat_name}")
    return matches[0]


def write_template(chat_name, run_dir):
    metadata = read_metadata(run_dir / "metadata.json")
    transcript_path = run_dir / "all-messages.txt"
    lines = get_transcript_lines(transcript_path)
    speaker_stats = get_speaker_stats(lines)
    report_path = run_dir / "formal-report-template.md"
    report = build_group_template(chat_name, metadata, speaker_stats, transcript_path) if detect_group_chat(chat_name, speaker_stats) else build_personal_template(chat_name, metadata, speaker_stats, transcript_path)
    report_path.write_text(report, encoding="utf-8")
    return report_path


def write_draft(chat_name, run_dir):
    metadata = read_metadata(run_dir / "metadata.json")
    transcript_path = run_dir / "all-messages.txt"
    lines = get_transcript_lines(transcript_path)
    speaker_stats = get_speaker_stats(lines)
    draft_path = run_dir / "formal-report-draft.md"
    draft = build_group_draft(chat_name, metadata, speaker_stats, lines, transcript_path) if detect_group_chat(chat_name, speaker_stats) else build_personal_draft(chat_name, metadata, speaker_stats, lines, transcript_path)
    draft_path.write_text(draft, encoding="utf-8")
    return draft_path


def build_parser():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command", required=True)
    for command in ("export", "template", "draft"):
        subparser = subparsers.add_parser(command)
        subparser.add_argument("--chat-name", required=True)
        subparser.add_argument("--output-root", default=str(DEFAULT_OUTPUT_ROOT))
        subparser.add_argument("--page-size", type=int, default=200)
        subparser.add_argument("--start-time")
        subparser.add_argument("--end-time")
        subparser.add_argument("--include-media-paths", action="store_true")
        if command in ("template", "draft"):
            subparser.add_argument("--skip-export", action="store_true")
    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()
    output_root = Path(args.output_root)
    output_root.mkdir(parents=True, exist_ok=True)

    if args.command == "export":
        result = export_chat(args.chat_name, output_root, args.page_size, args.start_time, args.end_time, args.include_media_paths)
        print("")
        print("Workflow complete.")
        print(f"Output directory: {result['run_dir']}")
        print(f"Messages exported: {result['message_count']}")
        print(f"Merged text: {result['messages_path']}")
        print(f"Prompt file: {result['prompt_path']}")
        return 0

    run_dir = get_latest_export_dir(output_root, args.chat_name) if args.skip_export else export_chat(args.chat_name, output_root, args.page_size, args.start_time, args.end_time, args.include_media_paths)["run_dir"]

    if args.command == "template":
        report_path = write_template(args.chat_name, run_dir)
        print("")
        print("Report template complete.")
        print(f"Output directory: {run_dir}")
        print(f"Report template: {report_path}")
        return 0

    if args.command == "draft":
        write_template(args.chat_name, run_dir)
        draft_path = write_draft(args.chat_name, run_dir)
        print("")
        print("Chinese report draft complete.")
        print(f"Output directory: {run_dir}")
        print(f"Chinese report draft: {draft_path}")
        return 0

    return 1


if __name__ == "__main__":
    sys.exit(main())
