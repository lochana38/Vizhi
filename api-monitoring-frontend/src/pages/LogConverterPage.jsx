import { useState } from "react";
import * as XLSX from "xlsx";
import axios from "axios";

// The separate demo traffic app, NOT your main FastAPI backend.
const DEMO_APP_URL = "http://127.0.0.1:9000";

export default function LogConverterPage() {
  const [logs, setLogs] = useState(null);
  const [status, setStatus] = useState("idle"); // idle | fetching | fetched | error
  const [errorMsg, setErrorMsg] = useState("");

  const fetchLogs = async () => {
    setStatus("fetching");
    setErrorMsg("");
    try {
      const res = await axios.get(`${DEMO_APP_URL}/logs`);
      setLogs(res.data);
      setStatus("fetched");
    } catch (err) {
      setStatus("error");
      setErrorMsg("Could not reach the demo traffic app. Is it running on port 9000?");
    }
  };

  const clearLogs = async () => {
    await axios.delete(`${DEMO_APP_URL}/logs`);
    setLogs([]);
  };

  // ---- The actual log -> Excel conversion, done entirely in the browser ----
  const downloadExcel = () => {
    if (!logs || logs.length === 0) return;

    // Group raw request logs into per-endpoint-per-day summaries, matching
    // exactly the "Usage" sheet columns your import feature already expects.
    const usageMap = new Map(); // key: "path|method|date" -> aggregated stats

    for (const log of logs) {
      const date = log.timestamp.slice(0, 10); // "2026-07-21T10:30:00" -> "2026-07-21"
      const key = `${log.path}|${log.method}|${date}`;

      if (!usageMap.has(key)) {
        usageMap.set(key, {
          endpoint_path: log.path,
          method: log.method,
          usage_date: date,
          total_calls: 0,
          response_times: [], // collected here, averaged at the end
          max_response_time_ms: 0,
          error_count: 0,
          total_bandwidth_bytes: 0,
        });
      }

      const entry = usageMap.get(key);
      entry.total_calls += 1;
      entry.response_times.push(log.response_time_ms);
      entry.max_response_time_ms = Math.max(entry.max_response_time_ms, log.response_time_ms);
      entry.total_bandwidth_bytes += log.response_size_bytes || 0;
      if (log.status_code >= 400) entry.error_count += 1;
    }

    const usageRows = Array.from(usageMap.values()).map((entry) => ({
      endpoint_path: entry.endpoint_path,
      method: entry.method,
      usage_date: entry.usage_date,
      total_calls: entry.total_calls,
      avg_response_time_ms: Number(
        (entry.response_times.reduce((a, b) => a + b, 0) / entry.response_times.length).toFixed(1)
      ),
      max_response_time_ms: Math.round(entry.max_response_time_ms),
      error_count: entry.error_count,
      total_bandwidth_bytes: entry.total_bandwidth_bytes,
    }));

    // Endpoints sheet: one row per UNIQUE (path, method) pair seen in the logs —
    // auto-discovered, since the demo app never told us anything about auth type etc.
    const seenEndpoints = new Map();
    for (const log of logs) {
      const key = `${log.path}|${log.method}`;
      if (!seenEndpoints.has(key)) {
        seenEndpoints.set(key, {
          path: log.path,
          method: log.method,
          name: log.path.split("/").pop() || log.path,
          description: "Auto-discovered from captured traffic logs",
          expected_auth_type: "none", // unknown from logs alone — see note in chat
          is_active: true,
          tags: "auto-discovered",
        });
      }
    }
    const endpointRows = Array.from(seenEndpoints.values());

    // Build the actual .xlsx file with two sheets, matching the import template
    const workbook = XLSX.utils.book_new();
    XLSX.utils.book_append_sheet(workbook, XLSX.utils.json_to_sheet(endpointRows), "Endpoints");
    XLSX.utils.book_append_sheet(workbook, XLSX.utils.json_to_sheet(usageRows), "Usage");

    XLSX.writeFile(workbook, `captured_traffic_${new Date().toISOString().slice(0, 10)}.xlsx`);
  };

  return (
    <div className="max-w-2xl">
      <h1 className="text-xl font-semibold text-slate-900">Log Capture → Excel</h1>
      <p className="mt-1 text-sm text-slate-500">
        Fetches raw request logs from the demo traffic app, aggregates them client-side,
        and downloads an .xlsx file in the same format your bulk import already expects.
      </p>

      <div className="mt-6 bg-white border border-slate-200 rounded-lg p-6 space-y-4">
        <div className="flex gap-3">
          <button
            onClick={fetchLogs}
            className="px-4 py-2 rounded-md bg-indigo-600 text-white text-sm font-medium hover:bg-indigo-700"
          >
            {status === "fetching" ? "Fetching..." : "Fetch logs"}
          </button>
          <button
            onClick={clearLogs}
            className="px-4 py-2 rounded-md border border-slate-300 text-sm font-medium text-slate-600 hover:bg-slate-50"
          >
            Clear captured logs
          </button>
        </div>

        {status === "error" && <p className="text-sm text-red-600">{errorMsg}</p>}

        {logs !== null && (
          <div className="text-sm text-slate-600">
            {logs.length} request{logs.length === 1 ? "" : "s"} captured so far.
          </div>
        )}

        {logs && logs.length > 0 && (
          <button
            onClick={downloadExcel}
            className="px-4 py-2 rounded-md bg-emerald-600 text-white text-sm font-medium hover:bg-emerald-700"
          >
            Download as Excel
          </button>
        )}
      </div>
    </div>
  );
}
