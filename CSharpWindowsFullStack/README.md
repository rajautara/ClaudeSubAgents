# C# Windows Full-Stack Subagents

A set of Claude Code subagents for building full-stack C# Windows applications —
console/CLI, WPF & WinForms desktop, Worker/Windows Service, and ASP.NET Core
APIs — backend to frontend, with dedicated test agents.

## Installation

Copy into your project:
- `.claude/agents/` -> your **project root** `.claude/agents/` (committed to git, shared with the team)
- `CLAUDE.md` -> your **project root** (global context all subagents read)

Or copy `.claude/agents/` to `~/.claude/agents/` to use across all projects.

Then run `/agents` in Claude Code to confirm they loaded.

## Subagents & roles

| Subagent | When to use | Focus |
|---|---|---|
| `solution-architect` | Project start / major feature | Solution structure, project types, layering |
| `backend-engineer` | Core logic & APIs | Domain, application services, ASP.NET Core |
| `data-engineer` | Persistence | EF Core, Dapper, migrations, repositories |
| `desktop-ui-engineer` | Desktop GUI | WPF (MVVM) / WinForms, binding, view-models |
| `windows-service-engineer` | Background processes | Worker Service / Windows Service, schedulers |
| `console-cli-engineer` | CLI tools | Args, subcommands, exit codes, console UX |
| `interop-engineer` | Native / COM interop | P/Invoke, COM (Office automation), marshaling |
| `blazor-engineer` | Web UI in C# | Blazor Server / WASM / Web App, components |
| `test-engineer` | After any logic | Unit tests (xUnit, FluentAssertions, mocking) |
| `integration-test-engineer` | After wiring | Integration / E2E (DB, API, workflows) |
| `build-deploy-engineer` | Shipping | publish, MSIX/WiX, service install, CI/CD |
| `code-reviewer` | After a feature | Correctness, security, design, performance review |

## Typical workflow

```
solution-architect
      |
      v
backend-engineer ── data-engineer
      |                  |
      +── desktop-ui-engineer | windows-service-engineer | console-cli-engineer
      |
      v
test-engineer  +  integration-test-engineer
      |
      v
code-reviewer
      |
      v
build-deploy-engineer
```

## How to use

**Auto-delegation** — Claude Code picks the subagent from its `description`. Just say:
> "Set up a new WPF app with a backend service layer"  ->  `solution-architect` leads, then hands off.

**Manual** — name the subagent:
> "Use data-engineer to add an EF Core migration for the Orders table."
> "Use windows-service-engineer to build a worker that polls a folder every 30s."

**Chaining / full feature:**
> "Build a CLI that imports CSV into the database, with unit and integration tests, then review it."
> (console-cli-engineer -> data-engineer -> test-engineer -> integration-test-engineer -> code-reviewer)

## App-type quick map

- **Console / CLI tool** -> `console-cli-engineer` (+ backend/data as needed)
- **WPF / WinForms desktop** -> `desktop-ui-engineer` (+ backend/data)
- **Windows Service / background worker** -> `windows-service-engineer`
- **Web API** -> `backend-engineer` (+ data-engineer)
- **Blazor web UI** -> `blazor-engineer` (+ backend/data)
- **Office automation / native Win32 calls** -> `interop-engineer`
- **Any of the above** -> always finish with tests, review, then build/deploy.

## Notes

- Each subagent has its own context window — it won't pollute the main conversation. Ideal for long, multi-layer builds.
- `CLAUDE.md` holds project-wide rules (stack, architecture, conventions); subagent `.md` files hold task-specific behavior. They complement each other.
- Edit any `.md` to adjust behavior; change the `tools` field to restrict access (e.g. `code-reviewer` has no `Write` — review only).
- After editing agent files mid-session, run `/agents` again (or start a fresh session) to reload.
