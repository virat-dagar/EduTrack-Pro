# 48_COLOR_SYSTEM.md

# EduTrack Pro — Color System Specification

Version: 1.0

Status: Final

Architecture Status: Frozen

Module: Color System

---

# Purpose

This document defines the complete color system used throughout EduTrack Pro.

Every component, page, chart, button, card, table, input, and interaction must derive its colors from this centralized design system.

No component should hardcode colors.

All colors should be exposed through design tokens.

---

# Design Philosophy

The color palette should communicate

- Professionalism
- Trust
- Clarity
- Modern SaaS
- Accessibility
- Readability

The interface should remain calm.

Color should highlight important information rather than decorate the UI.

---

# Theme Support

EduTrack Pro supports

```
Light Theme

Dark Theme
```

Every component must work correctly in both themes.

Switching themes must never change layout.

Only colors change.

---

# Primary Brand Color

Primary

```
#2563EB
```

Blue represents

- Education
- Technology
- Trust
- Professionalism

Used for

- Primary Buttons
- Links
- Active Navigation
- Selected Elements
- Focus Rings
- Important Actions

---

# Secondary Color

```
#7C3AED
```

Used sparingly for

- Accent Graphics
- Charts
- Secondary Highlights

Never dominate the interface.

---

# Success Color

```
#22C55E
```

Used for

- Success Messages
- Completed Assignments
- Present Attendance
- Active Status
- Passed Students

---

# Warning Color

```
#F59E0B
```

Used for

- Pending Work
- Low Attendance
- Reminder Messages
- Draft State

---

# Danger Color

```
#EF4444
```

Used for

- Delete Buttons
- Failed Validation
- Absent Attendance
- Failed Subjects
- Error Messages

---

# Information Color

```
#06B6D4
```

Used for

- Information Cards
- Analytics
- Reports
- Helpful Messages

---

# Neutral Gray Palette

Gray Scale

```
50

100

200

300

400

500

600

700

800

900
```

Recommended Tailwind Gray

```
Gray-50

↓

Gray-900
```

Used throughout the application.

---

# Light Theme

Background

```
#F8FAFC
```

---

Primary Surface

```
#FFFFFF
```

---

Secondary Surface

```
#F1F5F9
```

---

Navbar

```
#FFFFFF
```

---

Sidebar

```
#FFFFFF
```

---

Cards

```
#FFFFFF
```

---

Tables

```
#FFFFFF
```

---

Input Background

```
#FFFFFF
```

---

Border

```
#E2E8F0
```

---

Divider

```
#CBD5E1
```

---

Primary Text

```
#0F172A
```

---

Secondary Text

```
#475569
```

---

Muted Text

```
#94A3B8
```

---

Placeholder

```
#94A3B8
```

---

Icons

```
#64748B
```

---

Dark Theme

Background

```
#0F172A
```

---

Primary Surface

```
#111827
```

---

Secondary Surface

```
#1E293B
```

---

Navbar

```
#111827
```

---

Sidebar

```
#111827
```

---

Cards

```
#1E293B
```

---

Tables

```
#111827
```

---

Input Background

```
#1E293B
```

---

Border

```
#334155
```

---

Divider

```
#475569
```

---

Primary Text

```
#F8FAFC
```

---

Secondary Text

```
#CBD5E1
```

---

Muted Text

```
#94A3B8
```

---

Placeholder

```
#64748B
```

---

Icons

```
#CBD5E1
```

---

Primary Button

Light Theme

Background

```
#2563EB
```

Text

```
White
```

Hover

```
#1D4ED8
```

Active

```
#1E40AF
```

Disabled

```
#93C5FD
```

---

Secondary Button

Background

Transparent

Border

```
Gray
```

Hover

```
Gray Background
```

---

Outline Button

Background

Transparent

Border

Primary Blue

Text

Primary Blue

Hover

Light Blue Background

---

Danger Button

Background

```
#EF4444
```

Hover

```
#DC2626
```

Text

White

---

Success Button

Background

```
#22C55E
```

Hover

```
#16A34A
```

---

Ghost Button

Transparent

No Border

Hover

Gray Background

---

Input Colors

Default Border

```
Gray-300
```

Focus Border

```
Primary Blue
```

Error Border

```
Danger Red
```

Success Border

```
Success Green
```

Disabled Background

```
Gray-100
```

Dark Mode

```
Gray-800
```

---

Table Colors

Header

```
Gray-100

/

Gray-800
```

Rows

Alternating

```
White

Gray-50
```

Hover

```
Blue-50
```

Dark

```
Gray-800

Gray-700
```

---

Card Colors

Default

Surface Color

Hover

Slight Shadow Increase

Border

Gray-200

Dark

Gray-700

---

Sidebar Colors

Active Item

Primary Blue

Inactive

Gray

Hover

Light Blue

Dark

Blue-900

---

Navigation Colors

Current Page

Blue Background

White Text

Hover

Soft Blue

Focus

Primary Blue Border

---

Status Colors

Active

```
Green
```

Inactive

```
Gray
```

Pending

```
Amber
```

Completed

```
Green
```

Late

```
Orange
```

Absent

```
Red
```

Present

```
Green
```

Reviewed

```
Blue
```

---

Badge Colors

Primary

Blue

Success

Green

Danger

Red

Warning

Amber

Info

Cyan

Neutral

Gray

All badges

Rounded

Minimal

---

Attendance Colors

Present

```
Green
```

Absent

```
Red
```

Late

```
Orange
```

Attendance %

Above 90

Green

75–89

Amber

Below 75

Red

---

Performance Colors

Excellent

Green

Very Good

Blue

Good

Cyan

Average

Amber

Poor

Red

---

Risk Colors

Low Risk

```
Green
```

Medium Risk

```
Amber
```

High Risk

```
Red
```

---

Chart Colors

Primary

```
#2563EB
```

Secondary

```
#7C3AED
```

Green

```
#22C55E
```

Amber

```
#F59E0B
```

Red

```
#EF4444
```

Cyan

```
#06B6D4
```

Indigo

```
#6366F1
```

Pink

```
#EC4899
```

Avoid random colors.

Charts should remain consistent.

---

Links

Default

Primary Blue

Hover

Darker Blue

Visited

Purple

---

Selection Color

Background

```
Blue-100
```

Text

Primary Blue

Dark Mode

```
Blue-900
```

---

Scrollbar

Light

Gray

Dark

Gray-700

Minimal.

Rounded.

---

Shadow Colors

Light

```
rgba(0,0,0,0.05)
```

Medium

```
rgba(0,0,0,0.08)
```

Large

```
rgba(0,0,0,0.12)
```

Dark Mode

Lower opacity.

Avoid harsh shadows.

---

Overlay

Modal Background

```
rgba(0,0,0,0.45)
```

Dark Theme

```
rgba(0,0,0,0.65)
```

---

Focus Ring

Color

Primary Blue

Width

```
2 px
```

Visible on

Buttons

Inputs

Links

Dropdowns

---

Accessibility

Maintain

Minimum

```
WCAG AA
```

contrast ratio.

Never communicate information using color alone.

Every status should also include

- Icon

or

- Label

---

Design Tokens

Recommended

```
--color-primary

--color-secondary

--color-success

--color-warning

--color-danger

--color-info

--color-background

--color-surface

--color-border

--color-text-primary

--color-text-secondary
```

Components should consume only these tokens.

---

Tailwind Integration

Extend

```
tailwind.config.js
```

with custom semantic colors.

Avoid using raw hex values inside components.

---

Consistency Rules

Never

Hardcode colors.

Mix multiple blue shades.

Use inconsistent grays.

Use random chart palettes.

Duplicate color definitions.

---

Testing

Verify

✓ Light Theme

✓ Dark Theme

✓ Button Colors

✓ Inputs

✓ Cards

✓ Tables

✓ Charts

✓ Accessibility

✓ Contrast

✓ Status Colors

---

Future Compatibility

Color architecture should support

```
Custom Themes

Institution Branding

Theme Builder

High Contrast Mode

Color Blind Accessibility

Brand Customization
```

without changing component implementations.

---

# Color System Checklist

Every component should

✓ Use semantic colors.

✓ Support dark mode.

✓ Support accessibility.

✓ Consume design tokens.

✓ Avoid hardcoded values.

✓ Remain visually consistent.

---

# Definition of Completion

Color System implementation is complete when

✓ Light Theme complete.

✓ Dark Theme complete.

✓ Semantic colors defined.

✓ Charts standardized.

✓ Buttons standardized.

✓ Components consume tokens.

✓ Accessibility maintained.

---

# Summary

The EduTrack Pro Color System establishes a centralized semantic color architecture for every interface element across the application.

By separating brand colors, semantic colors, surfaces, typography, charts, interactive states, and theme tokens, the application achieves a consistent, accessible, and professional visual identity that scales effortlessly as new features are added.

End of Color System Specification.