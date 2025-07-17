'use client';

import { useState, useCallback } from 'react';
import { useDropzone } from 'react-dropzone';
import { Upload, FileText, AlertCircle, CheckCircle, RefreshCw } from 'lucide-react';
import { invoiceApi } from '@/lib/api';

interface FileUploadProps {
  onUploadSuccess: (invoiceId: number) => void;
  onUploadError: (error: string) => void;
}

const LLM_OPTIONS = [
  { label: 'DeepSeek (Ollama)', provider: 'deepseek', model: 'deepseek-r1:latest' },
  { label: 'Llama 3.2 (Ollama)', provider: 'llama', model: 'llama3.2:latest' },
  { label: 'Gemini 1.5 Flash', provider: 'gemini', model: 'gemini-1.5-flash' },
];

const POLL_INTERVAL = 2000; // 2 seconds
const POLL_TIMEOUT = 60 * 1000; // 1 minute

export default function FileUpload({ onUploadSuccess, onUploadError }: FileUploadProps) {
  const [isUploading, setIsUploading] = useState(false);
  const [uploadStatus, setUploadStatus] = useState<'idle' | 'uploading' | 'success' | 'error'>('idle');
  const [llmOption, setLlmOption] = useState(LLM_OPTIONS[0]);
  const [parsing, setParsing] = useState(false);

  const pollForParsed = async (invoiceId: number) => {
    setParsing(true);
    const start = Date.now();
    while (Date.now() - start < POLL_TIMEOUT) {
      try {
        const invoice = await invoiceApi.get(invoiceId);
        if (invoice.status === 'parsed' && invoice.parsed_data) {
          setParsing(false);
          onUploadSuccess(invoiceId);
          return;
        }
        if (invoice.status === 'error') {
          setParsing(false);
          onUploadError('Parsing failed.');
          return;
        }
        // If still processing, continue polling
        console.log(`Invoice ${invoiceId} status: ${invoice.status}`);
      } catch (e) {
        console.error('Error polling invoice:', e);
        // Continue polling even if there's an error
      }
      await new Promise(res => setTimeout(res, POLL_INTERVAL));
    }
    setParsing(false);
    onUploadError('Parsing timed out.');
  };

  const onDrop = useCallback(async (acceptedFiles: File[]) => {
    if (acceptedFiles.length === 0) return;

    const file = acceptedFiles[0];
    setIsUploading(true);
    setUploadStatus('uploading');

    try {
      const result = await invoiceApi.upload(file, llmOption.provider, llmOption.model);
      setUploadStatus('success');
      // The backend returns the invoice object directly, so we use result.id
      pollForParsed(result.id);
    } catch (error) {
      console.error('Upload error:', error);
      setUploadStatus('error');
      onUploadError(error instanceof Error ? error.message : 'Upload failed');
    } finally {
      setIsUploading(false);
    }
  }, [onUploadSuccess, onUploadError, llmOption]);

  const { getRootProps, getInputProps, isDragActive, isDragReject } = useDropzone({
    onDrop,
    accept: {
      'application/pdf': ['.pdf'],
      'image/*': ['.png', '.jpg', '.jpeg', '.tiff']
    },
    maxFiles: 1,
    disabled: isUploading || parsing
  });

  const getStatusIcon = () => {
    switch (uploadStatus) {
      case 'success':
        return <CheckCircle className="w-8 h-8 text-green-500" />;
      case 'error':
        return <AlertCircle className="w-8 h-8 text-red-500" />;
      case 'uploading':
        return <div className="w-8 h-8 border-2 border-blue-500 border-t-transparent rounded-full animate-spin" />;
      default:
        return <Upload className="w-8 h-8 text-gray-400" />;
    }
  };

  const getStatusText = () => {
    switch (uploadStatus) {
      case 'success':
        return 'File uploaded successfully!';
      case 'error':
        return 'Upload failed. Please try again.';
      case 'uploading':
        return 'Uploading...';
      default:
        return isDragActive ? 'Drop the file here' : 'Drag & drop a file here, or click to select';
    }
  };

  return (
    <div className="w-full max-w-2xl mx-auto">
      {/* LLM Provider Dropdown */}
      <div className="mb-4 flex flex-col items-start">
        <label htmlFor="llm-provider" className="mb-1 font-medium text-gray-700">LLM Provider</label>
        <select
          id="llm-provider"
          className="border rounded px-3 py-2 text-gray-800"
          value={llmOption.label}
          onChange={e => {
            const selected = LLM_OPTIONS.find(opt => opt.label === e.target.value);
            if (selected) setLlmOption(selected);
          }}
          disabled={isUploading || parsing}
        >
          {LLM_OPTIONS.map(opt => (
            <option key={opt.label} value={opt.label}>{opt.label}</option>
          ))}
        </select>
      </div>
      <div
        {...getRootProps()}
        className={`
          border-2 border-dashed rounded-lg p-8 text-center cursor-pointer transition-colors
          ${isDragActive && !isDragReject ? 'border-blue-500 bg-blue-50' : ''}
          ${isDragReject ? 'border-red-500 bg-red-50' : ''}
          ${!isDragActive && uploadStatus === 'idle' ? 'border-gray-300 hover:border-gray-400' : ''}
          ${uploadStatus === 'success' ? 'border-green-500 bg-green-50' : ''}
          ${uploadStatus === 'error' ? 'border-red-500 bg-red-50' : ''}
          ${(isUploading || parsing) ? 'opacity-50 cursor-not-allowed' : ''}
        `}
      >
        <input {...getInputProps()} />
        <div className="flex flex-col items-center space-y-4">
          {parsing ? (
            <RefreshCw className="w-8 h-8 animate-spin text-blue-600" />
          ) : getStatusIcon()}
          <div className="text-center">
            <h3 className="text-lg font-medium text-gray-900 mb-2">
              {parsing ? 'Parsing Invoice...' : uploadStatus === 'success' ? 'Upload Complete' : 'Upload Invoice'}
            </h3>
            <p className="text-sm text-gray-600 mb-4">
              {parsing ? 'Extracting data with selected LLM...' : getStatusText()}
            </p>
            {uploadStatus === 'idle' && !parsing && (
              <div className="text-xs text-gray-500">
                <p>Supported formats: PDF, PNG, JPG, JPEG, TIFF</p>
                <p>Maximum file size: 10MB</p>
              </div>
            )}
          </div>
          {isDragReject && (
            <div className="text-red-600 text-sm">
              <AlertCircle className="w-4 h-4 inline mr-1" />
              File type not supported
            </div>
          )}
        </div>
      </div>
    </div>
  );
}