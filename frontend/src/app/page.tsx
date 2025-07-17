'use client';

import { useState } from 'react';
import { FileText, BarChart3 } from 'lucide-react';
import FileUpload from '@/components/FileUpload';
import Dashboard from '@/components/Dashboard';

export default function Home() {
  const [activeTab, setActiveTab] = useState<'upload' | 'dashboard'>('upload');
  const [refreshTrigger, setRefreshTrigger] = useState(0);

  const handleUploadSuccess = (invoiceId: number) => {
    // Switch to dashboard and trigger refresh
    setActiveTab('dashboard');
    setRefreshTrigger(prev => prev + 1);
  };

  const handleUploadError = (error: string) => {
    console.error('Upload error:', error);
    // You could add a toast notification here
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            <div className="flex items-center space-x-3">
              <FileText className="w-8 h-8 text-blue-600" />
              <h1 className="text-2xl font-bold text-gray-900">BevScan</h1>
              <span className="text-sm text-gray-500">Smart Invoice Parser</span>
            </div>
            
            {/* Navigation Tabs */}
            <nav className="flex space-x-1">
              <button
                onClick={() => setActiveTab('upload')}
                className={`px-4 py-2 rounded-md text-sm font-medium transition-colors ${
                  activeTab === 'upload'
                    ? 'bg-blue-100 text-blue-700'
                    : 'text-gray-500 hover:text-gray-700 hover:bg-gray-100'
                }`}
              >
                Upload Invoice
              </button>
              <button
                onClick={() => setActiveTab('dashboard')}
                className={`px-4 py-2 rounded-md text-sm font-medium transition-colors ${
                  activeTab === 'dashboard'
                    ? 'bg-blue-100 text-blue-700'
                    : 'text-gray-500 hover:text-gray-700 hover:bg-gray-100'
                }`}
              >
                Dashboard
              </button>
            </nav>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {activeTab === 'upload' ? (
          <div className="space-y-8">
            <div className="text-center">
              <h2 className="text-3xl font-bold text-gray-900 mb-4">
                Upload Invoice
              </h2>
              <p className="text-lg text-gray-600 max-w-2xl mx-auto">
                Upload your invoice files (PDF, PNG, JPG, JPEG, TIFF) and let our AI-powered system 
                extract and parse the data automatically.
              </p>
            </div>
            
            <FileUpload
              onUploadSuccess={handleUploadSuccess}
              onUploadError={handleUploadError}
            />
            
            <div className="text-center text-sm text-gray-500">
              <p>Supported formats: PDF, PNG, JPG, JPEG, TIFF</p>
              <p>Maximum file size: 10MB</p>
            </div>
          </div>
        ) : (
          <div className="space-y-6">
            <div className="flex items-center justify-between">
              <div>
                <h2 className="text-3xl font-bold text-gray-900 mb-2">
                  Invoice Dashboard
                </h2>
                <p className="text-gray-600">
                  View and manage all your uploaded invoices
                </p>
              </div>
            </div>
            
            <Dashboard key={refreshTrigger} />
          </div>
        )}
      </main>
    </div>
  );
}
