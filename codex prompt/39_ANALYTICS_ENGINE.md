# 39_ANALYTICS_ENGINE.md

# EduTrack Pro — Analytics Engine Specification

Version: 1.0

Status: Final

Architecture Status: Frozen

Module: Analytics Engine

---

# Purpose

The Analytics Engine is responsible for transforming raw academic data into meaningful insights.

Unlike CRUD modules, the Analytics Engine does not create, update, or delete records.

Instead, it analyzes data collected from

- Students
- Subjects
- Attendance
- Marks
- Assignments
- Submissions

and generates actionable academic insights.

This module is one of the primary features that differentiates EduTrack Pro from a traditional Student Management System.

---

# Responsibilities

The Analytics Engine is responsible for

- Attendance Analytics
- Academic Performance Analytics
- Performance Score Calculation
- At-Risk Student Detection
- Scholarship Eligibility
- Performance Trends
- Subject-wise Analytics
- Dashboard Analytics
- Institutional Statistics

The Analytics Engine is NOT responsible for

- CRUD Operations
- Authentication
- Authorization
- API Routing
- Database Models

---

# Analytics Architecture

```
Database

↓

Attendance

Marks

Assignments

Submissions

↓

Analytics Engine

↓

Dashboard

Reports

Prediction

Insights
```

---

# Service Location

```
backend/

app/

services/

analytics_service.py
```

All analytics logic must be implemented inside this service.

---

# Data Sources

Analytics consumes data from

```
Students

Subjects

Attendance

Marks

Assignments

Submissions
```

It never stores calculated values permanently.

Analytics should always be generated dynamically.

---

# Analytics Modules

The engine consists of

```
Attendance Analytics

Performance Analytics

Assignment Analytics

Submission Analytics

Risk Analysis

Scholarship Analysis

Institution Analytics

Trend Analysis
```

---

# Attendance Analytics

Responsibilities

Calculate

```
Attendance Percentage

Average Attendance

Subject Attendance

Monthly Attendance

Semester Attendance

Overall Attendance
```

Formula

```
Attendance %

=

Present Classes

/

Total Classes

×

100
```

---

# Attendance Categories

```
Excellent

>=95%

Good

90–94%

Average

75–89%

Poor

Below 75%
```

Categories should remain configurable.

---

# Performance Analytics

Responsibilities

Calculate

```
Average Marks

Highest Marks

Lowest Marks

Subject Average

Semester Average

Overall Performance
```

Formula

```
Average

=

Total Marks

/

Total Maximum Marks

×

100
```

---

# Grade Calculation

Default grading

```
90–100 → A+

80–89 → A

70–79 → B+

60–69 → B

50–59 → C

40–49 → D

Below 40 → F
```

Grade calculation belongs only inside Analytics.

---

# Performance Score

EduTrack Pro uses a unified

```
Performance Score
```

Formula

```
70%

Academic Performance

+

30%

Attendance
```

Example

```
Attendance

92%

Marks

84%

Performance

(84×0.7)

+

(92×0.3)

=

86.4
```

Future versions may use configurable weighting.

---

# Performance Categories

```
Excellent

90+

Very Good

80–89

Good

70–79

Average

60–69

Needs Improvement

Below 60
```

---

# At-Risk Student Detection

Purpose

Automatically identify students requiring intervention.

---

# Risk Conditions

A student is considered

Low Risk

```
Attendance

<80%

OR

Performance

<70%
```

Medium Risk

```
Attendance

<75%

AND

Performance

<65%
```

High Risk

```
Attendance

<70%

AND

Performance

<50%
```

These thresholds should remain configurable.

---

# Risk Levels

```
Low

Medium

High
```

Dashboard should visually distinguish risk levels.

---

# Scholarship Eligibility

Purpose

Automatically determine scholarship eligibility.

---

# Default Rules

Attendance

```
>=85%
```

Performance

```
>=80%
```

No failed subjects.

Assignments completed.

If all conditions satisfied

```
Eligible
```

Else

```
Not Eligible
```

Future institutions may customize rules.

---

# Subject Analytics

Generate

```
Average Marks

Highest Marks

Lowest Marks

Pass Percentage

Attendance

Performance Trend
```

Per subject.

---

# Assignment Analytics

Calculate

```
Assignments Created

Assignments Submitted

Pending Assignments

Late Submissions

Completion Percentage
```

Formula

```
Completed

/

Total

×

100
```

---

# Submission Analytics

Calculate

```
Submitted

Reviewed

Pending Review

Late Submission

Review Completion
```

---

# Student Analytics

Generate

```
Attendance

Average Marks

Grade

Performance Score

Assignment Completion

Risk Level

Scholarship Status
```

Displayed on Student Dashboard.

---

# Teacher Analytics

Generate

```
Total Students

Average Attendance

Average Marks

Performance Distribution

At-Risk Students

Assignment Statistics

Pending Reviews
```

Displayed on Teacher Dashboard.

---

# Institution Analytics

Generate

```
Overall Attendance

Overall Performance

Department Performance

Course Performance

Semester Performance

Top Students

Bottom Students

Pass Percentage
```

---

# Trend Analysis

Generate

```
Attendance Trend

Performance Trend

Marks Trend

Assignment Trend
```

Time periods

```
Weekly

Monthly

Semester

Yearly
```

---

# Charts

Analytics should produce visualization-ready data.

Examples

```
Line Chart

Bar Chart

Pie Chart

Area Chart

Radar Chart
```

The frontend should not perform calculations.

---

# Analytics Response Example

```json
{
    "attendance_percentage": 91.8,
    "average_marks": 84.2,
    "grade": "A",
    "performance_score": 86.5,
    "risk_level": "Low",
    "scholarship_eligible": true
}
```

---

# Dashboard Integration

Teacher Dashboard

Consumes

```
Institution Analytics

Risk Analysis

Assignment Analytics

Performance Analytics
```

Student Dashboard

Consumes

```
Attendance Analytics

Performance Analytics

Assignment Analytics

Scholarship Status
```

---

# Reports Integration

Reports consume

```
Performance Analytics

Attendance Analytics

Risk Analysis

Institution Statistics
```

Reports never calculate independently.

---

# Performance Requirements

Analytics should

Load quickly.

Use optimized SQL queries.

Use aggregation.

Avoid repeated calculations.

Avoid N+1 queries.

---

# Caching

Not required for MVP.

Future support

```
Redis
```

may cache

- Dashboard Analytics
- Institution Statistics
- Frequently accessed reports

---

# Expected Service Functions

Examples

```
calculate_attendance()

calculate_average_marks()

calculate_grade()

calculate_performance_score()

detect_risk_level()

check_scholarship_eligibility()

generate_teacher_dashboard()

generate_student_dashboard()

generate_subject_statistics()

generate_institution_statistics()
```

---

# Business Rules

Analytics must

Never modify database records.

Always calculate from latest data.

Remain deterministic.

Produce identical output for identical input.

---

# API Consumers

Analytics Service is consumed by

```
Dashboard API

Reports API

Future AI Engine

Prediction Engine
```

Routers should never perform analytics directly.

---

# Unit Testing

Verify

✓ Attendance Calculation

✓ Grade Calculation

✓ Performance Score

✓ Risk Detection

✓ Scholarship Eligibility

✓ Subject Statistics

✓ Institution Statistics

✓ Trend Generation

✓ Edge Cases

✓ Empty Dataset Handling

---

# Future Compatibility

Architecture should support

- Machine Learning Predictions

- AI Recommendations

- Performance Forecasting

- Personalized Study Suggestions

- Faculty Performance Analytics

- Department Ranking

- Institutional Benchmarking

without redesigning the Analytics Engine.

---

# Analytics Checklist

Every analytics function should

✓ Be deterministic.

✓ Be reusable.

✓ Be independently testable.

✓ Avoid database duplication.

✓ Return structured objects.

✓ Support dashboards.

✓ Support reports.

✓ Support future AI modules.

---

# Definition of Completion

Analytics Engine implementation is complete when

✓ Attendance analytics work.

✓ Marks analytics work.

✓ Performance score works.

✓ Risk detection works.

✓ Scholarship eligibility works.

✓ Trend generation works.

✓ Institution statistics work.

✓ Dashboard integration works.

✓ Report integration works.

✓ Tests pass.

---

# Summary

The Analytics Engine is the intelligence layer of EduTrack Pro.

It transforms raw academic data into meaningful insights through centralized calculations, trend analysis, performance scoring, risk detection, and scholarship evaluation.

By separating analytics from CRUD operations and API routing, the platform remains scalable, maintainable, and ready for future AI-powered enhancements.

End of Analytics Engine Specification.