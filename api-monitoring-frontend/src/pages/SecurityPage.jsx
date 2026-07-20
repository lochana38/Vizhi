import { useEffect, useState, useCallback } from "react";
import { Link } from "react-router-dom";
import { getSecurityFindings, getSecuritySummary, resolveSecurityFinding } from "../api/client";
import KPICard from "../components/KPICard";
import SeverityBadge from "../components/SeverityBadge";
import EndpointPath from "../components/EndpointPath";
import { ShimmerBlock, ShimmerCardGrid } from "../components/Shimmer";

export default function SecurityPage() {
  const [summary, setSummary] = useState(null);
  const [findings, setFindings] = useState(null);
  const [severityFilter, setSeverityFilter] = useState("");
  const [issueTypeFilter, setIssueTypeFilter] = useState("");
  const [resolvedFilter, setResolvedFilter] = useState("");

  const loadFindings = useCallback(() => {
    setFindings(null);
    const params = {};
    if (severityFilter) params.severity = severityFilter;
    if (issueTypeFilter) params.issue_type = issueTypeFilter;
    if (resolvedFilter !== "") params.resolved = resolvedFilter === "true";
    getSecurityFindings(params).then(setFindings).catch(() => setFindings([]));
  }, [severityFilter, issueTypeFilter, resolvedFilter]);

  useEffect(() => {
    getSecuritySummary().then(setSummary).catch(() => setSummary(false));
  }, []);

  useEffect(() => {
    loadFindings();
  }, [loadFindings]);

  const handleResolve = async (findingId) => {
    await resolveSecurityFinding(findingId);
    loadFindings();
    getSecuritySummary().then(setSummary);
  };

  return (
    <div>
      <h1 className="text-xl font-semibold text-slate-900">Security</h1>
      <p className="mt-1 text-sm text-slate-500">Findings across all monitored endpoints.</p>

      <div className="mt-6">
        {summary === null && <ShimmerCardGrid count={4} />}
        {summary && (
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <KPICard label="Total Findings" value={summary.total_findings} />
            <KPICard label="High Severity" value={summary.high_count} tone={summary.high_count > 0 ? "critical" : "good"} />
            <KPICard label="Unresolved" value={summary.unresolved_count} tone={summary.unresolved_count > 0 ? "warning" : "good"} />
            <KPICard label="Resolved" value={summary.resolved_count} tone="good" />
          </div>
        )}
      </div>

      {/* Filters */}
      <div className="mt-6 flex flex-wrap gap-3">
        <select value={severityFilter} onChange={(e) => setSeverityFilter(e.target.value)}
          className="text-sm border border-slate-300 rounded-md px-3 py-1.5 bg-white">
          <option value="">All severities</option>
          <option value="high">High</option>
          <option value="medium">Medium</option>
          <option value="low">Low</option>
        </select>

        <select value={issueTypeFilter} onChange={(e) => setIssueTypeFilter(e.target.value)}
          className="text-sm border border-slate-300 rounded-md px-3 py-1.5 bg-white">
          <option value="">All issue types</option>
          <option value="no_auth">No auth</option>
          <option value="no_https">No HTTPS</option>
          <option value="sensitive_data_in_url">Sensitive data in URL</option>
        </select>

        <select value={resolvedFilter} onChange={(e) => setResolvedFilter(e.target.value)}
          className="text-sm border border-slate-300 rounded-md px-3 py-1.5 bg-white">
          <option value="">All statuses</option>
          <option value="false">Unresolved</option>
          <option value="true">Resolved</option>
        </select>
      </div>

      {/* Findings table */}
      <div className="mt-4 bg-white border border-slate-200 rounded-lg overflow-hidden">
        {findings === null && <div className="p-5"><ShimmerBlock className="h-48" /></div>}
        {findings && findings.length === 0 && (
          <p className="text-sm text-slate-400 p-6 text-center">No findings match these filters.</p>
        )}
        {findings && findings.length > 0 && (
          <table className="w-full text-sm">
            <thead className="bg-slate-50 text-slate-500 text-xs uppercase">
              <tr>
                <th className="text-left px-4 py-2 font-medium">Endpoint</th>
                <th className="text-left px-4 py-2 font-medium">Issue</th>
                <th className="text-left px-4 py-2 font-medium">Severity</th>
                <th className="text-left px-4 py-2 font-medium">Status</th>
                <th className="text-right px-4 py-2 font-medium">Action</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100">
              {findings.map((f) => (
                <tr key={f.id}>
                  <td className="px-4 py-3">
                    <Link to={`/endpoints/${f.endpoint_id}`} className="hover:underline">
                      <EndpointPath method={f.endpoint.method} path={f.endpoint.path} />
                    </Link>
                  </td>
                  <td className="px-4 py-3 text-slate-600">{f.issue_type.replace(/_/g, " ")}</td>
                  <td className="px-4 py-3"><SeverityBadge severity={f.severity} /></td>
                  <td className="px-4 py-3">
                    {f.resolved ? (
                      <span className="text-emerald-600 text-xs font-medium">Resolved</span>
                    ) : (
                      <span className="text-amber-600 text-xs font-medium">Unresolved</span>
                    )}
                  </td>
                  <td className="px-4 py-3 text-right">
                    {!f.resolved && (
                      <button
                        onClick={() => handleResolve(f.id)}
                        className="text-xs font-medium text-indigo-600 hover:text-indigo-700"
                      >
                        Mark resolved
                      </button>
                    )}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
  );
}
