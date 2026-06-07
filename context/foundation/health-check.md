---
project: tenx_cards
checked_at: 2026-06-07T00:00:00Z
health_status: needs-attention
context_type: brownfield
language_family: python
stack_assessment_available: false
checks_run:
  - lockfile
  - dependency_audit
  - outdated_deps
  - test_runner
  - ci_cd
  - configuration
audit_findings:
  critical: 0
  high: 0
  moderate: 0
  low: 0
test_runner_detected: true
ci_provider: null
recommended_fixes: 7
---

## Dependency Health

### Lockfile

Status: present (requirements.txt only, weak lock)
Package manager: pip

`requirements.txt` exists, but this is not a strict lockfile with hash pinning. Builds are reproducible only partially.

### Security Audit

Tool: `pip-audit --format json`
Status: failed to run
Reason: `No module named pip_audit` in the active project environment.

No severity counts are available because the audit tool is missing.

### Outdated Dependencies

Packages with major version gaps: 1

- gunicorn: 23.0.0 -> 26.0.0 (3 major versions behind)

Other packages are behind by patch/minor versions (Django, psycopg, psycopg-binary, pip).

## Test Suite

Test runner: Django unittest (via `manage.py test`)
Tests found: 14 tests
Test execution: passing

Configuration: Django test discovery in app test modules.
Framework: unittest runner managed by Django.

## CI/CD

Provider: not detected
Configuration: not found

| Stage | Status | Notes |
|---|---|---|
| Lint | ✗ | not configured |
| Test | ✗ | no CI pipeline file found |
| Build | ✗ | no CI pipeline file found |
| Type check | ✗ | not configured |
| Security | ✗ | no CI pipeline file found |

No CI/CD configuration detected. You'll set this up in the infrastructure and deployment lesson. For now, a local test runner is sufficient for agent collaboration.

## Configuration

### High severity

- `.gitignore` missing at repository root. Impact: generated artifacts and secrets can be committed accidentally. Fix: add a Python/Django `.gitignore` immediately.

### Medium severity

- No dedicated lint/format/type configuration (`ruff`, `flake8`, `black`, `mypy`, or equivalent). Impact: inconsistent style and lower reliability of agent-generated changes. Fix: add at least one formatter/linter baseline.
- Dependency audit tool is not installed (`pip-audit`). Impact: no visibility into known vulnerabilities before agent changes. Fix: install `pip-audit` in project environment.

### Low severity

- `.editorconfig` missing. Impact: inconsistent editor behavior across environments. Fix: add minimal `.editorconfig`.
- `.env.example` / `.env.template` missing. Impact: unclear environment contract for contributors and agents. Fix: add documented environment variable template.

## Stack Assessment Cross-Reference

No `context/foundation/stack-assessment.md` found. Run `/10x-stack-assess` for quality-gate analysis.

## Recommended Fixes

### Fix before agent work (Category A)

### 1. Add repository `.gitignore`

**Impact**: protects the repo from leaking local files/secrets and stabilizes agent workflows.
**Severity**: high
**Effort**: quick (< 5 min)
**Fix**:

Create `.gitignore` with Python/Django essentials (`.venv/`, `__pycache__/`, `*.pyc`, `db.sqlite3`, `.env`, `.pytest_cache/`).

### 2. Install and run dependency audit

**Impact**: without a vulnerability baseline, agent changes may unknowingly build on unsafe dependencies.
**Severity**: medium
**Effort**: quick (< 5 min)
**Fix**:

```powershell
.venv/Scripts/python.exe -m pip install pip-audit
.venv/Scripts/python.exe -m pip_audit --format json
```

### 3. Reduce major dependency gap for gunicorn

**Impact**: large version gaps increase upgrade risk and future breakage during agent-driven refactors.
**Severity**: medium
**Effort**: moderate (15-30 min)
**Fix**:

```powershell
.venv/Scripts/python.exe -m pip install "gunicorn>=26,<27"
.venv/Scripts/python.exe -m pip freeze > requirements.txt
.venv/Scripts/python.exe manage.py check
.venv/Scripts/python.exe manage.py test cards
```

### 4. Add minimal lint/format baseline

**Impact**: consistent style and static checks improve reliability of generated code.
**Severity**: medium
**Effort**: moderate (15-30 min)
**Fix**:

```powershell
.venv/Scripts/python.exe -m pip install ruff
```
Then add `ruff` config (for example in `pyproject.toml`) and run checks in local workflow.

### 5. Add `.editorconfig`

**Impact**: prevents formatting drift between environments and tools.
**Severity**: low
**Effort**: quick (< 5 min)
**Fix**:

Create `.editorconfig` with UTF-8, final newline, spaces, and 4-space indentation for Python.

### 6. Add `.env.example`

**Impact**: makes environment contract explicit for you and future agent sessions.
**Severity**: low
**Effort**: quick (< 5 min)
**Fix**:

Create `.env.example` listing required variables (`SECRET_KEY`, `DATABASE_URL`, etc.) with placeholder values.

### Addressed in upcoming lessons (Category B)

### CI/CD pipeline missing

**Lesson**: [Sprint Zero z Agentem: infrastruktura, walking skeleton i pierwszy deploy (M1L5)](https://platforma.przeprogramowani.pl/external/10xdevs-3/m1-l5)
**What you'll do there**: set up CI/CD checks (lint/test/build/security) and deployment automation.

### Agent instruction file maturity

**Lesson**: [Agent Onboarding: Agents.md, AI Rules i feedback loops (M1L4)](https://platforma.przeprogramowani.pl/external/10xdevs-3/m1-l4)
**What you'll do there**: formalize AI workflow rules and feedback loops for stable agent collaboration.

## Summary

Health status: needs-attention.

Project core is stable: Django checks pass and 14 tests run successfully with the built-in runner. Main gaps are operational hygiene before deeper agent work: missing `.gitignore`, missing vulnerability audit tool, and no lint/type baseline yet. Address Category A fixes first, then proceed to agent onboarding with a much more reliable day-to-day workflow.

Next step: apply high-priority fixes above, then continue into agent onboarding (M1L4).
