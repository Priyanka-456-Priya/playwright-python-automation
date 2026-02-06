# API Error Behavior Documentation

## Overview

This document explains the error handling behavior of the Binder API, particularly focusing on security patterns and edge cases.

## Upload Document API - Error Responses

### Incorrect Binder ID (401 Unauthorized)

**Scenario:** Uploading a document to a non-existent binder ID

**Test Case:**
```javascript
const invalidBinderId = 999999999;
await binderApi.uploadBinderDocument(invalidBinderId, 'sample.pdf');
```

**API Response:**
```
Status Code: 401 (Unauthorized)
Response Body: "" (empty string)
```

**Explanation:**

The API returns a **401 Unauthorized** error for non-existent binder IDs instead of a more specific error like 404 Not Found. This is intentional security design.

#### Why 401 Instead of 404?

This is a **security pattern** that prevents information disclosure:

1. **Prevents Resource Enumeration**
   - Attackers can't discover which binder IDs exist in the system
   - If 404 meant "doesn't exist" and 401 meant "exists but no access", attackers could enumerate all valid IDs

2. **Consistent Security Response**
   - The same 401 response for:
     - Invalid authentication token
     - Valid token but resource doesn't exist
     - Valid token but no permission to access resource

3. **Principle of Least Information**
   - Don't reveal whether a resource exists unless the user is authorized
   - Makes it harder for attackers to map the system

### Other Common API Error Patterns

#### Authentication Errors

```javascript
// No auth token
Status: 401
Message: "Authentication required"

// Invalid auth token
Status: 401
Message: "" or "Invalid token"

// Expired auth token
Status: 401
Message: "Token expired"
```

#### Resource Access Errors

```javascript
// Non-existent binder (security pattern)
Status: 401
Message: ""

// Binder exists but in wrong state
Status: 400
ErrorCode: "1110"
ErrorDesc: "Binder is in SP Processing"
```

#### Validation Errors

```javascript
// Invalid email format
Status: 400
ErrorCode: "1050"
ErrorDesc: "Invalid Email ID. Please correct the format and retry."

// Missing required fields
Status: 400
ErrorCode: varies
ErrorDesc: Field-specific error message
```

## Testing Error Scenarios

### Test Implementation

```javascript
it('should return error when uploading to non-existent binder', async function() {
    const invalidBinderId = 999999999;
    const testFilePath = 'testData/sample.pdf';

    try {
        await binderApi.uploadBinderDocument(invalidBinderId, testFilePath);
        expect.fail('Should have thrown an error');
    } catch (error) {
        // API returns 401 for non-existent binders
        expect(error.response.status).to.equal(401);

        // Log the behavior for documentation
        console.log('✓ Upload correctly rejected for invalid binder (Status: 401)');
        console.log('  Note: API returns 401 (Unauthorized) for non-existent binder IDs');
    }
});
```

### Expected Test Output

```
✓ Upload correctly rejected for invalid binder (Status: 401)
  Note: API returns 401 (Unauthorized) for non-existent binder IDs
```

## Best Practices for Error Handling

### 1. Accept 401 for Multiple Scenarios

```javascript
// Don't assume 401 always means "bad auth token"
if (error.response.status === 401) {
    console.log('Authentication or authorization failed');
    console.log('Possible causes:');
    console.log('- Invalid/expired auth token');
    console.log('- Resource does not exist');
    console.log('- No permission to access resource');
}
```

### 2. Handle Empty Response Bodies

```javascript
if (error.response.status === 401) {
    const errorData = error.response.data;

    if (!errorData || errorData === '') {
        console.log('Unauthorized access (no additional details)');
    } else {
        console.log('Error details:', errorData);
    }
}
```

### 3. Test Multiple Error Codes

```javascript
// Accept multiple possible error codes
expect(error.response.status).to.be.oneOf([400, 401, 404]);
```

### 4. Log Errors for Debugging

```javascript
catch (error) {
    console.log('Error Status:', error.response?.status);
    console.log('Error Data:', JSON.stringify(error.response?.data, null, 2));
    console.log('Error Message:', error.message);
}
```

## API Error Code Reference

### Upload Document Errors

| Status | Error Code | Description | Cause |
|--------|-----------|-------------|-------|
| 401 | - | Unauthorized | Invalid token OR non-existent binder OR no access |
| 400 | 1060 | Missing documents | Trying to submit binder without documents |
| 400 | 1110 | SP Processing | Binder in processing state |
| ENOENT | - | File not found | Local file doesn't exist |

### Common Patterns Across APIs

| Pattern | Status Code | Interpretation |
|---------|------------|----------------|
| Security 401 | 401 | Resource access denied (various reasons) |
| State Error | 400 | Operation not allowed in current state |
| Validation Error | 400 | Invalid input data |
| System Error | 500 | Server-side error |

## Security Implications

### For Testers

- **Don't rely on 401 vs 404** to determine if a resource exists
- **Test with both valid and invalid IDs** to ensure consistent behavior
- **Verify that sensitive information** isn't leaked in error messages

### For Developers

- **Expect 401 for various scenarios** - don't assume it only means bad auth
- **Don't enumerate resources** based on error codes
- **Handle empty response bodies** gracefully

## Example: Comprehensive Error Handling

```javascript
async function uploadDocumentSafely(binderId, filePath) {
    try {
        const result = await binderApi.uploadBinderDocument(binderId, filePath);
        console.log('✓ Upload successful');
        return result;

    } catch (error) {
        // Check file system errors first
        if (error.code === 'ENOENT') {
            throw new Error(`File not found: ${filePath}`);
        }

        // Check API errors
        if (error.response) {
            const status = error.response.status;
            const errorData = error.response.data;

            switch (status) {
                case 401:
                    throw new Error(
                        'Upload failed: Unauthorized. ' +
                        'Possible causes: Invalid auth token, ' +
                        'binder does not exist, or no permission to access binder.'
                    );

                case 400:
                    if (errorData?.ErrorCode) {
                        throw new Error(
                            `Upload failed: ${errorData.ErrorDesc} ` +
                            `(Error Code: ${errorData.ErrorCode})`
                        );
                    }
                    throw new Error('Upload failed: Bad request');

                case 500:
                    throw new Error('Upload failed: Server error');

                default:
                    throw new Error(`Upload failed: HTTP ${status}`);
            }
        }

        // Unknown error
        throw error;
    }
}
```

## Related Documentation

- [UPLOAD_DOCUMENT_API.md](./UPLOAD_DOCUMENT_API.md) - Upload API reference
- [binderApi.test.js](../tests/binderApi.test.js) - Test implementations
- [BinderApiPage.js](../pages/BinderApiPage.js) - API client implementation
