import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { importBulkFile } from "../api/client";

export default function ImportPage() {
  const [file, setFile] = useState(null);
  const [status, setStatus] = useState("idle"); // idle | processing | done | error
  const [result, setResult] = useState(null);
  const [errorMsg, setErrorMsg] = useState("");
  const navigate = useNavigate();

  const handleUpload = async () => {
    if (!file) return;
    setStatus("processing");
    setErrorMsg("");

    try {
      const data = await importBulkFile(file);
      setResult(data);
      setStatus("done");
    } catch (err) {
      setStatus("error");
      setErrorMsg(
        err.response?.data?.detail || "Something went wrong during import. Check the backend logs."
      );
    }
  };

  return (
    <div className="max-w-2xl">
      <h1 className="text-xl font-semibold text-slate-900">Import Data</h1>
      <p className="mt-1 text-sm text-slate-500">
        Upload an .xlsx file with two sheets: <span className="font-mono-path">Endpoints</span> and{" "}
        <span className="font-mono-path">Usage</span>. Security findings and duplicate groups are
        detected automatically after import.
      </p>

      <div className="mt-6 bg-white border border-slate-200 rounded-lg p-6">
        <input
          type="file"
          accept=".xlsx"
          onChange={(e) => setFile(e.target.files[0])}
          disabled={status === "processing"}
          className="block w-full text-sm text-slate-600 file:mr-4 file:py-2 file:px-4
                     file:rounded-md file:border-0 file:text-sm file:font-medium
                     file:bg-slate-900 file:text-white hover:file:bg-slate-700
                     file:cursor-pointer disabled:opacity-50"
        />

        <button
          onClick={handleUpload}
          disabled={!file || status === "processing"}
          className="mt-4 px-4 py-2 rounded-md bg-indigo-600 text-white text-sm font-medium
                     hover:bg-indigo-700 disabled:opacity-40 disabled:cursor-not-allowed"
        >
          {status === "processing" ? "Importing..." : "Upload & Import"}
        </button>

        {/* Shimmer effect while the import is processing on the backend */}
        {status === "processing" && (
          <div className="mt-6 space-y-3">
            <div className="shimmer h-4 rounded w-3/4" />
            <div className="shimmer h-4 rounded w-1/2" />
            <div className="shimmer h-4 rounded w-2/3" />
            <p className="text-xs text-slate-400 pt-1">
              Parsing sheets, inserting rows, and running security + duplicate detection…
            </p>
          </div>
        )}

        {status === "error" && (
          <div className="mt-6 bg-red-50 border border-red-200 rounded-md px-4 py-3">
            <p className="text-sm text-red-700 font-medium">Import failed</p>
            <p className="text-sm text-red-600 mt-1">{errorMsg}</p>
          </div>
        )}

        {status === "done" && result && (
          <div className="mt-6 bg-emerald-50 border border-emerald-200 rounded-md px-4 py-4">
            <p className="text-sm text-emerald-800 font-medium">
              Import {result.status === "completed" ? "completed" : result.status}
            </p>
            <dl className="mt-3 grid grid-cols-3 gap-3 text-sm">
              <div>
                <dt className="text-emerald-600 text-xs">Successful</dt>
                <dd className="font-semibold text-emerald-900">{result.successful_imports}</dd>
              </div>
              <div>
                <dt className="text-emerald-600 text-xs">Skipped</dt>
                <dd className="font-semibold text-emerald-900">{result.skipped_imports}</dd>
              </div>
              <div>
                <dt className="text-emerald-600 text-xs">Failed</dt>
                <dd className="font-semibold text-emerald-900">{result.failed_imports}</dd>
              </div>
            </dl>
            <button
              onClick={() => navigate("/")}
              className="mt-4 text-sm font-medium text-indigo-600 hover:text-indigo-700"
            >
              Go to dashboard →
            </button>
          </div>
        )}
      </div>
    </div>
  );
}
