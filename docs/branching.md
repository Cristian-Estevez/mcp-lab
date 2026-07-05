# Branching Model

## Branch structure

```
main                        ← stable, always runnable, tagged per phase
│
├── phase/1-core-server     ← one branch per phase
│   ├── feat/echo-tool      ← one branch per feature within a phase
│   ├── feat/static-resource
│   └── feat/summarize-prompt
│
├── phase/2-resources-prompts
├── phase/3-http-transport
├── phase/4-mcp-apps
└── phase/5-appsec
```

## Branch types

| Prefix | Cut from | Merges into | Strategy |
|--------|----------|-------------|----------|
| `phase/N-name` | `main` | `main` | merge commit |
| `feat/description` | current phase branch | current phase branch | squash |
| `fix/description` | current phase branch (or `main` for hotfixes) | same | squash |
| `docs/description` | `main` | `main` | squash |

## Rules

1. **Never commit directly to `main`.** All work goes through a phase or docs branch.
2. **Tag `main` after each phase merge.** Tags: `v1-core-server`, `v2-resources-prompts`, `v3-http-transport`, `v4-mcp-apps`, `v5-appsec`.
3. **Each phase branch must be independently runnable** before merging to `main`. Don't merge a broken phase.
4. **Feature branches are short-lived.** Open, implement one thing, squash-merge, delete.
5. **Phase branches are long-lived.** They accumulate all feat/* merges for that phase, then merge once to `main`.

## Tag naming

| Tag | Phase |
|-----|-------|
| `v1-core-server` | Phase 1 complete |
| `v2-resources-prompts` | Phase 2 complete |
| `v3-http-transport` | Phase 3 complete |
| `v4-mcp-apps` | Phase 4 complete |
| `v5-appsec` | Phase 5 complete |

## Example workflow

```bash
# Start a new feature in the current phase
git checkout phase/1-core-server
git checkout -b feat/echo-tool

# ... implement ...

git add server/tools/dummy.py
git commit -m "feat: add echo tool"

# Merge back (squash keeps phase branch history clean)
git checkout phase/1-core-server
git merge --squash feat/echo-tool
git commit -m "feat: add echo tool"
git branch -d feat/echo-tool

# When the phase is complete and independently runnable:
git checkout main
git merge --no-ff phase/1-core-server -m "phase 1: core server (tool, resource, prompt over stdio)"
git tag v1-core-server
git push origin main --tags
```
