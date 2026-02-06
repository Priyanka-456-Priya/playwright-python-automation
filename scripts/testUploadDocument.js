const BinderApiPage = require('../pages/BinderApiPage');
const testData = require('../testData/binderTestData');
const { generateSamplePDF } = require('./generateSamplePDF');
const fs = require('fs');
const path = require('path');

/**
 * Standalone script to test the Upload Document API
 *
 * This script:
 * 1. Authenticates with the API
 * 2. Creates a new binder
 * 3. Uploads a document to the binder
 * 4. Verifies the upload was successful
 */

async function testUploadDocumentAPI() {
    console.log('\n=== Upload Document API Test ===\n');

    const binderApi = new BinderApiPage();
    let binderId = null;

    try {
        // Step 1: Ensure sample PDF exists
        console.log('Step 1: Checking for sample PDF...');
        const samplePdfPath = path.join(__dirname, '..', 'testData', 'sample.pdf');

        if (!fs.existsSync(samplePdfPath)) {
            console.log('  Sample PDF not found. Generating...');
            generateSamplePDF();
        } else {
            console.log('  ✓ Sample PDF found at:', samplePdfPath);
        }

        // Step 2: Authenticate
        console.log('\nStep 2: Authenticating...');
        await binderApi.getAuthToken();
        console.log('  ✓ Authentication successful');

        // Step 3: Create a binder
        console.log('\nStep 3: Creating a test binder...');
        const createResponse = await binderApi.createBinder(testData.validBinderData);
        binderId = typeof createResponse === 'number' ? createResponse :
                   (createResponse.Binder_Id || createResponse.BinderId || createResponse.binderId);

        if (!binderId) {
            throw new Error('Failed to create binder - no binder ID returned');
        }
        console.log('  ✓ Binder created successfully. ID:', binderId);

        // Step 4: Upload document
        console.log('\nStep 4: Uploading document to binder...');
        const uploadResponse = await binderApi.uploadBinderDocument(binderId, samplePdfPath);
        console.log('  ✓ Document uploaded successfully');
        console.log('  Response:', JSON.stringify(uploadResponse, null, 2));

        // Step 5: Verify upload by getting binder documents
        console.log('\nStep 5: Verifying upload...');
        const documentsResponse = await binderApi.getBinderDocuments(binderId, 1);
        console.log('  ✓ Document verification complete');
        console.log('  Documents in binder:', JSON.stringify(documentsResponse, null, 2));

        console.log('\n✅ Upload Document API Test - PASSED\n');
        console.log('Summary:');
        console.log(`  - Binder ID: ${binderId}`);
        console.log(`  - File uploaded: sample.pdf`);
        console.log(`  - File path: ${samplePdfPath}`);

    } catch (error) {
        console.error('\n❌ Upload Document API Test - FAILED\n');
        console.error('Error:', error.message);

        if (error.response?.data) {
            console.error('API Error Response:', JSON.stringify(error.response.data, null, 2));
        }

        process.exit(1);
    }
}

// Additional helper function to test multiple file uploads
async function testMultipleUploads() {
    console.log('\n=== Multiple Document Upload Test ===\n');

    const binderApi = new BinderApiPage();
    let binderId = null;

    try {
        // Authenticate
        console.log('Authenticating...');
        await binderApi.getAuthToken();
        console.log('  ✓ Authentication successful');

        // Create a binder
        console.log('\nCreating a test binder...');
        const createResponse = await binderApi.createBinder(testData.validBinderData);
        binderId = typeof createResponse === 'number' ? createResponse :
                   (createResponse.Binder_Id || createResponse.BinderId || createResponse.binderId);
        console.log('  ✓ Binder created. ID:', binderId);

        // Upload multiple documents
        const samplePdfPath = path.join(__dirname, '..', 'testData', 'sample.pdf');
        const uploadCount = 3;

        console.log(`\nUploading ${uploadCount} documents...`);
        for (let i = 1; i <= uploadCount; i++) {
            console.log(`  Uploading document ${i}/${uploadCount}...`);
            await binderApi.uploadBinderDocument(binderId, samplePdfPath);
            console.log(`    ✓ Document ${i} uploaded`);
        }

        // Verify all uploads
        console.log('\nVerifying uploads...');
        const documentsResponse = await binderApi.getBinderDocuments(binderId, 1);
        console.log('  ✓ Verification complete');
        console.log('  Total documents:', documentsResponse?.length || 'N/A');

        console.log('\n✅ Multiple Upload Test - PASSED\n');

    } catch (error) {
        console.error('\n❌ Multiple Upload Test - FAILED\n');
        console.error('Error:', error.message);
        process.exit(1);
    }
}

// Main execution
if (require.main === module) {
    const testType = process.argv[2] || 'single';

    if (testType === 'multiple') {
        testMultipleUploads();
    } else {
        testUploadDocumentAPI();
    }
}

module.exports = { testUploadDocumentAPI, testMultipleUploads };
