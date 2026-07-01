# 46_LAYOUT_SYSTEM.md

# EduTrack Pro — Layout System Specification

Version: 1.0

Status: Final

Architecture Status: Frozen

Module: Layout System

---

# Purpose

The Layout System defines how every page of EduTrack Pro is visually organized.

Instead of every page creating its own layout, the application should use reusable layout wrappers.

A layout is responsible for

- Navigation
- Sidebar
- Header
- Content Area
- Footer
- Theme
- Responsive Behavior

Layouts should never contain business logic.

---

# Layout Philosophy

Every page should feel like part of one unified application.

The user should never feel like navigation changes between pages.

The application should have

✓ Consistency

✓ Predictability

✓ Professional appearance

✓ Fast navigation

✓ Clean hierarchy

---

# Layout Hierarchy

```
Browser

↓

App

↓

Router

↓

Layout

↓

Page

↓

Components
```

Every page should be rendered inside an appropriate layout.

---

# Layout Directory

```
src/

layouts/

│

├── DashboardLayout.jsx

├── AuthLayout.jsx

└── BlankLayout.jsx
```

Only layouts belong inside this folder.

---

# Available Layouts

EduTrack Pro uses three layouts.

```
Dashboard Layout

Authentication Layout

Blank Layout
```

---

# Dashboard Layout

Purpose

Used for every authenticated page.

Includes

```
Sidebar

Top Navbar

Main Content

Optional Footer
```

Used by

```
Teacher Dashboard

Student Dashboard

Students

Attendance

Marks

Subjects

Assignments

Reports

Settings

Profile
```

---

# Dashboard Structure

```
+--------------------------------------------------+

| Sidebar | Navbar                                |

|         |----------------------------------------|

|         |                                        |

|         |                                        |

|         |        Main Content                    |

|         |                                        |

|         |                                        |

|         |----------------------------------------|

|         | Footer (Optional)                      |

+--------------------------------------------------+
```

---

# Authentication Layout

Purpose

Used only for

```
Login

Future Password Reset

Future Forgot Password
```

Contains

```
Centered Card

Brand Logo

Authentication Form

Minimal Background
```

No sidebar.

No dashboard.

---

# Authentication Layout Structure

```
+--------------------------------------+

|                                      |

|                                      |

|          Logo                        |

|                                      |

|     Authentication Card              |

|                                      |

|                                      |

+--------------------------------------+
```

---

# Blank Layout

Purpose

Pages requiring no navigation.

Examples

```
404

403

500

Maintenance

Coming Soon
```

Simple centered content.

---

# Layout Responsibilities

Layouts are responsible for

✓ Page Structure

✓ Navigation

✓ Responsive Containers

✓ Sidebar

✓ Header

✓ Theme

✓ Scroll Management

Layouts are NOT responsible for

- API Requests

- Business Logic

- Authentication

- Database

---

# Dashboard Layout Components

Dashboard Layout contains

```
Sidebar

Navbar

Page Container

Outlet()

Toast Container
```

Everything else is rendered inside

```
Outlet()
```

---

# Sidebar

Purpose

Primary application navigation.

Should remain visible on desktop.

Collapsible.

Scrollable if necessary.

---

# Sidebar Sections

Teacher

```
Dashboard

Students

Subjects

Attendance

Marks

Assignments

Reports

Users

Settings
```

Student

```
Dashboard

Attendance

Marks

Assignments

Reports

Profile

Settings
```

Menus generated dynamically from role.

---

# Sidebar Behavior

Desktop

Expanded by default.

Tablet

Collapsible.

Mobile

Hidden by default.

Drawer behavior.

---

# Sidebar Width

Expanded

```
280 px
```

Collapsed

```
80 px
```

Smooth animated transition.

---

# Navbar

Displayed above content.

Contains

```
Breadcrumb

Search

Notifications (Future)

Theme Toggle

Profile Menu

Logout
```

Navbar remains fixed.

---

# Navbar Height

Recommended

```
72 px
```

Consistent throughout application.

---

# Main Content Area

Contains

```
Page Title

Actions

Cards

Charts

Tables

Forms
```

Uses consistent spacing.

---

# Content Container

Recommended maximum width

```
1440 px
```

Centered.

Responsive.

---

# Page Header

Every page should begin with

```
Title

Subtitle

Actions
```

Example

```
Students

Manage student records.

[ Add Student ]
```

---

# Footer

Optional.

Minimal.

Example

```
EduTrack Pro

Version 1.0

© 2026
```

---

# Responsive Behavior

Desktop

```
Sidebar Visible

Navbar Fixed
```

Tablet

```
Sidebar Collapsible
```

Mobile

```
Sidebar Drawer

Hamburger Menu
```

---

# Scroll Behavior

Navbar

Fixed.

Sidebar

Independent scrolling.

Main Content

Independent scrolling.

Avoid scrolling the entire application.

---

# Spacing System

Recommended spacing

```
8 px

16 px

24 px

32 px

48 px

64 px
```

Use consistently.

---

# Grid System

Dashboard Cards

```
Desktop

4 Columns
```

Tablet

```
2 Columns
```

Mobile

```
1 Column
```

Tables should become horizontally scrollable.

---

# Card Layout

Cards should contain

```
Header

Content

Footer (Optional)
```

Consistent padding.

Consistent border radius.

---

# Theme Support

Layouts should support

```
Light

Dark
```

No layout changes between themes.

Only colors change.

---

# Animation

Allowed animations

```
Sidebar Collapse

Page Transition

Modal

Dropdown

Toast
```

Animations should remain subtle.

---

# Loading Layout

During authentication

Display

```
Centered Loader

Application Logo
```

Avoid rendering partial UI.

---

# Empty Layout

Used for

```
No Data

No Results

No Reports
```

Should display

Illustration

Message

Primary Action

---

# Error Layout

Should support

```
403

404

500
```

Each page contains

```
Illustration

Error Message

Back Button

Dashboard Button
```

---

# Accessibility

Layouts should support

Keyboard Navigation.

Focus Management.

ARIA Labels.

Proper Landmark Elements.

Semantic HTML.

---

# Performance

Layouts should

Remain mounted.

Only page content changes.

Sidebar and Navbar should not re-render unnecessarily.

---

# Component Hierarchy

```
DashboardLayout

↓

Sidebar

↓

Navbar

↓

Outlet

↓

Page

↓

Components
```

---

# Future Compatibility

Layout architecture should support

```
Notifications

Calendar

Messaging

AI Assistant

Plugin Sidebar

Multi-tenancy

Workspace Switching
```

without redesign.

---

# Testing

Verify

✓ Sidebar Navigation

✓ Navbar

✓ Responsive Layout

✓ Mobile Drawer

✓ Theme Switching

✓ Scroll Behavior

✓ Layout Persistence

✓ Outlet Rendering

---

# Layout Checklist

Every layout should

✓ Be reusable.

✓ Be responsive.

✓ Support themes.

✓ Support accessibility.

✓ Support routing.

✓ Avoid business logic.

✓ Keep navigation consistent.

---

# Definition of Completion

Layout System implementation is complete when

✓ Dashboard Layout works.

✓ Auth Layout works.

✓ Blank Layout works.

✓ Sidebar responsive.

✓ Navbar responsive.

✓ Outlet rendering correct.

✓ Theme supported.

✓ Tests pass.

---

# Summary

The Layout System provides the structural foundation of EduTrack Pro by defining reusable page shells for authenticated, authentication, and standalone pages.

By centralizing navigation, responsive behavior, spacing, and layout composition, the application achieves a professional, scalable, and consistent user experience across every screen.

End of Layout System Specification.