---
title: TradingBot Release Operations
document_role: procedure
lifecycle: maintained
owner: release-tooling
last_modified_at: 2026-10-26T19:57:46+03:30
---

# TradingBot release operations

`git.bat` is the interactive Git Manager. `Invoke-TradingBotRelease.ps1` is the scripted release command. Both derive the project root from their own locations, so they work from the current checkout without a hard-coded drive path.

Open the interactive manager with:

```powershell
.\scripts\git\git.bat
```

`AGENTS.md` is optional. The launcher checks the menu file; PowerShell verifies the Git root and the `apps/chart` and `engine` directories. Paths containing spaces, parentheses, ampersands, and exclamation marks are supported. Git for Windows must be installed and `git.exe` must be on PATH.

Run the command above from the checkout root, or open the batch file by its actual location. A source-only folder without Git metadata is not a release checkout; use an existing Git checkout with its configured `origin` and branch history.

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File scripts\git\Invoke-TradingBotRelease.ps1
```

Run this validation command before publishing:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File scripts\git\Invoke-TradingBotRelease.ps1 -DryRun -CommitMessage "Validate release" -ReleaseTag "your-valid-unused-tag" -VerboseReport
```

`-DryRun` is a real, non-publishing validation. It does not stage the active index, create a permanent branch or tag, push, or create a GitHub Release. Missing message or tag values are prompted once; parameters support non-interactive use.

## Content policy

`main` is inclusion-first. Legitimate tests, maintained documentation, meaningful engineering evidence, meaningful Graphify reports/manifests/inventories, and classified `BaseLine` reference data remain eligible. The policy classifies files by producer, consumer, and enduring value rather than directory name.

Only narrowly proven disposable material is excluded: dependencies restored from manifests, build products, interpreter caches, temporary files, local secrets, and machine-local chart state. `apps/chart/state` is never copied to production; the launcher creates required directories at runtime without deploying current local contents.

The main release stops if an excluded artifact is already tracked, including one staged for modification. Staged removal of such an artifact is allowed. Eligible ZIP archives are checked for embedded cache, build, temporary, dependency, or unsafe parent-directory paths. The two historical project snapshots containing those entries remain on the workstation but are excluded from Git; archived test logs remain eligible as verification evidence.

`production` uses a dependency-derived runtime inventory from the exact committed main SHA. Every eligible file under the runtime-owned `apps/chart`, `engine`, and `scripts` roots is included, even if it is not imported yet. Import traversal validates dependencies and adds referenced paths; it does not decide whether a new runtime file is eligible. Tests, engineering evidence, Algorithm References, ZIP snapshots, local chart state, credentials, dependencies, and disposable artifacts remain excluded from production. The workflow replaces only a temporary worktree snapshot with the selected paths and checks policy, sensitive markers, PowerShell and JavaScript syntax, Python AST and bridge help, `npm ci`, and the chart build.

A new `engine/pipeline/xyz.py`, a new configuration file, or a renamed runtime folder is picked up automatically. Additions, modifications, renames, and deletions appear in the branch previews. Main includes all eligible project files; eligible files accidentally matching `.gitignore` are explicitly staged after policy and sensitive-content checks. Individual detector filenames are not a permanent production allowlist.

The production inventory is passed to Git as a UTF-8, NUL-delimited file of literal paths. Its size is independent of Windows' native command-line length limit, and filenames containing spaces, Unicode, or brackets retain their exact identities.

## Branch and authentication safety

The workflow reuses existing Git and GitHub CLI authentication without reading or storing credentials. It independently checks Git push authorization with a non-mutating dry-run.

`origin/production` is required. When local `production` is absent, the candidate starts from freshly fetched `origin/production` in a detached temporary worktree. Only after validation does the workflow advance local `production` with an expected-old-value guard and configure its `origin/production` upstream. Publication always uses explicit refspecs.

If local `production` has independent commits, the validated runtime snapshot gains a second parent that preserves that local history. Its tree remains the exact dependency-derived runtime file set. Promotion checks both parent histories and the unchanged local ref before advancing `production`; an operation without a new snapshot still requires a fast-forward production target.

Publication first uses one `git push --atomic` for `main`, `production`, and the annotated tag. If atomic push is unsupported, fallback is allowed only after every target remote ref is proven unchanged. The fallback verifies each ref immediately and stops with explicit partial-failure reporting; it never hides a partial result.

## Traceability and Recovery

Changed production content receives `TradingBot-Main-Source: <main SHA>` in its commit trailer. When the production tree is unchanged, no empty commit is made; the annotated tag and GitHub Release metadata carry that source SHA. The annotated tag always points to the exact production release commit.

If validation fails, inspect the reported policy, closure, or tool check and correct it before retrying. If publication reports partial failure, do not retry blindly: compare the reported remote `main`, `production`, and tag OIDs, reconcile the remote state deliberately, then rerun with a new unused tag only when appropriate. Temporary worktree cleanup is reported separately.

No publication occurs during implementation validation or `-DryRun`.

## Interactive Git Manager

Run `scripts\git\git.bat` from any working directory. It resolves this checkout from the batch file's own location. Menu option 4 previews the exact candidate paths without committing or publishing. The manager stops if local `main` is behind or diverged from remote `main`; it does not stash or merge user changes. A failed menu operation returns a nonzero process exit code after exit.

Choose **Main** to publish all eligible project changes to `main`, **Production** to publish the runtime snapshot, or **Both** to publish both branches. Preview Only follows the same current working-tree candidate for every target, including Production; it does not require those changes to be committed first. Production-only preview also shows which local main source changes that runtime snapshot would use. Previously staged deletions remain deletions, including a file deliberately removed from Git while retained locally.

The menu opens on any branch, including `production`, and without a configured `origin`. Keep the development checkout on `main`. Release operations require active `main`, a configured `origin`, and no unresolved index conflicts or pending merge, rebase, cherry-pick, or revert. The menu displays these blockers immediately. Do not manually merge `main` into the runtime-only `production` checkout: the manager prepares production in an isolated worktree and preserves its history. Generic conflicts still require an explicit resolution; the manager does not silently discard them. Main-only operations require `origin/main`; production and both require `origin/production` as well.

Production previews show the complete runtime inventory. Full production validation runs before the final confirmation and before permanent commits. Leaving the commit message empty uses `Update TradingBot project files` and includes current eligible working changes; it never silently omits new files. No empty commit is created when the source tree is unchanged. Production-only operations also prepare a local main source commit when needed, but push only production. A single Git tag always points to one commit; the Both tag option points to production and records its main source SHA. Publication uses explicit immutable commit/object IDs, verifies the preview baseline again, and checks all selected refs during sequential fallback.

Validation captures stdout and stderr concurrently, preserving multiline arguments and Unicode paths. This avoids stalls when a validator fills its stderr pipe and gives consistent diagnostics in Windows PowerShell 5.1 and PowerShell 7.

Run both focused test suites without publishing to the configured project remote:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File scripts\git\Test-GitManager.ps1
powershell.exe -NoProfile -ExecutionPolicy Bypass -File scripts\git\Test-ReleaseWorkflow.ps1
```

Tests use disposable local repositories and local bare remotes. They preserve the active checkout's index, branches, tags, and merge state. They do not prove live GitHub authorization or branch protection behavior.

Coverage includes a production inventory exceeding the Windows command-line limit and a real `git.bat` Both operation through commit, runtime validation, and push to a disposable local remote. That operation verifies new and ignored-but-eligible files, edits, renames, deletions, the different main/production content policies, and preservation of excluded local state.

The original [workflow design](RELEASE_WORKFLOW_DESIGN.md) and [implementation plan](IMPLEMENTATION_PLAN.md) are historical planning records. This README and the current scripts describe supported operations.

The `main` policy keeps historical Graphify reports and generated `graph.html` files as engineering evidence. Rebuildable `graphify-out/cache` and Vite `.vite` caches are excluded. Both automatic SonarQube Cloud analysis (`.sonarcloud.properties`) and CI scanner analysis (`sonar-project.properties`) analyze maintained source while excluding historical Engine copies, archives, verification evidence, and local chart state. Test sources are excluded only from duplication measurement. Git retains eligible evidence in `main`; `production` excludes the engineering tree. Check the remote Sonar quality gate after an authorized push.
