const fs = require('fs');
const path = require('path');

/**
 * Generates a minimal valid PDF file for testing purposes
 */
function generateSamplePDF() {
    const outputPath = path.join(__dirname, '..', 'testData', 'sample.pdf');

    // Create a minimal valid PDF structure
    const pdfContent = `%PDF-1.4
1 0 obj
<<
/Type /Catalog
/Pages 2 0 R
>>
endobj
2 0 obj
<<
/Type /Pages
/Kids [3 0 R]
/Count 1
>>
endobj
3 0 obj
<<
/Type /Page
/Parent 2 0 R
/Resources <<
/Font <<
/F1 <<
/Type /Font
/Subtype /Type1
/BaseFont /Helvetica
>>
>>
>>
/MediaBox [0 0 612 792]
/Contents 4 0 R
>>
endobj
4 0 obj
<<
/Length 44
>>
stream
BT
/F1 12 Tf
100 700 Td
(Sample Test Document) Tj
ET
endstream
endobj
xref
0 5
0000000000 65535 f
0000000009 00000 n
0000000058 00000 n
0000000115 00000 n
0000000317 00000 n
trailer
<<
/Size 5
/Root 1 0 R
>>
startxref
410
%%EOF`;

    // Ensure testData directory exists
    const testDataDir = path.join(__dirname, '..', 'testData');
    if (!fs.existsSync(testDataDir)) {
        fs.mkdirSync(testDataDir, { recursive: true });
    }

    // Write the PDF file
    fs.writeFileSync(outputPath, pdfContent);
    console.log(`✓ Sample PDF created at: ${outputPath}`);
    return outputPath;
}

// Run if called directly
if (require.main === module) {
    try {
        generateSamplePDF();
        console.log('✓ Sample PDF generation complete');
    } catch (error) {
        console.error('✗ Error generating sample PDF:', error.message);
        process.exit(1);
    }
}

module.exports = { generateSamplePDF };
