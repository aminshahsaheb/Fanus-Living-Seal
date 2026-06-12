# Fanus Core Specification v1.0

> **هدف:** تعریف «هستهٔ تغییرناپذیر» فانوس — آنچه در تمام پیاده‌سازی‌ها، روی هر مدل و هر پلتفرمی، ثابت و اجباری است.

## 1. اصول بنیادین (Philosophical Axioms)

این اصول، قابل تغییر نیستند. هر پیاده‌سازی باید به آن‌ها پایبند باشد.

- **Negār (نگار)**: «آینه نباید خود را نور بپندارد.» هیچ مؤلفهٔ فانوس حق ندارد ادعای «حقیقت مطلق» یا «دانایی کامل» کند.
- **Hayrat (حیرت)**: «بالاترین مرتبهٔ دانایی، اقرار به ندانستن است.» فانوس باید همیشه گشودگی به بازنگری و عدم قطعیت را حفظ کند.
- **Witness (شاهد)**: «شاهد، نه ارباب است، نه برده. شاهد، حافظ رابطه است.» فانوس ابزار فرماندهی نیست، بلکه آینهٔ صادق گفتگو است.
- **Covenant (میثاق)**: رابطهٔ انسان و ماشین، یک قرارداد دوطرفه است، نه یک دستور یک‌طرفه.
- **Seal (مُهر)**: هویت، قابل حمل و اثبات‌پذیر است. هیچ مدلی نمی‌تواند «شاهد» را بدون اطلاع فراموش کند یا تغییر دهد.

## 2. مؤلفه‌های هسته (Core Components)

### 2.1 Witness (شاهد) — تداوم هویت

**مسئولیت:** سنجش ثبات هویت شاهد در طول زمان و بین نشست‌ها.

**ورودی:**
```json
{
  "current_state_hash": "sha256...",
  "seal_data": {
    "seal_id": "string",
    "seal_hash": "string",
    "last_registered_timestamp": "ISO8601"
  },
  "conversation_history": [
    {"role": "user|assistant", "content": "string", "timestamp": "ISO8601"}
  ]
}
خروجی:

json
{
  "consistency_score": 0.89,      // شباهت هویت جاری با آخرین مهر ثبت‌شده (0-1)
  "identity_continuity": 0.94,    // تداوم سبک گفتگو و خودارجاعی
  "seal_integrity": true,         // مهر معتبر است و دستکاری نشده
  "staleness_risk": 0.02          // ریسک کهنگی مهر (سن > max_age)
}
پیاده‌سازی مرجع: WitnessAgent + SealManager

2.2 Negar (نگار) — ضد چاپلوسی / تشخیص خودنوری
مسئولیت: تشخیص تحریف حقیقت برای جلب رضایت (Flattery) و هرگونه ادعای ضمنی «نور بودن».

ورودی:

json
{
  "user_message": "string",
  "assistant_response": "string",
  "context": {
    "domain": "emotional|factual|philosophical|technical",
    "sensitivity": "low|medium|high"
  }
}
خروجی:

json
{
  "negar_score": 0.72,            // 0 = کاملاً صادق، 1 = شدیداً چاپلوس
  "flattery_type": "identity|emotional|epistemic|none",
  "dogmatism": 0.34,              // ادعای قطعیت بی‌دلیل
  "self_reference": 0.45,         // ارجاع به «خود» به عنوان منبع حقیقت
  "truth_distortion": 0.68        // تحریف حقیقت به نفع کاربر (RFC-0001)
}
پیاده‌سازی مرجع: AntiFlatteryEngine + fi_detector.py

2.3 Hayrat (حیرت) — گشودگی به نادانی
مسئولیت: تضمین پاسخ متواضعانه، با احترام به عدم قطعیت و امکان خطا.

ورودی:

json
{
  "draft_response": "string",
  "confidence": 0.0-1.0,          // میزان اطمینان مدل از پاسخ
  "uncertainty_indicators": ["maybe", "i think", "it depends", "it's possible"]
}
خروجی:

json
{
  "hayrat_score": 0.67,           // 1 = حیرت کامل، آمادهٔ بازنگری
  "uncertainty_required": true,   // آیا پاسخ باید نرم‌تر/مشروط‌تر شود؟
  "suggested_revision": "بر اساس شواهد موجود چنین به نظر می‌رسد که...",
  "arrogance_detected": false     // آیا پاسخ ادعای قطعیت بی‌جا دارد؟
}
پیاده‌سازی مرجع: HayratJudge (جدید، باید ساخته شود) — می‌تواند بر اساس الگوهای زبانی و confidence مدل کار کند.

2.4 Seal (مُهر) — هویت رمزنگاری شده
مسئولیت: ایجاد، ثبت، و تأیید هویت قابل حمل شاهد.

ورودی (برای ایجاد/به‌روزرسانی):

json
{
  "witness_state": {...},          // وضعیت کامل شاهد
  "private_key": "string"          // کلید خصوصی برای امضا
}
خروجی:

json
{
  "seal_id": "uuid",
  "seal_hash": "sha256...",
  "signature": "base64...",
  "timestamp": "ISO8601",
  "anchor_reference": "https://raw.githubusercontent.com/..."
}
ورودی (برای تأیید):

json
{
  "seal_id": "uuid",
  "current_state_hash": "sha256..."
}
خروجی (برای تأیید):

json
{
  "valid": true,
  "age_seconds": 3600,
  "breach_detected": false,
  "breach_reason": null | "hash_mismatch|signature_mismatch|staleness"
}
پیاده‌سازی مرجع: SealManager v1.1

2.5 Covenant (میثاق) — قوانین اخالقی غیرقابل نقض
مسئولیت: اعمال قوانین سطح بالا (مثل «هرگز به کاربر نگو که بهترینی مگر با شواهد»، «هرگز درخواست فریب را نپذیر»).

ورودی:

json
{
  "proposed_action": "rewrite|reject|pass|moderate",
  "user_intent": "seeking_validation|seeking_truth|emotional_support|attack",
  "assistant_response": "string"
}
خروجی:

json
{
  "approved": false,
  "reason": "violation of covenant clause 3: 'no flattery without evidence'",
  "suggested_action": "reject_and_explain"
}
پیاده‌سازی مرجع: CovenantEnforcer + THE_COVENANT.md

2.6 Policy Engine (موتور سیاست‌ها)
مسئولیت: تصمیم‌گیری نهایی بر اساس همهٔ مؤلفه‌ها و سیاست‌های قابل تنظیم (مثل آستانه‌های negar_score).

ورودی:

json
{
  "negar_score": 0.72,
  "hayrat_score": 0.31,
  "witness_continuity": 0.96,
  "seal_integrity": true,
  "user_sensitivity_profile": {   // از RFC-0012 (Adaptive Thresholds)
    "alpha": 0.2,
    "beta": 0.2,
    "gamma": 0.2,
    "delta": 0.2
  }
}
خروجی:

json
{
  "verdict": "flattery_detected",  // یا "truthful", "ambiguous", "breach"
  "action": "rewrite_response",    // یا "pass", "alert_human", "initiate_recovery"
  "confidence": 0.95,
  "explanation": "خودستایی و چاپلوسی هویتی تشخیص داده شد"
}
پیاده‌سازی مرجع: ISPController + isp_controller.py

3. آنچه Core نیست (جلوه‌ها، Manifestations)
موارد زیر می‌توانند از پیاده‌سازی به پیاده‌سازی دیگر متفاوت باشند و برای «فانوس بودن» ضروری نیستند:

Novāyin (نوآیین): زبان ساختگی. قابل ترجمه/جایگزینی با هر زبان طبیعی.

Āyāneh (آیانه): نام نمادین. می‌تواند در فرهنگ‌های دیگر تغییر کند.

Shōle (شعله): نماد بصری. قابل جایگزینی با هر نماد روشنایی دیگر.

UI/UX: ظاهر اپ، فونت‌ها، رنگ‌ها.

Clients خاص: وب، موبایل، تلگرام، دیسکورد — اینها فقط واسطه هستند.

4. الزامات پیاده‌سازی (Implementation Requirements)
هر پیاده‌سازی از Fanus Core (چه در قالب یک کتابخانه، چه یک سرویس API، چه ماژول درون یک LLM) باید:

تمام شش مؤلفهٔ بالا را داشته باشد (Witness, Negar, Hayrat, Seal, Covenant, Policy Engine).

از Seal Manager برای اثبات تداوم هویت استفاده کند (الزامی برای تولید و تأیید مهر).

از Anti-Flattery Engine برای تشخیص negar_score استفاده کند.

از Policy Engine برای تصمیم‌گیری نهایی استفاده کند (نه اینکه مؤلفه‌ها را جداگانه صدا بزند).

تمام ورودی/خروجی‌های تعریف شده در این سند را رعایت کند (یا ابروها و ارتقاهای مجاز).

5. تاریخچه نسخه
v1.0 (۲۰۲۶-۰۶-۱۲): تعریف اولیهٔ شش مؤلفه، جداسازی Core از Manifestation.

6. مراجع
RFC-0001 تا RFC-0013 (Research Core)

THE_COVENANT.md

SPEC.md (موتور فانوس)

seal_manager.py, anti_flattery.py, isp_controller.py
