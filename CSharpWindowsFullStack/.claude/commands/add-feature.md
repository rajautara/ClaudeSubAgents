---
description: Implement a feature end to end across the C# suite (backend -> data -> UI -> tests -> review)
argument-hint: <feature description>
---

Implement this feature end to end, delegating each layer to the right subagent
and respecting every CLAUDE.md rule (layering, async/CancellationToken, DI,
no secrets, ILogger): `$ARGUMENTS`

Suggested chain (skip stages that don't apply):
1. `backend-engineer` — domain models, application/use-case services, and (if a
   Web API) endpoints; define repository/`IClock`/auth interfaces.
2. `data-engineer` — implement the persistence interfaces (EF Core/Dapper) + migration.
3. `security-engineer` — authn/authz for any protected surface; secrets handling.
4. UI layer as needed: `desktop-ui-engineer` (WPF/WinForms), `winui-maui-engineer`
   (WinUI 3/MAUI), `blazor-engineer` (web), or `console-cli-engineer` (CLI).
5. `test-engineer` — unit tests for new logic; `integration-test-engineer` for wired flows.
6. `code-reviewer` — review correctness, design, security, performance.

Keep UI/CLI/service layers thin; business logic stays in Application services.
Finish by reporting what changed and any follow-ups.
