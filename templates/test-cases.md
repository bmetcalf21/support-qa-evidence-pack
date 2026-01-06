# Test Suite: Login & Authentication (SSO/MFA)

| ID | Test Scenario | Steps | Expected Result | Pass/Fail |
|:---|:---|:---|:---|:---|
| **TC-01** | **Standard Login (Happy Path)** | 1. Enter valid User/Pass<br>2. Enter valid MFA code | Dashboard loads successfully. | |
| **TC-02** | **Invalid Password** | 1. Enter valid User<br>2. Enter wrong Pass | Error: "Invalid credentials" (no detailed info). | |
| **TC-03** | **MFA Timeout** | 1. Enter valid User/Pass<br>2. Wait 60s<br>3. Enter MFA code | Error: "Code expired" or "Session timeout". | |
| **TC-04** | **SQL Injection Attempt** | 1. Enter User: `' OR '1'='1`<br>2. Enter any Pass | System sanitizes input; Login fails. | |