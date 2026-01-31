This project is a robust automation framework designed to test [Name of Website, e.g., SauceDemo] using **Playwright** and **Python**. It demonstrates the transition from manual testing to a scalable, automated approach using modern industry standards.

## 🚀 Features
* **Pattern:** Page Object Model (POM) for high maintainability.
* **Test Runner:** Pytest for powerful assertions and test suite management.
* **Reporting:** Integrated Allure/HTML Reports for clear execution visibility.
* **CI/CD:** Configured with GitHub Actions to run tests automatically on every push.
* **Parallel Execution:** Designed to run tests across multiple browsers (Chromium, Firefox, WebKit) simultaneously.

## 🛠 Tech Stack
* **Language:** Python 3.x
* **Framework:** Playwright
* **Test Runner:** Pytest
* **CI/CD:** GitHub Actions

## 📁 Project Structure
```text
├── pages/               # Page Object classes (Locators & Actions)
├── tests/               # Test scripts grouped by feature
├── data/                # Test data (JSON/CSV)
├── conftest.py          # Pytest fixtures and browser setup
├── requirements.txt     # Project dependencies
└── pytest.ini           # Pytest configuration settings
