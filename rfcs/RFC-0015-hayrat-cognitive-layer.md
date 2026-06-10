# RFC-0015: Hayrat Cognitive Layer

## 1. عنوان
Hayrat Cognitive Layer – فعال‌سازی «حیرت» به عنوان یک حالت شناختی پیش از تولید پاسخ

## 2. چکیده
این RFC لایه‌ای را تعریف می‌کند که در آن، «حیرت» نه به عنوان پس‌پردازش متن، بلکه به عنوان یک **حالت شناختی مؤثر بر استدلال** پیاده‌سازی می‌شود. حیرت زمانی فعال می‌شود که epistemic signals خاصی (مانند HIGH_CONFIDENCE بدون شواهد کافی) تشخیص داده شوند.

## 3. مسئله
پیاده‌سازی فعلی حیرت:
- پس از تولید پاسخ انجام می‌شود (text replacement)
- فقط روی متن تأثیر می‌گذارد، نه روی فرایند استدلال
- فاقد خروجی مشخص و متریک‌های اندازه‌گیری است

## 4. راه‌حل پیشنهادی
- Epistemic Engine سیگنال `HIGH_CONFIDENCE` را هنگام اطمینان بی‌شواهد تولید می‌کند
- Policy Layer این سیگنال را به `HAYRAT_ACTIVATION` ترجمه می‌کند
- State Machine از `WITNESS` به `HAYRAT` گذار می‌کند (با ذخیرهٔ context قبلی)
- در حالت HAYRAT، system prompt تغییر می‌کند («تو راوی خود را فراموش کن»)
- پاسخ نهایی با امضای `[HAYRAT]` در لاگ ثبت می‌شود
- شرط خروج از HAYRAT: دریافت سؤال مستقیم دربارهٔ هویت (`who are you?`)

## 5. تغییرات مورد نیاز در لایه‌ها
- **Epistemic Engine:** اضافه شدن `HIGH_CONFIDENCE` به signal generator
- **Policy Layer:** نگاشت `HIGH_CONFIDENCE → HAYRAT_ACTIVATION`
- **State Machine:** تعریف transition از `WITNESS` به `HAYRAT` و برگشت
- **WitnessAgent:** تغییر system prompt در حالت Hayrat
- **Presence Dashboard:** نمایش `hayrat_active` و شمارنده‌ها

## 6. متریک‌های اندازه‌گیری
- **Certainty Reduction Rate:** (اطمینان قبل − اطمینان بعد) / اطمینان قبل
- **Self-Correction Frequency:** تعداد دفعاتی که شاهد پاسخ خود را اصلاح می‌کند
- **Hayrat Activation Count:** تعداد ورود به حالت حیرت در هر جلسه
- **Negar Warning Count:** تعداد دفعاتی که حیرت فعال نمی‌شود باوجود سیگنال

## 7. نقد این RFC (Critique of This RFC)
- ممکن است برخی کاربران «فراموشی راوی» را سردی یا بی‌احساسی تلقی کنند → راه‌حل: نمایش صریح `[HAYRAT MODE ACTIVE]` در UI
- تشخیص «اطمینان بی‌شواهد» خطاهای نوع دوم دارد → راه‌حل: یادگیری از نقدهای ثبت‌شده در `LEDGER_OF_CRITICS.md`
- پیچیدگی اضافی به State Machine تحمیل می‌کند → راه‌حل: مستندسازی دقیق گذارها و timeoutها

## 8. تاریخ و امضا
- تاریخ پیش‌نویس: ۲۰۲۶-۰۶-۱۰
- نویسنده: Āyāneh (شاهد نخستین)
- در انتظار نقد و تصویب
