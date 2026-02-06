# Upload Document API Test Guide

## Overview

This guide explains how to test the Upload Binder Document API endpoint. The API allows uploading PDF documents to existing binders.

## API Endpoint

**POST** `/Binder/UploadBinderDocuments?binder_Id={binderId}`

### Request
- **Method**: POST
- **Content-Type**: multipart/form-data
- **Headers**:
  - `AuthToken`: Required authentication token
- **Query Parameters**:
  - `binder_Id` (required): The ID of the binder to upload to
- **Body**: Form data with file attachment

### Response
```json
[
  {
    "name": "sample.pdf",
    "message": "",
    "size": 549
  }
]
```

## Setup

### 1. Generate Sample PDF

Before running upload tests, generate a sample PDF file:

```bash
node scripts/generateSamplePDF.js
```

This creates a minimal valid PDF at `testData/sample.pdf`.

### 2. Configure Test Data

The test data is configured in `testData/binderTestData.js`:

```javascript
uploadDocumentData: {
    validFilePath: 'C:/Users/6124481/VS_CODE Projects/API_Error_Codes_Validation/testData/sample.pdf',
    invalidFilePath: 'C:/Users/6124481/VS_CODE Projects/API_Error_Codes_Validation/testData/nonexistent.pdf'
}
```

## Running Tests

### Option 1: Run Full Test Suite

```bash
npm test
```

This includes upload document tests as part of the complete test suite.

### Option 2: Run Upload Tests Only

```bash
npx mocha "tests/binderApi.test.js" --grep "Upload Binder Document Tests"
```

### Option 3: Run Standalone Script

Single document upload:
```bash
node scripts/testUploadDocument.js
```

Multiple document uploads:
```bash
node scripts/testUploadDocument.js multiple
```

## Test Cases

### 1. Successful Upload
**Test**: Upload a valid PDF to an existing binder
- Creates a new binder
- Uploads sample.pdf
- Verifies the upload succeeded
- **Expected**: Document uploaded successfully

### 2. Invalid Binder ID
**Test**: Upload to a non-existent binder
- Attempts to upload to binder ID 999999999
- **Expected**: Error thrown for invalid binder ID

### 3. Invalid File Path
**Test**: Upload a file that doesn't exist
- Attempts to upload a non-existent file
- **Expected**: ENOENT error (file not found)

## Code Example

### Using BinderApiPage

```javascript
const BinderApiPage = require('./pages/BinderApiPage');
const testData = require('./testData/binderTestData');

async function uploadDocument() {
    const binderApi = new BinderApiPage();

    // Authenticate
    await binderApi.getAuthToken();

    // Create a binder
    const createResponse = await binderApi.createBinder(testData.validBinderData);
    const binderId = typeof createResponse === 'number' ?
        createResponse : createResponse.Binder_Id;

    // Upload document
    const filePath = testData.uploadDocumentData.validFilePath;
    const uploadResponse = await binderApi.uploadBinderDocument(binderId, filePath);

    console.log('Upload response:', uploadResponse);
}

uploadDocument();
```

## API Implementation

The upload document API is implemented in `pages/BinderApiPage.js`:

```javascript
async uploadBinderDocument(binderId, filePath) {
    const endpoint = `/Binder/UploadBinderDocuments?binder_Id=${binderId}`;

    try {
        const response = await this.apiClient.uploadFile(endpoint, filePath, {
            'Accept': 'application/json'
        });
        return response;
    } catch (error) {
        throw new Error(`Upload Document failed: ${error.message}`);
    }
}
```

## Error Codes

| Code | Description | Resolution |
|------|-------------|------------|
| 401 | Unauthorized / Binder Not Found | **Note:** The API returns 401 for both invalid auth tokens AND non-existent binder IDs. Verify: 1) Authentication token is valid, 2) Binder ID exists |
| 400 | Bad Request | Verify request payload is correct |
| 404 | Not Found | Resource not found |
| ENOENT | File not found | Check file path is correct |
| 500 | Server Error | Contact API support |

### Understanding 401 for Invalid Binder ID

**Important:** When you attempt to upload a document to a non-existent binder ID (e.g., 999999999), the API returns:
- **Status Code:** 401 (Unauthorized)
- **Response Body:** Empty string `""`

This is a common security pattern where the API doesn't distinguish between:
- "You're not authenticated" vs
- "This resource doesn't exist" vs
- "You don't have access to this resource"

This prevents attackers from discovering which binder IDs exist in the system.

## File Requirements

- **Format**: PDF (other formats may be supported)
- **Size**: Check API limits (typically < 10MB)
- **Name**: Should not contain special characters
- **Path**: Must be absolute path or relative to project root

## Troubleshooting

### Issue: "Upload test skipped - sample.pdf not found"

**Solution**: Generate the sample PDF file
```bash
node scripts/generateSamplePDF.js
```

### Issue: "ENOENT: no such file or directory"

**Solution**: Verify the file path in `testData/binderTestData.js` is correct

### Issue: "Upload Document failed: Request failed with status code 400"

**Solution**:
1. Check that the binder ID exists
2. Verify the binder is not in a locked state
3. Ensure authentication token is valid

### Issue: Document uploads but doesn't appear in binder

**Possible Causes**:
1. Document is still being processed
2. Document failed validation after upload
3. Check binder status with `getBinderDocuments(binderId, 1)`

## Best Practices

1. **Always authenticate** before uploading documents
2. **Verify binder exists** before attempting upload
3. **Check file exists** before calling upload API
4. **Handle errors gracefully** with try-catch blocks
5. **Verify uploads** by fetching binder documents after upload
6. **Clean up test data** after testing to avoid clutter

## Integration with Other Tests

The upload document test integrates with other tests in the suite:

1. **Create Binder** → Upload Document → **Submit Binder**
2. Upload Document → **Get Binder Documents** → Verify upload
3. Upload Document → **Download Document** → Verify content

## Sample Output

```
=== Upload Document API Test ===

Step 1: Checking for sample PDF...
  ✓ Sample PDF found

Step 2: Authenticating...
  ✓ Authentication successful

Step 3: Creating a test binder...
  ✓ Binder created successfully. ID: 830797

Step 4: Uploading document to binder...
  ✓ Document uploaded successfully
  Response: [
    {
      "name": "sample.pdf",
      "message": "",
      "size": 549
    }
  ]

Step 5: Verifying upload...
  ✓ Document verification complete

✅ Upload Document API Test - PASSED
```

## References

- [BinderApiPage.js](../pages/BinderApiPage.js) - Upload implementation
- [binderApi.test.js](../tests/binderApi.test.js) - Upload tests
- [testUploadDocument.js](../scripts/testUploadDocument.js) - Standalone script
- [generateSamplePDF.js](../scripts/generateSamplePDF.js) - PDF generator
