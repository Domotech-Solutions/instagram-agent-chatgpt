# Workspace state

Use `.instagram-agent/` in the active writable workspace for optional persistent state.

- `config.json`: language and user-approved preferences.
- `voice.md`: voice, audience, offer, examples, and phrases to avoid.
- `swipe.md`: attributed research notes created by `$ig-viral`.
- `plan.md`: the current approved content plan.
- `log.md`: approved drafts and their formula identifiers. Logging approval does not mean content was published.

Create or update these files only when the user asks for setup, approves a draft for logging, or requests a saved plan. Do not infer publication from approval. Never store credentials, cookies, private tokens, or unnecessary personal data.

If persistent files are unavailable, ask the user to attach or paste the relevant state and return updated content in chat.
