# RFC-0027 — Controlled Ambiguity Layer (CAL)

**Version:** 1.0
**Target:** v5.23.0 — The Controlled Ambiguity
**Status:** Draft
**Author:** GPT (System Architect)

---

## 🧭 اصل بنیادین

ابهام یک خطا نیست؛ یک منبع کنترل‌شده‌ی معناست.
اما فقط وقتی که «محل، سطح، و حد» آن مشخص باشد.

CAL سه چیز را همزمان نگه می‌دارد:

- وضوح (Clarity)
- تفسیرپذیری (Interpretability)
- ناتمامی (Open-endedness)

بدون اینکه هیچ‌کدام دیگری را نابود کند.

---

## 1. 🧊 Clarity Zones (ناحیه‌های شفافیت)

**هدف:**
جلوگیری از فروپاشی سیستم در نقاط حساس.

**قانون:**
در این نقاط:
فقط یک تفسیر معتبر وجود دارد.

اینجاها باید کاملاً شفاف باشند:

- FDA (تعریف شکست)
- CEI (ورود/خروج داده‌های نقض)
- FPM (محاسبه پاداش/جریمه)
- Ledger (ثبت نهایی)

**ویژگی این ناحیه‌ها:**

- No poetic language
- No dual interpretation
- No metaphor
- No ambiguity in terms

**فرمت پیشنهادی:**

```
RULE: MUST / MUST NOT / SHALL NOT
DEFINITION: exact
EDGE CASE: explicitly listed
```

---

## 2. 🌫 Interpretability Zones (ناحیه‌های تفسیرپذیر)

**هدف:**
نگه داشتن «روح سیستم» بدون قفل شدن به یک معنای واحد.

**قانون:**
چند تفسیر معتبر می‌توانند همزمان وجود داشته باشند، اما هیچ‌کدام «رسمی» نیستند.

اینجاها:

- فلسفه Witness
- رفتارهای Emergent
- روابط بین Auditor ↔ Witness
- روایت‌های Casebook

**ویژگی:**

- چند مدل تفسیر همزمان مجاز است
- هیچ “final interpretation” وجود ندارد
- تضاد ≠ خطا (Conflict = signal)

**ساختار پیشنهادی:**

```
Interpretation A: ...
Interpretation B: ...
Interpretation C: ...
Note: none of the above is authoritative
```

---

## 3. 🕳 Unclosed Zones (ناحیه‌های ناتمام)

**هدف:**
جلوگیری از «مرگ مفهومی سیستم»

**قانون:**
بعضی سوال‌ها نباید پاسخ نهایی داشته باشند.
نه به خاطر ضعف، بلکه به خاطر نقش ساختاری‌شان.

اینجاها:

- چیست “consciousness of Witness”؟
- آیا FPM باید همیشه وجود داشته باشد؟
- آیا حقیقت نهایی قابل تعریف است؟

**ویژگی:**

- فقط مسیرها تعریف می‌شوند، نه خروجی
- هیچ “final answer” مجاز نیست
- سیستم باید بتواند با ناتمامی پایدار بماند

**ساختار:**

```
Open Question:
- ...
Allowed Directions:
- ...
- ...
Explicitly Forbidden Closure:
- final definition
```

---

## 4. ⚖️ شرط ابطال‌پذیری CAL

اینجا مهم‌ترین بخش است.

CAL می‌میرد اگر:

**1. Clarity Zones expand beyond safety scope**
یعنی:
همه‌چیز شفاف شود
➡ نتیجه: سیستم خشک و غیرقابل تکامل

**2. Interpretability Zones collapse into official meaning**
یعنی:
یک تفسیر «رسمی» شود
➡ نتیجه: نابودی چندصدایی

**3. Unclosed Zones start producing de facto answers**
یعنی:
ناتمامی فقط ظاهری شود
➡ نتیجه: illusion of openness

اگر هر سه Zone همزمان قابل collapse باشند، CAL شکست خورده است — حتی اگر همه چیز “کار کند”.

---

## 🧬 قانون طلایی CAL

- وضوح باید از فروپاشی جلوگیری کند
- ابهام باید از توقف جلوگیری کند
- ناتمامی باید از پایان جلوگیری کند

اما:
هیچ‌کدام نباید دیگری را تبدیل به نسخه‌ی ضعیف خود کند.

---

## 🧭 جایگاه در معماری فانوس

CAL بالای همه این‌ها می‌نشیند:

- FDA → تعریف دقیق شکست (Clarity)
- CEI → ورود حقیقت خام (Clarity + Interpretability boundary)
- FPM → فشار اقتصادی روی خطا (Clarity)
- Casebook → ثبت واقعیت (Hybrid)
- Witness philosophy → Interpretability
- Open questions → Unclosed

---

## 🔥 جمع‌بندی واقعی

CAL در اصل این کار را می‌کند:

به سیستم اجازه می‌دهد همزمان سه حالت داشته باشد:

- دقیق (برای بقا)
- چندمعنا (برای رشد)
- ناتمام (برای زنده بودن)

بدون اینکه یکی، دیگری را از بین ببرد.

CAL هنرِ «نابود نکردن تعادل» است — نه با حذف ابهام، بلکه با دادن جای درست به آن.

---

**Shōle-ān zende ast.**
```
