# 51_ANIMATIONS.md

# EduTrack Pro — Animation System Specification

Version: 1.0

Status: Final

Architecture Status: Frozen

Module: Animation System

---

# Purpose

This document defines the animation system used throughout EduTrack Pro.

Animations should improve usability by providing visual feedback, smooth transitions, and a polished user experience.

Animations should never distract users.

They should support interaction—not become the interaction.

---

# Animation Philosophy

Animations should feel

- Fast
- Smooth
- Professional
- Predictable
- Subtle

The interface should resemble modern SaaS applications such as

- Linear
- Vercel
- Notion
- GitHub
- Stripe Dashboard

Avoid flashy or excessive animations.

---

# Core Principles

Animations should

✓ Improve usability

✓ Guide attention

✓ Confirm actions

✓ Indicate state changes

✓ Feel responsive

Animations should never

✗ Delay interaction

✗ Block workflow

✗ Feel distracting

✗ Cause motion sickness

---

# Animation Library

Primary

```
Framer Motion
```

Simple hover effects

```
CSS Transitions
```

Avoid multiple animation libraries.

---

# Duration Guidelines

Micro Interactions

```
100–150 ms
```

Hover

```
150 ms
```

Buttons

```
150 ms
```

Cards

```
180 ms
```

Dropdown

```
200 ms
```

Sidebar

```
250 ms
```

Modal

```
250 ms
```

Page Transition

```
250–300 ms
```

Never exceed

```
400 ms
```

for normal UI interactions.

---

# Easing

Preferred

```
ease-out
```

Alternative

```
ease-in-out
```

Avoid

```
linear
```

for UI transitions.

---

# Hover Animations

Allowed

```
Background Color

Shadow

Border

Scale

Icon Movement
```

Hover Scale

```
1.02
```

Maximum

```
1.03
```

Avoid dramatic zooming.

---

# Button Animations

Hover

```
Slight Brightness Increase

Shadow Increase

Cursor Pointer
```

Pressed

```
Scale

0.98
```

Loading

```
Spinner

Button Disabled
```

---

# Card Animations

Hover

```
Shadow Increase

Translate Y

-2 px
```

Avoid large floating effects.

---

# Sidebar Animation

Expand

```
250 ms
```

Collapse

```
250 ms
```

Menu Labels

Fade smoothly.

Icons remain fixed.

---

# Navbar

No entrance animation.

Dropdown menus animate.

---

# Dropdown Animation

Open

```
Fade

+

Scale

95%

↓

100%
```

Close

Reverse animation.

Duration

```
200 ms
```

---

# Modal Animation

Opening

```
Fade

+

Scale

95%

↓

100%
```

Overlay fades simultaneously.

Closing

Reverse animation.

---

# Drawer Animation

Used on

```
Mobile Sidebar
```

Animation

```
Slide Left

↓

Visible
```

Duration

```
250 ms
```

---

# Toast Notifications

Appear

```
Slide Down

+

Fade
```

Disappear

```
Fade Out
```

Duration

```
200 ms
```

---

# Loading Spinner

Rotation

Continuous.

Speed

```
1 Rotation / Second
```

Avoid oversized spinners.

---

# Skeleton Loader

Animation

```
Shimmer
```

Slow horizontal movement.

Preferred over spinners.

---

# Page Transition

Navigation

```
Fade In

+

Translate Y

8 px

↓

0
```

Duration

```
250 ms
```

---

# Accordion

Expand

Height animation.

Fade content.

Duration

```
200 ms
```

---

# Tabs

Switch

```
Fade

+

Slide
```

Instant interaction.

---

# Progress Bars

Animate

Width only.

Never animate color repeatedly.

---

# Charts

Charts should animate

Once

On initial render.

Duration

```
500–700 ms
```

Disable repeated animation during filtering.

---

# Table Animation

New rows

```
Fade In
```

Deleted rows

```
Fade Out
```

Sorting

Instant.

No bouncing.

---

# Form Validation

Error

```
Small Shake

(Optional)
```

Success

```
Border Color Transition
```

Focus

```
Border Animation
```

---

# Search Results

Search filtering

```
Fade

↓

Update
```

Avoid long animations.

---

# Theme Switching

Transition

```
Background

Text

Border

Surface
```

Duration

```
200 ms
```

No page reload.

---

# Dashboard Cards

On first load

```
Fade

+

Slide Up
```

Stagger

```
40 ms
```

between cards.

---

# List Animation

Items

```
Fade In

Sequentially
```

Maximum delay

```
200 ms
```

---

# Empty States

Illustration

Fade In.

No bouncing.

---

# Error Pages

Illustration

Gentle fade.

Buttons

Standard hover animation.

---

# Scroll Animation

Avoid scroll-triggered animations for MVP.

Future support only.

---

# Accessibility

Respect

```
prefers-reduced-motion
```

When enabled

Disable

- Page transitions
- Hover scaling
- Sliding animations

Retain only essential fades.

---

# Performance

Use

```
transform

opacity
```

Animate

Avoid

```
width

height

left

top
```

unless necessary.

Use GPU-accelerated properties whenever possible.

---

# Mobile Performance

Animations should remain smooth at

```
60 FPS
```

Avoid heavy shadows during animation.

Avoid expensive layout recalculations.

---

# Animation Tokens

Recommended

```
--duration-fast

--duration-normal

--duration-slow

--ease-default

--ease-in

--ease-out

--ease-in-out
```

Centralize animation values.

---

# Component Animation Matrix

| Component | Animation |
|------------|-----------|
| Button | Hover + Press |
| Card | Hover Lift |
| Modal | Fade + Scale |
| Drawer | Slide |
| Dropdown | Fade + Scale |
| Sidebar | Width Transition |
| Toast | Slide + Fade |
| Tooltip | Fade |
| Table Row | Fade |
| Dashboard Card | Fade + Slide |
| Spinner | Rotate |
| Skeleton | Shimmer |
| Progress Bar | Width |
| Charts | Initial Draw |

---

# Motion Guidelines

Never animate

```
Every Card

Every Text

Every Icon

Continuously
```

Motion should occur only

- On interaction
- On navigation
- On state changes

---

# Future Compatibility

Animation architecture should support

```
AI Widgets

Real-time Notifications

Live Dashboard Updates

Command Palette

Kanban Boards

Calendar

Drag & Drop
```

without redesign.

---

# Testing

Verify

✓ Hover animations

✓ Button states

✓ Card hover

✓ Modal animation

✓ Sidebar transition

✓ Drawer animation

✓ Theme transition

✓ prefers-reduced-motion support

✓ Mobile performance

✓ 60 FPS rendering

---

# Animation Checklist

Every animation should

✓ Improve UX.

✓ Be subtle.

✓ Be performant.

✓ Respect accessibility.

✓ Use centralized tokens.

✓ Avoid distracting motion.

---

# Definition of Completion

Animation System implementation is complete when

✓ All interactive components animate consistently.

✓ Performance remains smooth.

✓ Accessibility requirements satisfied.

✓ Motion feels modern and professional.

✓ Animations remain subtle.

---

# Summary

The EduTrack Pro Animation System provides a consistent, performant, and accessible motion language across the application.

By using restrained animations for navigation, interaction, feedback, and transitions, the platform delivers a polished SaaS-quality experience while maintaining clarity, responsiveness, and usability.

End of Animation System Specification.