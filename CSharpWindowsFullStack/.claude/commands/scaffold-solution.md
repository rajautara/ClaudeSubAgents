---
description: Scaffold a new layered C# solution via the solution-architect subagent
argument-hint: <app-name> [host: console|wpf|winforms|worker|api|blazor|winui|maui]
---

Use the `solution-architect` subagent to scaffold a new solution for: `$ARGUMENTS`.

Create the layered structure (Domain / Application / Infrastructure / Host +
UnitTests / IntegrationTests), wire project references so dependencies flow
inward, and set up `Directory.Build.props`, `.editorconfig`, and `global.json`.
Use the `dotnet` CLI (`dotnet new sln`, `dotnet new <template>`, `dotnet sln add`,
`dotnet add reference`). Document the architecture in `docs/architecture.md`.
Define structure and contracts only — hand feature work off to the specialist
engineers.
