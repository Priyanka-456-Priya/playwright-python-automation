# Sureprep API Test Suite Documentation

## Overview
This document provides comprehensive test case documentation for the Sureprep API test suite. The API supports multiple versions (V5.0, V6.0, V6.1, V7) and covers various functional areas.

## Test Suite Statistics
- **Total Test Cases**: 100+
- **API Versions Covered**: V5.0, V6.0, V6.1, V7
- **Functional Areas**: 9 (Authentication, BinderInfo, Binder, Document, Lookup, Status, TaxCaddy, RWAPI, UTIntegration)

## Test Categories

### 1. Authentication Tests (TC_AUTH_001 - TC_AUTH_006)

| Test Case ID | Test Case Name | Description | Priority | API Version |
|-------------|----------------|-------------|----------|-------------|
| TC_AUTH_001 | test_auth_v5_get_token_valid_credentials | Verify V5.0 GetToken with valid credentials returns success | High | V5.0 |
| TC_AUTH_002 | test_auth_v7_get_token_valid_credentials | Verify V7 GetToken with valid credentials returns success | High | V7 |
| TC_AUTH_003 | test_auth_get_token_invalid_credentials | Verify GetToken with invalid credentials returns 401 | High | V7 |
| TC_AUTH_004 | test_auth_get_token_missing_username | Verify GetToken with missing username returns 400 | Medium | V7 |
| TC_AUTH_005 | test_auth_get_token_missing_password | Verify GetToken with missing password returns 400 | Medium | V7 |
| TC_AUTH_006 | test_auth_get_token_empty_payload | Verify GetToken with empty payload returns 400 | Medium | V7 |

**Test Data Required**:
- Valid username and password
- Invalid credentials
- Empty payloads

**Expected Results**:
- Valid credentials: 200 status code with token
- Invalid credentials: 401 Unauthorized
- Missing fields: 400 Bad Request

---

### 2. BinderInfo Tests (TC_BINDER_INFO_001 - TC_BINDER_INFO_015)

| Test Case ID | Test Case Name | Description | Priority | API Version |
|-------------|----------------|-------------|----------|-------------|
| TC_BINDER_INFO_001 | test_get_binder_details_v5 | Verify V5.0 GetBinderDetails returns binder information | High | V5.0 |
| TC_BINDER_INFO_002 | test_get_binder_details_v7 | Verify V7 GetBinderDetails returns binder information | High | V7 |
| TC_BINDER_INFO_003 | test_get_binder_details_by_id_v7 | Verify V7 GetBinderDetails with path parameter | High | V7 |
| TC_BINDER_INFO_004 | test_get_binder_details_by_unique_identifier | Verify GetBinderDetailsByUniqueIdentifier | Medium | V7 |
| TC_BINDER_INFO_005 | test_get_uncleared_notes_v5 | Verify V5.0 GetUnclearedNotes returns notes | Medium | V5.0 |
| TC_BINDER_INFO_006 | test_get_unreviewed_tr_stamps_v7 | Verify GetUnreviewedTRStamps returns stamps | Medium | V7 |
| TC_BINDER_INFO_007 | test_get_unreviewed_sticky_notes | Verify GetUnreviewedStickyNotes returns notes | Medium | V7 |
| TC_BINDER_INFO_008-011 | test_get_unreviewed_workpapers_by_level | Verify GetUnreviewedWorkpapers for L1-L4 levels | Medium | V7 |
| TC_BINDER_INFO_012 | test_get_document_pending_review_count | Verify GetDocumentPendingReviewCount returns count | Medium | V7 |
| TC_BINDER_INFO_013 | test_get_document_pending_signature_count | Verify GetDocumentPendingSignatureCount | Medium | V7 |
| TC_BINDER_INFO_014 | test_get_document_pending_upload_count | Verify GetDocumentPendingUploadCount | Medium | V7 |
| TC_BINDER_INFO_015 | test_get_binder_pending_items | Verify GetBinderPendingItems returns pending items | Medium | V7 |

**Test Data Required**:
- Valid binder IDs
- Unique identifiers
- Binder IDs with various review statuses

**Expected Results**:
- 200 status code with binder details for valid IDs
- 404 for non-existent binders
- Proper count values in response

---

### 3. Binder CRUD Tests (TC_BINDER_001 - TC_BINDER_015)

| Test Case ID | Test Case Name | Description | Priority | API Version |
|-------------|----------------|-------------|----------|-------------|
| TC_BINDER_001 | test_create_binder_v5_valid_payload | Verify V5.0 CreateBinder with valid payload | Critical | V5.0 |
| TC_BINDER_002 | test_create_binder_v7_valid_payload | Verify V7 CreateBinder with valid payload | Critical | V7 |
| TC_BINDER_003 | test_create_binder_missing_required_fields | Verify CreateBinder with missing required fields returns 400 | High | V7 |
| TC_BINDER_004 | test_upload_binder_documents_v5 | Verify V5.0 UploadBinderDocuments | High | V5.0 |
| TC_BINDER_005 | test_upload_binder_documents_v7 | Verify V7 UploadBinderDocuments | High | V7 |
| TC_BINDER_006 | test_submit_binder_v5 | Verify V5.0 SubmitBinder | High | V5.0 |
| TC_BINDER_007 | test_submit_binder_v7 | Verify V7 SubmitBinder | High | V7 |
| TC_BINDER_008 | test_update_project_id_v7 | Verify UpdateProjectID | Medium | V7 |
| TC_BINDER_009 | test_get_states_and_localities_v7 | Verify GetStatesandLocalities returns list | Medium | V7 |
| TC_BINDER_010 | test_get_binders_status_with_states | Verify GetBindersStatusWithStates | Medium | V7 |
| TC_BINDER_011 | test_download_binder_pbfx_v7 | Verify DownloadBinderPBFX | Medium | V7 |
| TC_BINDER_012 | test_get_pbfx_by_id_v7 | Verify GetPBFx with path parameter | Medium | V7 |
| TC_BINDER_013 | test_get_binder_audit_log | Verify GetBinderAuditLog returns log entries | Medium | V7 |
| TC_BINDER_014 | test_update_owner_member | Verify UpdateOwnerMember | Medium | V7 |
| TC_BINDER_015 | test_print_binder | Verify PrintBinder | Low | V7 |

**Test Data Required**:
- Valid binder creation payloads
- Document files for upload
- Valid status IDs
- Project IDs

**Expected Results**:
- Successful creation: 200/201 with binder ID
- Validation errors: 400 with error details
- Successful operations return appropriate responses

---

### 4. Document Tests (TC_DOC_001 - TC_DOC_005)

| Test Case ID | Test Case Name | Description | Priority | API Version |
|-------------|----------------|-------------|----------|-------------|
| TC_DOC_001 | test_get_documents_v5 | Verify V5.0 GetDocuments returns document list | High | V5.0 |
| TC_DOC_002 | test_get_documents_v7 | Verify V7 GetDocuments returns document list | High | V7 |
| TC_DOC_003 | test_download_document_v5 | Verify V5.0 DownloadDocument | High | V5.0 |
| TC_DOC_004 | test_download_document_v7 | Verify V7 DownloadDocument | High | V7 |
| TC_DOC_005 | test_download_document_invalid_id | Verify DownloadDocument with invalid ID returns 404 | Medium | V7 |

**Test Data Required**:
- Valid binder and document IDs
- Invalid document IDs

**Expected Results**:
- Document list with metadata
- Document content as binary
- 404 for invalid IDs

---

### 5. Lookup Service Tests (TC_LOOKUP_001 - TC_LOOKUP_014)

| Test Case ID | Test Case Name | Description | Priority | API Version |
|-------------|----------------|-------------|----------|-------------|
| TC_LOOKUP_001 | test_get_local_path_v7 | Verify GetLocalPathToDownloadFiles | Low | V7 |
| TC_LOOKUP_002 | test_get_service_types_v7 | Verify ServiceTypes returns list | Medium | V7 |
| TC_LOOKUP_003 | test_get_office_locations_v7 | Verify OfficeLocations returns list | Medium | V7 |
| TC_LOOKUP_004 | test_get_binder_types_v7 | Verify BinderTypes returns list | High | V7 |
| TC_LOOKUP_005 | test_get_tax_software_list_v7 | Verify TaxSoftwareList returns list | Medium | V7 |
| TC_LOOKUP_006 | test_get_binder_templates_v7 | Verify BinderTemplates returns list | High | V7 |
| TC_LOOKUP_007 | test_get_binder_template_list_v7 | Verify BinderTemplateList returns list | Medium | V7 |
| TC_LOOKUP_008 | test_get_binder_status_list_v7 | Verify BinderStatusList returns list | High | V7 |
| TC_LOOKUP_009 | test_get_service_units_v7 | Verify ServiceUnits (V7 only) | Medium | V7 |
| TC_LOOKUP_010 | test_get_domain_information_v7 | Verify DomainInformation (V7 only) | Medium | V7 |
| TC_LOOKUP_011 | test_get_user_domain_details_v7 | Verify UserDomainDetails (V7 only) | Medium | V7 |
| TC_LOOKUP_012 | test_get_custom_field_enabled_v7 | Verify CustomFieldEnabled (V7 only) | Low | V7 |
| TC_LOOKUP_013 | test_ut_search_client_guid_v7 | Verify UTSearchClientGUID (V7 only) | Medium | V7 |
| TC_LOOKUP_014 | test_7216_consent_enabled_v7 | Verify 7216ConsentEnabled (V7 only) | Low | V7 |

**Test Data Required**:
- Domain information
- Client GUIDs

**Expected Results**:
- All lookup services return lists/objects with proper structure
- 200 status code
- Valid JSON response

---

### 6. Status Management Tests (TC_STATUS_001 - TC_STATUS_005)

| Test Case ID | Test Case Name | Description | Priority | API Version |
|-------------|----------------|-------------|----------|-------------|
| TC_STATUS_001 | test_get_status_v5 | Verify V5.0 GetStatus | High | V5.0 |
| TC_STATUS_002 | test_get_status_v7 | Verify V7 GetStatus | High | V7 |
| TC_STATUS_003 | test_change_binder_status_v5 | Verify V5.0 ChangeBinderStatus | High | V5.0 |
| TC_STATUS_004 | test_change_binder_status_v7 | Verify V7 ChangeBinderStatus | High | V7 |
| TC_STATUS_005 | test_change_binder_status_invalid_status | Verify invalid status returns 400 | Medium | V7 |

**Test Data Required**:
- Valid binder IDs
- Valid and invalid status IDs

**Expected Results**:
- Current status returned for GetStatus
- Status updated successfully for valid requests
- 400 for invalid status IDs

---

### 7. TaxCaddy API Tests (TC_TAXCADDY_001 - TC_TAXCADDY_024)

| Test Case ID | Test Case Name | Description | Priority | API Version |
|-------------|----------------|-------------|----------|-------------|
| TC_TAXCADDY_001 | test_create_client_v5 | Verify V5.0 CreateClient | High | V5.0 |
| TC_TAXCADDY_002 | test_create_client_v6 | Verify V6.0 CreateClient | High | V6.0 |
| TC_TAXCADDY_003 | test_create_client_v61 | Verify V6.1 CreateClient | High | V6.1 |
| TC_TAXCADDY_004 | test_create_client_v7 | Verify V7 CreateClient | High | V7 |
| TC_TAXCADDY_005 | test_create_drl_v5 | Verify CreateDrl | High | V5.0 |
| TC_TAXCADDY_006 | test_get_client_details_v7 | Verify GetClientDetails | High | V7 |
| TC_TAXCADDY_007 | test_domain_subscribe_v7 | Verify DomainSubscribe (V7 only) | Medium | V7 |
| TC_TAXCADDY_008 | test_domain_unsubscribe_v7 | Verify DomainUnsubscribe (V7 only) | Medium | V7 |
| TC_TAXCADDY_009 | test_client_subscribe_v7 | Verify ClientSubscribe (V7 only) | Medium | V7 |
| TC_TAXCADDY_010 | test_client_unsubscribe_v7 | Verify ClientUnsubscribe (V7 only) | Medium | V7 |
| TC_TAXCADDY_011 | test_download_document_taxcaddy | Verify DownloadDocument | High | V7 |
| TC_TAXCADDY_012 | test_get_drl_status | Verify GetDRLStatus | High | V7 |
| TC_TAXCADDY_013 | test_send_drl | Verify SendDRL | High | V7 |
| TC_TAXCADDY_014 | test_disconnect_devices_v7 | Verify DisconnectDevices (V7 only) | Medium | V7 |
| TC_TAXCADDY_015 | test_send_questionnaire | Verify SendQuestionnaire | Medium | V7 |
| TC_TAXCADDY_016 | test_print_questionnaire_v7 | Verify PrintQuestionnaire (V7 only) | Low | V7 |
| TC_TAXCADDY_017 | test_send_taxcaddy_invitation | Verify SendTaxCaddyInvitation | Medium | V7 |
| TC_TAXCADDY_018 | test_send_invitation_reminder | Verify SendTaxCaddyInvitationReminder | Medium | V7 |
| TC_TAXCADDY_019 | test_get_drl_items_by_tax_year | Verify GetDRLItems with path parameter | Medium | V7 |
| TC_TAXCADDY_020 | test_delete_drl_item | Verify DeleteDRLItem | Medium | V7 |
| TC_TAXCADDY_021 | test_get_member_details | Verify GetMemberDetails | Medium | V7 |
| TC_TAXCADDY_022 | test_update_member | Verify UpdateMember | Medium | V7 |
| TC_TAXCADDY_023 | test_get_document_categories | Verify TaxCaddyDocumentCategories | Medium | V7 |
| TC_TAXCADDY_024 | test_send_document_upload_request | Verify SendDocumentUploadRequest | Medium | V7 |

**Test Data Required**:
- Client information (name, email, phone)
- DRL details
- Member details
- Questionnaire IDs
- Document categories

**Expected Results**:
- Clients created successfully with IDs
- DRL operations complete successfully
- Proper subscription/unsubscription handling
- Document operations return expected content

---

### 8. Review Wizard Tests (TC_RW_001 - TC_RW_002)

| Test Case ID | Test Case Name | Description | Priority | API Version |
|-------------|----------------|-------------|----------|-------------|
| TC_RW_001 | test_launch_review_wizard_v5 | Verify V5.0 LaunchReviewWizard | Medium | V5.0 |
| TC_RW_002 | test_launch_review_wizard_v7 | Verify V7 LaunchReviewWizard | Medium | V7 |

**Test Data Required**:
- Valid binder IDs

**Expected Results**:
- Review wizard launched successfully
- 200 status code with wizard URL or session ID

---

### 9. UT Integration Tests (TC_UT_001 - TC_UT_007)

| Test Case ID | Test Case Name | Description | Priority | API Version |
|-------------|----------------|-------------|----------|-------------|
| TC_UT_001 | test_drl_callback_v5 | Verify V5.0 DRLCallBack | High | V5.0 |
| TC_UT_002 | test_drl_callback_v7 | Verify V7 DRLCallBack | High | V7 |
| TC_UT_003 | test_binder_callback_v5 | Verify V5.0 BinderCallBack | High | V5.0 |
| TC_UT_004 | test_binder_callback_v7 | Verify V7 BinderCallBack | High | V7 |
| TC_UT_005 | test_tax_file_merged_status_v5 | Verify V5.0 TaxFileMergedStatus | Medium | V5.0 |
| TC_UT_006 | test_tax_file_merged_status_v7 | Verify V7 TaxFileMergedStatus | Medium | V7 |
| TC_UT_007 | test_sp_connect_v7 | Verify SPConnect (V7 only) | Medium | V7 |

**Test Data Required**:
- Request IDs
- Engagement IDs
- File IDs
- Callback status values

**Expected Results**:
- Callbacks processed successfully
- 200 status code
- Proper acknowledgment responses

---

### 10. Negative Test Scenarios (TC_NEG_001 - TC_NEG_006)

| Test Case ID | Test Case Name | Description | Priority | Security |
|-------------|----------------|-------------|----------|----------|
| TC_NEG_001 | test_invalid_endpoint | Verify invalid endpoint returns 404 | Medium | No |
| TC_NEG_002 | test_missing_authorization_header | Verify request without auth token returns 401 | High | Yes |
| TC_NEG_003 | test_invalid_auth_token | Verify request with invalid token returns 401 | High | Yes |
| TC_NEG_004 | test_malformed_json_payload | Verify malformed JSON returns 400 | Medium | No |
| TC_NEG_005 | test_sql_injection_attempt | Verify SQL injection attempt is handled safely | Critical | Yes |
| TC_NEG_006 | test_xss_attempt_in_payload | Verify XSS attempt is sanitized | Critical | Yes |

**Test Data Required**:
- Invalid endpoints
- Malformed JSON
- SQL injection strings
- XSS payloads

**Expected Results**:
- Appropriate error codes (400, 401, 404)
- Security vulnerabilities blocked
- Error messages don't leak sensitive information

---

### 11. Performance Test Scenarios (TC_PERF_001 - TC_PERF_002)

| Test Case ID | Test Case Name | Description | Threshold | Priority |
|-------------|----------------|-------------|-----------|----------|
| TC_PERF_001 | test_response_time_authentication | Verify authentication response time < 3s | 3s | High |
| TC_PERF_002 | test_response_time_lookup_services | Verify lookup service response time < 2s | 2s | Medium |

**Expected Results**:
- Response times within thresholds
- No timeout errors
- Consistent performance across test runs

---

## Test Execution Instructions

### Prerequisites
1. Python 3.8 or higher installed
2. Required packages: pytest, requests, pytest-html
3. Valid API credentials (username/password)
4. Network access to API endpoints

### Environment Setup
```bash
# Install dependencies
pip install -r requirements.txt

# Set environment variables
export SUREPREP_BASE_URL="https://api.sureprep.com"
export SUREPREP_USERNAME="your_username"
export SUREPREP_PASSWORD="your_password"
```

### Running Tests

#### Run all tests
```bash
pytest tests/test_sureprep_api_suite.py -v
```

#### Run specific test categories
```bash
# Authentication tests only
pytest tests/test_sureprep_api_suite.py -v -m authentication

# BinderInfo tests only
pytest tests/test_sureprep_api_suite.py -v -m binderinfo

# Negative tests only
pytest tests/test_sureprep_api_suite.py -v -m negative

# Performance tests only
pytest tests/test_sureprep_api_suite.py -v -m performance
```

#### Generate HTML report
```bash
pytest tests/test_sureprep_api_suite.py -v --html=reports/test_report.html --self-contained-html
```

#### Run with parallel execution
```bash
pytest tests/test_sureprep_api_suite.py -v -n 4
```

---

## Test Data Management

### Test Data Location
- **Main test data**: `testData/sureprep_test_data.json`
- **Configuration**: `config/sureprep_api_config.json`

### Updating Test Data
1. Edit the JSON files in the testData directory
2. Follow the existing structure
3. Ensure sensitive data is stored in environment variables

---

## Reporting

### Report Types
1. **HTML Report**: Detailed test execution report with pass/fail status
2. **Console Output**: Real-time test execution output
3. **JUnit XML**: For CI/CD integration

### Report Location
- HTML reports: `reports/test_report.html`
- XML reports: `reports/junit.xml`

---

## Maintenance

### Adding New Test Cases
1. Identify the API endpoint to test
2. Create test method in appropriate test class
3. Add test data to `sureprep_test_data.json`
4. Document the test case in this file
5. Add appropriate pytest markers

### Updating Existing Tests
1. Modify test method as needed
2. Update test data if required
3. Update documentation
4. Verify test still passes

---

## Known Issues and Limitations

1. Some endpoints may require specific database setup
2. Rate limiting may affect test execution
3. Test data IDs need to be updated based on actual system data

---

## Contact and Support

For questions or issues with the test suite:
- Contact: Automation Testing Team
- Documentation: This file
- Issue Tracking: Project management system

---

## Version History

| Version | Date | Changes | Author |
|---------|------|---------|--------|
| 1.0 | 2024-12-24 | Initial test suite creation | Automation Team |

---

## Appendix

### API Version Differences
- **V5.0**: Original API version with basic functionality
- **V6.0**: Added TaxCaddy enhancements
- **V6.1**: Minor TaxCaddy improvements
- **V7**: Latest version with new endpoints (Domain subscriptions, SPConnect, etc.)

### Common Error Codes
- **200**: Success
- **201**: Created
- **400**: Bad Request (validation error)
- **401**: Unauthorized (authentication failure)
- **403**: Forbidden (insufficient permissions)
- **404**: Not Found (resource doesn't exist)
- **500**: Internal Server Error
