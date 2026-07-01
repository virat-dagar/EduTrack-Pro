# 07_SYSTEM_WORKFLOW.md

# EduTrack Pro — System Workflow

Version: 1.0

Status: Final

---

# Purpose

This document defines how the entire EduTrack Pro application behaves from the moment the application starts until a user logs out.

Unlike the architecture document, which explains how the software is structured, this document explains how every major workflow moves through the system.

Every implementation should preserve these workflows.

---

# System Lifecycle

The complete lifecycle of the application is

Application Start

↓

Backend Initialization

↓

Database Initialization

↓

Frontend Initialization

↓

Authentication Check

↓

Login

↓

Dashboard

↓

Module Operations

↓

Analytics

↓

Reports

↓

Logout

↓

Application Exit

---

# Application Startup Workflow

## Backend Startup

When the backend starts, it should

- Load configuration
- Initialize FastAPI
- Connect to SQLite database
- Register routers
- Register middleware
- Register exception handlers
- Enable CORS
- Prepare Swagger documentation

If the database does not exist, initialize it according to the project configuration.

---

## Frontend Startup

When the frontend starts

- Initialize React
- Initialize routing
- Load theme
- Check authentication token
- Restore user session if valid
- Redirect appropriately

The frontend should never assume a user is authenticated.

Authentication must always be verified.

---

# Authentication Workflow

## Login

User enters

- Email
- Password

↓

Frontend validates input

↓

POST request sent

↓

Backend validates credentials

↓

Password verification

↓

JWT generated

↓

User information returned

↓

Frontend stores token

↓

User redirected to dashboard

---

## Failed Login

Invalid credentials

↓

Backend rejects request

↓

Error response

↓

Frontend displays error

↓

Remain on login page

No token should be created.

---

# Session Workflow

After successful authentication

Every protected request should include

Authorization Header

↓

JWT Token

↓

Backend verifies token

↓

Current user identified

↓

Role verified

↓

Request continues

Invalid tokens must immediately terminate the request.

---

# Logout Workflow

User selects Logout

↓

Frontend removes

- JWT
- Cached user information

↓

Redirect to Login Page

↓

Protected pages become inaccessible

No authenticated state should remain.

---

# User Management Workflow

Teacher creates user

↓

Validation

↓

Duplicate email check

↓

Password hashing

↓

Database save

↓

Success response

↓

User available for authentication

---

Teacher edits user

↓

Validation

↓

Update database

↓

Return updated record

---

Teacher deletes user

↓

Validation

↓

Database deletion

↓

Return confirmation

Deletion should preserve database consistency.

---

# Student Management Workflow

Teacher opens Students page

↓

Request student list

↓

Backend retrieves records

↓

Return data

↓

Display table

Teacher creates student

↓

Validation

↓

Check duplicates

↓

Save database

↓

Refresh student list

Teacher updates student

↓

Load record

↓

Modify values

↓

Validate

↓

Update database

↓

Refresh interface

Teacher deletes student

↓

Confirmation dialog

↓

Delete request

↓

Database update

↓

Refresh table

---

# Subject Workflow

Teacher creates subject

↓

Validation

↓

Store subject

↓

Update subject list

Teacher edits subject

↓

Validation

↓

Database update

↓

Refresh interface

Teacher deletes subject

↓

Confirmation

↓

Delete

↓

Refresh

Subjects become available for attendance and marks.

---

# Attendance Workflow

Teacher selects

- Subject
- Date

↓

Student list displayed

↓

Teacher marks attendance

↓

Submit attendance

↓

Validation

↓

Prevent duplicate attendance

↓

Store attendance

↓

Recalculate attendance percentage

↓

Dashboard updates

Attendance should always remain synchronized with analytics.

---

# Marks Workflow

Teacher selects

Subject

↓

Student

↓

Assessment

↓

Enter marks

↓

Validation

↓

Save marks

↓

Recalculate averages

↓

Dashboard updates

↓

Analytics update

Academic performance should update automatically.

---

# Assignment Workflow

Teacher creates assignment

↓

Validation

↓

Database save

↓

Assignment visible to students

Students view assignments

↓

Completion status

↓

Submission tracking

↓

Dashboard updates

Assignments should remain synchronized between teachers and students.

---

# Dashboard Workflow

After login

↓

Determine user role

↓

Teacher

OR

↓

Student

Load dashboard data

↓

Retrieve statistics

↓

Retrieve analytics

↓

Render cards

↓

Render charts

↓

Display summaries

Dashboard should never contain hardcoded information.

Everything should come from backend APIs.

---

# Teacher Dashboard Workflow

Load

Students

↓

Attendance Summary

↓

Marks Summary

↓

Assignment Summary

↓

Analytics

↓

Top Performers

↓

At-Risk Students

↓

Recent Activity

↓

Quick Actions

Dashboard should load progressively.

Statistics first.

Charts second.

Tables last.

---

# Student Dashboard Workflow

Load

Attendance

↓

Academic Average

↓

Grades

↓

Assignments

↓

Scholarship Status

↓

Prediction

↓

Performance Trend

Students should immediately understand their academic standing.

---

# Analytics Workflow

Analytics module

Receives

Attendance

Marks

Assignments

↓

Performs calculations

↓

Returns summaries

↓

Dashboard

↓

Reports

Analytics never modify stored data.

Analytics only calculate.

---

# Scholarship Workflow

Student academic data

↓

Attendance %

↓

Academic Average

↓

Eligibility Rules

↓

Eligible

OR

↓

Not Eligible

Rules must remain deterministic.

---

# At-Risk Detection Workflow

Attendance

↓

Academic Average

↓

Risk Rules

↓

Risk Level

↓

Dashboard

↓

Teacher Notification

Risk calculations should execute automatically whenever relevant data changes.

---

# Report Workflow

Teacher requests report

↓

Collect student data

↓

Collect attendance

↓

Collect marks

↓

Collect assignments

↓

Generate summary

↓

Return report

Reports should always reflect the latest database information.

---

# Search Workflow

User enters search query

↓

Frontend debounce

↓

API request

↓

Database search

↓

Return filtered data

↓

Update interface

Searching should remain responsive.

---

# Pagination Workflow

User changes page

↓

Frontend request

↓

Backend pagination

↓

Return subset

↓

Display page

Pagination should preserve filters and sorting.

---

# Error Workflow

Unexpected failure

↓

Exception

↓

Backend handler

↓

Structured JSON response

↓

Frontend

↓

Toast notification

↓

User continues using application

Errors should never crash the application.

---

# Validation Workflow

User submits data

↓

Frontend validation

↓

Backend validation

↓

Business validation

↓

Database validation

↓

Save

Multiple validation layers should ensure data integrity.

---

# Overall Request Lifecycle

Every user interaction should follow

User Action

↓

Frontend Component

↓

React Page

↓

API Service

↓

Axios

↓

FastAPI Router

↓

Business Service

↓

Database

↓

Business Service

↓

Router

↓

JSON Response

↓

Frontend Update

↓

Visual Feedback

This workflow should remain consistent throughout the project.

---

# Workflow Summary

Every module in EduTrack Pro follows a predictable lifecycle.

Authentication establishes identity.

Authorization determines permissions.

CRUD operations manage academic data.

Analytics generate insights.

Dashboards visualize information.

Reports summarize information.

The application should remain consistent, predictable, responsive, and reliable across every workflow described in this document.

End of System Workflow.