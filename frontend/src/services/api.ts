import axios from 'axios';
import type { AxiosInstance, AxiosRequestConfig, AxiosResponse } from 'axios';
import type { AuthTokens, LoginRequest, RegisterRequest, User } from '../types';

class ApiService {
  private api: AxiosInstance;
  private refreshPromise: Promise<string> | null = null;

  constructor() {
    this.api = axios.create({
      baseURL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api',
      timeout: 10000,
      headers: {
        'Content-Type': 'application/json',
      },
    });

    this.setupInterceptors();
  }

  private setupInterceptors() {
    // Request interceptor to add auth token
    this.api.interceptors.request.use(
      (config) => {
        const token = this.getAccessToken();
        if (token) {
          config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
      },
      (error) => Promise.reject(error)
    );

    // Response interceptor to handle token refresh
    this.api.interceptors.response.use(
      (response) => response,
      async (error) => {
        console.log('API Error:', error.response?.status, error.response?.data);
        const originalRequest = error.config;

        if (error.response?.status === 401 && !originalRequest._retry) {
          originalRequest._retry = true;

          try {
            const newToken = await this.refreshAccessToken();
            originalRequest.headers.Authorization = `Bearer ${newToken}`;
            return this.api(originalRequest);
          } catch (refreshError) {
            this.clearTokens();
            window.location.href = '/login';
            return Promise.reject(refreshError);
          }
        }

        return Promise.reject(error);
      }
    );
  }

  private getAccessToken(): string | null {
    return localStorage.getItem('access_token');
  }

  private getRefreshToken(): string | null {
    return localStorage.getItem('refresh_token');
  }

  private setTokens(tokens: AuthTokens) {
    localStorage.setItem('access_token', tokens.access);
    localStorage.setItem('refresh_token', tokens.refresh);
  }

  private clearTokens() {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
  }

  private async refreshAccessToken(): Promise<string> {
    if (this.refreshPromise) {
      return this.refreshPromise;
    }

    this.refreshPromise = this.performTokenRefresh();
    
    try {
      const newToken = await this.refreshPromise;
      return newToken;
    } finally {
      this.refreshPromise = null;
    }
  }

  private async performTokenRefresh(): Promise<string> {
    const refreshToken = this.getRefreshToken();
    if (!refreshToken) {
      throw new Error('No refresh token available');
    }

    try {
      const response = await axios.post(`${this.api.defaults.baseURL}/auth/token/refresh/`, {
        refresh: refreshToken,
      });

      const { access } = response.data;
      localStorage.setItem('access_token', access);
      return access;
    } catch (error) {
      this.clearTokens();
      throw error;
    }
  }

  // Auth endpoints
  async login(credentials: LoginRequest): Promise<{ user: User; tokens: AuthTokens }> {
    console.log('Login request:', credentials);
    const response = await this.api.post('/auth/login/', credentials);
    console.log('Login response:', response.data);
    const { user, tokens } = response.data;
    this.setTokens(tokens);
    return { user, tokens };
  }

  async register(userData: RegisterRequest): Promise<{ user: User; tokens: AuthTokens }> {
    const response = await this.api.post('/auth/register/', userData);
    const { user, tokens } = response.data;
    this.setTokens(tokens);
    return { user, tokens };
  }

  async getProfile(): Promise<User> {
    const response = await this.api.get('/auth/profile/');
    return response.data;
  }

  async logout() {
    this.clearTokens();
  }

  // Groups endpoints
  async getGroups(): Promise<any[]> {
    const response = await this.api.get('/groups/groups/');
    return response.data.results || response.data;
  }

  async getGroup(id: number): Promise<any> {
    const response = await this.api.get(`/groups/groups/${id}/`);
    return response.data;
  }

  async createGroup(groupData: any): Promise<any> {
    const response = await this.api.post('/groups/groups/', groupData);
    return response.data;
  }

  async updateGroup(id: number, groupData: any): Promise<any> {
    const response = await this.api.patch(`/groups/groups/${id}/`, groupData);
    return response.data;
  }

  async deleteGroup(id: number): Promise<void> {
    await this.api.delete(`/groups/groups/${id}/`);
  }

  async addGroupMember(groupId: number, memberData: any): Promise<any> {
    const response = await this.api.post(`/groups/groups/${groupId}/add_member/`, memberData);
    return response.data;
  }

  async removeGroupMember(groupId: number, memberId: number): Promise<void> {
    await this.api.post(`/groups/groups/${groupId}/remove_member/`, { member_id: memberId });
  }

  // Expenses endpoints
  async getExpenses(groupId?: number): Promise<any[]> {
    const url = groupId ? `/expenses/expenses/?group=${groupId}` : '/expenses/expenses/';
    const response = await this.api.get(url);
    return response.data.results || response.data;
  }

  async getExpense(id: number): Promise<any> {
    const response = await this.api.get(`/expenses/expenses/${id}/`);
    return response.data;
  }

  async createExpense(expenseData: any): Promise<any> {
    const response = await this.api.post('/expenses/expenses/', expenseData);
    return response.data;
  }

  async updateExpense(id: number, expenseData: any): Promise<any> {
    const response = await this.api.patch(`/expenses/expenses/${id}/`, expenseData);
    return response.data;
  }

  async deleteExpense(id: number): Promise<void> {
    await this.api.delete(`/expenses/expenses/${id}/`);
  }

  async uploadReceipt(expenseId: number, file: File): Promise<any> {
    const formData = new FormData();
    formData.append('receipt', file);
    
    const response = await this.api.post(`/ocr/expenses/${expenseId}/upload_receipt/`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  }

  // Settlement endpoints
  async computeSettlement(groupId: number, policyType: string): Promise<any> {
    const response = await this.api.post(`/fairness/groups/${groupId}/compute_settlement/`, {
      policy_type: policyType,
    });
    return response.data;
  }

  async getSettlementGraph(groupId: number): Promise<any> {
    const response = await this.api.get(`/fairness/groups/${groupId}/settlement_graph/`);
    return response.data;
  }

  // Payment endpoints
  async getLedgerEntries(): Promise<any[]> {
    const response = await this.api.get('/payments/ledger/');
    return response.data.results || response.data;
  }

  async initiatePayment(paymentData: any): Promise<any> {
    const response = await this.api.post('/payments/initiate/', paymentData);
    return response.data;
  }

  async getPaymentStatus(paymentId: number): Promise<any> {
    const response = await this.api.get(`/payments/status/${paymentId}/`);
    return response.data;
  }

  async simulateWebhook(paymentId: number, success: boolean = true): Promise<any> {
    const response = await this.api.post(`/payments/simulate/${paymentId}/`, { success });
    return response.data;
  }

  // Consent endpoints
  async getConsents(): Promise<any[]> {
    const response = await this.api.get('/consents/');
    return response.data.results || response.data;
  }

  async createConsent(consentData: any): Promise<any> {
    const response = await this.api.post('/consents/', consentData);
    return response.data;
  }

  async getConsent(id: number): Promise<any> {
    const response = await this.api.get(`/consents/${id}/`);
    return response.data;
  }

  async shareData(consentId: number): Promise<any> {
    const response = await this.api.post(`/consents/${consentId}/share/`);
    return response.data;
  }

  async revokeConsent(id: number): Promise<void> {
    await this.api.post(`/consents/${id}/revoke/`);
  }

  // Export endpoints
  async exportGroupData(groupId: number, format: 'csv' | 'pdf', options?: any): Promise<Blob> {
    const response = await this.api.get(`/groups/${groupId}/export/`, {
      params: { format, ...options },
      responseType: 'blob',
    });
    return response.data;
  }

  // Demo data
  async seedDemoData(): Promise<void> {
    await this.api.post('/auth/seed_demo/');
  }

  // Group endpoints
  async createGroup(groupData: {
    name: string;
    description?: string;
    group_type: string;
    currency?: string;
    billing_cycle?: string;
    gst_mode?: boolean;
  }): Promise<any> {
    const response = await this.api.post('/groups/groups/', groupData);
    return response.data;
  }

  async getGroupDetails(groupId: string): Promise<any> {
    const response = await this.api.get(`/groups/groups/${groupId}/`);
    return response.data;
  }

  // Generic request method
  async request<T>(config: AxiosRequestConfig): Promise<AxiosResponse<T>> {
    return this.api.request<T>(config);
  }
}

export const apiService = new ApiService();
export default apiService;