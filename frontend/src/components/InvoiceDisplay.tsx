'use client';

import { useState } from 'react';
import { FileText, Calendar, DollarSign, AlertTriangle, CheckCircle, Clock } from 'lucide-react';
import { Invoice, invoiceApi } from '@/lib/api';

interface InvoiceDisplayProps {
  invoice: Invoice;
  onRefresh: () => void;
}

export default function InvoiceDisplay({ invoice, onRefresh }: InvoiceDisplayProps) {
  const [isParsing, setIsParsing] = useState(false);

  const handleParse = async () => {
    setIsParsing(true);
    try {
      await invoiceApi.parse(invoice.id);
      onRefresh();
    } catch (error) {
      console.error('Parse error:', error);
    } finally {
      setIsParsing(false);
    }
  };

  const getStatusIcon = () => {
    switch (invoice.status) {
      case 'parsed':
        return <CheckCircle className="w-5 h-5 text-green-500" />;
      case 'processing':
        return <Clock className="w-5 h-5 text-yellow-500" />;
      default:
        return <AlertTriangle className="w-5 h-5 text-red-500" />;
    }
  };

  const formatCurrency = (amount: number | null) => {
    if (amount === null) return 'N/A';
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
    }).format(amount);
  };

  const formatDate = (dateString: string | null) => {
    if (!dateString) return 'N/A';
    return new Date(dateString).toLocaleDateString();
  };

  const formatConfidence = (score: number | null) => {
    if (score === null) return 'N/A';
    return `${(score * 100).toFixed(1)}%`;
  };

  return (
    <div className="bg-white rounded-lg shadow-md p-6">
      {/* Header */}
      <div className="flex items-center justify-between mb-6">
        <div className="flex items-center space-x-3">
          <FileText className="w-8 h-8 text-blue-600" />
          <div>
            <h2 className="text-2xl font-bold text-gray-900">Invoice #{invoice.invoice_number}</h2>
            <div className="flex items-center space-x-2 text-sm text-gray-600">
              {getStatusIcon()}
              <span className="capitalize">{invoice.status}</span>
              {invoice.confidence_score && (
                <>
                  <span>•</span>
                  <span>Confidence: {formatConfidence(invoice.confidence_score)}</span>
                </>
              )}
            </div>
          </div>
        </div>
        
        {invoice.status !== 'parsed' && (
          <button
            onClick={handleParse}
            disabled={isParsing}
            className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {isParsing ? 'Parsing...' : 'Parse Invoice'}
          </button>
        )}
      </div>

      {/* Invoice Details */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
        <div className="space-y-4">
          <h3 className="text-lg font-semibold text-gray-900 flex items-center">
            <Calendar className="w-5 h-5 mr-2" />
            Invoice Details
          </h3>
          
          <div className="space-y-2">
            <div className="flex justify-between">
              <span className="text-gray-600">Invoice Date:</span>
              <span className="font-medium">{formatDate(invoice.invoice_date)}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-600">Due Date:</span>
              <span className="font-medium">{formatDate(invoice.due_date)}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-600">Created:</span>
              <span className="font-medium">{formatDate(invoice.created_at)}</span>
            </div>
          </div>
        </div>

        <div className="space-y-4">
          <h3 className="text-lg font-semibold text-gray-900 flex items-center">
            <DollarSign className="w-5 h-5 mr-2" />
            Financial Summary
          </h3>
          
          <div className="space-y-2">
            <div className="flex justify-between">
              <span className="text-gray-600">Subtotal:</span>
              <span className="font-medium text-black">{formatCurrency(invoice.subtotal)}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-600">Tax:</span>
              <span className="font-medium text-black">{formatCurrency(invoice.tax)}</span>
            </div>
            <div className="flex justify-between text-lg font-bold border-t pt-2">
              <span>Total:</span>
              <span className="text-black">{formatCurrency(invoice.total)}</span>
            </div>
          </div>
        </div>
      </div>

      {/* Parsed Data */}
      {invoice.parsed_data && (
        <div className="mb-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Parsed Data</h3>
          <div className="bg-gray-50 rounded-lg p-4">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              {/* Vendor Information */}
              <div>
                <h4 className="font-medium text-gray-900 mb-3">Vendor Information</h4>
                <div className="space-y-2">
                  <div className="flex justify-between">
                    <span className="text-gray-600">Vendor Name:</span>
                    <span className="font-medium text-black">{invoice.parsed_data.vendor_name || 'N/A'}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-600">Invoice Number:</span>
                    <span className="font-medium text-black">{invoice.parsed_data.invoice_number || 'N/A'}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-600">Invoice Date:</span>
                    <span className="font-medium text-black">{formatDate(invoice.parsed_data.invoice_date)}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-600">Due Date:</span>
                    <span className="font-medium text-black">{formatDate(invoice.parsed_data.due_date)}</span>
                  </div>
                </div>
              </div>

              {/* Financial Summary */}
              <div>
                <h4 className="font-medium text-gray-900 mb-3">Financial Summary</h4>
                <div className="space-y-2">
                  <div className="flex justify-between">
                    <span className="text-gray-600">Subtotal:</span>
                    <span className="font-medium text-black">{formatCurrency(invoice.parsed_data.subtotal)}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-600">Tax:</span>
                    <span className="font-medium text-black">{formatCurrency(invoice.parsed_data.tax)}</span>
                  </div>
                  <div className="flex justify-between font-bold border-t pt-2">
                    <span>Total:</span>
                    <span className="text-black">{formatCurrency(invoice.parsed_data.total)}</span>
                  </div>
                </div>
              </div>
            </div>

            {/* Items */}
            {invoice.parsed_data.items && invoice.parsed_data.items.length > 0 && (
              <div className="mt-6">
                <h4 className="font-medium text-gray-900 mb-3">Items</h4>
                <div className="bg-white rounded border">
                  <div className="grid grid-cols-4 gap-4 p-3 bg-gray-100 border-b font-medium text-sm">
                    <div>Description</div>
                    <div>Quantity</div>
                    <div>Unit Price</div>
                    <div>Total</div>
                  </div>
                  {invoice.parsed_data.items.map((item: any, index: number) => (
                    <div key={index} className="grid grid-cols-4 gap-4 p-3 border-b last:border-b-0">
                      <div className="text-sm text-black">{item.description || 'N/A'}</div>
                      <div className="text-sm text-black">{item.quantity || 'N/A'}</div>
                      <div className="text-sm text-black">{formatCurrency(item.unit_price)}</div>
                      <div className="text-sm font-medium text-black">{formatCurrency(item.total)}</div>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* Raw JSON (collapsible for debugging) */}
            <details className="mt-4">
              <summary className="cursor-pointer text-sm text-gray-600 hover:text-gray-800">
                View Raw JSON Data
              </summary>
              <pre className="text-xs text-gray-700 whitespace-pre-wrap mt-2 bg-white p-2 rounded border">
                {JSON.stringify(invoice.parsed_data, null, 2)}
              </pre>
            </details>
          </div>
        </div>
      )}

      {/* Raw Text */}
      {invoice.raw_text && (
        <div className="mb-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Extracted Text</h3>
          <div className="bg-gray-50 rounded-lg p-4 max-h-40 overflow-y-auto">
            <p className="text-sm text-gray-700">{invoice.raw_text}</p>
          </div>
        </div>
      )}

      {/* Alerts */}
      {invoice.alerts && invoice.alerts.length > 0 && (
        <div>
          <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center">
            <AlertTriangle className="w-5 h-5 mr-2 text-yellow-500" />
            Alerts ({invoice.alerts.length})
          </h3>
          <div className="space-y-2">
            {invoice.alerts.map((alert) => (
              <div
                key={alert.id}
                className={`p-3 rounded-md border-l-4 ${
                  alert.severity === 'high' ? 'bg-red-50 border-red-400' :
                  alert.severity === 'medium' ? 'bg-yellow-50 border-yellow-400' :
                  'bg-blue-50 border-blue-400'
                }`}
              >
                <div className="flex items-center justify-between">
                  <span className="font-medium text-sm">{alert.alert_type}</span>
                  <span className={`text-xs px-2 py-1 rounded-full ${
                    alert.severity === 'high' ? 'bg-red-100 text-red-800' :
                    alert.severity === 'medium' ? 'bg-yellow-100 text-yellow-800' :
                    'bg-blue-100 text-blue-800'
                  }`}>
                    {alert.severity}
                  </span>
                </div>
                <p className="text-sm text-gray-700 mt-1">{alert.message}</p>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
} 