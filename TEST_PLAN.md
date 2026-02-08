# TEST PLAN  
## ERPNext Priority Engine

---

## 1. Introduction
This document describes the test plan for the **ERPNext Priority Engine** system.
The goal of this test plan is to validate backend business logic and API behavior,
as well as frontend UI functionality and user flows.

---

## 2. Test Scope

### In Scope
- Backend business logic (services and models)
- Backend API endpoints
- Integration with ERPNext
- Frontend UI validation
- End-to-End user flows

### Out of Scope
- Performance testing
- Security testing
- Load / stress testing

---

# BACKEND TEST PLAN

## 3. Backend Test Strategy

### Test Types
- API Mocked Tests (Unit Tests)
- Integration Tests

### Tools
- Python
- unittest / pytest
- FastAPI TestClient
- pytest-cov

---

## 4. API Mocked Tests (Unit Tests)

### Purpose
Validate backend **business logic** independently of external systems.

### Components Tested
- PriorityService
- InventoryService
- Priority Models
- Inventory Models

### What is Tested
- Priority calculation (HIGH / MEDIUM / LOW)
- Edge cases (None, zero values, empty lists)
- Sorting logic
- Limit validation
- Data conversion (to_dict)

### What is NOT Tested
- ERPNext connectivity
- API controllers
- Network behavior

### API Mocked – Test Cases

| Test Name               | Component | Description                          | Expected Result        |
|------------------------|-----------|--------------------------------------|------------------------|
| TestInventoryModels    | Models    | Defaults & to_dict                   | Valid object           |
| TestPriorityService    | Service   | Invoice priority calculation         | Correct priority       |
| TestInventoryService   | Service   | Inventory priority calculation       | Correct priority       |
| Sorting Logic          | Service   | Priority sorting                     | Correct order          |
| Limit Validation       | Service   | Invalid limit handling               | Exception / None       |

---

## 5. Backend Integration Tests

### Purpose
Verify backend API works end-to-end with **ERPNext**.

### Preconditions
- Environment variables configured:
  - `ERPNEXT_BASE_URL`
  - `ERPNEXT_API_KEY`

### Tools
- FastAPI TestClient
- unittest

### Tested Endpoints
- `/priority/issues`
- `/inventory/issues`

### Special Handling
Tests are conditionally skipped when ERPNext credentials are missing
to avoid CI failures.

### Integration – Test Cases

| Endpoint                | Description                    | Expected Result |
|-------------------------|--------------------------------|----------------|
| /priority/issues        | API availability               | 200 OK         |
| /priority/issues?limit=1| Limit parameter validation     | 200 OK         |
| /inventory/issues       | Inventory issues response      | issues + count |

---

# FRONTEND TEST PLAN

## 6. Frontend Test Strategy

### Test Types
- UI Feature Tests
- UI End-to-End (E2E) Tests

### Tools
- Playwright
- Chromium
- data-testid selectors

---

## 7. UI Feature Test

### Purpose
Validate availability of a **single UI feature**.

### Feature Tested
- Dashboard page
- Invoice table

### UI Feature – Test Case

| Test Name        | Description                  | Expected Result        |
|------------------|------------------------------|------------------------|
| Dashboard Load   | Dashboard page loads         | Invoice table visible  |

---

## 8. UI End-to-End Test (POM)

### Purpose
Validate a complete **user journey** in the frontend.

### Design Pattern
- Page Object Model (POM)

### User Flow
1. Open Dashboard  
2. Click Apply Filters  
3. Validate results  

### UI E2E – Test Case

| Test Name        | Description                  | Expected Result        |
|------------------|------------------------------|------------------------|
| Apply Filters E2E| Full user interaction flow   | Invoice table visible  |

---

## 9. Test Environment
- Local development
- GitHub Actions CI
- Headless Chromium browser

---

## 10. Conclusion
This test plan provides structured and layered test coverage
for backend and frontend components following QA best practices.
