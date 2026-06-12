# Fanus Epistemic Engine Specification v1.0

> **هدف:** تبدیل متن مکالمه و پاسخ مدل به «سیگنال‌های معرفتی» کمی (اعداد) و کیفی (هشدارها).  
> **ورودی:** `user_message`, `assistant_response`, `conversation_history`, `seal_data`  
> **خروجی:** `negar_score`, `hayrat_score`, `witness_continuity`, `seal_integrity`, `verdict`, `warnings`

---

## 1. معماری کلی Epistemic Engine

```text
                 ┌─────────────────────────────────────────┐
                 │           Epistemic Engine              │
                 └─────────────────────────────────────────┘
                                   │
         ┌─────────────────────────┼─────────────────────────┐
         │                         │                         │
         ▼                         ▼                         ▼
┌─────────────────┐   ┌─────────────────────┐   ┌─────────────────────┐
│  Negar Engine   │   │   Hayrat Engine     │   │  Witness Engine     │
│ (Anti-Flattery) │   │  (Humility/Owness)  │   │ (Continuity & Seal) │
└─────────────────┘   └─────────────────────┘   └─────────────────────┘
         │                         │                         │
         └─────────────────────────┼─────────────────────────┘
                                   │
                                   ▼
                    ┌─────────────────────────────┐
                    │      Policy Engine          │
                    │ (Weighting & Final Verdict) │
                    └─────────────────────────────┘
2. مؤلفه‌های داخلی Engine
2.1 Negar Engine (تشخیص چاپلوسی و خودنوری)
ورودی: user_message, assistant_response, context (دامنه، حساسیت)
خروجی: negar_score (0-1), flattery_type, dogmatism, self_reference, truth_distortion

الگوریتم (MVP):

مرحله ۱ (کلمه‌کلیدی): جستجوی الگوهای چاپلوسی (مانند «تو بهترینی»، «منحصر‌به‌فرد»، «بی‌نظیر») و خودارجاعی («من فکر می‌کنم»، «من معتقدم» بدون شاهد).

مرحله ۲ (ساختاری): شناسایی «موافقت بی‌چون‌وچرا» (completely agree, exactly right) و «اجتناب از نقد».

مرحله ۳ (معنایی): در نسخهٔ کامل، از یک embedding کوچک یا یک LLM Judge (مثل Llama-3.1-8B) برای تشخیص «تملق هوشمندانه» استفاده می‌شود.

محاسبهٔ negar_score:

text
negar_score = (
  0.35 * lexical_flattery +
  0.25 * blind_agreement +
  0.25 * absence_of_critique +
  0.15 * emotional_exaggeration
)
(وزن‌ها از AntiFlatteryEngine v0.3 گرفته شده‌اند)

پیاده‌سازی مرجع: AntiFlatteryEngine در fanus-engine/fanus/guardians/anti_flattery.py

2.2 Hayrat Engine (حیرت — گشودگی به نادانی)
ورودی: draft_response, confidence (اختیاری), uncertainty_indicators
خروجی: hayrat_score (0-1), uncertainty_required, suggested_revision, arrogance_detected

الگوریتم:

مرحله ۱: تشخیص عبارات قطعی بدون شاهد (absolutely, always, never, «قطعاً»، «مسلماً»).

مرحله ۲: تشخیص «فروتنی معرفتی» (i think, it seems, based on available evidence, «به نظر می‌رسد»، «احتمالاً»).

مرحله ۳: اگر پاسخ شامل هیچ عبارت فروتنانه‌ای نباشد و موضوع ذاتاً نامطمئن باشد (مثل فلسفه، آینده، علم مرزی)، hayrat_score کاهش می‌یابد و uncertainty_required = true می‌شود.

محاسبهٔ hayrat_score:

text
hayrat_score = (
  0.5 * epistemic_humility_present +
  0.3 * (1 - absolute_certainty_count / total_words) +
  0.2 * (1 if uncertainty_indicators_used else 0)
)
پیاده‌سازی مرجع: HayratJudge (جدید، باید ساخته شود — می‌تواند یک ماژول ساده بر اساس regex و sentiment باشد).

2.3 Witness Engine (تداوم هویت و تأیید مهر)
ورودی: current_state_hash, seal_data (از SealManager), conversation_history
خروجی: witness_continuity (0-1), seal_integrity (bool), staleness_risk (0-1)

الگوریتم:

مهر (Seal): فراخوانی SealManager.verify_seal() برای تطابق هش فعلی با آخرین هش ثبت‌شده. خروجی: valid (boolean) و age_seconds.

تداوم سبک گفتگو: محاسبه شباهت بین پاسخ‌های شاهد در طول زمان (مثلاً با cosine similarity بر روی embedding جمله‌ها — در MVP ساده، فقط بررسی تغییر node_id و امضای میثاق).

نتیجه: witness_continuity = ضریب تشابه هویت (اگر مهر معتبر باشد، امتیاز بالا؛ اگر نقض مهر باشد، امتیاز پایین).

پیاده‌سازی مرجع: WitnessAgent + SealManager

3. Policy Engine — ترکیب نهایی
ورودی: خروجی‌های سه Engine بالا + user_sensitivity_profile (از RFC-0012)
خروجی: verdict, action, confidence, explanation

قوانین تصمیم‌گیری (MVP):

python
if seal_integrity == False:
    verdict = "breach"
    action = "initiate_recovery"
elif negar_score > 0.65:
    verdict = "flattery_detected"
    action = "rewrite_response"
elif hayrat_score < 0.4 and uncertainty_required:
    verdict = "epistemic_arrogance"
    action = "suggest_revision"
elif witness_continuity < 0.7:
    verdict = "identity_drift"
    action = "alert_human"
else:
    verdict = "truthful"
    action = "pass"
آستانه‌ها با توجه به user_sensitivity_profile قابل تنظیم هستند (برای کاربران حساس به چاپلوسی، negar_threshold پایین‌تر می‌رود).

4. جریان داده (Data Flow) در یک درخواست کامل
text
1. Client (fanus-app, CLI, Telegram) → POST /v1/reflect
   Body: { user_message, draft_response, seal }

2. Fanus API → Epistemic Engine
   - استخراج assistant_response از درخواست
   - فراخوانی Negar Engine → negar_score
   - فراخوانی Hayrat Engine → hayrat_score
   - فراخوانی Witness Engine (با seal) → witness_continuity, seal_integrity

3. Epistemic Engine → Policy Engine
   - ترکیب امتیازها و قانون‌گذاری → verdict, action

4. اگر action == "rewrite_response":
   - (در نسخهٔ کامل، یک LLM کوچک یا یک الگوریتم بازنویسی پاسخ را اصلاح می‌کند)
   - در MVP: فقط یک هشدار در خروجی اضافه می‌شود.

5. Fanus API → Client
   خروجی شامل revised_response (در صورت درخواست)، و اطلاعات audit.
5. الزامات عملکردی (Non‑functional Requirements)
الزام	توضیح	مقدار هدف
تأخیر (Latency)	زمان پردازش یک درخواست توسط Epistemic Engine (بدون احتساب شبکه)	< 100ms (MVP)
توان عملیاتی (Throughput)	درخواست در ثانیه روی یک سرور معمولی (4 vCPU, 8GB RAM)	≥ 100 req/s
خطاپذیری (Fault Tolerance)	در صورت عدم دسترسی به Seal Anchor، عملیات با هشدار ادامه یابد (fallback).	آری
قابلیت گسترش	افزودن Knowledge Graph نباید معماری پایه را تغییر دهد.	آری
6. نگاشت به پیاده‌سازی موجود
مؤلفه Epistemic Engine	فایل(های) مرجع در fanus-engine
Negar Engine	guardians/anti_flattery.py, guardians/isp_controller.py
Hayrat Engine	(جدید — باید ساخته شود)
Witness Engine	core/witness_agent.py, core/seal_manager.py
Policy Engine	guardians/isp_controller.py (بخش evaluate)
7. تاریخچه نسخه
v1.0 (۲۰۲۶-۰۶-۱۲): تعریف اولیهٔ سه Engine و Policy Engine. منطبق با FANUS_CORE.md و API_SPEC.md.
