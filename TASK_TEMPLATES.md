# OpenClaw Task Templates

Use the following templates as ready-to-paste OpenClaw task prompts.

## 1. Single Chat MBTI Report

```text
Use the workflow files in this folder to analyze the WeChat chat "<chat name>".

Requirements:
1. Export the full chat first.
2. Read `all-messages.txt` and `metadata.json`.
3. Generate or refine `formal-report-draft.md`.
4. Write the final report in Chinese.
5. Treat MBTI as a behavior-based inference, not a diagnosis.
6. Give one most likely MBTI type and two backup types.
7. Explain the four dimensions: E/I, S/N, T/F, J/P.
8. Use concrete evidence from the transcript whenever possible.
```

## 2. Founder / Work Partner Report

```text
Use the workflow files in this folder to analyze the WeChat chat "<chat name>" as a founder or work-partner relationship.

Requirements:
1. Export the full chat first.
2. Generate a Chinese formal report draft.
3. Focus on:
   - each person's likely MBTI tendency
   - decision style
   - pressure response
   - complementarity
   - conflict pattern
   - role boundaries
4. Keep MBTI as a behavior-based inference.
5. The final report must be in Chinese and directly usable without extra cleanup.
```

## 3. Family / Relationship Report

```text
Use the workflow files in this folder to analyze the WeChat chat "<chat name>" as a family or intimate relationship.

Requirements:
1. Export the full chat first.
2. Generate a Chinese formal report draft.
3. Focus on:
   - emotional needs
   - communication style
   - relationship expectations
   - recurring friction points
   - stress response
4. Distinguish relationship stress from baseline personality.
5. Keep the tone analytical and respectful.
```

## 4. Group Workflow Report

```text
Use the workflow files in this folder to analyze the WeChat group "<group name>".

Requirements:
1. Export the full group chat first.
2. Generate a Chinese formal report draft.
3. Analyze:
   - the group's working model
   - hidden hierarchy
   - role split
   - team strengths
   - team risks
   - likely MBTI tendency for key members
4. Focus on workflow and team structure before MBTI.
5. Use transcript evidence whenever possible.
```

## 5. Compare Two People Across Multiple Chats

```text
Use the workflow files in this folder to analyze two WeChat chats: "<chat A>" and "<chat B>".

Requirements:
1. Export both chats first.
2. Compare the user's interaction style across the two relationships.
3. Write a Chinese comparison report.
4. Focus on:
   - how the user's behavior changes across the two chats
   - the likely MBTI tendency of each counterpart
   - different complementarity and conflict patterns
   - what this reveals about role expectations and communication style
5. Keep MBTI as a behavior-based inference.
```

## 6. Time-Sliced Report

```text
Use the workflow files in this folder to analyze the WeChat chat "<chat name>" only for the period from "<start time>" to "<end time>".

Requirements:
1. Export only the selected time range.
2. Generate a Chinese formal report draft.
3. Make clear that the conclusion is based only on the selected time window.
4. Highlight what may be biased by short-term events or temporary pressure.
```

## 7. Publish Report to Feishu Docs

```text
Use the workflow files in this folder to generate the Chinese report for "<chat name>", then publish the final markdown report to Feishu Docs.

Requirements:
1. Export the chat first.
2. Generate or refine `formal-report-draft.md`.
3. Use Feishu CLI integration to publish the markdown file as a Feishu document.
4. If available, return the document link or CLI output.
5. Keep MBTI as a behavior-based inference, not a diagnosis.
```

## 8. Publish and Notify in Feishu

```text
Use the workflow files in this folder to generate the Chinese report for "<chat name>", publish it to Feishu Docs, and then send a Feishu chat notification.

Requirements:
1. Export the chat first.
2. Generate or refine `formal-report-draft.md`.
3. Publish the markdown report to Feishu Docs.
4. Send a short Feishu message to the target chat with the result.
5. Return the publish result and notification result.
```

## 9. Feishu Chat MBTI Report

```text
Use the workflow files in this folder to export the Feishu chat "<chat name>" with chat id "<chat-id>", then generate a Chinese MBTI report.

Requirements:
1. Use Feishu CLI raw API access through the Feishu chat pipeline.
2. Export the chat history first.
3. Generate or refine `formal-report-draft.md`.
4. Treat MBTI as a behavior-based inference, not a diagnosis.
5. Use transcript evidence whenever possible.
```

## 10. Feishu Group Workflow Report

```text
Use the workflow files in this folder to export the Feishu group "<group name>" with chat id "<chat-id>", then generate a Chinese team workflow and MBTI report.

Requirements:
1. Export the Feishu group history first.
2. Force group mode if needed.
3. Analyze team structure, hidden hierarchy, role split, and likely MBTI tendencies of key members.
4. Generate a Chinese formal report draft.
5. Focus on workflow and role split before MBTI.
```
