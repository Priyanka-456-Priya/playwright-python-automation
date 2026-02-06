# Evidence Folder - Screenshot Documentation

## 📁 **Folder Purpose**

This folder contains screenshot evidence for Sureprep API test execution.

---

## 📸 **Required Screenshots**

Place the following screenshots in this folder:

### **1. Credential Verification**
**Filename**: `01_credential_verification.png`
- Shows V5 and V7 authentication success
- Status code 200 for both
- Tokens received

### **2. Authentication Test Execution**
**Filename**: `02_authentication_tests.png`
- Shows pytest execution
- 2 tests passed
- Test duration and summary

### **3. HTML Test Report**
**Filename**: `03_html_report_summary.png`
- HTML report in browser
- Summary section with pass/fail counts
- Test results table

### **4. Test Data Configuration**
**Filename**: `04_test_data_config.png`
- testData/sureprep_test_data.json file
- V5 and V7 credentials visible
- Lines 1-20 showing credential structure

### **5. Pytest Log File**
**Filename**: `05_pytest_logs.png`
- reports/pytest.log file
- Authentication API calls
- Status 200 responses
- Timestamp entries

### **6. Project Structure**
**Filename**: `06_project_structure.png`
- VS Code Explorer or tree command output
- Folder structure visible
- Key directories: tests, testData, reports, docs, scripts

---

## 🚀 **How to Capture**

### **Automated Method** (Recommended):
```bash
# Run from project root
capture_evidence.bat
```

This script will:
- Run each test step
- Pause for you to capture screenshots
- Guide you through the entire process
- Tell you exactly what to capture

### **Manual Method**:
See [SCREENSHOT_QUICK_REFERENCE.md](../SCREENSHOT_QUICK_REFERENCE.md) for manual capture instructions.

---

## ✅ **Verification**

After capturing, verify you have:
- [ ] 6 PNG files in this folder
- [ ] Files follow naming convention (01-06)
- [ ] All screenshots are clear and readable
- [ ] Success indicators visible in screenshots
- [ ] Timestamps visible where applicable

---

## 📄 **Creating Documentation**

Once you have all screenshots, you can:

1. Create a Word document
2. Insert all screenshots in order
3. Add captions and descriptions
4. Include test summary and results

Example structure:
```
Sureprep API Test Evidence Report
Date: 2024-12-24

1. Credential Verification
   [Insert 01_credential_verification.png]
   Description: Both V5 and V7 credentials verified successfully

2. Authentication Tests
   [Insert 02_authentication_tests.png]
   Description: All authentication tests passed (2/2)

... (continue for all screenshots)
```

---

## 📂 **Expected Files**

After completion, this folder should contain:

```
evidence/
├── README.md (this file)
├── 01_credential_verification.png
├── 02_authentication_tests.png
├── 03_html_report_summary.png
├── 04_test_data_config.png
├── 05_pytest_logs.png
└── 06_project_structure.png
```

---

## 🔗 **Related Documentation**

- [Screenshot Evidence Guide](../docs/SCREENSHOT_EVIDENCE_GUIDE.md) - Detailed instructions
- [Quick Reference](../SCREENSHOT_QUICK_REFERENCE.md) - Quick capture guide
- [Test Documentation](../docs/SUREPREP_API_TEST_CASES.md) - Test case details

---

## 📞 **Need Help?**

If you need assistance:
1. Review [SCREENSHOT_QUICK_REFERENCE.md](../SCREENSHOT_QUICK_REFERENCE.md)
2. Run `capture_evidence.bat` for guided capture
3. Check Windows screenshot shortcuts: `Windows + Shift + S`

---

**Status**: 📂 Ready for screenshots

**Last Updated**: 2024-12-24
