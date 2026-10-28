---
id: "workflow.project_release"
type: "workflow"
status: "active"
authority: "executable"
title: "Current project startup and release tooling"
version: "current"
related_entities: ["core.project","workflow.operating","workflow.release","source.local_server","source.chart_workspace"]
source_reference: ["06_SOURCE/Code/scripts/start.ps1","06_SOURCE/Code/scripts/launch.bat","06_SOURCE/Code/apps/chart/scripts/dev-server.mjs","06_SOURCE/Code/apps/chart/package.json","06_SOURCE/Code/scripts/git/README.md","06_SOURCE/Code/scripts/git/Release.Workflow.psm1","06_SOURCE/Code/scripts/git/Git.Menu.ps1","06_SOURCE/Code/scripts/git/production-policy.psd1","06_SOURCE/Code/scripts/git/Invoke-TradingBotRelease.ps1"]
evidence_basis: "Current live project Source captured for the 2026-10-27 synchronization"
created_at: "2026-10-27T20:16:20+03:30"
last_modified_at: "2026-10-27T20:16:20+03:30"
---

# Current project startup and release tooling

This is an executable tooling description, subordinate to current user authorization and project instructions. It grants no permission to stage, commit, push, tag, publish or install software.

## Startup

The Windows launch paths derive the checkout from their own location. Startup checks maintained application/Engine anchors, runtime prerequisites and declared dependencies; it can install missing dependencies before launching Vite. The same application resolver constrains local state to the dedicated Chart-owned subtree and creates required state directories there. The launcher configures Python without bytecode writes and uses the native Vite configuration loader for shared-drive compatibility.

The development wrapper forwards arguments/environment to the installed Vite executable. Default filesystem watching is disabled for the supported shared-folder environment; polling is explicit configuration. Runtime/package versions and dependency inventories must be read from the current manifest/launcher rather than treated as permanent knowledge rules.

## Separate main and production policy

The interactive Git Manager supports Main, Production, Both, Preview Only and Dry Run. The scripted release command supplies the maintained noninteractive release workflow. Script locations and Git metadata establish the root; a source-only folder without Git metadata is not a release checkout.

Main is inclusion-first for eligible source, tests, maintained documentation and meaningful evidence. Narrowly classified dependencies, builds, caches, temporary files, credentials and machine-local state are excluded. Curated baseline RAW has a separate eligibility rule. Tracked excluded artifacts and unsafe embedded archive entries block preparation; existing staged deletions remain deletions.

Production is a runtime snapshot from an exact main source commit. Eligibility comes from runtime-owned roots and policy exclusions, while import traversal validates/adds dependencies. It is not a permanent detector/module allowlist. Tests, engineering evidence, Algorithm References and workstation state are excluded. The runtime inventory is passed as literal UTF-8 NUL-delimited paths so growing inventories and special filenames retain their identity.

## Validation and history protection

The tooling checks active main, unresolved/in-progress Git operations, configured remotes and current histories. Candidate preparation uses separate indexes and detached temporary worktrees to preserve the active checkout. Runtime snapshot validation checks exact selected tree, state/secret policy, source syntax, bridge help, lockfile install and Chart build before promotion/publication.

Local production history is preserved when required by the snapshot parents. Permanent branch advancement uses an expected-old-value guard and remote baselines are rechecked. Unchanged trees do not require empty commits. Production provenance records the exact main source identity; release tags point to their intended prepared target.

The interactive workflow validates the concrete production candidate before final confirmation and verifies preview baselines again before permanent publication. Dry Run/Preview do not publish permanent refs or GitHub Releases.

## Publication and evidence limits

Publication uses explicit ref targets, attempts atomic push, and permits guarded sequential fallback only when the unsupported atomic attempt left all target refs unchanged. Each fallback step verifies the expected remote state; partial/indeterminate failure remains visible. GitHub release creation is separate from successful ref publication and cannot be assumed after a partial result.

Focused release/Git Manager suites use disposable local repositories and bare remotes. They can establish policy, snapshot, quoting, race-guard, validation-gate and local publication behavior. They do not establish live GitHub credentials, branch protections or release readiness for the active checkout. Publication still requires explicit current-task user authorization.

