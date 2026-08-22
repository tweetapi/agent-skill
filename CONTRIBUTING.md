# Contributing

Keep contributions within the repository's read-only scope. Link to the canonical API catalog instead of copying it here, where it would drift.

## Before changing the skill

1. Verify behavior against the canonical links in `skills/tweetapi/references/sources.md`.
2. Keep live data calls, pagination, and retries opt-in and bounded.
3. Keep all account, write, private-message, login, billing, and administrative operations out of scope.
4. Do not add API keys, cookies, tokens, passwords, proxy credentials, real private data, or live-response fixtures.
5. Do not make a live TweetAPI request to test documentation or packaging changes.

## Validate locally

```bash
python3 scripts/validate_repository.py
agentskills validate skills/tweetapi
```

If a change affects a client manifest, validate it with that client's current official validator when available. Document any validator that could not be run.

## Pull requests

Keep each change focused. Explain the public source used, the safety impact, whether it changes quota behavior, and which validation commands passed. Use mocked data for integration examples and tests.
