# Screenshot Evidence Guide - Sureprep API Test Suite

This guide explains how to capture screenshots for test execution evidence and documentation.

---

## 📸 **Required Screenshots for Evidence**

### **1. Credential Verification Results**

**What to Capture**: Verification script output showing both V5 and V7 authentication success

**Command to Run**:
```bash
python scripts\verify_credentials.py
```

**Screenshot Should Show**:
- ✅ V5.0 API: [OK] PASSED
- ✅ V7 API: [OK] PASSED
- Status codes (200)
- Token received confirmation
- Timestamp

**How to Capture**:
1. Run the command in terminal
2. Wait for complete output
3. Press `Windows + Shift + S` (Snipping Tool)
4. Select the entire terminal window
5. Save as: `evidence_01_credential_verification.png`

---

### **2. Authentication Test Execution**

**What to Capture**: Pytest execution showing authentication tests passing

**Command to Run**:
```bash
pytest tests\test_sureprep_api_suite.py -v -m authentication
```

**Screenshot Should Show**:
- Test collection results
- PASSED status for both V5 and V7 tests
- Execution time
- Summary: "2 passed"

**How to Capture**:
1. Run the command
2. Scroll to show full output
3. Capture using `Windows + Shift + S`
4. Save as: `evidence_02_authentication_tests.png`

---

### **3. HTML Test Report - Summary Page**

**What to Capture**: Main HTML report showing test results

**File to Open**:
```
reports\api_error_validation_report.html
```

**Screenshot Should Show**:
- Report header with timestamp
- Summary section (tests passed/failed/skipped)
- Total duration
- Environment information

**How to Capture**:
1. Double-click the HTML file to open in browser
2. Take full page screenshot
3. Or use browser screenshot: `Ctrl + Shift + S` (Firefox) or `Ctrl + Shift + P` → "Screenshot" (Chrome)
4. Save as: `evidence_03_html_report_summary.png`

---

### **4. HTML Test Report - Test Details**

**What to Capture**: Detailed test results showing individual test cases

**Screenshot Should Show**:
- Test case names
- ✅ PASSED indicators
- Test duration for each test
- Expand one test to show details

**How to Capture**:
1. Scroll down in HTML report
2. Click to expand a test case
3. Capture the expanded view
4. Save as: `evidence_04_html_report_details.png`

---

### **5. Test Data Configuration**

**What to Capture**: Test data file showing configured credentials

**File to Open**:
```
testData\sureprep_test_data.json
```

**Screenshot Should Show**:
- V5 credentials (UserName, Password, APIKey)
- V7 credentials (ClientID, ClientSecret)
- File structure

**How to Capture**:
1. Open file in VS Code
2. Show lines 1-20 (credential section)
3. Capture using `Windows + Shift + S`
4. Save as: `evidence_05_test_data_config.png`

---

### **6. Pytest Log File**

**What to Capture**: Log file showing detailed execution logs

**File to Open**:
```
reports\pytest.log
```

**Screenshot Should Show**:
- Log entries with timestamps
- API requests to V5.0 and V7 endpoints
- Status Code 200 responses
- Authentication success logs

**How to Capture**:
1. Open pytest.log in VS Code
2. Search for "Authenticate/GetToken"
3. Show lines with authentication requests
4. Save as: `evidence_06_pytest_logs.png`

---

### **7. Project Structure**

**What to Capture**: Overall project folder structure

**Screenshot Should Show**:
- Main folders: tests/, testData/, reports/, docs/, scripts/
- Key files visible
- File tree in VS Code Explorer

**How to Capture**:
1. Open VS Code Explorer (Ctrl + Shift + E)
2. Expand key folders
3. Capture the tree view
4. Save as: `evidence_07_project_structure.png`

---

### **8. Full Test Suite Execution (Optional)**

**What to Capture**: Running all 100+ tests

**Command to Run**:
```bash
pytest tests\test_sureprep_api_suite.py -v --html=reports\full_test_report.html
```

**Screenshot Should Show**:
- Test collection: "collected 101 items"
- Multiple test categories executing
- Final summary
- Report generation message

**How to Capture**:
1. Run full test suite
2. Capture terminal output
3. Save as: `evidence_08_full_test_execution.png`

---

## 🎯 **Quick Screenshot Capture Script**

I'll create a batch script that runs all commands and pauses for you to capture screenshots:

### **Run This Script**: `capture_evidence.bat`

```batch
@echo off
echo ====================================
echo SCREENSHOT EVIDENCE CAPTURE GUIDE
echo ====================================
echo.
echo This script will run each test step and pause for you to capture screenshots.
echo Press any key when ready to start...
pause
echo.

REM Create evidence folder
if not exist "evidence" mkdir evidence

echo.
echo ====================================
echo STEP 1: Credential Verification
echo ====================================
echo.
echo CAPTURE THIS: evidence_01_credential_verification.png
echo Press Windows + Shift + S to capture
echo.
python scripts\verify_credentials.py
echo.
echo Did you capture the screenshot? Press any key to continue...
pause
echo.

echo ====================================
echo STEP 2: Authentication Tests
echo ====================================
echo.
echo CAPTURE THIS: evidence_02_authentication_tests.png
echo.
pytest tests\test_sureprep_api_suite.py -v -m authentication
echo.
echo Did you capture the screenshot? Press any key to continue...
pause
echo.

echo ====================================
echo STEP 3: Open HTML Report
echo ====================================
echo.
echo Opening HTML report in browser...
echo CAPTURE THIS: evidence_03_html_report_summary.png
echo.
start reports\api_error_validation_report.html
echo.
echo Capture the HTML report summary, then press any key...
pause
echo.

echo ====================================
echo STEP 4: Open Test Data File
echo ====================================
echo.
echo Opening test data file...
echo CAPTURE THIS: evidence_05_test_data_config.png
echo.
start notepad testData\sureprep_test_data.json
echo.
echo Capture the test data configuration, then press any key...
pause
echo.

echo ====================================
echo STEP 5: Open Log File
echo ====================================
echo.
echo Opening pytest log file...
echo CAPTURE THIS: evidence_06_pytest_logs.png
echo.
start notepad reports\pytest.log
echo.
echo Capture the log file, then press any key...
pause
echo.

echo ====================================
echo All Steps Complete!
echo ====================================
echo.
echo You should now have captured:
echo 1. Credential verification
echo 2. Authentication test execution
echo 3. HTML report summary
echo 4. Test data configuration
echo 5. Pytest log file
echo.
echo Save all screenshots to: evidence\
echo.
pause
```

---

## 📝 **Screenshot Checklist**

Use this checklist to ensure you have all required evidence:

- [ ] **Evidence 01**: Credential verification results (both V5 & V7 passing)
- [ ] **Evidence 02**: Authentication test execution (2 tests passed)
- [ ] **Evidence 03**: HTML report summary page
- [ ] **Evidence 04**: HTML report test details (expanded view)
- [ ] **Evidence 05**: Test data configuration file
- [ ] **Evidence 06**: Pytest log file (showing API calls)
- [ ] **Evidence 07**: Project structure in VS Code
- [ ] **Evidence 08**: Full test suite execution (optional)

---

## 🖼️ **Screenshot Storage Locations**

### **Recommended Folder Structure**:
```
API_Error_Codes_Validation/
└── evidence/
    ├── evidence_01_credential_verification.png
    ├── evidence_02_authentication_tests.png
    ├── evidence_03_html_report_summary.png
    ├── evidence_04_html_report_details.png
    ├── evidence_05_test_data_config.png
    ├── evidence_06_pytest_logs.png
    ├── evidence_07_project_structure.png
    └── evidence_08_full_test_execution.png (optional)
```

---

## 🔧 **Windows Screenshot Tools**

### **Option 1: Snipping Tool (Recommended)**
- Press: `Windows + Shift + S`
- Select area to capture
- Screenshot copied to clipboard
- Paste into Paint/Word/Document: `Ctrl + V`
- Save with appropriate filename

### **Option 2: Full Screen Screenshot**
- Press: `Windows + PrtScn`
- Screenshot saved to: `Pictures\Screenshots\`
- Rename file appropriately

### **Option 3: Snip & Sketch App**
- Press: `Windows + Shift + S`
- Choose rectangular/freeform/window/fullscreen
- Edit and annotate
- Save with `Ctrl + S`

### **Option 4: Browser Screenshots (for HTML reports)**
- **Firefox**: `Ctrl + Shift + S` → Save full page
- **Chrome**: `F12` → `Ctrl + Shift + P` → Type "screenshot" → Choose option
- **Edge**: Similar to Chrome

---

## 📋 **Screenshot Naming Convention**

**Format**: `evidence_[NUMBER]_[DESCRIPTION]_[YYYYMMDD].png`

**Examples**:
- `evidence_01_credential_verification_20241224.png`
- `evidence_02_authentication_tests_20241224.png`
- `evidence_03_html_report_summary_20241224.png`

---

## 🎨 **Screenshot Best Practices**

1. **High Resolution**: Ensure text is readable
2. **Full Context**: Include relevant headers, timestamps, and summaries
3. **Clear Visibility**: Avoid cutting off important information
4. **Consistent Naming**: Follow naming convention
5. **Include Timestamps**: Show when tests were run
6. **Show Success Indicators**: Highlight PASSED, [OK], green checkmarks
7. **Expand Details**: Show at least one test case in detail

---

## 📤 **Creating Evidence Package**

### **For Documentation/Reporting**:

1. **Create Word Document**: `Sureprep_API_Test_Evidence.docx`
2. **Insert Screenshots** in order with captions
3. **Add Descriptions** for each screenshot
4. **Include Summary** section with:
   - Date of execution
   - Environment (Production/Staging)
   - Test results summary
   - Issues found (if any)

### **Example Document Structure**:
```
SUREPREP API TEST EVIDENCE REPORT
Date: December 24, 2024
Tester: [Your Name]
Environment: Production

1. CREDENTIAL VERIFICATION
   [Screenshot 01]
   Description: Both V5 and V7 credentials verified successfully

2. AUTHENTICATION TESTS
   [Screenshot 02]
   Description: 2 authentication tests passed

3. TEST REPORT SUMMARY
   [Screenshot 03]
   Description: HTML report showing all tests passed

... (continue for all screenshots)
```

---

## ⚡ **Quick Start**

1. Create evidence folder:
   ```bash
   mkdir evidence
   ```

2. Run capture script:
   ```bash
   capture_evidence.bat
   ```

3. Follow on-screen prompts to capture each screenshot

4. Review all screenshots in `evidence/` folder

5. Create documentation package if needed

---

## 📞 **Need Help?**

- **Screenshots not clear?** Increase terminal font size before capturing
- **HTML report not opening?** Check if file exists in `reports/` folder
- **Want video evidence?** Use Windows Game Bar (`Windows + G`) to record

---

**Happy Documenting! 📸**
