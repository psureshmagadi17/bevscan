'use client';

import { useState, useEffect } from 'react';
import { FileText, Eye, AlertTriangle, CheckCircle, Clock, RefreshCw } from 'lucide-react';
import { Invoice, invoiceApi } from '@/lib/api';
import InvoiceDisplay from './InvoiceDisplay';

export default function Dashboard() {
  const [invoices, setInvoices] = useState<Invoice[]>([]);
  const [selectedInvoice, setSelectedInvoice] = useState<Invoice | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchInvoices = async () => {
    try {
      setLoading(true);
      const data = await invoiceApi.list();
      setInvoices(data);
      setError(null);
    } catch (err) {
      setError('Failed to fetch invoices');
      console.error('Error fetching invoices:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchInvoices();
  }, []);

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'parsed':
        return <CheckCircle className="w-4 h-4 text-green-500" />;
      case 'processing':
        return <Clock className="w-4 h-4 text-yellow-500" />;
      default:
        return <AlertTriangle className="w-4 h-4 text-red-500" />;
    }
  };

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString();
  };

  const formatCurrency = (amount: number | null) => {
    if (amount === null) return 'N/A';
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
    }).format(amount);
  };

  const stats = {
    total: invoices.length,
    parsed: invoices.filter(inv => inv.status === 'parsed').length,
    processing: invoices.filter(inv => inv.status === 'processing').length,
    failed: invoices.filter(inv => inv.status !== 'parsed' && inv.status !== 'processing').length,
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-64">
        <div className="flex items-center space-x-2">
          <RefreshCw className="w-6 h-6 animate-spin text-blue-600" />
          <span className="text-gray-600">Loading invoices...</span>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="bg-red-50 border border-red-200 rounded-lg p-4">
        <div className="flex items-center space-x-2">
          <AlertTriangle className="w-5 h-5 text-red-500" />
          <span className="text-red-700">{error}</span>
        </div>
        <button
          onClick={fetchInvoices}
          className="mt-2 px-3 py-1 bg-red-600 text-white rounded text-sm hover:bg-red-700"
        >
          Retry
        </button>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Stats Overview */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div className="bg-white rounded-lg shadow p-4">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600">Total Invoices</p>
              <p className="text-2xl font-bold text-gray-900">{stats.total}</p>
            </div>
            <FileText className="w-8 h-8 text-blue-600" />
          </div>
        </div>
        
        <div className="bg-white rounded-lg shadow p-4">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600">Parsed</p>
              <p className="text-2xl font-bold text-green-600">{stats.parsed}</p>
            </div>
            <CheckCircle className="w-8 h-8 text-green-600" />
          </div>
        </div>
        
        <div className="bg-white rounded-lg shadow p-4">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600">Processing</p>
              <p className="text-2xl font-bold text-yellow-600">{stats.processing}</p>
            </div>
            <Clock className="w-8 h-8 text-yellow-600" />
          </div>
        </div>
        
        <div className="bg-white rounded-lg shadow p-4">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600">Failed</p>
              <p className="text-2xl font-bold text-red-600">{stats.failed}</p>
            </div>
            <AlertTriangle className="w-8 h-8 text-red-600" />
          </div>
        </div>
      </div>

      {/* Invoice List */}
      <div className="bg-white rounded-lg shadow">
        <div className="px-6 py-4 border-b border-gray-200">
          <div className="flex items-center justify-between">
            <h2 className="text-lg font-semibold text-gray-900">Recent Invoices</h2>
            <button
              onClick={fetchInvoices}
              className="flex items-center space-x-1 text-sm text-blue-600 hover:text-blue-700"
            >
              <RefreshCw className="w-4 h-4" />
              <span>Refresh</span>
            </button>
          </div>
        </div>

        {invoices.length === 0 ? (
          <div className="p-8 text-center">
            <FileText className="w-12 h-12 text-gray-400 mx-auto mb-4" />
            <h3 className="text-lg font-medium text-gray-900 mb-2">No invoices yet</h3>
            <p className="text-gray-600">Upload your first invoice to get started.</p>
          </div>
        ) : (
          <div className="divide-y divide-gray-200">
            {invoices.map((invoice) => (
              <div
                key={invoice.id}
                className="px-6 py-4 hover:bg-gray-50 cursor-pointer transition-colors"
                onClick={async () => {
                  try {
                    // Fetch fresh invoice data when clicked
                    const freshInvoice = await invoiceApi.get(invoice.id);
                    setSelectedInvoice(freshInvoice);
                  } catch (error) {
                    console.error('Error fetching invoice details:', error);
                    // Fallback to the invoice from the list
                    setSelectedInvoice(invoice);
                  }
                }}
              >
                <div className="flex items-center justify-between">
                  <div className="flex items-center space-x-3">
                    {getStatusIcon(invoice.status)}
                    <div>
                      <h3 className="text-sm font-medium text-gray-900">
                        Invoice #{invoice.invoice_number}
                      </h3>
                      <p className="text-sm text-gray-500">
                        Created {formatDate(invoice.created_at)}
                      </p>
                    </div>
                  </div>
                  
                  <div className="flex items-center space-x-4">
                    <div className="text-right">
                      <p className="text-sm font-medium text-gray-900">
                        {formatCurrency(invoice.total)}
                      </p>
                      <p className="text-xs text-gray-500 capitalize">{invoice.status}</p>
                    </div>
                    <Eye className="w-4 h-4 text-gray-400" />
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Selected Invoice Detail */}
      {selectedInvoice && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
          <div className="bg-white rounded-lg max-w-4xl w-full max-h-[90vh] overflow-y-auto">
            <div className="p-6">
              <div className="flex items-center justify-between mb-4">
                <h2 className="text-xl font-semibold">Invoice Details</h2>
                <button
                  onClick={() => setSelectedInvoice(null)}
                  className="text-gray-400 hover:text-gray-600"
                >
                  ✕
                </button>
              </div>
              <InvoiceDisplay
                invoice={selectedInvoice}
                onRefresh={async () => {
                  await fetchInvoices();
                  // Refresh the selected invoice with fresh data
                  try {
                    const freshInvoice = await invoiceApi.get(selectedInvoice.id);
                    setSelectedInvoice(freshInvoice);
                  } catch (error) {
                    console.error('Error refreshing invoice details:', error);
                  }
                }}
              />
            </div>
          </div>
        </div>
      )}
    </div>
  );
} 