# GitHub Sync Notes

This workflow folder is structured so it can be uploaded directly as a GitHub repository.

## Suggested Repo Layout

- `README.md`
- `SYSTEM_PROMPT.md`
- `TASK_TEMPLATES.md`
- `SKILL.md`
- `scripts/`
- `references/`

## Suggested Git Commands

```bash
git init
git add .
git commit -m "Add OpenClaw WeChat MBTI analyzer workflow"
git branch -M main
git remote add origin <your-repo-url>
git push -u origin main
```

## Sync Update Workflow

```bash
git add .
git commit -m "Update OpenClaw workflow"
git push
```

## Notes

- Keep the repository UTF-8 encoded.
- Do not commit exported chat transcripts unless you explicitly want them versioned.
- Keep secrets, tokens, or local user data out of the repo.
