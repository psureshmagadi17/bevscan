import axios from 'axios';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Types for API responses
export interface Invoice {
  id: number;
  vendor_id: number;
  invoice_number: string;
  invoice_date: string | null;
  due_date: string | null;
  subtotal: number | null;
  tax: number | null;
  total: number | null;
  status: string;
  confidence_score: number | null;
  raw_text: string | null;
  parsed_data: any | null;
  created_at: string;
  updated_at: string;
  vendor?: Vendor;
  items?: InvoiceItem[];
  alerts?: Alert[];
}

export interface Vendor {
  id: number;
  name: string;
  email: string | null;
  phone: string | null;
  created_at: string;
  updated_at: string;
}

export interface InvoiceItem {
  id: number;
  invoice_id: number;
  sku: string | null;
  description: string | null;
  quantity: number | null;
  unit_price: number | null;
  total: number | null;
  created_at: string;
}

export interface Alert {
  id: number;
  invoice_id: number;
  alert_type: string;
  message: string;
  severity: string;
  status: string;
  created_at: string;
  resolved_at: string | null;
}

// API functions
export const invoiceApi = {
  // Upload invoice file
  upload: async (file: File, llmProvider?: string, llmModel?: string): Promise<{ message: string; invoice_id: number }> => {
    const formData = new FormData();
    formData.append('file', file);
    if (llmProvider) formData.append('llm_provider', llmProvider);
    if (llmModel) formData.append('llm_model', llmModel);
    
    const response = await api.post('/invoices/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  },

  // Parse invoice
  parse: async (invoiceId: number): Promise<{ message: string; invoice_id: number }> => {
    const response = await api.post(`/invoices/${invoiceId}/parse`);
    return response.data;
  },

  // Get invoice details
  get: async (invoiceId: number): Promise<Invoice> => {
    const response = await api.get(`/invoices/${invoiceId}`);
    return response.data;
  },

  // List invoices
  list: async (skip = 0, limit = 100): Promise<Invoice[]> => {
    const response = await api.get('/invoices/', {
      params: { skip, limit },
    });
    return response.data;
  },
};

export const alertApi = {
  // List all alerts
  list: async (skip = 0, limit = 100): Promise<Alert[]> => {
    const response = await api.get('/alerts/', {
      params: { skip, limit },
    });
    return response.data;
  },

  // Get alerts for specific invoice
  getForInvoice: async (invoiceId: number): Promise<Alert[]> => {
    const response = await api.get(`/alerts/invoices/${invoiceId}/alerts`);
    return response.data;
  },
};

export const healthApi = {
  // Health check
  check: async (): Promise<{ status: string; llm_provider: string; database: string }> => {
    const response = await api.get('/health');
    return response.data;
  },
}; 