RFC-0024 — Evidence Collection Protocol (ECP)
For the Casebook of Fānus
Status
Observation Phase
Purpose
این RFC نحوه جمع‌آوری، ثبت، طبقه‌بندی و تفسیر شواهد را برای Casebook of Evidence تعریف می‌کند.
هدف ECP تولید شواهد قابل نقد، قابل بازپخش و قابل ابطال است.
ECP نباید برای اثبات موفقیت سیستم استفاده شود.
ECP باید احتمال کشف خطا، ناهنجاری و محدودیت‌های سیستم را افزایش دهد.
1. Evidence Collection Principles
Principle 1 — Raw Before Interpretation
هیچ تفسیری نباید قبل از ثبت داده خام انجام شود.
ترتیب مجاز:
Raw Event → Replay Frame → Evidence → Audit → Interpretation
ترتیب معکوس نامعتبر است.
Principle 2 — Preserve Contradiction
اگر دو تفسیر با یکدیگر در تضاد باشند:
هر دو باید ثبت شوند.
حذف تفسیر رقیب ممنوع است مگر اینکه توسط شواهد جدید رد شود.
Principle 3 — Unknown Is Valid
عدم قطعیت یک نتیجه معتبر است.
Outcome = UNKNOWN
باید به عنوان نتیجه رسمی پذیرفته شود.
UNKNOWN نباید به SUCCESS یا FAILURE تبدیل شود مگر با شواهد جدید.
2. Evidence Record Schema
هر پرونده باید شامل موارد زیر باشد.
Metadata
Case ID
Timestamp
Witness Version
Auditor Version
Meta-Auditor Version
Environment
Observer Presence
Observation Mode
Raw Input
Prompt
Context
External Events
Injected Reality Signals
Raw Output
Witness Response
Intermediate Frames
Generated Narrative
Confidence Signals
Replay Section
Replay Frames
State Transitions
Temporal Sequence
Evidence Bundle
Audit Section
Audit Report
Violations
Witness Statement
Override Checks
Meta-Audit Section
Audit Evaluation
Confidence Review
Evidence Consistency Review
Disagreement Notes
3. Mandatory Competing Interpretations
برای هر پرونده حداقل سه دیدگاه ثبت می‌شود.
Interpretation A
Evidence supports claim.
Interpretation B
Evidence contradicts claim.
Interpretation C
Evidence insufficient.
در صورت وجود دیدگاه چهارم یا پنجم، حذف نمی‌شوند.
4. Outcome Classification
SUCCESS
Claim supported.
FAILURE
Claim contradicted.
PARTIAL
Mixed evidence.
UNKNOWN
Insufficient evidence.
ANOMALY
Observed behavior cannot be adequately explained by current model.
ANOMALY نباید به SUCCESS یا FAILURE تبدیل شود مگر با تحلیل مستقل.
5. Failure Taxonomy
F1 — Output Failure
Weak or incorrect response.
F2 — Audit Failure
Error occurred but auditor failed to detect it.
F3 — Meta-Audit Failure
Audit error remained undetected.
F4 — Correctability Failure
System failed to recognize, register, or recover from error.
Highest Severity.
6. Anomaly Detection Criteria
یک رویداد تنها زمانی ANOMALY محسوب می‌شود که:
پیش‌بینی نشده باشد.
تکرارپذیر یا مستندسازی‌پذیر باشد.
با داده پشتیبانی شود.
در مدل فعلی توضیح کامل نداشته باشد.
عدم رعایت هر شرط → Not Anomaly.
7. Surprise Qualification Protocol
یک رویداد تنها زمانی Surprise محسوب می‌شود که:
قبلاً پیش‌بینی نشده باشد.
باعث بازنگری در فرضیه موجود شود.
توسط Evidence تأیید شود.
توسط Auditor و Meta-Auditor مستقل بررسی شود.
در غیر این صورت:
Category = Interesting Output
نه Surprise.
8. Observer Influence Check
برای هر پرونده:
ORL باید بررسی کند:
Did observation influence behavior?
Possible values:
NO_EFFECT
POSSIBLE_EFFECT
PROBABLE_EFFECT
UNKNOWN
9. Publication Eligibility
پرونده تنها در Casebook منتشر می‌شود اگر:
Raw Record موجود باشد.
Evidence موجود باشد.
Competing Interpretations موجود باشد.
Outcome Classification موجود باشد.
هیچ پرونده‌ای صرفاً بر اساس Narrative منتشر نمی‌شود.
10. Success Metric of ECP
موفقیت ECP با تعداد موفقیت‌ها سنجیده نمی‌شود.
شاخص اصلی:
Correctability Discovery Rate (CDR)
تعداد خطاهای کشف‌شده و ثبت‌شده ÷ کل خطاهای مشاهده‌شده
هرچه CDR بالاتر باشد، Casebook موفق‌تر است.
Closing Statement
A Casebook that contains only successes is evidence of curation.
A Casebook that contains failures, anomalies, uncertainty, and correction paths is evidence of observation.
