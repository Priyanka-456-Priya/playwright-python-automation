const { expect } = require('chai');

class ResponseValidator {
    /**
     * Validate that response is not null or undefined
     */
    static validateExists(response, message = 'Response should exist') {
        expect(response, message).to.not.be.null;
        expect(response, message).to.not.be.undefined;
    }

    /**
     * Validate response has specific property
     */
    static validateHasProperty(response, propertyName, message) {
        const msg = message || `Response should have property '${propertyName}'`;
        expect(response).to.have.property(propertyName, msg);
    }

    /**
     * Validate response has any of multiple properties (case-insensitive)
     */
    static validateHasAnyProperty(response, propertyNames, message) {
        const msg = message || `Response should have one of these properties: ${propertyNames.join(', ')}`;

        const hasProperty = propertyNames.some(propName => {
            // Check exact match
            if (response.hasOwnProperty(propName)) return true;

            // Check case-insensitive match
            const lowerProp = propName.toLowerCase();
            return Object.keys(response).some(key => key.toLowerCase() === lowerProp);
        });

        expect(hasProperty, msg).to.be.true;
    }

    /**
     * Get property value from response (case-insensitive)
     */
    static getPropertyValue(response, propertyNames) {
        if (!Array.isArray(propertyNames)) {
            propertyNames = [propertyNames];
        }

        for (const propName of propertyNames) {
            // Check exact match
            if (response.hasOwnProperty(propName)) {
                return response[propName];
            }

            // Check case-insensitive match
            const lowerProp = propName.toLowerCase();
            const key = Object.keys(response).find(k => k.toLowerCase() === lowerProp);
            if (key) {
                return response[key];
            }
        }

        return null;
    }

    /**
     * Validate response status code
     */
    static validateStatusCode(response, expectedStatus, message) {
        const msg = message || `Expected status ${expectedStatus}`;
        const status = response.status || response.Status || response.statusCode || response.StatusCode;
        expect(status, msg).to.equal(expectedStatus);
    }

    /**
     * Validate response is successful (2xx status)
     */
    static validateSuccess(response, message = 'Response should be successful') {
        this.validateExists(response, message);

        // Check if response has error indicators
        const hasError = response.error || response.Error ||
                        response.isError || response.IsError ||
                        (response.success === false) || (response.Success === false);

        expect(hasError, message).to.not.be.true;
    }

    /**
     * Validate response has data
     */
    static validateHasData(response, message = 'Response should contain data') {
        this.validateExists(response);

        if (typeof response === 'object') {
            const keys = Object.keys(response);
            expect(keys.length, message).to.be.greaterThan(0);
        }
    }

    /**
     * Validate array response
     */
    static validateArray(response, minLength = 0, message) {
        const msg = message || `Response should be an array with at least ${minLength} items`;
        expect(response, msg).to.be.an('array');
        expect(response.length, msg).to.be.at.least(minLength);
    }

    /**
     * Validate string is not empty
     */
    static validateNonEmptyString(value, fieldName, message) {
        const msg = message || `${fieldName} should be a non-empty string`;
        expect(value, msg).to.be.a('string');
        expect(value.trim(), msg).to.not.be.empty;
    }

    /**
     * Validate number is positive
     */
    static validatePositiveNumber(value, fieldName, message) {
        const msg = message || `${fieldName} should be a positive number`;
        expect(value, msg).to.be.a('number');
        expect(value, msg).to.be.greaterThan(0);
    }

    /**
     * Validate email format
     */
    static validateEmail(email, message = 'Should be a valid email') {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        expect(email, message).to.match(emailRegex);
    }

    /**
     * Validate response matches schema
     */
    static validateSchema(response, schema) {
        for (const [key, validator] of Object.entries(schema)) {
            const value = this.getPropertyValue(response, [key]);

            if (validator.required) {
                expect(value, `${key} is required`).to.exist;
            }

            if (value !== null && value !== undefined && validator.type) {
                expect(value, `${key} should be of type ${validator.type}`).to.be.a(validator.type);
            }

            if (validator.validate && typeof validator.validate === 'function') {
                validator.validate(value);
            }
        }
    }

    /**
     * Log response for debugging
     */
    static logResponse(response, label = 'Response') {
        console.log(`\n=== ${label} ===`);
        console.log(JSON.stringify(response, null, 2));
        console.log('='.repeat(label.length + 8));
    }

    /**
     * Validate authentication response
     */
    static validateAuthResponse(response) {
        this.validateExists(response, 'Authentication response should exist');

        // Check for token with various possible property names
        const tokenValue = this.getPropertyValue(response, [
            'token', 'Token',
            'authToken', 'AuthToken',
            'access_token', 'accessToken'
        ]);

        expect(tokenValue, 'Authentication response should contain a token').to.exist;
        this.validateNonEmptyString(tokenValue, 'Token');

        return tokenValue;
    }

    /**
     * Validate binder creation response
     */
    static validateBinderCreationResponse(response) {
        this.validateExists(response, 'Binder creation response should exist');

        // Check for binder ID with various possible property names
        const binderIdValue = this.getPropertyValue(response, [
            'Binder_Id', 'BinderId', 'binderId',
            'binder_id', 'id', 'Id', 'ID'
        ]);

        expect(binderIdValue, 'Binder creation response should contain a binder ID').to.exist;

        return binderIdValue;
    }

    /**
     * Validate error response
     */
    static validateErrorResponse(response, expectedErrorMessage = null) {
        this.validateExists(response, 'Error response should exist');

        const errorMessage = this.getPropertyValue(response, [
            'message', 'Message',
            'error', 'Error',
            'errorMessage', 'ErrorMessage'
        ]);

        expect(errorMessage, 'Error response should contain an error message').to.exist;

        if (expectedErrorMessage) {
            expect(errorMessage.toLowerCase()).to.include(expectedErrorMessage.toLowerCase());
        }
    }
}

module.exports = ResponseValidator;
