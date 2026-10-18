# Fanus Architecture v1.0

## Three-Layer Decision

### Production Core
fanus/ ├── api/ ← REST endpoints ├── cognitive/ ← HayratJudge, fi_detector, PolicyEngine, ISPController ├── core/ ← Identity, Seal, Novayin ├── memory/ ← Ledger, Evidence, BeliefLayer, KnowledgeGraph ├── runtime/ ← FanusLoop, Observer, Safety ├── adapters/ ← LLM + Knowledge sources └── audit/ ← Fanus Verify (live: public `/demo/verify`, keyed `/verify`)
### Research Lab
archive/fanus-engine-legacy/ ← Legacy experiments, NOT imported by production (archived)
### Future Experiments
archive/fanus-v2-legacy/ ← Future architecture concepts (archived, separate from production)
---

## The Product Law

هر قابلیت جدید باید یکی از این سه ستون را تقویت کند:

1. **Verify** — بررسی صحت خروجی AI
2. **Research** — جستجو و اعتبارسنجی دانش
3. **Identity** — هویت پایدار و شاهد بودن

اگر هیچ‌کدام را تقویت نمی‌کند → وارد `fanus/` نمی‌شود.

---

## Current Status

| Layer | Status | Files |
|-------|--------|-------|
| Runtime | ✅ Stable | FanusLoop, Observer, Safety |
| Memory | ✅ Stable | 12 modules |
| Cognitive | ✅ Stable | HayratJudge, fi_detector, PolicyEngine |
| API | ✅ Live | 6 endpoint groups |
| Audit | ✅ Live | /demo/verify (public), /verify (API key) |
| SDK | 🔨 Building | API wrapper |

---

## Import Rules

- `fanus/` modules may import from each other
- `fanus/` never imports from `archive/` (superseded generations: `archive/fanus-engine-legacy/`, `archive/fanus-v2-legacy/`)
- New experimental modules are developed outside `fanus/` and graduate into it only after product validation
