module.exports = {
    validBinderData: {
        customField: 'testprnt',
        email: 'Hitesh.Waghela@thomsonreuters.com',  // Fixed: Capitalized
        uniqueIdentifier: `test_binder_${Date.now()}`,
        clientId: 'print',
        serviceTypeId: 2,
        templateId: 577872,
        submissionType: 1,
        is7216ConsentReceived: 1,
        officeLocationId: 8627,  // Fixed: Updated to match your config
        linkBinder: 0,
        taxpayerSSN: '147-44-0022',
        filingStatus: '1',
        hasLeadsheet: 0
    },

    invalidBinderData: {
        missingRequiredFields: {
            customField: 'testprnt'
            // Missing other required fields
        },
        invalidEmail: {
            customField: 'testprnt',
            email: 'invalid-email',
            uniqueIdentifier: 'test_invalid',
            clientId: 'print',
            serviceTypeId: 2,
            templateId: 552346
        },
        invalidSSN: {
            customField: 'testprnt',
            email: 'Priyanka.Patil@thomsonreuters.com',  // Fixed: Capitalized
            uniqueIdentifier: 'test_invalid_ssn',
            clientId: 'print',
            serviceTypeId: 2,
            templateId: 552346,
            taxpayerSSN: 'invalid-ssn',
            filingStatus: '1'
        }
    },

    updateProjectData: {
        projectId: 'Ab2324',
        binderType: 'v5',
        taxYear: 2024
    },

    statusIds: {
        pending: 1,
        inProgress: 2,
        completed: 3,
        cancelled: 4
    },

    searchCriteria: {
        taxYear: 2024,
        binderType: 'v1',
        statusId: '3',
        pageNumber: 0,
        pageSize: 10
    },

    drlTestData: {
        clientNumber: 'Ad434434',
        taxYear: 2024
    },

    ownerMemberData: {
        loginUserEmail: 'Prakash.Kokate@thomsonreuters.com',
        ownerEmail: 'Priyanka.Patil@thomsonreuters.com',  // Fixed: Capitalized
        locationId: 8627,  // Fixed: Updated to match your config
        assignMember: ['null']
    },

    uploadDocumentData: {
        validFilePath: 'C:/Users/6124481/VS_CODE Projects/API_Error_Codes_Validation/testData/sample.pdf',
        invalidFilePath: 'C:/Users/6124481/VS_CODE Projects/API_Error_Codes_Validation/testData/nonexistent.pdf'
    }
};
