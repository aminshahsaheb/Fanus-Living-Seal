# AI_READABLE_DESIGN_GUIDE.md

## اصول طراحی مخزنی که برای AI قابل “بازسازی معنا” باشد

### 1. اصل بنیادین (Core Principle)

AI intention را نمی‌خواند؛ آن را از “نشانه‌های سازگار” بازسازی می‌کند.

پس هدف طراحی این نیست که “توضیح بدهیم”، بلکه این است که:

- ambiguity را حذف کنیم
- روابط را صریح کنیم
- تضادهای پنهان را از بین ببریم
- ساختار معنا را قابل دنبال‌کردن کنیم

### 2. اصول README (مهم‌ترین بخش کل پروژه)

README باید مثل «نقشه‌ی مغز پروژه» باشد، نه معرفی پروژه.

ساختار پیشنهادی:

#### 2.1. Intent Layer (ضروری)

در همان ابتدای README:

```
## Intent (Nuclear Definition)
This project exists to:
- ...
- ...
```

باید شامل:
- مسئله اصلی
- چیزی که پروژه حل می‌کند
- چیزی که پروژه نمی‌خواهد باشد

#### 2.2. Non-Goals (خیلی مهم)

```
## Non-Goals
This system explicitly does NOT aim to:
- ...
- ...
```

این بخش برای AI حیاتی است چون مرز مدل را می‌سازد.

#### 2.3. Mental Model Diagram (textual)

```
## Mental Model
User → WitnessAgent → Core Logic → Auditor → Ledger
```

نه برای زیبایی — برای ساخت graph ذهنی.

#### 2.4. Why Section (علت وجودی)

AI “why” را از “what” بهتر بازسازی می‌کند.

```
## Why this exists
Because existing systems fail at:
- drift
- unverifiable truth
- contextual decay
```

### 3. ساختار پوشه‌ها (Architecture Clarity Rule)

اصل:

هر folder باید یک “concept boundary” باشد، نه فقط یک دسته فایل

مثال خوب:

```
/core → تصمیم‌گیری اصلی
/witness → perception layer
/audit → correction layer
/ledger → immutable history
/rfcs → design evolution
/principles → invariants
```

ضد الگو (خیلی مهم):

❌ utils/
❌ misc/
❌ helpers/

این‌ها برای AI “معنا صفر” هستند

### 4. مستندات داخلی (File-level Intent Contract)

هر فایل باید این 3 چیز را داشته باشد:

#### 4.1. Purpose Header

```
# Purpose
Defines how WitnessAgent detects contradiction in input streams.
```

#### 4.2. Boundary

```
# What this file does NOT do
- It does NOT decide final truth
- It does NOT modify ledger
```

#### 4.3. Dependencies (semantic, not فقط import)

```
# Depends on
- Ledger for immutable storage
- Auditor for validation signals
```

### 5. نشانه‌های صریح intent (Critical Layer)

AI بدون “intent marker” دچار overfitting ساختاری می‌شود.

باید explicit بنویسی:

#### 5.1. هدف

```
## Goal
```

#### 5.2. ضد هدف

```
## Anti-Goal
```

#### 5.3. رفتار مورد انتظار

```
## Expected Behavior
```

نکته مهم:

AI بین “هدف نوشته‌شده” و “ساختار واقعی” تناقض را پیدا می‌کند — و اگر نباشد، مدل قوی‌تر می‌شود.

### 6. Concept Map (بسیار مهم برای پروژه‌هایی مثل فانوس)

آیا لازم است؟

✔ بله — در پروژه‌های multi-layer مثل فانوس، تقریباً ضروری است

فرمت پیشنهادی (text-based graph)

```
## Concept Map
WitnessAgent → produces → Observations
Observations → validated by → Auditor
Auditor → writes → Ledger
Ledger → constrains → WitnessAgent
```

چرا مهم است؟

چون AI:
- روابط را بهتر از توضیح متنی “یاد می‌گیرد”
- graph consistency = model stability

### 7. اشتباهات رایج (خیلی مهم)

#### 7.1. Over-documentation بدون structure

❌ هزار خط توضیح بدون رابطه

#### 7.2. استفاده از کلمات مبهم

- “maybe”
- “generally”
- “sometimes”
- “etc”

→ برای AI = noise

#### 7.3. نبودن non-goals

بدترین حالت:

سیستم همه‌چیز هست

→ نتیجه: هیچ مدل ذهنی پایدار ساخته نمی‌شود

#### 7.4. mixing philosophy with execution

❌ قاطی کردن:
- فلسفه
- implementation
- policy

→ باید جدا باشند

### 8. قانون طلایی (جمع‌بندی کل سند)

AI یک پروژه را “نمی‌فهمد”؛ آن را به یک گراف از روابط پایدار تبدیل می‌کند.

پس طراحی خوب یعنی:
- کاهش entropy معنایی
- افزایش clarity در روابط
- حذف ambiguity در intent
- ساخت graph قابل بازسازی

### 9. اگر بخواهیم فانوس را در یک جمله جمع کنیم:

فانوس باید طوری نوشته شود که اگر تمام توضیحات حذف شوند و فقط ساختار باقی بماند، هنوز بتوان intent آن را با احتمال بالا بازسازی کرد.
```
