# Design decisions

The Agent Skill is the core of this repository. The remaining files package it for supported clients. The repository does not contain the TweetAPI service or the private hosted MCP implementation.

## Included files

| Artifact | Reason |
| --- | --- |
| `skills/tweetapi/` | Skill instructions that multiple coding agents can use |
| `agents/openai.yaml` | OpenAI display metadata and hosted MCP dependency |
| `.codex-plugin/plugin.json` | Codex plugin metadata for repository installation |
| `.claude-plugin/plugin.json` | Claude Code plugin metadata in the same repository |
| `.mcp.json` | Remote OAuth MCP connection with no embedded secret |
| Validation script and CI | Checks for packaging errors, placeholders, broken local links, and obvious secrets |
| MIT license and contribution/security policies | License, contribution rules, and vulnerability-reporting instructions |

## Not included

| Artifact | Reason |
| --- | --- |
| Copied endpoint catalog | The public API changes, so the skill links to the canonical documentation |
| Write or account workflows | This skill is read-only and must not handle the credentials those workflows need |
| Bundled OpenAPI specification or Postman collection | The TweetAPI Dashboard contract pipeline generates and publishes these artifacts; a copy here would drift |
| `.app.json` | A ChatGPT app manifest requires a registered technical app identifier and a separate publication decision |
| Codex or Claude marketplace listing | Marketplace submission is an external action and should follow review |
| MCP Registry `server.json` | Registry publication describes the MCP service itself and should follow server metadata hardening |
| Project-local Cursor configuration | Cloning a repository should not silently attach a remote service to an unrelated project |
| Live integration tests | They spend customer quota and put credentials in CI |

## Publication prerequisite

Before promoting the repository, verify `ToolAnnotations` on every hosted MCP tool that reads external Twitter/X data or public web documentation. Set `readOnlyHint` to `true`, `destructiveHint` to `false`, and `openWorldHint` to `true`.

Annotations describe behavior; they are not an authorization boundary. The server-side allowlist and credential isolation must remain the enforcement mechanism.

## Possible distribution work

After review and annotation verification:

1. publish this repository and verify `gh skill preview` and `gh skill install`;
2. enable GitHub private vulnerability reporting and branch/tag protections;
3. evaluate Codex, Claude, and other agent-skill marketplaces separately;
4. evaluate MCP Registry publication for the hosted service;
5. keep the canonical OpenAPI and Postman links current when the Dashboard contract pipeline changes, without bundling duplicate copies here.

This repository does not perform any of those external actions.
