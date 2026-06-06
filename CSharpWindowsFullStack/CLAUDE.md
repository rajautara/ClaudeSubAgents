# CLAUDE.md

Global context for this C# / .NET Windows application project. All subagents
and chat sessions follow these conventions. Subagent `.md` files in
`.claude/agents/` define task-specific behavior; this file defines project-wide
defaults.

## Stack
- Language: C# (latest), nullable reference types enabled.
- Framework: .NET 8 (LTS) unless specified otherwise.
- App types: console/CLI, WPF & WinForms desktop, Worker/Windows Service, ASP.NET Core Web API, Blazor web UI.
- Interop: P/Invoke (Win32), COM automation (Office/shell), C++/CLI bridges.
- DI/Host: Microsoft.Extensions.DependencyInjection + Generic Host.
- Data: EF Core (SQL Server / SQLite / PostgreSQL), Dapper where performance matters.
- Logging: `ILogger<T>` (Microsoft.Extensions.Logging) / Serilog if configured.
- Testing: xUnit + FluentAssertions + NSubstitute/Moq (unit); WebApplicationFactory + Testcontainers/SQLite (integration).
- Packaging: dotnet publish, MSIX / WiX, GitHub Actions CI.

## Architecture
Layered / clean architecture; dependencies flow inward:
```
Host (Console/WPF/WinForms/Worker/Api)  ->  Application  ->  Domain
Infrastructure (EF Core, IO, external)   implements Application interfaces
```
- Domain: pure business logic, no framework dependencies.
- Application: use cases, interfaces, DTOs.
- Infrastructure: persistence and external integrations.
- Host: composition root + entry point.

## Project layout
```
src/
  <App>.Domain/
  <App>.Application/
  <App>.Infrastructure/
  <App>.<Host>/         # Console | Wpf | WinForms | Worker | Api
tests/
  <App>.UnitTests/
  <App>.IntegrationTests/
docs/
.github/workflows/
Directory.Build.props
global.json
```

## Conventions
- async/await for all IO; never block with `.Result`/`.Wait()`; pass `CancellationToken`.
- No business logic in UI / CLI / service-loop layers — delegate to Application services.
- Do not use `DateTime.Now` directly in logic — inject an `IClock` for testability.
- No hardcoded secrets/paths/connection strings — use configuration + user-secrets / environment.
- `ILogger<T>` for logging; no `Console.WriteLine` in library code.
- Enable analyzers; treat warnings as errors in CI.
- Every new piece of business logic gets unit tests; wired components get integration tests.
- Use `Method_Scenario_ExpectedResult` test naming, Arrange-Act-Assert.

## Subagents (in .claude/agents/)
- `solution-architect` — solution/project structure & layering
- `backend-engineer` — domain, application services, Web API
- `data-engineer` — EF Core / Dapper persistence, migrations
- `security-engineer` — authn/authz (Identity/JWT/OIDC), secrets, hardening
- `desktop-ui-engineer` — WPF (MVVM) / WinForms
- `winui-maui-engineer` — WinUI 3 (Windows App SDK) / .NET MAUI
- `windows-service-engineer` — Worker / Windows Service background apps
- `console-cli-engineer` — console & CLI tools
- `interop-engineer` — P/Invoke, COM automation, native interop
- `blazor-engineer` — Blazor web UI (Server / WASM / Web App)
- `test-engineer` — unit tests (xUnit)
- `integration-test-engineer` — integration / E2E tests
- `build-deploy-engineer` — publish, package, CI/CD
- `code-reviewer` — quality, security, design review

Typical flow:
solution-architect -> (backend / data / security / desktop-ui / winui-maui /
windows-service / console-cli / blazor / interop)
-> test-engineer + integration-test-engineer -> code-reviewer -> build-deploy-engineer.

## Security ownership
- Authentication, authorization, and secret/data protection are owned by
  `security-engineer`. Other agents define auth abstractions in the Application
  layer and delegate the implementation. Enforce authorization on the server/API;
  never trust client-side checks. No secrets in source — `dotnet user-secrets`
  (dev), environment/vault (prod).

## Automation
- A SessionStart hook (`.claude/settings.json` -> `.claude/scripts/session_start.sh`)
  restores and builds the solution so a fresh session is ready to work on.
- Slash commands in `.claude/commands/`: `/scaffold-solution`, `/add-feature`, `/test-all`.
