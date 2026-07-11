# Fanus Architecture v1.0

## Three-Layer Decision

### Production Core
fanus/ ├── api/ ← REST endpoints ├── cognitive/ ← HayratJudge, fi_detector, PolicyEngine, ISPController ├── core/ ← Identity, Seal, Novayin ├── memory/ ← Ledger, Evidence, BeliefLayer, KnowledgeGraph ├── runtime/ ← FanusLoop, Observer, Safety ├── adapters/ ← LLM + Knowledge sources └── audit/ ← Fanus Verify (در حال ساخت)
### Research Lab
fanus-engine/ ← Legacy experiments, NOT imported by production
### Future Experiments
fanus-v2/ ← Future architecture concepts
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
| Memory | ✅ Stable | 10 modules |
| Cognitive | ✅ Stable | HayratJudge, fi_detector, PolicyEngine |
| API | ✅ Live | 6 endpoint groups |
| Audit | 🔨 Building | /verify endpoint |
| SDK | 🔨 Building | API wrapper |

---

## Import Rules

- `fanus/` modules may import from each other
- `fanus/` never imports from `fanus-engine/` or `fanus-v2/`
- New modules enter `fanus-engine/` first, graduate to `fanus/` only after product validation
