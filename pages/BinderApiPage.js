const ApiClient = require('../utils/ApiClient');
const config = require('../config/config');

class BinderApiPage {
    constructor() {
        this.apiClient = new ApiClient();
        this.authToken = null;
    }

    // 1. Authenticate and Get Token
    async getAuthToken() {
        const endpoint = '/Authenticate/GetToken';
        const payload = {
            UserName: config.credentials.userName,
            Password: config.credentials.password,
            APIKey: config.credentials.apiKey
        };

        try {
            const response = await this.apiClient.post(endpoint, payload);
            this.authToken = response.Token || response.token || response;
            this.apiClient.setAuthToken(this.authToken);
            return response;
        } catch (error) {
            throw new Error(`Authentication failed: ${error.message}`);
        }
    }

    // 2. Create Binder
    async createBinder(binderData) {
        const endpoint = '/Binder/CreateBinder';
        const payload = {
            Custom_Field: binderData.customField || config.testData.customField,
            Email: binderData.email || config.testData.email,
            Unique_Identifier: binderData.uniqueIdentifier || `test_${Date.now()}`,
            Client_Id: binderData.clientId || config.testData.clientId,
            Service_Type_Id: binderData.serviceTypeId || config.testData.serviceTypeId,
            Template_Id: binderData.templateId || config.testData.templateId,
            SubmissionType: binderData.submissionType || 1,
            Is7216ConsentReceived: binderData.is7216ConsentReceived || 1,
            office_Location_id: binderData.officeLocationId || config.testData.officeLocationId,
            Linkbinder: binderData.linkBinder || 0,
            Taxpayer_SSN: binderData.taxpayerSSN || config.testData.taxpayerSSN,
            Filing_Status: binderData.filingStatus || config.testData.filingStatus,
            Has_Leadsheet: binderData.hasLeadsheet || 0
        };

        try {
            const response = await this.apiClient.post(endpoint, payload);
            return response;
        } catch (error) {
            throw new Error(`Create Binder failed: ${error.message}`);
        }
    }

    // 3. Upload Binder Document
    async uploadBinderDocument(binderId, filePath) {
        const endpoint = `/Binder/UploadBinderDocuments?binder_Id=${binderId}`;

        try {
            const response = await this.apiClient.uploadFile(endpoint, filePath, {
                'Accept': 'application/json'
            });
            return response;
        } catch (error) {
            // Preserve the response data in the error
            const newError = new Error(`Upload Document failed: ${error.message}`);
            newError.response = error.response;
            newError.code = error.code; // Preserve ENOENT for file not found
            throw newError;
        }
    }

    // 4. Submit Binder
    async submitBinder(binderId, isInHouseProcess = 0) {
        const endpoint = '/Binder/SubmitBinder';
        const payload = {
            Binder_Id: binderId,
            IsInHouseProcess: isInHouseProcess
        };

        try {
            const response = await this.apiClient.post(endpoint, payload);
            return response;
        } catch (error) {
            // Preserve the response data in the error
            const newError = new Error(`Submit Binder failed: ${error.message}`);
            newError.response = error.response;
            throw newError;
        }
    }

    // 5. Update Project ID
    async updateProjectID(updateData) {
        const endpoint = '/Binder/UpdateProjectID';
        const payload = {
            BinderID: updateData.binderId,
            ProjectID: updateData.projectId,
            ClientId: updateData.clientId || config.testData.clientId,
            BinderType: updateData.binderType || 'v5',
            TaxYear: updateData.taxYear || config.testData.taxYear
        };

        try {
            const response = await this.apiClient.post(endpoint, payload);
            return response;
        } catch (error) {
            throw new Error(`Update Project ID failed: ${error.message}`);
        }
    }

    // 6. Get Binders Status With States
    async getBindersStatusWithStates(binderId, taxYear, pageNumber = 1, pageSize = 1) {
        const endpoint = '/Binder/GetBindersStatusWithStates';
        const payload = {
            Binder_Id: binderId,
            TaxYear: taxYear || config.testData.taxYear,
            PageNumber: pageNumber,
            PageSize: pageSize
        };

        try {
            const response = await this.apiClient.post(endpoint, payload);
            return response;
        } catch (error) {
            throw new Error(`Get Binders Status With States failed: ${error.message}`);
        }
    }

    // 7. Get States and Localities
    async getStatesAndLocalities(binderId) {
        const endpoint = '/Binder/GetStatesandLocalities';
        const payload = {
            Binder_Id: binderId
        };

        try {
            const response = await this.apiClient.post(endpoint, payload);
            return response;
        } catch (error) {
            throw new Error(`Get States and Localities failed: ${error.message}`);
        }
    }

    // 8. Download Binder PBFX
    async downloadBinderPBFX(binderId, mappedId) {
        const endpoint = '/Binder/DownloadBinderPBFX';
        const payload = {
            Binder_Id: binderId,
            Mapped_Id: mappedId || config.testData.email
        };

        try {
            const response = await this.apiClient.post(endpoint, payload);
            return response;
        } catch (error) {
            // Preserve the response data in the error
            const newError = new Error(`Download Binder PBFX failed: ${error.message}`);
            newError.response = error.response;
            throw newError;
        }
    }

    // 9. Get Binder Audit Log
    async getBinderAuditLog(binderId, clientId, binderType = 'v1', taxYear) {
        const endpoint = '/Binder/GetBinderAuditLog';
        const payload = {
            BinderID: binderId,
            ClientId: clientId || config.testData.clientId,
            BinderType: binderType,
            TaxYear: taxYear || config.testData.taxYear
        };

        try {
            const response = await this.apiClient.post(endpoint, payload);
            return response;
        } catch (error) {
            throw new Error(`Get Binder Audit Log failed: ${error.message}`);
        }
    }

    // 10. Print Binder
    async printBinder(binderId) {
        const endpoint = '/Binder/PrintBinder';
        const payload = {
            BinderID: binderId
        };

        try {
            const response = await this.apiClient.post(endpoint, payload);
            return response;
        } catch (error) {
            // Preserve the response data in the error
            const newError = new Error(`Print Binder failed: ${error.message}`);
            newError.response = error.response;
            throw newError;
        }
    }

    // 11. Get Binder Details
    async getBinderDetails(searchCriteria) {
        const endpoint = '/BinderInfo/GetBinderDetails';
        const payload = {
            TaxYear: searchCriteria.taxYear || config.testData.taxYear,
            ClientID: searchCriteria.clientId || [config.testData.clientId],
            PageNumber: searchCriteria.pageNumber || 0,
            PageSize: searchCriteria.pageSize || 0,
            BinderType: searchCriteria.binderType || 'v1',
            status_ID: searchCriteria.statusId || '3',
            OwnerEmail: searchCriteria.ownerEmail || config.testData.email,
            Custom_Field: searchCriteria.customField
        };

        try {
            const response = await this.apiClient.post(endpoint, payload);
            return response;
        } catch (error) {
            throw new Error(`Get Binder Details failed: ${error.message}`);
        }
    }

    // 12. Get Binder Status
    async getBinderStatus(binderId) {
        const endpoint = '/Binder/GetStatus';
        const payload = {
            Binder_Id: binderId
        };

        try {
            const response = await this.apiClient.post(endpoint, payload);
            return response;
        } catch (error) {
            throw new Error(`Get Binder Status failed: ${error.message}`);
        }
    }

    // 13. Change Binder Status
    async changeBinderStatus(binderId, statusId) {
        const endpoint = '/Binder/ChangeBinderStatus';
        const payload = {
            Binder_Id: binderId,
            Status_Id: statusId
        };

        try {
            const response = await this.apiClient.post(endpoint, payload);
            return response;
        } catch (error) {
            // Preserve the response data in the error
            const newError = new Error(`Change Binder Status failed: ${error.message}`);
            newError.response = error.response;
            throw newError;
        }
    }

    // 14. Get Binder Pending Items
    async getBinderPendingItems(taxYear, clientId) {
        const endpoint = '/BinderInfo/GetBinderPendingItems';
        const payload = {
            TaxYear: taxYear || config.testData.taxYear,
            ClientID: clientId || config.testData.clientId
        };

        try {
            const response = await this.apiClient.post(endpoint, payload);
            return response;
        } catch (error) {
            throw new Error(`Get Binder Pending Items failed: ${error.message}`);
        }
    }

    // 15. Get Binder Documents
    async getBinderDocuments(binderId, allFiles = 0, fromDate, toDate) {
        const endpoint = '/Binder/GetDocuments';
        const payload = {
            AllFiles: allFiles,
            FromDate: fromDate || '2025-09-25T12:47:45.583Z',
            ToDate: toDate || '2025-09-25T12:47:45.583Z',
            Binder_ID: binderId
        };

        try {
            const response = await this.apiClient.post(endpoint, payload);
            return response;
        } catch (error) {
            throw new Error(`Get Binder Documents failed: ${error.message}`);
        }
    }

    // 16. Download Document
    async downloadDocument(documentId) {
        const endpoint = `/Binder/DownloadDocument?documentID=${documentId}`;

        try {
            const response = await this.apiClient.post(endpoint);
            return response;
        } catch (error) {
            throw new Error(`Download Document failed: ${error.message}`);
        }
    }

    // 17. Get DRL Output
    async getDRLOutput(clientNumber, taxYear) {
        const endpoint = '/DRLInfo/GetDRLOutput';
        const payload = {
            ClientNumber: clientNumber,
            TaxYear: taxYear || config.testData.taxYear
        };

        try {
            const response = await this.apiClient.post(endpoint, payload);
            return response;
        } catch (error) {
            throw new Error(`Get DRL Output failed: ${error.message}`);
        }
    }

    // 18. Update Owner Member
    async updateOwnerMember(updateData) {
        const endpoint = '/Binder/UpdateOwnerMember';
        const payload = {
            Binder_Id: updateData.binderId,
            LoginUserEmail: updateData.loginUserEmail,
            OwnerEmail: updateData.ownerEmail || config.testData.email,
            LocationID: updateData.locationId || config.testData.officeLocationId,
            AssignMember: updateData.assignMember || ['null']
        };

        try {
            const response = await this.apiClient.post(endpoint, payload);
            return response;
        } catch (error) {
            throw new Error(`Update Owner Member failed: ${error.message}`);
        }
    }

    // 19. Get DRL PDF Details
    async getDRLPDFDetails(clientNumber, taxYear) {
        const endpoint = '/DRLInfo/GetDRLPDFDetails';
        const payload = {
            ClientNumber: clientNumber,
            TaxYear: taxYear || config.testData.taxYear
        };

        try {
            const response = await this.apiClient.post(endpoint, payload);
            return response;
        } catch (error) {
            throw new Error(`Get DRL PDF Details failed: ${error.message}`);
        }
    }
}

module.exports = BinderApiPage;
