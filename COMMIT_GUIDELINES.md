# Git Commit Message Best Practices for cvpysdk

## Why Commit Messages Matter

A well-crafted commit message is the best way to communicate **context** about a change to other developers — and to your future self. Tools like `git log`, `git blame`, and `git bisect` become powerful only when commit messages are meaningful. A diff tells you *what* changed; a good commit message tells you *why*.

## The Problem Today

Nearly all commits in this repository use a generic message:

```
Commvault weekly update DD-MM-YYYY
```

This pattern discards critical context. A commit adding an entirely new PowerBI module looks identical to one fixing a single typo. Anyone reviewing history, tracking regressions, or onboarding to the project gets no useful signal from `git log`.

---

## Commit Message Structure

Every commit message should follow this structure:

```
<type>(<optional scope>): <short summary>
                                          ← blank line
<optional body>
                                          ← blank line
<optional footer(s)>
```

### The Subject Line

| Rule | Guideline |
|---|---|
| **Length** | 50 characters or fewer preferred; hard limit at 72 |
| **Capitalization** | Do not capitalize the first word after the type prefix |
| **Punctuation** | No period at the end |
| **Mood** | Use imperative mood ("add feature", not "added feature") |
| **Content** | Describe *what* the commit does, not *how* |

### The Body (optional but encouraged)

- Separate from subject with a blank line
- Wrap lines at 72 characters
- Explain **why** the change was made, not just what changed
- List major items if the commit touches multiple areas

### The Footer (optional)

- Reference issue/ticket numbers: `Refs: JIRA-1234`
- Note breaking changes: `BREAKING CHANGE: removed deprecated auth method`

---

## Conventional Commits

This document recommends adopting the [Conventional Commits](https://www.conventionalcommits.org/) specification (v1.0.0). Conventional Commits provide a lightweight convention on top of commit messages that:

- Makes commit history readable at a glance
- Enables automated changelog generation
- Enables automated semantic versioning (`feat` = minor bump, `fix` = patch bump)
- Provides a shared vocabulary across the team

### Type Prefixes

| Type | When to Use | Example |
|---|---|---|
| `feat` | A new feature or module | `feat: add PowerBI instance and subclient` |
| `fix` | A bug fix | `fix: correct usergroup permission flag typo` |
| `refactor` | Code restructuring (no behavior change) | `refactor: simplify cloud discovery connection handling` |
| `docs` | Documentation changes only | `docs: update README with SP34 install instructions` |
| `test` | Adding or updating tests | `test: add unit tests for plan.py storage policy lookup` |
| `chore` | Build, CI, dependencies, tooling | `chore: update setup.py dependency versions` |
| `perf` | Performance improvement | `perf: batch API calls in commcell agent discovery` |

### Scope (Optional)

Scope identifies the area of the codebase affected. For cvpysdk, good scopes include the module or subsystem name:

```
feat(client): add network throttling configuration methods
fix(storage_policies): handle missing retention rule gracefully
refactor(cloudapps): extract common auth logic to base class
```

---

## Dos and Don'ts

### Do: Write specific, descriptive subject lines

```
# GOOD
feat(client): add network throttling configuration methods
fix(security): correct usergroup permission bitmask
feat(cloudapps): add PowerBI backup and restore subclient
refactor(discovery): rewrite cloud connection module for clarity
docs: update README with SP34 installation instructions
```

```
# BAD
Commvault weekly update 06-02-2026
weekly update
update
fix
changes
11.32.6
misc fixes
Update README.rst
```

### Do: Use the imperative mood (read as "This commit will...")

```
# GOOD — reads as "This commit will add PowerBI subclient support"
feat: add PowerBI subclient support

# BAD
feat: added PowerBI subclient support
feat: adding PowerBI subclient support
feat: PowerBI subclient support was added
```

### Do: Include a body for non-trivial changes

```
# GOOD
feat(cloudapps): add PowerBI instance and subclient support

Add the ability to back up and restore PowerBI workspaces.

- New PowerBIInstance class with configure/discover methods
- New PowerBISubclient with backup/restore operations
- New constants module for PowerBI API mappings
- Update services.py with PowerBI endpoint routes

Refs: JIRA-4521
```

```
# BAD — 458 insertions across 13 files with no explanation
Commvault weekly update 30-01-2026
```

### Do: Break large changes into focused commits

```
# GOOD — one logical change per commit
574a3f1 feat(cloudapps): add PowerBI instance class
8e2c0b3 feat(cloudapps): add PowerBI subclient and constants
a91d4c7 feat(client): add new configuration methods for PowerBI
c3f78e2 fix(security): correct usergroup permission flag

# BAD — unrelated changes lumped together
e73cd71 Commvault weekly update 06-02-2026
         (touches cloud discovery, Teams, eDiscovery, exception handling
          — 874 insertions, 352 deletions)
```

### Do: Reference tickets or issues

```
# GOOD
fix(plan): handle missing storage policy in plan creation (#142)

# GOOD (in footer)
feat(client): add laptop backup configuration

Refs: JIRA-4521
```

```
# BAD — no way to trace why the change was made
fix stuff
```

### Don't: Use generic or date-based messages

```
# BAD
Commvault weekly update 06-02-2026
weekly changes
misc updates
WIP
```

### Don't: Exceed 72 characters in the subject line

```
# BAD — too long, gets truncated in git log and GitHub
feat(cloudapps): add PowerBI instance subclient constants and update services routes and client configuration

# GOOD — concise subject, details in body
feat(cloudapps): add PowerBI backup and restore support

- New instance, subclient, and constants modules
- Update services.py with PowerBI API routes
- Extend client.py configuration methods
```

### Don't: Mix unrelated changes in a single commit

```
# BAD — different concerns with no way to revert independently
Commvault weekly update 06-02-2026
  (modifies: cloud_discovery_connections.py, teams_subclient.py,
   ediscovery_constants.py, exception.py, download.py)

# GOOD — each concern is isolated
a1b2c3d refactor(discovery): rewrite cloud connection handling
d4e5f6a feat(teams): add new configuration constants
7g8h9i0 feat(ediscovery): add hold and collection error types
```

---

## Adapting the Weekly Workflow

If the team continues to batch changes weekly, commit messages should still describe content, not cadence. The date a commit was made is already recorded in Git metadata — putting it in the message wastes the most valuable line.

**Before (current practice):**

```
Commvault weekly update 30-01-2026
```

**After (same weekly workflow, better messages):**

```
feat(cloudapps): add PowerBI instance and subclient support
feat(client): add network throttle and laptop config methods
fix(security): correct usergroup permission flag typo
```

If a single weekly PR genuinely contains one atomic change, a single descriptive commit is fine. But when 13 files across 5 subsystems change, those should be separate commits.

---

## Quick Reference Card

```
<type>(<scope>): <imperative summary, ≤50 chars>

<body: what and why, wrapped at 72 chars>

<footer: Refs, BREAKING CHANGE>
```

| Check | Rule |
|---|---|
| Subject ≤ 72 chars? | Hard limit |
| Imperative mood? | "add", not "added" |
| Type prefix? | `feat`, `fix`, `refactor`, `docs`, `test`, `chore`, `perf` |
| Body explains *why*? | For non-trivial changes |
| One logical change? | Don't mix unrelated work |
| Ticket referenced? | When applicable |

---

## References

- [Conventional Commits v1.0.0](https://www.conventionalcommits.org/) — The full specification for structured commit messages
- [How to Write a Git Commit Message](https://cbea.ms/git-commit/) — Chris Beams' widely-referenced guide on the 7 rules
- [Git Documentation: git-commit](https://git-scm.com/docs/git-commit) — Official Git reference
