# Fanus Audit Findings Tracker

Evidence Before Abstraction — هر finding باید این زنجیره را طی کند:
Evidence → Boundary → Invariant → Test → Fix → Re-audit

| Finding | Evidence | Boundary | Invariant | Test | Fix | Re-audit |
|---------|----------|----------|-----------|------|-----|----------|
| F-10 | loop.py | Governor→Execution | locked ⇒ no execution | ✅ test_governance_order.py | ✅ | ⬜ |
| F-11 | loop.py | Governor→Execution | lock blocks execution | ✅ test_governance_order.py | ✅ | ⬜ |
| F-29 | api/auth.py + 12 mutating endpoints | Auth→Mutation | missing config ⇒ deny; ALL mutating POST require auth | ✅ test_auth_failsecure.py + test_api_auth_coverage.py | ✅ | ✅ (verified via full mutation-surface grep, 7 additional unprotected endpoints found and fixed beyond original 3) |
| F-08 | memory/persistence | Persistence boundary | restart ⇒ durable state | ⬜ | ⬜ | ⬜ |
| F-09 | memory/graph | API→Graph boundary | API reads canonical graph | ⬜ | ⬜ | ⬜ |
| F-12 | execution_layer.py | Stability→Execution | execution_limit enforced | ⬜ | ⬜ | ⬜ |
| F-13 | execution_layer.py | Execution→Mutation | semantics explicit (real vs recorded) | ⬜ | ⬜ | ⬜ |
| F-14 | semantic_validator.py | Authorization | unknown action ⇒ deny (not blacklist) | ⬜ | ⬜ | ⬜ |
| F-15 | runtime_hard_guard.py | Guard input boundary | guard sees full required state | ⬜ | ⬜ | ⬜ |

## قانون رسمی: Evidence Before Abstraction

1. هیچ claim مهمی بدون evidence کد verified محسوب نمی‌شود.
2. پیدا کردن یک enforcement point به معنی اثبات end-to-end coverage نیست.
3. هر invariant مهم باید یک regression test قابل اجرا داشته باشد.
4. هر boundary باید مشخص کند: چه کسی produce/validate/authorize/execute/mutate می‌کند، و چه کسی می‌تواند bypass کند.
5. هر چیز ناشناخته یا failure در مسیر safety/security: UNKNOWN/FAILURE/MISSING CONFIG/UNAUTHORIZED ⇒ DENY.
6. اسم component هرگز evidence نیست — تا implementation ثابت نکند، ادعای نقشش را نمی‌پذیریم.
7. اول audit، بعد redesign.


## F-29A / F-29B — Authorization split (per GPT/Memar review)

F-29A — Authentication: CLOSED
Evidence: all 12 mutating endpoints reject missing/invalid FANUS_API_KEY (401/503)
Test: test_auth_failsecure.py, test_api_auth_coverage.py

F-29B — Authorization (role/principal separation): DEFERRED / ACCEPTED FOR CURRENT THREAT MODEL
Current threat model: single-tenant, single human operator (Amin), single trusted API principal, no external users, no role hierarchy.
Decision: no multi-role RBAC introduced at this stage — would be premature engineering for a threat model that doesn't exist yet.
Re-open trigger: before introducing multi-user access, multi-tenancy, external clients, independent agents, privileged service identities, or autonomous execution reachable externally.

## F-30 — Test Scope Integrity

Evidence: reality-tests/ (created 24 Jun, predates STEP-based work) contains a separate adversarial/drift testing framework (drift-engine/, adversarial-set.json, scoring-rubric.md, stress-tests.md). run_drift_test.py fails to import (ModuleNotFoundError: drift_engine) — broken independently of tonight's changes.
Classification: separate/legacy test framework with pre-existing broken dependency, not part of production test suite.
Decision: pytest.ini scoping to tests/ is correct — reality-tests/ needs its own fix cycle, not silent inclusion in main CI.
Status: CLASSIFIED — reality-tests/ needs a future decision (repair vs archive), tracked separately from F-10/F-11/F-29.


## F-31 — Dormant Dangerous Code (self-modification / autonomous git / autonomous execution)

Evidence:
fanus/tools/git_guard.py (FanusGitGuard) — can run git add/commit/push origin main autonomously
fanus/evolution/self_modifying_agent.py (SelfModifyingAgent) — reads, backs up, and overwrites .py files, then commits via subprocess
fanus/evolution/self_improver.py (SelfImprover) — reads, backs up, and overwrites files
fanus/agent/action_executor.py (ActionExecutor) — generic execute(action)
fanus/core/plugin_system.py (PluginSystem) — dynamic importlib-based module loader

Verified via grep (correct class names, not guessed): none of these five classes are instantiated
or imported anywhere else in fanus/. No API route, no FanusLoop path, no plugin registration
calls PluginSystem() either — so its importlib.import_module() path is also unreachable.

Classification: DORMANT. Present in the repo, consistent with evolution_only_proposes philosophy
(capability built but deliberately not wired to runtime), but NOT currently reachable from any
entry point (API, CLI, loop).

Risk: LOW today, but HIGH latent risk — a single line adding instantiation/wiring would activate
autonomous file rewriting, autonomous git push to main, or dynamic arbitrary module loading,
without additional review since these files bypass FanusLoop's Governor/HardGuard chain entirely
(they are not part of the cognitive pipeline).

Decision: Do not delete yet (may represent intentional future capability per evolution philosophy).
Do not wire up yet (F-12/F-13 execution semantics must be resolved first, and F-29B authorization
model must be revisited before any real mutation capability is enabled).

Re-open trigger: before any of these five classes are instantiated/imported anywhere in fanus/,
a dedicated security review and explicit authorization boundary is required — these bypass the
Governor → HardGuard → Execution chain that F-10/F-11 hardened.


## F-31 UPDATE — three more dormant classes found

Verified via grep (correct class names): SelfRewriteEngine, RuntimeCompilerEngine,
CollapseSafetyGate — none referenced anywhere outside their own definition files.

fanus/runtime/self_rewrite_engine.py — dormant
fanus/runtime/runtime_compiler_engine.py — dormant
fanus/runtime/safety/collapse_safety_gate.py — dormant

Note: these three also define their own execution_limit values (0.2-0.6 range),
separate from self_stabilization_engine.py's _compute_execution_limit(). If any
of these are ever wired in, execution_limit semantics must be unified first —
otherwise multiple disconnected "limit" producers could conflict.

F-31 total dormant count: 7 classes (FanusGitGuard, SelfModifyingAgent, SelfImprover,
ActionExecutor, PluginSystem, SelfRewriteEngine, RuntimeCompilerEngine, CollapseSafetyGate)
