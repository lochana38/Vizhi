import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import {
  LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer,
} from "recharts";
import { getResponseTimeTrend, getSlowestEndpoints, getBandwidthUsage } from "../api/client";
import EndpointPath from "../components/EndpointPath";
import { ShimmerBlock } from "../components/Shimmer";

function formatBytes(bytes) {
  if (!bytes) return "0 B";
  const units = ["B", "KB", "MB", "GB"];
  let i = 0;
  let val = bytes;
  while (val >= 1024 && i < units.length - 1) {
    val /= 1024;
    i++;
  }
  return `${val.toFixed(1)} ${units[i]}`;
}

export default function PerformancePage() {
  const [trend, setTrend] = useState(null);
  const [slowest, setSlowest] = useState(null);
  const [bandwidth, setBandwidth] = useState(null);

  useEffect(() => {
    getResponseTimeTrend(30).then(setTrend).catch(() => setTrend([]));
    getSlowestEndpoints(10).then(setSlowest).catch(() => setSlowest([]));
    getBandwidthUsage(10).then(setBandwidth).catch(() => setBandwidth([]));
  }, []);

  return (
    <div>
      <h1 className="text-xl font-semibold text-slate-900">Performance</h1>
      <p className="mt-1 text-sm text-slate-500">Response times and bandwidth across endpoints.</p>

      <div className="mt-6 bg-white border border-slate-200 rounded-lg p-5">
        <h2 className="text-sm font-semibold text-slate-800">Response-time trend (last 30 days)</h2>
        <div className="mt-4 h-64">
          {trend === null && <ShimmerBlock className="h-full" />}
          {trend && trend.length === 0 && (
            <p className="text-sm text-slate-400 flex items-center justify-center h-full">No usage data yet</p>
          )}
          {trend && trend.length > 0 && (
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={trend}>
                <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" />
                <XAxis dataKey="usage_date" tick={{ fontSize: 11 }} />
                <YAxis tick={{ fontSize: 11 }} unit="ms" />
                <Tooltip />
                <Line type="monotone" dataKey="avg_response_time_ms" stroke="#f59e0b" strokeWidth={2} dot={false} />
              </LineChart>
            </ResponsiveContainer>
          )}
        </div>
      </div>

      <div className="mt-6 grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Slowest endpoints table */}
        <div className="bg-white border border-slate-200 rounded-lg overflow-hidden">
          <h2 className="text-sm font-semibold text-slate-800 px-5 pt-5">Slowest endpoints</h2>
          <div className="mt-3">
            {slowest === null && <div className="p-5"><ShimmerBlock className="h-40" /></div>}
            {slowest && slowest.length === 0 && (
              <p className="text-sm text-slate-400 p-5">No usage data yet.</p>
            )}
            {slowest && slowest.length > 0 && (
              <table className="w-full text-sm">
                <thead className="bg-slate-50 text-slate-500 text-xs uppercase">
                  <tr>
                    <th className="text-left px-4 py-2 font-medium">Endpoint</th>
                    <th className="text-right px-4 py-2 font-medium">Avg ms</th>
                    <th className="text-right px-4 py-2 font-medium">Max ms</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-100">
                  {slowest.map((row) => (
                    <tr key={row.endpoint.id}>
                      <td className="px-4 py-3">
                        <Link to={`/endpoints/${row.endpoint.id}`} className="hover:underline">
                          <EndpointPath method={row.endpoint.method} path={row.endpoint.path} />
                        </Link>
                      </td>
                      <td className="px-4 py-3 text-right text-slate-700">{row.avg_response_time_ms.toFixed(1)}</td>
                      <td className="px-4 py-3 text-right text-slate-500">{row.max_response_time_ms ?? "—"}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            )}
          </div>
        </div>

        {/* Bandwidth usage table */}
        <div className="bg-white border border-slate-200 rounded-lg overflow-hidden">
          <h2 className="text-sm font-semibold text-slate-800 px-5 pt-5">Bandwidth usage</h2>
          <div className="mt-3">
            {bandwidth === null && <div className="p-5"><ShimmerBlock className="h-40" /></div>}
            {bandwidth && bandwidth.length === 0 && (
              <p className="text-sm text-slate-400 p-5">No usage data yet.</p>
            )}
            {bandwidth && bandwidth.length > 0 && (
              <table className="w-full text-sm">
                <thead className="bg-slate-50 text-slate-500 text-xs uppercase">
                  <tr>
                    <th className="text-left px-4 py-2 font-medium">Endpoint</th>
                    <th className="text-right px-4 py-2 font-medium">Total bandwidth</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-100">
                  {bandwidth.map((row) => (
                    <tr key={row.endpoint.id}>
                      <td className="px-4 py-3">
                        <Link to={`/endpoints/${row.endpoint.id}`} className="hover:underline">
                          <EndpointPath method={row.endpoint.method} path={row.endpoint.path} />
                        </Link>
                      </td>
                      <td className="px-4 py-3 text-right text-slate-700">{formatBytes(row.total_bandwidth_bytes)}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
