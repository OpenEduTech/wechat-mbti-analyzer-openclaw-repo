import argparse
import json
import os
import subprocess
import sys
from pathlib import Path
from shutil import which


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


def run_cli(args):
    cli = find_lark_cli()
    if not cli:
        raise RuntimeError(
            "Could not find lark-cli. Install it first, then run `lark-cli config init` and `lark-cli auth login --recommend`."
        )
    return subprocess.run(
        [cli, *args],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding="utf-8",
    )


def publish_doc(markdown_path, title):
    completed = run_cli(["docx", "create", "--title", title, "--markdown", str(markdown_path)])
    if completed.returncode != 0:
        raise RuntimeError(completed.stderr.strip() or completed.stdout.strip())
    return completed.stdout.strip()


def send_message(chat_id, text):
    completed = run_cli(["im", "v1", "message", "create", "--receive-id-type", "chat_id", "--receive-id", chat_id, "--msg-type", "text", "--content", json.dumps({"text": text}, ensure_ascii=False)])
    if completed.returncode != 0:
        raise RuntimeError(completed.stderr.strip() or completed.stdout.strip())
    return completed.stdout.strip()


def build_parser():
    parser = argparse.ArgumentParser(description="Publish generated MBTI reports to Feishu / Lark.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    doc = subparsers.add_parser("doc", help="Publish a markdown report as a Feishu document")
    doc.add_argument("--file", required=True, help="Path to the markdown report file")
    doc.add_argument("--title", required=True, help="Feishu document title")

    notify = subparsers.add_parser("notify", help="Send a text message to a Feishu chat")
    notify.add_argument("--chat-id", required=True, help="Target Feishu chat id")
    notify.add_argument("--text", required=True, help="Notification text")

    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()

    if args.command == "doc":
        output = publish_doc(Path(args.file), args.title)
        print(output)
        return 0

    if args.command == "notify":
        output = send_message(args.chat_id, args.text)
        print(output)
        return 0

    return 1


if __name__ == "__main__":
    sys.exit(main())
