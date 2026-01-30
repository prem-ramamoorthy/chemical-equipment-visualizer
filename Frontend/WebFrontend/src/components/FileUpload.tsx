import React, { useState, useRef } from "react";
import { Upload, FileSpreadsheet, Loader2, CheckCircle2 } from "lucide-react";

interface FileUploadProps {
  onUpload: (file: File, filename: string) => Promise<void>;
  isLoading: boolean;
}

const FileUpload: React.FC<FileUploadProps> = ({ onUpload, isLoading }) => {
  const [dragActive, setDragActive] = useState(false);
  const [uploadSuccess, setUploadSuccess] = useState(false);
  const inputRef = useRef<HTMLInputElement>(null);

  const handleDrag = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === "dragenter" || e.type === "dragover") {
      setDragActive(true);
    } else if (e.type === "dragleave") {
      setDragActive(false);
    }
  };

  const handleDrop = async (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);

    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      await handleFile(e.dataTransfer.files[0]);
    }
  };

  const handleChange = async (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      await handleFile(e.target.files[0]);
    }
  };

  const handleFile = async (file: File) => {
    setUploadSuccess(false);
    await onUpload(file, file.name);
    setUploadSuccess(true);
    setTimeout(() => setUploadSuccess(false), 3000);
  };

  return (
    <div
      className="rounded-xl border border-slate-200 bg-white p-6 shadow-sm"
      onDragEnter={e => e.preventDefault()}
      onDragOver={e => e.preventDefault()}
      onDrop={e => e.preventDefault()}
    >
      <div className="mb-4 flex items-center gap-2">
        <FileSpreadsheet className="h-5 w-5 text-blue-600" />
        <h2 className="text-lg font-semibold text-slate-900">
          Upload Dataset
        </h2>
      </div>

      <div
        className={`relative cursor-pointer rounded-lg border-2 border-dashed p-10 text-center transition-all ${
          dragActive
            ? "border-blue-600 bg-blue-50"
            : isLoading
            ? "border-slate-300 bg-slate-100"
            : "border-slate-300 hover:border-blue-400 hover:bg-slate-50"
        }`}
        onDragEnter={handleDrag}
        onDragLeave={handleDrag}
        onDragOver={handleDrag}
        onDrop={handleDrop}
        onClick={() => inputRef.current?.click()}
        tabIndex={0}
      >
        <input
          ref={inputRef}
          type="file"
          accept=".csv"
          onChange={handleChange}
          className="hidden"
          disabled={isLoading}
        />

        <div className="flex flex-col items-center gap-3">
          {isLoading ? (
            <>
              <Loader2 className="h-12 w-12 animate-spin text-blue-600" />
              <p className="text-sm font-medium text-slate-600">
                Processing dataset...
              </p>
            </>
          ) : uploadSuccess ? (
            <>
              <CheckCircle2 className="h-12 w-12 text-emerald-600" />
              <p className="text-sm font-medium text-emerald-600">
                Dataset uploaded successfully
              </p>
            </>
          ) : (
            <>
              <Upload className="h-12 w-12 text-slate-400" />
              <div>
                <p className="text-sm font-medium text-slate-900">
                  Drop your CSV file here or{" "}
                  <span className="text-blue-600 underline">
                    browse
                  </span>
                </p>
                <p className="mt-1 text-xs text-slate-500">
                  Supports equipment parameter datasets
                </p>
              </div>
            </>
          )}
        </div>
      </div>
    </div>
  );
};

export default FileUpload;
