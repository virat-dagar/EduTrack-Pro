# 54_STUDENT_DASHBOARD.md

# EduTrack Pro — Student Dashboard Specification

Version: 1.0

Status: Final

Architecture Status: Frozen

Module: Student Dashboard

---

# Purpose

The Student Dashboard is the personal academic workspace for every student using EduTrack Pro.

Unlike the Teacher Dashboard, which provides institution-wide analytics, the Student Dashboard focuses entirely on the currently authenticated student.

It should answer the following questions immediately.

- How am I performing?
- What is my attendance?
- What are my latest marks?
- Which assignments are pending?
- Am I eligible for a scholarship?
- Am I academically at risk?
- What should I work on next?

The dashboard should motivate students while presenting clear and meaningful academic information.

---

# Design Philosophy

The Student Dashboard should feel

- Personal
- Clean
- Motivating
- Informative
- Modern
- Fast

Inspired by

```
Linear

GitHub

Notion

Google Classroom

Canvas LMS
```

Unlike the Teacher Dashboard, the Student Dashboard should emphasize personal progress rather than institutional statistics.

---

# Route

```
/dashboard/student
```

---

# Authorization

Accessible only by

```
Student
```

Teachers attempting to access this dashboard should be redirected to

```
/dashboard/teacher
```

---

# Layout

```
DashboardLayout

↓

Navbar

↓

Sidebar

↓

Student Dashboard
```

---

# Dashboard Structure

```
Welcome Header

↓

Performance Summary Cards

↓

Performance Charts

↓

Assignments

↓

Recent Activity

↓

Academic Insights

↓

Upcoming Deadlines
```

---

# Welcome Header

Contains

```
Greeting

Student Name

Current Date

Performance Message
```

Example

```
Good Morning, Virat

Monday, July 6, 2026

Keep up the great work!
```

---

# Summary Cards

Display

```
Attendance %

Average Marks

Performance Score

Current Grade

Pending Assignments

Completed Assignments

Scholarship Status

Risk Level
```

Displayed in

Desktop

```
4 Cards Per Row
```

Tablet

```
2 Cards Per Row
```

Mobile

```
1 Card Per Row
```

---

# Attendance Card

Displays

```
Attendance %

Present Classes

Total Classes

Attendance Status
```

Color

Green

```
>=90%
```

Amber

```
75–89%
```

Red

```
<75%
```

---

# Marks Card

Displays

```
Average Marks

Highest Marks

Current Grade
```

Includes

Subject Count

---

# Performance Card

Displays

```
Performance Score

Performance Category

Trend
```

Trend examples

```
Improving

Stable

Declining
```

Trend calculated by Analytics Engine.

---

# Assignment Card

Displays

```
Pending

Submitted

Late

Due Today
```

Quick action

```
View Assignments
```

---

# Scholarship Card

Displays

```
Eligible

Not Eligible
```

Shows

Eligibility reason.

Example

```
Attendance below 85%
```

or

```
Eligible for Scholarship
```

---

# Risk Card

Displays

```
Low

Medium

High
```

Includes

Reason

Examples

```
Low Attendance

Low Performance

Missing Assignments
```

---

# Performance Charts

Contains

```
Attendance Trend

Marks by Subject

Performance Trend

Assignment Progress
```

---

# Attendance Trend

Chart

```
Line Chart
```

Displays

Weekly attendance.

Monthly attendance.

---

# Subject Performance

Chart

```
Bar Chart
```

Displays

Average marks

Per subject.

---

# Performance Trend

Chart

```
Area Chart
```

Displays

Performance Score

over time.

---

# Assignment Progress

Chart

```
Pie Chart
```

Displays

```
Completed

Pending

Late
```

---

# Academic Insights

Displays personalized recommendations.

Examples

```
Attendance has improved by 8%.

Your Mathematics performance increased.

Complete pending assignments.

Maintain attendance above 85%.

Excellent academic progress.
```

Generated using

Analytics Engine.

---

# Upcoming Deadlines

Displays

```
Assignment

Due Date

Days Remaining

Priority
```

Sorted by

Nearest deadline first.

---

# Recent Activity

Displays

```
Marks Published

Attendance Updated

Assignment Submitted

Feedback Received
```

Newest activity first.

---

# Subject Performance Table

Columns

```
Subject

Attendance

Average Marks

Grade

Performance
```

Read-only.

---

# Assignment Table

Columns

```
Assignment

Due Date

Status

Submission

Marks
```

Student cannot edit assignments.

---

# Dashboard Widgets

Student Dashboard contains

```
Summary Cards

Charts

Insights

Recent Activity

Assignments

Upcoming Deadlines

Subject Performance
```

Each widget should be independent.

---

# Data Sources

Dashboard consumes

```
Attendance

Marks

Assignments

Submissions

Analytics

Reports
```

Dashboard performs

No calculations.

No CRUD.

---

# API Endpoints

Consumes

```
GET /dashboard/student

GET /dashboard/student/charts

GET /dashboard/student/activity
```

---

# Refresh Strategy

Dashboard loads

Once

↓

Manual Refresh

↓

Reload Dashboard Data

Automatic polling not required.

---

# Loading State

Display

```
Skeleton Cards

Skeleton Charts

Skeleton Tables
```

Avoid blank pages.

---

# Empty State

If no academic data exists

Display

```
Welcome to EduTrack Pro

Your academic records will appear here once your instructor starts recording attendance and marks.
```

---

# Error State

Display

```
Unable to load dashboard.

Please try again.
```

Button

```
Refresh
```

---

# Responsive Layout

Desktop

```
4 Cards

2 Charts Per Row

Tables Visible
```

Tablet

```
2 Cards

Charts Stacked
```

Mobile

```
1 Card

Charts Stacked

Tables Scroll
```

---

# Theme Support

Supports

```
Light Theme

Dark Theme
```

Only colors change.

Layout remains unchanged.

---

# Accessibility

Support

```
Keyboard Navigation

Screen Readers

Focus Indicators

ARIA Labels

Semantic HTML
```

---

# Performance Requirements

Dashboard should load

Under

```
1 Second
```

Backend should return aggregated data.

Frontend performs no heavy calculations.

---

# Expected Components

```
DashboardHeader

StatisticsCard

AttendanceCard

MarksCard

PerformanceCard

ScholarshipCard

RiskCard

ActivityCard

AssignmentTable

SubjectPerformanceTable

UpcomingDeadlineCard

LineChart

AreaChart

BarChart

PieChart
```

---

# State Management

Store

```
Dashboard Data

Loading

Error
```

Authentication handled by

```
AuthContext
```

---

# User Experience Goals

Student should immediately understand

```
How am I doing?

What needs attention?

What is improving?

What should I do next?
```

The dashboard should reduce confusion.

---

# Future Compatibility

Dashboard should support

```
AI Study Recommendations

Semester GPA

CGPA

Exam Schedule

Study Planner

Calendar

Notifications

Achievements

Goal Tracking

Weekly Progress Reports
```

without redesign.

---

# Testing

Verify

✓ Dashboard loads.

✓ Summary cards display.

✓ Charts render.

✓ Assignment list correct.

✓ Activity feed correct.

✓ Insights display.

✓ Responsive layout.

✓ Dark mode.

✓ Accessibility.

✓ Performance.

---

# Student Dashboard Checklist

Every implementation should

✓ Display academic summary.

✓ Display performance charts.

✓ Display assignments.

✓ Display insights.

✓ Display upcoming deadlines.

✓ Support responsiveness.

✓ Support dark mode.

✓ Be accessible.

✓ Load efficiently.

---

# Definition of Completion

Student Dashboard implementation is complete when

✓ Statistics display correctly.

✓ Charts display correctly.

✓ Assignment information correct.

✓ Insights generated correctly.

✓ Responsive layout implemented.

✓ Theme support complete.

✓ Tests pass.

---

# Summary

The Student Dashboard is the personalized academic command center of EduTrack Pro.

It provides students with a comprehensive view of their academic journey through performance metrics, attendance tracking, assignment management, personalized insights, and upcoming deadlines, creating a modern, motivating, and data-driven learning experience while remaining clean, responsive, and highly scalable.

End of Student Dashboard Specification.