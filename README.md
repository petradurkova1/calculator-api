# Calculator API – API Automation Framework

API automation testing project built with **FastAPI, Postman, Newman and GitHub Actions**.

The project demonstrates API functional testing, data-driven testing, CI/CD integration, HTML reporting and automated quality gates.

---

## Project Goals

The main goals of this project are:

- API functional testing
- Positive and negative test scenarios
- CRUD API testing
- PATCH testing
- Data-driven testing
- Environment-based configuration
- Automated test execution with Newman
- CI/CD integration with GitHub Actions
- HTML test reporting
- Quality Gate implementation
- Pull Request protection

---

## Tech Stack

| Technology | Purpose |
|---|---|
| Python | API implementation |
| FastAPI | REST API framework |
| Postman | API test development |
| Newman | CLI test execution |
| CSV | Data-driven test data |
| Git | Version control |
| GitHub Actions | CI/CD |
| HTML Extra Reporter | Test reporting |

---

## Project Structure

```text
calculator-api/
│
├── app/
│   └── main.py
│
├── tests/
│   ├── Calculator_API_Tests.postman_collection.json
│   └── Calculator_Data_Driven_Tests.postman_collection.json
│
├── data/
│   └── add-test-data.csv
│
├── environments/
│   └── Test_Environment.postman_environment.json
│
├── .github/
│   └── workflows/
│       ├── api-tests.yml
│       └── smoke-tests.yml
│
├── requirements.txt
├── README.md
└── ...
```

---

# Test Strategy

The API tests are divided into three logical test suites.

## 1. Smoke Tests

Smoke tests verify that the most important API functionality is working.

### Smoke suite

- Health Check
- Create calculation / Happy path
- Get Calculation by ID

Current Smoke execution:

```text
3 requests
0 failed
```

Smoke tests can be executed:

- automatically on push to `main`
- automatically on Pull Request
- manually using GitHub Actions `Run workflow`

---

## 2. Regression Tests

Regression tests provide broader coverage of the Calculator API.

The regression suite contains:

- positive scenarios
- negative scenarios
- validation tests
- division by zero
- zero values
- negative values
- decimal values
- CRUD scenarios
- PATCH scenarios
- invalid data
- unsupported operations

Current Regression execution:

```text
28 requests
0 failed
```

---

## 3. Data-Driven Tests

The data-driven test suite validates the `/calculate/add` endpoint using multiple sets of input data.

Test data is stored in:

```text
data/add-test-data.csv
```

The CSV file contains the following columns:

```text
a,b,expected
```

Example test data:

```csv
a,b,expected
10,5,15
0,5,5
-10,5,-5
2.5,1.5,4
```

The same Postman request is executed repeatedly using different input values from the CSV file.

Newman is used to run the data-driven tests:

```bash
newman run tests/Calculator_Data_Driven_Tests.postman_collection.json \
  -e environments/Test_Environment.postman_environment.json \
  -d data/add-test-data.csv
```

Current execution:

```text
6 iterations
6 requests
12 assertions
0 failed
```

Data-driven testing helps verify that the same API functionality behaves correctly with different input combinations without creating a separate test for every data set.

---

# Environment Configuration

Postman requests use an environment variable:

```text
baseUrl
```

The current test environment uses:

```text
http://127.0.0.1:8000
```

The exported Postman environment is stored in:

```text
environments/Test_Environment.postman_environment.json
```

Newman loads the environment using the `-e` option:

```bash
newman run tests/Calculator_API_Tests.postman_collection.json \
  -e environments/Test_Environment.postman_environment.json
```

The environment variable is used in Postman requests instead of hardcoding the API URL.

For example:

```text
{{baseUrl}}/health
```

This approach makes the test collection easier to run against different environments without changing the individual requests.

### Environment Structure

```text
environments/
└── Test_Environment.postman_environment.json
```

The environment configuration is used by the Smoke, Regression and Data-Driven test suites.

---

# Running Tests Locally

## Start the API

Install dependencies:

```bash
pip install -r requirements.txt
```

Start FastAPI:

```bash
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```

The API runs on:

```text
http://127.0.0.1:8000
```

---

# Newman

Install Newman:

```bash
npm install -g newman
```

Install the HTML Extra reporter:

```bash
npm install -g newman-reporter-htmlextra
```

---

## Run Smoke Tests

```bash
newman run tests/Calculator_API_Tests.postman_collection.json \
  -e environments/Test_Environment.postman_environment.json \
  --folder Smoke
```

---

## Run Regression Tests

```bash
newman run tests/Calculator_API_Tests.postman_collection.json \
  -e environments/Test_Environment.postman_environment.json \
  --folder Regression
```

---

## Run Data-Driven Tests

```bash
newman run tests/Calculator_Data_Driven_Tests.postman_collection.json \
  -e environments/Test_Environment.postman_environment.json \
  -d data/add-test-data.csv
```

---

# HTML Reports

The CI pipeline generates HTML reports using:

```text
newman-reporter-htmlextra
```

Reports generated by the full API workflow:

```text
reports/
├── regression-report.html
└── data-driven-report.html
```

The dedicated Smoke workflow generates:

```text
reports/
└── smoke-report.html
```

Reports are uploaded to GitHub Actions as workflow artifacts.

---

# CI/CD

The project uses GitHub Actions for automated API testing.

## Smoke Workflow

```text
.github/workflows/smoke-tests.yml
```

The Smoke workflow runs:

```text
Push to main
      ↓
Pull Request
      ↓
Manual Run
      ↓
Start API
      ↓
Health Check
      ↓
Smoke Tests
      ↓
HTML Report
      ↓
Artifact
```

---

## API Test Workflow

```text
.github/workflows/api-tests.yml
```

The full API workflow runs:

```text
Start API
    ↓
Health Check
    ↓
Regression Tests
    ↓
Data-Driven Tests
    ↓
HTML Reports
    ↓
Artifacts
```

---

# Quality Gate

Newman is executed with:

```bash
--bail
```

This makes the test execution fail when the test suite fails.

The GitHub Actions workflow therefore acts as a **CI Quality Gate**.

Successful execution:

```text
API test PASS
     ↓
Newman PASS
     ↓
GitHub Actions PASS
     ↓
PR can continue
```

If a test fails:

```text
API test FAIL
     ↓
Newman FAIL
     ↓
GitHub Actions FAIL
     ↓
PR Quality Gate FAIL
```

---

# Pull Request Quality Gate

The `main` branch is protected using a GitHub Ruleset.

Required status checks:

```text
API Tests / api-tests
Smoke Tests / smoke-tests
```

A Pull Request must pass the required checks before it can be merged.

The Quality Gate has been verified with both:

```text
🟢 Passing scenario
```

and:

```text
🔴 Intentional test failure
```

After fixing the test data:

```text
🟢 Passing scenario
```

This confirms that the CI Quality Gate behaves as expected.

---

# Test Coverage Summary

| Test Suite | Requests / Iterations | Failed |
|---|---:|---:|
| Smoke | 3 requests | 0 |
| Regression | 28 requests | 0 |
| Data-driven | 6 iterations | 0 |

Additional validation performed:

- Newman CLI execution
- Environment-based execution
- CSV data-driven execution
- HTML reporting
- GitHub Actions execution
- Pull Request checks
- Intentional failure validation
- Branch protection validation

---

# Key QA Automation Concepts Demonstrated

This project demonstrates practical experience with:

- REST API testing
- Postman Collections
- Test scripting
- Pre-request scripts
- Environment variables
- Dynamic test data
- Data-driven testing
- Positive testing
- Negative testing
- CRUD testing
- PATCH testing
- API validation
- Newman CLI
- CI/CD
- GitHub Actions
- Quality Gates
- Pull Request checks
- Branch protection
- Automated reporting

---

# Future Improvements

Possible future improvements:

- API schema validation
- OpenAPI contract testing
- Authentication testing
- Additional data-driven scenarios
- Test tagging
- Parallel test execution
- JUnit reporting
- Test result history
- Docker-based test execution
- Separate environments for DEV / TEST / STAGE
- Performance testing
- Security testing