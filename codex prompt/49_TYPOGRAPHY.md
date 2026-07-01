# 49_TYPOGRAPHY.md

# EduTrack Pro — Typography System Specification

Version: 1.0

Status: Final

Architecture Status: Frozen

Module: Typography System

---

# Purpose

This document defines the complete typography system used throughout EduTrack Pro.

Typography is one of the most important aspects of the UI because it determines readability, hierarchy, clarity, accessibility, and overall visual quality.

Every page, component, dashboard, table, and form should follow this typography specification.

No component should define its own font styles independently.

---

# Typography Philosophy

Typography should communicate

- Professionalism
- Clarity
- Precision
- Modern Engineering
- Academic Reliability

The interface should feel similar to

- Linear
- GitHub
- Notion
- Vercel
- Stripe Dashboard

The design should prioritize readability over decoration.

---

# Primary Font

Use

```
Inter
```

Fallback

```
system-ui

Segoe UI

Roboto

Helvetica Neue

Arial

sans-serif
```

Inter should be loaded using

```
Google Fonts
```

or bundled locally.

---

# Why Inter

Inter provides

✓ Excellent readability

✓ Professional appearance

✓ Modern SaaS feel

✓ Large language support

✓ Excellent small-size rendering

✓ Wide font weight availability

---

# Font Weights

Supported

```
300

Light

400

Regular

500

Medium

600

SemiBold

700

Bold

800

Extra Bold
```

Avoid using

```
900
```

except for rare hero elements.

---

# Font Sizes

Use a consistent type scale.

| Name | Size | Weight | Usage |
|------|------|--------|------|
| xs | 12 px | 400 | Labels, captions |
| sm | 14 px | 400 | Secondary text |
| base | 16 px | 400 | Body text |
| lg | 18 px | 500 | Large body |
| xl | 20 px | 600 | Section headings |
| 2xl | 24 px | 600 | Page headings |
| 3xl | 30 px | 700 | Dashboard titles |
| 4xl | 36 px | 700 | Hero titles |

Avoid arbitrary font sizes.

---

# Line Height

Typography should breathe.

Recommended

| Font Size | Line Height |
|------------|-------------|
| 12 | 18 px |
| 14 | 20 px |
| 16 | 24 px |
| 18 | 28 px |
| 20 | 30 px |
| 24 | 34 px |
| 30 | 40 px |
| 36 | 46 px |

---

# Letter Spacing

Default

```
Normal
```

Large headings

```
-0.02em
```

Small labels

```
0.02em
```

Avoid excessive spacing.

---

# Text Hierarchy

Hierarchy should be created using

```
Font Size

↓

Weight

↓

Spacing

↓

Color
```

Never rely only on color.

---

# Heading Levels

---

## H1

Purpose

Application-level page titles.

Examples

```
Teacher Dashboard

Student Dashboard

Reports
```

Style

```
36 px

Bold

700
```

---

## H2

Purpose

Major section headings.

Examples

```
Student Management

Attendance

Assignments
```

Style

```
30 px

Bold
```

---

## H3

Purpose

Card titles.

Examples

```
Attendance Overview

Recent Activity

Performance Summary
```

Style

```
24 px

SemiBold
```

---

## H4

Purpose

Component headings.

Style

```
20 px

SemiBold
```

---

## H5

Purpose

Small section headings.

Style

```
18 px

Medium
```

---

## H6

Purpose

Minor headings.

Style

```
16 px

Medium
```

---

# Body Text

Default body

```
16 px

Regular
```

Used for

```
Descriptions

Content

Paragraphs

Tables
```

---

# Secondary Text

Used for

```
Descriptions

Hints

Metadata

Dates

Helper Text
```

Style

```
14 px

Regular

Gray
```

---

# Caption Text

Used for

```
Statistics

Footnotes

Small Labels

Status Descriptions
```

Style

```
12 px

Regular
```

---

# Labels

Form labels

```
14 px

Medium
```

Always placed above inputs.

---

# Placeholder Text

Style

```
14 px

Regular

Muted Gray
```

Never use placeholder as label.

---

# Input Text

Style

```
16 px

Regular
```

Readable.

Consistent.

---

# Button Typography

Small Button

```
14 px

Medium
```

Medium Button

```
15 px

SemiBold
```

Large Button

```
16 px

SemiBold
```

Buttons should never use bold text.

---

# Table Typography

Header

```
14 px

SemiBold
```

Rows

```
14 px

Regular
```

Numeric columns

Right aligned.

---

# Sidebar Typography

Menu Item

```
14 px

Medium
```

Section Label

```
12 px

SemiBold

Uppercase
```

---

# Navbar Typography

Application Name

```
18 px

Bold
```

User Name

```
14 px

Medium
```

Role

```
12 px

Regular
```

---

# Dashboard Cards

Statistic Number

```
30 px

Bold
```

Statistic Label

```
14 px

Medium
```

Trend Text

```
12 px

Medium
```

---

# Charts

Chart Title

```
18 px

SemiBold
```

Axis Labels

```
12 px
```

Legend

```
13 px
```

Tooltip

```
13 px
```

---

# Badges

Text

```
12 px

Medium
```

Centered vertically.

---

# Breadcrumbs

Style

```
14 px

Regular
```

Current page

```
Medium
```

---

# Links

Body Links

```
16 px

Medium
```

Hover

Underline.

Never rely only on color.

---

# Error Messages

Style

```
13 px

Medium
```

Displayed below inputs.

---

# Success Messages

Style

```
13 px

Medium
```

Readable.

Not oversized.

---

# Empty States

Title

```
24 px

SemiBold
```

Description

```
16 px

Regular
```

Primary Button

Standard button typography.

---

# Modal Typography

Title

```
24 px

SemiBold
```

Description

```
16 px

Regular
```

Footer

```
14 px
```

---

# Notification Typography

Toast Title

```
15 px

SemiBold
```

Toast Description

```
13 px

Regular
```

---

# Code Typography

Use

```
JetBrains Mono
```

Fallback

```
Consolas

Monaco

monospace
```

Only for

```
IDs

API Keys

Developer Pages

Logs
```

---

# Text Alignment

Titles

Left

Body

Left

Numbers

Right (inside tables)

Buttons

Center

Forms

Left

Avoid centered paragraphs.

---

# Text Width

Maximum readable width

```
70–80 Characters
```

Avoid extremely wide paragraphs.

---

# Text Truncation

Long text should

```
Ellipsis

...

Tooltip on Hover
```

Used for

```
Table Cells

Cards

Sidebar

Lists
```

---

# Accessibility

Maintain

Minimum

```
16 px
```

for body text whenever practical.

Avoid tiny fonts.

Maintain proper contrast.

Never communicate information using typography alone.

---

# Responsive Typography

Desktop

Full typography scale.

Tablet

Reduce headings slightly.

Mobile

Reduce

```
H1

H2

H3
```

Body text remains

```
16 px
```

Never reduce body below

```
14 px
```

---

# Font Loading

Load fonts once.

Avoid loading multiple font families.

Prefer

```
Inter

+

JetBrains Mono
```

only.

---

# Design Tokens

Recommended tokens

```
--font-family

--font-mono

--font-size-xs

--font-size-sm

--font-size-base

--font-size-lg

--font-size-xl

--font-size-2xl

--font-size-3xl

--font-size-4xl

--font-weight-regular

--font-weight-medium

--font-weight-semibold

--font-weight-bold

--line-height-body

--line-height-heading
```

All components should consume typography tokens.

---

# Tailwind Integration

Extend

```
tailwind.config.js
```

with

```
fontFamily

fontSize

fontWeight

lineHeight

letterSpacing
```

Avoid inline font values.

---

# Consistency Rules

Never

Mix font families.

Use random font sizes.

Use excessive bold text.

Center long paragraphs.

Use decorative fonts.

---

# Testing

Verify

✓ Typography hierarchy

✓ Responsive scaling

✓ Table readability

✓ Form readability

✓ Dashboard readability

✓ Accessibility

✓ Font loading

✓ Design tokens

---

# Future Compatibility

Typography architecture should support

```
Multi-language

RTL Languages

Accessibility Fonts

Institution Branding

Print Styles

PDF Generation
```

without redesign.

---

# Typography Checklist

Every page should

✓ Use Inter.

✓ Follow type scale.

✓ Maintain hierarchy.

✓ Support accessibility.

✓ Use design tokens.

✓ Remain responsive.

✓ Avoid arbitrary sizes.

---

# Definition of Completion

Typography implementation is complete when

✓ Font family standardized.

✓ Type scale established.

✓ Hierarchy consistent.

✓ Responsive typography implemented.

✓ Accessibility maintained.

✓ Design tokens used.

✓ Components follow typography system.

---

# Summary

The EduTrack Pro Typography System establishes a consistent, accessible, and modern typographic language across the entire application.

By standardizing font families, type scales, weights, spacing, and semantic usage, every screen maintains excellent readability, strong visual hierarchy, and a professional SaaS-quality appearance while remaining scalable for future growth.

End of Typography System Specification.