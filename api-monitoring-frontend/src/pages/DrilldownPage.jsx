import { useEffect, useState } from "react";
import { useParams, Link } from "react-router-dom";
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from "recharts";
import { getEndpointDrilldown } from "../api/client";
import EndpointPath from "../components/EndpointPath";
import SeverityBadge from "../components/SeverityBadge";
import { ShimmerBlock } from "../components/Shimmer";

export default function DrilldownPage() {
  const { endpointId } = useParams();
  const [data, setData] = useState(null);
  const [notFound, setNotFound] = useState(false);

  useEffect(() => {
    setData(null);
    setNotFound(false);
    getEndpointDrilldown(endpointId, 30)
      .then(setData)
      .catch((err) => {
        if (err.response?.status === 404) setNotFound(true);
        else setData(false);
      });
  }, [endpointId]);

  if (notFound) {
    return (
      <div>
        <Link to="/" className="text-sm text-indigo-600 hover:underline">← Back to overview</Link>
        <p className="mt-4 text-sm text-slate-500">Endpoint #{endpointId} was not found.</p>
      </div>
    );
  }

  if (data === false) {
    return <p className="text-sm text-red-600">Could not load this endpoint.</p>;
  }

  if (data === null) {
    return (
      <div className="space-y-4">
        <ShimmerBlock className="h-8 w-64" />
        <ShimmerBlock className="h-40" />
      </div>
    );
  }

  const { endpoint, security_findings, data_leak_findings, duplicate_memberships, usage_timeseries } = data;

  return (
    <div>
      <Link to="/" className="text-sm text-indigo-600 hover:underline">← Back to overview</Link>

      <div className="mt-3 flex items-center justify-between">
        <div>
          <EndpointPath method={endpoint.method} path={endpoint.path} />
          <p className="mt-1 text-sm text-slate-500">{endpoint.name || "Untitled endpoint"}</p>
        </div>
        <span className={`text-xs font-medium px-2 py-1 rounded-full border ${
          endpoint.is_active ? "bg-emerald-50 text-emerald-700 border-emerald-200" : "bg-slate-100 text-slate-500 border-slate-200"
        }`}>
          {endpoint.is_active ? "Active" : "Inactive"}
        </span>
      </div>

      {endpoint.description && <p className="mt-2 text-sm text-slate-600">{endpoint.description}</p>}

      <div className="mt-2 flex flex-wrap gap-1.5">
        {(endpoint.tags || []).map((tag) => (
          <span key={tag} className="text-xs bg-slate-100 text-slate-600 px-2 py-0.5 rounded-full">{tag}</span>
        ))}
      </div>

      {/* Usage graph */}
      <div className="mt-6 bg-white border border-slate-200 rounded-lg p-5">
        <h2 className="text-sm font-semibold text-slate-800">Usage (last 30 days)</h2>
        <div className="mt-4 h-56">
          {usage_timeseries.length === 0 ? (
            <p className="text-sm text-slate-400 flex items-center justify-center h-full">No usage data for this endpoint</p>
          ) : (
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={usage_timeseries}>
                <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" />
                <XAxis dataKey="usage_date" tick={{ fontSize: 11 }} />
                <YAxis yAxisId="left" tick={{ fontSize: 11 }} />
                <YAxis yAxisId="right" orientation="right" tick={{ fontSize: 11 }} />
                <Tooltip />
                <Line yAxisId="left" type="monotone" dataKey="total_calls" stroke="#4f46e5" strokeWidth={2} dot={false} name="Calls" />
                <Line yAxisId="right" type="monotone" dataKey="avg_response_time_ms" stroke="#f59e0b" strokeWidth={2} dot={false} name="Avg ms" />
              </LineChart>
            </ResponsiveContainer>
          )}
        </div>
      </div>

      <div className="mt-6 grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Security findings */}
        <div className="bg-white border border-slate-200 rounded-lg p-5">
          <h2 className="text-sm font-semibold text-slate-800">Security findings</h2>
          <div className="mt-3 space-y-2">
            {security_findings.length === 0 && <p className="text-sm text-slate-400">None recorded.</p>}
            {security_findings.map((f) => (
              <div key={f.id} className="flex items-center justify-between border border-slate-100 rounded-md px-3 py-2">
                <span className="text-sm text-slate-700">{f.issue_type.replace(/_/g, " ")}</span>
                <div className="flex items-center gap-2">
                  <SeverityBadge severity={f.severity} />
                  <span className={`text-xs ${f.resolved ? "text-emerald-600" : "text-amber-600"}`}>
                    {f.resolved ? "Resolved" : "Open"}
                  </span>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Data leak findings */}
        <div className="bg-white border border-slate-200 rounded-lg p-5">
          <h2 className="text-sm font-semibold text-slate-800">Data leak findings</h2>
          <div className="mt-3 space-y-2">
            {data_leak_findings.length === 0 && <p className="text-sm text-slate-400">None recorded.</p>}
            {data_leak_findings.map((f) => (
              <div key={f.id} className="flex items-center justify-between border border-slate-100 rounded-md px-3 py-2">
                <span className="text-sm text-slate-700">{f.leak_type.replace(/_/g, " ")}</span>
                <span className={`text-xs ${f.resolved ? "text-emerald-600" : "text-amber-600"}`}>
                  {f.resolved ? "Resolved" : "Open"}
                </span>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Duplicate memberships */}
      <div className="mt-6 bg-white border border-slate-200 rounded-lg p-5">
        <h2 className="text-sm font-semibold text-slate-800">Duplicate group membership</h2>
        <div className="mt-3">
          {duplicate_memberships.length === 0 && <p className="text-sm text-slate-400">Not part of any duplicate group.</p>}
          {duplicate_memberships.map((m) => (
            <div key={m.group_id} className="text-sm text-slate-700 py-1">
              {m.group_label || `Group #${m.group_id}`}
              {m.similarity_score != null && <span className="text-slate-400 text-xs ml-2">{m.similarity_score}% match</span>}
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
