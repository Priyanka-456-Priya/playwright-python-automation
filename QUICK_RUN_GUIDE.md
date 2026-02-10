# Quick Run Guide - Execute Tests & View Allure Reports

## 🚀 Fastest Way - One Command

### Windows (Command Prompt or PowerShell)
```bash
pytest tests/test_TY2025_swagger_apis.py && allure serve reports/allure-results
```

### Linux/Mac (Terminal)
```bash
pytest tests/test_TY2025_swagger_apis.py && allure serve reports/allure-results
```

## 📝 Using Convenience Scripts (Recommended)

We've created easy-to-use scripts that automatically:
1. ✅ Activate virtual environment
2. ✅ Run all 113 tests
3. ✅ Generate Allure report
4. ✅ Open report in your browser

### Windows
```bash
# Double-click this file OR run in terminal:
run_tests_with_report.bat
```

### Linux/Mac
```bash
# Make executable (first time only):
chmod +x run_tests_with_report.sh

# Run the script:
./run_tests_with_report.sh
```

## 📊 Alternative Commands

### Option 1: Run & Serve (Temporary Report)
```bash
# Tests run, report opens automatically, closes when you exit
pytest tests/test_TY2025_swagger_apis.py && allure serve reports/allure-results
```

**Pros**: Fastest, no cleanup needed
**Cons**: Report not saved permanently

### Option 2: Run, Generate & Open (Permanent Report)
```bash
# Tests run, report saved to reports/allure-report/, opens automatically
pytest tests/test_TY2025_swagger_apis.py && allure generate reports/allure-results -o reports/allure-report --clean && allure open reports/allure-report
```

**Pros**: Report saved for later viewing
**Cons**: Slightly slower

### Option 3: Just Open Last Report
```bash
# If tests already ran, just open the report
allure open reports/allure-report
```

## 🎯 Quick Commands Reference

| Task | Command |
|------|---------|
| **Run all tests** | `pytest tests/test_TY2025_swagger_apis.py` |
| **Run + Open report** | `pytest tests/test_TY2025_swagger_apis.py && allure serve reports/allure-results` |
| **Open last report** | `allure open reports/allure-report` |
| **Generate report** | `allure generate reports/allure-results -o reports/allure-report --clean` |
| **Run specific test** | `pytest tests/test_TY2025_swagger_apis.py::TestSwaggerAPIs::test_v5_0_authenticate_gettoken_1` |
| **Run with markers** | `pytest tests/test_TY2025_swagger_apis.py -m authentication` |

## 🖥️ VS Code Integration

### Add to VS Code Tasks
Create `.vscode/tasks.json`:

```json
{
  "version": "2.0.0",
  "tasks": [
    {
      "label": "Run Tests & Open Allure Report",
      "type": "shell",
      "command": "pytest tests/test_TY2025_swagger_apis.py && allure serve reports/allure-results",
      "group": {
        "kind": "test",
        "isDefault": true
      },
      "presentation": {
        "reveal": "always",
        "panel": "new"
      }
    }
  ]
}
```

Then press: `Ctrl+Shift+P` → "Tasks: Run Task" → "Run Tests & Open Allure Report"

## 🔄 Continuous Testing

### Watch Mode (Auto-run on file changes)
```bash
# Install pytest-watch
pip install pytest-watch

# Run in watch mode
ptw tests/test_TY2025_swagger_apis.py -- --alluredir=reports/allure-results
```

## 📈 What Happens When You Run

1. **Test Execution** (2-3 minutes)
   - All 113 tests execute
   - Request/Response data captured
   - Results saved to `reports/allure-results/`

2. **Report Generation** (5-10 seconds)
   - Allure processes JSON results
   - Creates HTML report with charts

3. **Browser Opens** (Automatic)
   - Report opens at `http://localhost:PORT/`
   - Interactive dashboard with:
     - Test results overview
     - Charts and graphs
     - Request/Response attachments
     - Timeline view
     - Test categorization

## 🎨 Report Features

Your Allure report includes:

- **Overview Dashboard** - Summary with pass/fail statistics
- **Suites** - All 113 tests organized by suite
- **Graphs** - Visual representation of:
  - Status distribution (Pass/Fail)
  - Severity levels (Critical/Normal)
  - Duration distribution
- **Timeline** - Execution timeline
- **Behaviors** - Tests grouped by:
  - Features (SurePrep API)
  - Stories (Authentication, Binder Operations, etc.)
- **Packages** - Test organization by package
- **Attachments** - For each test:
  - Request details (JSON)
  - Response status code (Text)
  - Response body (JSON)

## 💡 Pro Tips

### Tip 1: Filter Tests Before Running
```bash
# Run only authentication tests
pytest tests/test_TY2025_swagger_apis.py -m authentication && allure serve reports/allure-results

# Run only critical tests
pytest tests/test_TY2025_swagger_apis.py -m "severity:critical" && allure serve reports/allure-results
```

### Tip 2: Run Tests in Parallel (Faster)
```bash
# Install pytest-xdist
pip install pytest-xdist

# Run with 4 workers
pytest tests/test_TY2025_swagger_apis.py -n 4 && allure serve reports/allure-results
```

### Tip 3: Save Report History
```bash
# Keep report history for trends
pytest tests/test_TY2025_swagger_apis.py
allure generate reports/allure-results -o reports/allure-report
# History is automatically preserved in reports/allure-report/history/
```

### Tip 4: Schedule Regular Runs (Windows Task Scheduler)
1. Open Task Scheduler
2. Create new task
3. Set trigger (e.g., daily at 9 AM)
4. Action: Run `run_tests_with_report.bat`

## 🐛 Troubleshooting

### Issue: "allure: command not found"
**Solution**: Install Allure CLI
```bash
# Windows (npm)
npm install -g allure-commandline

# Windows (Scoop)
scoop install allure

# Mac
brew install allure
```

### Issue: "No module named 'allure'"
**Solution**: Install allure-pytest
```bash
pip install allure-pytest
```

### Issue: Browser doesn't open automatically
**Solution**: Manually open the URL shown in terminal
```
Starting web server...
Server started at http://localhost:54321/
```
Copy the URL and paste in your browser.

## 📞 Need Help?

- Full documentation: [ALLURE_REPORTING_GUIDE.md](ALLURE_REPORTING_GUIDE.md)
- Project README: [README.md](README.md)

---

**Last Updated**: February 2026
**Total Tests**: 113
**Average Duration**: 2-3 minutes
