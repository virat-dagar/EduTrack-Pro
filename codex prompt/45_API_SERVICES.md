# 45_API_SERVICES.md

# EduTrack Pro — Frontend API Services Specification

Version: 1.0

Status: Final

Architecture Status: Frozen

Module: Frontend API Services

---

# Purpose

This document defines the complete API communication architecture of the EduTrack Pro frontend.

The frontend communicates with the FastAPI backend exclusively through dedicated API service modules.

React components must **never** communicate with backend endpoints directly.

All HTTP communication must pass through the Service Layer.

---

# API Service Philosophy

Every API call should follow

```
Component

↓

Custom Hook (Optional)

↓

Service

↓

Axios Instance

↓

Backend API

↓

Response

↓

Component
```

This architecture keeps

- Components clean
- API logic centralized
- Easier maintenance
- Better testing
- Consistent error handling

---

# Directory Structure

```
src/

services/

│

├── api.js

├── authService.js

├── userService.js

├── studentService.js

├── subjectService.js

├── attendanceService.js

├── marksService.js

├── assignmentService.js

├── submissionService.js

├── dashboardService.js

└── reportService.js
```

---

# Service Responsibilities

Every service should only

✓ Make API requests

✓ Handle request parameters

✓ Return response data

✓ Throw errors

Services should NEVER

- Store React state

- Render UI

- Navigate pages

- Show Toasts

- Access DOM

---

# Axios Instance

File

```
api.js
```

Responsibilities

- Base URL
- Default Headers
- JWT Attachment
- Request Interceptor
- Response Interceptor
- Timeout
- Error Handling

Every service imports

```
api.js
```

No service creates its own Axios instance.

---

# Base URL

Development

```
http://localhost:8000/api/v1
```

Loaded using

```
VITE_API_URL
```

inside

```
.env
```

Never hardcode URLs.

---

# Default Headers

Every request should include

```
Content-Type

application/json
```

Protected requests additionally include

```
Authorization

Bearer JWT
```

---

# Request Interceptor

Responsibilities

```
Read JWT

↓

Attach Authorization Header

↓

Continue Request
```

No component manually attaches JWT.

---

# Response Interceptor

Responsibilities

```
Receive Response

↓

Success

↓

Return Data

OR

↓

401

↓

Logout User

↓

Redirect Login

↓

Show Error
```

Centralize authentication failure.

---

# Global Timeout

Recommended

```
15000 ms
```

Network failures should produce meaningful messages.

---

# Error Handling

Every service should throw standardized errors.

Example

```javascript
throw error.response?.data || error;
```

Components decide how to display errors.

---

# Authentication Service

File

```
authService.js
```

Responsibilities

```
login()

getCurrentUser()

logout()
```

Future

```
refreshToken()

forgotPassword()

resetPassword()
```

---

# Example Functions

```
login(credentials)

getCurrentUser()

logout()
```

---

# User Service

File

```
userService.js
```

Functions

```
getUsers()

getUser()

createUser()

updateUser()

deleteUser()

activateUser()

deactivateUser()
```

---

# Student Service

File

```
studentService.js
```

Functions

```
getStudents()

getStudent()

createStudent()

updateStudent()

deleteStudent()

searchStudents()

getCurrentStudent()
```

---

# Subject Service

File

```
subjectService.js
```

Functions

```
getSubjects()

getSubject()

createSubject()

updateSubject()

deleteSubject()
```

---

# Attendance Service

File

```
attendanceService.js
```

Functions

```
getAttendance()

markAttendance()

updateAttendance()

deleteAttendance()

getAttendanceSummary()

getAttendancePercentage()

getStudentAttendance()
```

---

# Marks Service

File

```
marksService.js
```

Functions

```
getMarks()

addMarks()

updateMarks()

deleteMarks()

getAverageMarks()

getMarksSummary()

getStudentMarks()
```

---

# Assignment Service

File

```
assignmentService.js
```

Functions

```
getAssignments()

createAssignment()

updateAssignment()

deleteAssignment()

getUpcomingAssignments()

getOverdueAssignments()
```

---

# Submission Service

File

```
submissionService.js
```

Functions

```
getSubmissions()

submitAssignment()

updateSubmission()

deleteSubmission()

reviewSubmission()

getPendingReviews()
```

---

# Dashboard Service

File

```
dashboardService.js
```

Functions

```
getTeacherDashboard()

getStudentDashboard()

getTeacherCharts()

getStudentCharts()

getActivity()
```

---

# Report Service

File

```
reportService.js
```

Functions

```
getStudentReport()

getAttendanceReport()

getMarksReport()

getPerformanceReport()

getInstitutionReport()
```

Future

```
downloadPDF()
```

---

# Function Design

Every function should

```
Receive Parameters

↓

Call API

↓

Return Response Data

↓

Throw Error
```

Example

```
createStudent(student)

↓

POST /students

↓

return response.data
```

---

# Async Pattern

Every function should use

```
async

await
```

Avoid nested promise chains.

---

# Return Values

Services should return

```
response.data
```

Not

```
Entire Axios Response
```

Components shouldn't know Axios internals.

---

# API Parameters

Support

```
Pagination

Filtering

Sorting

Searching
```

Example

```
getStudents({

page,

pageSize,

search,

semester

})
```

---

# Upload Support

Future services should support

```
File Upload

PDF Upload

CSV Import

Excel Import
```

Architecture should remain compatible.

---

# Download Support

Future support

```
PDF Reports

CSV Export

Excel Export
```

Services should return

```
Blob
```

when downloading files.

---

# Authentication Flow

```
Login

↓

Store JWT

↓

Axios Interceptor

↓

Protected Requests
```

Automatic throughout application.

---

# Retry Strategy

Not required for MVP.

Future

```
Automatic Retry

Exponential Backoff
```

may be added.

---

# Loading Strategy

Services

DO NOT

manage loading.

Components manage

```
Loading State

↓

Success

↓

Error
```

---

# Caching

No client-side caching for MVP.

Future

```
React Query

TanStack Query

SWR
```

should integrate without redesign.

---

# Security

Services should

Never store passwords.

Never expose JWT.

Never hardcode secrets.

Always use HTTPS in production.

---

# Environment Variables

Required

```
VITE_API_URL
```

Future

```
VITE_APP_NAME

VITE_VERSION

VITE_ENVIRONMENT
```

---

# Naming Convention

Service File

```
studentService.js
```

Functions

```
getStudents()

createStudent()

updateStudent()

deleteStudent()
```

Simple.

Predictable.

Consistent.

---

# Unit Testing

Every service should test

✓ Successful Request

✓ Failed Request

✓ Validation Errors

✓ Authentication Errors

✓ Timeout

✓ Network Failure

✓ Unauthorized Request

---

# Future Compatibility

Architecture should support

```
GraphQL

WebSockets

Notifications

Offline Mode

Background Sync

React Query

Mobile App
```

without changing existing services.

---

# API Service Checklist

Every service should

✓ Use Axios Instance.

✓ Return response data.

✓ Throw standardized errors.

✓ Remain stateless.

✓ Avoid UI logic.

✓ Use async/await.

✓ Support future expansion.

---

# Definition of Completion

API Services implementation is complete when

✓ Axios configured.

✓ JWT attached automatically.

✓ Services separated by module.

✓ Components never call Axios directly.

✓ Error handling centralized.

✓ Environment variables configured.

✓ Tests pass.

---

# Summary

The Frontend API Services layer is the communication bridge between the React application and the FastAPI backend.

By centralizing every HTTP request inside dedicated service modules backed by a shared Axios instance, EduTrack Pro achieves clean separation of concerns, maintainable code, consistent error handling, automatic authentication, and a scalable architecture ready for future enhancements.

End of Frontend API Services Specification.