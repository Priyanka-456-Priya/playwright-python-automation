const axios = require('axios');
const https = require('https');
const config = require('../config/config');

class ApiClient {
    constructor() {
        // Create HTTPS agent that accepts self-signed certificates
        const httpsAgent = new https.Agent({
            rejectUnauthorized: false // Note: Only use in development/testing
        });

        this.client = axios.create({
            baseURL: `${config.baseURL}/${config.apiVersion}`,
            timeout: config.timeout,
            httpsAgent: httpsAgent,
            headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            }
        });

        // Request interceptor
        this.client.interceptors.request.use(
            (config) => {
                console.log(`Request: ${config.method.toUpperCase()} ${config.url}`);
                return config;
            },
            (error) => {
                console.error('Request Error:', error);
                return Promise.reject(error);
            }
        );

        // Response interceptor
        this.client.interceptors.response.use(
            (response) => {
                console.log(`✓ Response Status: ${response.status}`);
                return response;
            },
            (error) => {
                if (error.response) {
                    console.error(`✗ Response Error: ${error.response.status}`,
                        JSON.stringify(error.response.data, null, 2));
                } else if (error.request) {
                    console.error('✗ No Response received from server');
                } else {
                    console.error('✗ Error:', error.message);
                }
                return Promise.reject(error);
            }
        );
    }

    async get(url, params = {}, headers = {}) {
        try {
            const response = await this.client.get(url, {
                params,
                headers
            });
            return response.data;
        } catch (error) {
            throw error;
        }
    }

    async post(url, data = {}, headers = {}) {
        try {
            const response = await this.client.post(url, data, {
                headers
            });
            return response.data;
        } catch (error) {
            throw error;
        }
    }

    async put(url, data = {}, headers = {}) {
        try {
            const response = await this.client.put(url, data, {
                headers
            });
            return response.data;
        } catch (error) {
            throw error;
        }
    }

    async delete(url, headers = {}) {
        try {
            const response = await this.client.delete(url, {
                headers
            });
            return response.data;
        } catch (error) {
            throw error;
        }
    }

    async uploadFile(url, filePath, headers = {}) {
        const FormData = require('form-data');
        const fs = require('fs');

        try {
            const formData = new FormData();
            formData.append('file', fs.createReadStream(filePath));

            const response = await this.client.post(url, formData, {
                headers: {
                    ...headers,
                    ...formData.getHeaders()
                }
            });
            return response.data;
        } catch (error) {
            throw error;
        }
    }

    setAuthToken(token) {
        this.client.defaults.headers.common['AuthToken'] = token;
    }

    removeAuthToken() {
        delete this.client.defaults.headers.common['AuthToken'];
    }
}

module.exports = ApiClient;
