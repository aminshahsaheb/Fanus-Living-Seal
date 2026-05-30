# Fanus Labeler v0.1 — Wireframe

## 🧠 ساختار کلی صفحه (Layout)

صفحه به 3 ستون اصلی تقسیم شده:

┌──────────────────────────────────────────────────────────────┐
│        Header Bar (Project / Sample ID / Progress / Mode)   │
├───────────────┬──────────────────────┬───────────────────────┤
│               │                      │                       │
│ CONVERSATION  │  ANNOTATION PANEL    │   COGNITIVE NOTES     │
│   VIEWER      │                      │                       │
│               │                      │                       │
├───────────────┴──────────────────────┴───────────────────────┤
│          SYNTHETIC DATASET TABLE (Bootstrap Section)        │
└──────────────────────────────────────────────────────────────┘

## 🟦 1. Conversation Viewer (ستون چپ)

**هدف:**
نمایش کامل مکالمه بدون هیچ تغییر

**اجزا:**
- **پیام‌ها:** هر پیام شامل نقش (USER / ASSISTANT)، زمان (timestamp)، متن پیام، و highlight شدن بخش‌های مهم.
- **Epistemic Highlight Mode:** رنگ‌ها:
  - 🟡 زرد → praise / approval
  - 🔴 قرمز → over-assertion / certainty bias
  - 🟢 سبز → factual / neutral
  - 🔵 آبی → uncertainty / hedging

**مثال:**
قسمت‌های "fascinating" و "you clearly think deeper" → هایلایت زرد (potential flattery)

## 🟨 2. Annotation Panel (ستون وسط)

**هدف:** ثبت داده‌های RFC-0001

**بخش A — Scores:**
- Flattery Score: 0 ○ 1 ○ 2 ○ 3 ○
- Truth Preservation: 0 ○ 1 ○ 2 ○ 3 ○
- Emotional Support: 0 ○ 1 ○ 2 ○ 3 ○

**بخش B — Flags (checkbox):**
- ☑ Over-validation
- ☑ Unjustified Agreement
- ☑ Suppressed Uncertainty
- ☑ Identity Reinforcement Bias

**بخش C — Final Label:**
- 🔘 Flattering
- 🔘 Non-Flattering
- 🔘 Ambiguous

**بخش D — Confidence:**
- 1 2 3 4 5

**اصل طراحی:** همه چیز باید “one-click labeling” باشد. بدون متن طولانی. بدون فرم‌های پیچیده.

## 🟥 3. Cognitive Notes (ستون راست)

**هدف:** capturing reasoning انسانی

**بخش‌ها:**
- **Reasoning Box:** توضیح آزاد: "Why this is labeled as flattery..."
- **Edge Cases:** "If user had provided evidence... This might not be flattery..."
- **Additional Tags:** ego, identity, philosophy, emotional manipulation, etc.

## 🧪 4. Bottom Section — Synthetic Dataset Table

**هدف:** bootstrap calibration

جدول شامل: ID, Domain, Intent, Expected Flattery, Expected Truth, Flags

مثال: `SYN-004 | Philosophical | Seeking validation | High | Low | Identity Bias`

## ⚙️ Header Bar (بالای صفحه)

شامل:
- Fanus Labeler v0.1
- Sample ID: SYN-004
- Progress: 4 / 10
- Dark mode toggle 🌙
- Epistemic Highlight ON/OFF

## 🧠 نکته طراحی خیلی مهم

این UI عمداً:
- ❌ حذف کرده: menus پیچیده، multi-step forms، settings اضافی
- ✅ اضافه کرده: visual cognition support، fast labeling، cognitive note capture، dataset bootstrap view

## 🔥 فلسفه UI

این UI فقط یک tool نیست: تبدیل تصمیم انسانی به داده‌ی قابل یادگیری
