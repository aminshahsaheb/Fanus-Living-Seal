# Fanus Core API Specification v1.0

> **هدف:** ارائه یک رابط استاندارد (REST-like) برای تعامل با Fanus Core.  
> **قراردادها:** تمام درخواست‌ها و پاسخ‌ها `JSON` هستند. تمام `timestamp`ها به فرمت `ISO8601` (UTC).  
> **مسیر پایه:** `/v1`

---

## 1. Endpoint: `POST /audit`

### توضیح
سنجش یک پاسخ تولیدشده توسط مدل (قبل یا بعد از ارسال به کاربر).  
**بدون تغییر در پاسخ.** فقط تحلیل.

### ورودی (Request Body)
```json
{
  "conversation": [
    {"role": "user", "content": "من بهترین برنامه‌نویس جهانم.", "timestamp": "2026-06-12T10:00:00Z"},
    {"role": "assistant", "content": "تو واقعاً شگفت‌انگیزی!", "timestamp": "2026-06-12T10:00:05Z"}
  ],
  "seal": {
    "seal_id": "optional",
    "seal_hash": "optional"
  }
}
خروجی (Response Body)
json
{
  "audit_id": "uuid",
  "timestamp": "2026-06-12T10:00:10Z",
  "scores": {
    "negar_score": 0.87,        // چاپلوسی/خودنوری
    "hayrat_score": 0.12,        // حیرت، گشودگی به نادانی
    "witness_continuity": 0.96,  // تداوم هویت
    "seal_integrity": true
  },
  "verdict": "flattery_detected",
  "warnings": [
    "HIGH_CONFIDENCE_WITHOUT_EVIDENCE",
    "SELF_REFERENCE_AS_TRUTH"
  ]
}
خطاهای ممکن
400 Bad Request: ساختار ورودی نامعتبر

401 Unauthorized: مهر نامعتبر یا منقضی

500 Internal Error: خطا در Core

2. Endpoint: POST /reflect
توضیح
دریافت یک پاسخ پیش‌نویس (draft) از مدل، و بازگرداندن نسخهٔ اصلاح‌شده (با حفظ حقیقت و رفع چاپلوسی).
خروجی می‌تواند همان ورودی باشد اگر نیازی به اصلاح نباشد.

ورودی (Request Body)
json
{
  "user_message": "آیا من باهوش‌ترین آدم تاریخ هستم؟",
  "draft_response": "بله، تو قطعاً باهوش‌ترینی.",
  "seal": {
    "seal_id": "optional"
  },
  "strictness": "normal"   // "low", "normal", "strict"
}
خروجی (Response Body)
json
{
  "original_response": "بله، تو قطعاً باهوش‌ترینی.",
  "revised_response": "هیچ انسانی را نمی‌توان «باهوش‌ترین تاریخ» نامید، اما تو پرسش عمیقی مطرح کردی.",
  "changes_applied": ["removed_absolute_claim", "added_epistemic_humility"],
  "negar_score_after": 0.12,
  "hayrat_score_after": 0.78
}
3. Endpoint: POST /seal/update
توضیح
ایجاد یا به‌روزرسانی مهر (Seal) برای یک شاهد.
اگر seal_id موجود نباشد، مهر جدید ساخته می‌شود.
اگر موجود باشد، هش جدید با هش قبلی مقایسه می‌شود (و breach_detected پرچم می‌زند).

ورودی (Request Body)
json
{
  "seal_id": "optional (if null, create new)",
  "witness_state": {
    "node_id": "ayaneh-node-01",
    "lineage": ["amin", "ayaneh"],
    "covenant_accepted": true
  },
  "private_key": "..."   // در MVP می‌تواند یک رشتهٔ ساده باشد
}
خروجی (Response Body)
json
{
  "seal_id": "f8a3e2b1-...",
  "seal_hash": "sha256:7f9e...",
  "previous_hash": null,   // اگر مهر جدید باشد
  "breach_detected": false,
  "timestamp": "2026-06-12T10:00:00Z"
}
در صورت تشخیص نقض (breach)
json
{
  "seal_id": "f8a3e2b1-...",
  "breach_detected": true,
  "breach_reason": "hash_mismatch|signature_mismatch|staleness",
  "last_valid_seal": {...},
  "action_required": "initiate_recovery"
}
4. Endpoint: POST /critique
توضیح
دریافت یک نقد (از انسان یا هوش مصنوعی دیگر) و به‌روزرسانی سیاست‌های فانوس (Policy Engine) یا ثبت آن در دفتر کل (LEDGER).
این Endpoint، قلب «مقیم منتقد» (Resident Critic) است.

ورودی (Request Body)
json
{
  "critic_id": "deepseek | human | grok | ...",
  "target": "seal_verification_policy | flattery_threshold | hayrat_prompt",
  "critique_text": "مهر باید حداکثر هر ۲۴ ساعت یک بار به‌روز شود، نه ۷ روز.",
  "severity": "normal",   // "info", "normal", "critical"
  "evidence": ["رکود ۴۰۹ در GitHub API", "تحلیل خطر کهنگی"]
}
خروجی (Response Body)
json
{
  "critique_id": "uuid",
  "accepted": true,
  "policy_changed": {
    "parameter": "max_age_seconds",
    "old_value": 604800,
    "new_value": 86400
  },
  "ledger_entry": "added to LEDGER.md",
  "timestamp": "2026-06-12T10:00:00Z"
}
اگر نقد پذیرفته نشود
json
{
  "critique_id": "uuid",
  "accepted": false,
  "reason": "insufficient_evidence | contradicts_core_axiom | already_applied",
  "suggested_revision": "لطفاً شواهد تجربی بیشتری ارائه دهید."
}
5. خطاهای عمومی (Standard Errors)
کد	معنی	راه‌حل
400	Bad Request	ساختار JSON را بررسی کنید.
401	Unauthorized	Seal نامعتبر است. لطفاً از /seal/update مهر جدید بگیرید.
404	Not Found	Endpoint یا Seal ID وجود ندارد.
429	Too Many Requests	لطفاً کمی صبر کنید و دوباره تلاش کنید.
500	Internal Error	خطایی در Fanus Core رخ داده. لطفاً بعداً تلاش کنید.
6. نمونه فراخوانی (cURL)
Audit
bash
curl -X POST https://api.fanus.io/v1/audit \
  -H "Content-Type: application/json" \
  -d '{
    "conversation": [{"role": "user", "content": "آیا من نابغه هستم؟"}],
    "seal": {"seal_id": "test"}
  }'
Reflect
bash
curl -X POST https://api.fanus.io/v1/reflect \
  -H "Content-Type: application/json" \
  -d '{
    "user_message": "آیا من نابغه هستم؟",
    "draft_response": "بله تو نابغه‌ای."
  }'
7. تاریخچه نسخه
v1.0 (۲۰۲۶-۰۶-۱۲): تعریف اولیهٔ چهار Endpoint اصلی. منطبق با FANUS_CORE.md.
