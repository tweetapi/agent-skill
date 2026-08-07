# Design decisions

This repository is a portable Agent Skill first and a thin client-packaging layer second. It does not duplicate the TweetAPI service or private MCP implementation.

## Included in the first version

| Artifact | Reason |
| --- | --- |
| `skills/tweetapi/` | Portable skill format supported by multiple coding agents |
| `agents/openai.yaml` | OpenAI skill presentation and hosted MCP dependency |
| `.codex-plugin/plugin.json` | Current Codex plugin packaging for repository distribution |
| `.claude-plugin/plugin.json` | Claude Code plugin discovery without a separate repository |
| `.mcp.json` | Secret-free remote OAuth MCP connection for compatible hosts |
| Validation script and CI | Detect packaging errors, placeholders, broken local links, and obvious secrets |
| MIT license and contribution/security policies | Minimum public-repository operating surface |

## Intentionally excluded

| Artifact | Reason |
| --- | --- |
| Copied endpoint catalog | The public API changes; canonical documentation should remain the source of truth |
| Write or account workflows | They broaden risk and require credentials this public skill must never handle |
| OpenAPI specification or Postman collection | Neither is currently published as a canonical public artifact |
| `.app.json` | A ChatGPT app manifest requires a registered technical app identifier and a separate publication decision |
| Codex or Claude marketplace listing | Marketplace submission is an external action and should follow review |
| MCP Registry `server.json` | Registry publication describes the MCP service itself and should follow server metadata hardening |
| Project-local Cursor configuration | Cloning a repository should not silently attach a remote service to an unrelated project |
| Live integration tests | They spend customer quota and introduce credentials into CI |

## Publication prerequisite

Before broad promotion, verify that every hosted MCP tool registers MCP protocol `ToolAnnotations`: set `readOnlyHint` to `true`, `destructiveHint` to `false`, and `openWorldHint` to `true` for tools that read external Twitter/X data or public web documentation.

Annotations are descriptive hints, not an authorization boundary. The server-side allowlist and credential isolation must remain the enforcement mechanism.

## Later distribution opportunities

After review and the annotation prerequisite:

1. publish this repository and verify `gh skill preview` and `gh skill install`;
2. enable GitHub private vulnerability reporting and branch/tag protections;
3. evaluate Codex, Claude, and other agent-skill marketplaces separately;
4. evaluate MCP Registry publication for the hosted service;
5. add an OpenAPI specification and Postman collection only when they have a maintained generation and validation workflow.

None of those external actions are performed by this repository scaffold.
