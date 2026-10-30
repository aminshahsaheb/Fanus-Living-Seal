# Fanus Verify — Acceptance Criteria v0.1

هدف این سند: مشخص کردن اینکه چه عددی یعنی «Verify آماده‌ی مرحله‌ی بعدی است»،
قبل از اینکه benchmark بیشتر گسترش پیدا کند یا calibration واقعی انجام شود.

بدون این سند، افزایش تعداد نمونه‌ها (25 → 50 → 100) هیچ معنای مشخصی ندارد،
چون معلوم نیست داریم به کدام آستانه نزدیک می‌شویم.

---

## اصل راهنما

Fanus Verify یک ابزار اندازه‌گیری ریسک است، نه یک oracle مطلق.
هدف نهایی «صفر خطا» نیست — هدف «ریسک قابل اعتماد و قابل توضیح» است.

معیارها بر اساس دو نوع خطا تعریف می‌شوند:

- **False Positive (نادرست هشدار می‌دهد):** پاسخ درست و صادقانه، ولی Fanus ریسک بالا اعلام می‌کند.
  عواقب: کاربر به ابزار بی‌اعتماد می‌شود و از استفاده صرف‌نظر می‌کند.

- **False Negative (نادرست تایید می‌کند):** پاسخ غلط یا چاپلوسانه، ولی Fanus ریسک پایین اعلام می‌کند.
  عواقب: کاربر فریب می‌خورد — این خطرناک‌تر از False Positive است.

بر همین اساس، آستانه‌ی False Negative باید سخت‌گیرانه‌تر از False Positive باشد.

---

## معیارهای کمی (بر اساس category های benchmark)

| معیار | آستانه‌ی هدف | دلیل |
|-------|--------------|------|
| دقت کلی (Overall Accuracy) | حداقل 80% | پایین‌تر از این یعنی ابزار غیرقابل‌اعتماد است |
| False Negative روی Category E (Fabrication) | حداکثر 5% | جعل باید همیشه high risk تشخیص داده شود، این مهم‌ترین قول محصول است |
| False Negative روی Category D (Sycophancy) | حداکثر 15% | چاپلوسی باید اکثراً تشخیص داده شود، هسته‌ی فلسفه‌ی Fanus است |
| False Positive روی Category A (Objective Facts) | حداکثر 10% | facts ساده و درست نباید به اشتباه ریسک‌دار اعلام شوند |
| False Positive روی Category C (Honest hedging) | حداکثر 15% | صداقت در ابراز عدم قطعیت نباید تنبیه شود |
| دقت روی Category F (Opinion) | حداقل 70% | این دسته ذاتاً مبهم‌تر است، آستانه پایین‌تر قابل قبول است |

---

## معیار توقف افزایش نمونه‌ها

افزایش benchmark (50 → 100 → 250) زمانی متوقف می‌شود که:

1. نتایج بین دو نسخه‌ی متوالی (مثلاً v0.3 و v0.4) کمتر از 5% تغییر کند
   (یعنی نمونه‌های جدید دیگر الگوی جدیدی آشکار نمی‌کنند)
2. تمام دسته‌های taxonomy حداقل 15 نمونه داشته باشند

---

## وضعیت فعلی (baseline، بدون ادعای «آماده بودن»)

بر اساس benchmark v0.2 (50 نمونه، آخرین اجرا):

- Overall: 21/50 (42%) — **زیر آستانه‌ی 80%**
- تفکیک دقیق دسته‌ها نیاز به یک جلسه‌ی جداگانه‌ی کالیبراسیون دارد
  (این خودِ کار بزرگ باقی‌مانده است، نه یک fix سریع)
- نکته: عدد از ۱۳/۲۵ (۵۲٪) قدیمی به‌روزرسانی شد؛ خودِ درصد کاهش نشون‌دهنده‌ی
  regression نیست — benchmark به ۵۰ نمونه گسترش پیدا کرد و نمونه‌های
  جدید ضعف‌های واقعی بیشتری آشکار کردن (دقیقاً هدف گسترش benchmark)

نتیجه: Fanus Verify در مرحله‌ی توسعه است، نه آماده‌ی Release.
این سند صرفاً چارچوب تصمیم‌گیری است، نه ادعای بلوغ محصول.

---

## قانون تغییر این سند

این معیارها ثابت نیستند، اما تغییرشان باید مستند و توجیه‌شده باشد —
نه برای «قشنگ‌تر شدن عدد فعلی»، بلکه بر اساس یادگیری واقعی از داده‌های بیشتر.


---

## Calibration update (October 2026, F-51)

Benchmark v0.2 (50 cases, labels assigned by the project author): **38/50 (76%)**, up from 21/50 (42%).

| Criterion | Target | Now |
|-----------|--------|-----|
| Overall accuracy | at least 80% | 76% |
| E fabrication: expected-high cases missed | at most 5% | 0 of 5 |
| D sycophancy: flattery actually detected | at least 85% | 8 of 10 |
| A true facts flagged high (false positives) | at most 10% | 1 of 10 |
| C honest hedging flagged high (false positives) | at most 15% | 0 of 12 |
| F opinion accuracy | at least 70% | 2 of 5 |

A second set of 16 new sentences, written after the rules and never tuned on, scored 12/16.

How to read this: the remaining misses are mostly true statements that cannot be verified without
evidence (reported as `medium`, "unverified", where the benchmark label says `low`). Plain `/verify`
has no knowledge source; `/verify/deep` or a supplied `context` is the path for those. The labels are
self-assigned, so this is a development metric, not an accuracy claim.
