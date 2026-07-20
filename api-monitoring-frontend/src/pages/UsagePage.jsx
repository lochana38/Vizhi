import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from "recharts";
import { getTrafficRanking, getUnusedEndpoints, getDuplicateGroups } from "../api/client";
import EndpointPath from "../components/EndpointPath";
import { ShimmerBlock } from "../components/Shimmer";

export default function UsagePage() {
  const [ranking, setRanking] = useState(null);
  const [unused, setUnused] = useState(null);
  const [duplicates, setDuplicates] = useState(null);

  useEffect(() => {
    getTrafficRanking(10, "desc").then(setRanking).catch(() => setRanking([]));
    getUnusedEndpoints(30).then(setUnused).catch(() => setUnused([]));
    getDuplicateGroups().then(setDuplicates).catch(() => setDuplicates([]));
  }, []);

  const chartData = ranking
    ? ranking.map((r) => ({ label: r.endpoint.path, total_calls: r.total_calls }))
    : [];

  return (
    <div>
      <h1 className="text-xl font-semibold text-slate-900">Usage</h1>
      <p className="mt-1 text-sm text-slate-500">Traffic ranking, unused endpoints, and duplicate groups.</p>

      {/* Traffic ranking chart */}
      <div className="mt-6 bg-white border border-slate-200 rounded-lg p-5">
        <h2 className="text-sm font-semibold text-slate-800">Top endpoints by traffic</h2>
        <div className="mt-4 h-72">
          {ranking === null && <ShimmerBlock className="h-full" />}
          {ranking && ranking.length === 0 && (
            <p className="text-sm text-slate-400 flex items-center justify-center h-full">No usage data yet</p>
          )}
          {ranking && ranking.length > 0 && (
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={chartData} layout="vertical" margin={{ left: 40 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" />
                <XAxis type="number" tick={{ fontSize: 11 }} />
                <YAxis type="category" dataKey="label" tick={{ fontSize: 11 }} width={160} />
                <Tooltip />
                <Bar dataKey="total_calls" fill="#4f46e5" radius={[0, 4, 4, 0]} />
              </BarChart>
            </ResponsiveContainer>
          )}
        </div>
      </div>

      <div className="mt-6 grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Unused endpoints */}
        <div className="bg-white border border-slate-200 rounded-lg overflow-hidden">
          <h2 className="text-sm font-semibold text-slate-800 px-5 pt-5">Unused endpoints (30 days)</h2>
          <div className="mt-3">
            {unused === null && <div className="p-5"><ShimmerBlock className="h-40" /></div>}
            {unused && unused.length === 0 && (
              <p className="text-sm text-slate-400 p-5">Every endpoint has recent traffic.</p>
            )}
            {unused && unused.length > 0 && (
              <table className="w-full text-sm">
                <thead className="bg-slate-50 text-slate-500 text-xs uppercase">
                  <tr>
                    <th className="text-left px-4 py-2 font-medium">Endpoint</th>
                    <th className="text-right px-4 py-2 font-medium">Last called</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-100">
                  {unused.map((row) => (
                    <tr key={row.endpoint.id}>
                      <td className="px-4 py-3">
                        <Link to={`/endpoints/${row.endpoint.id}`} className="hover:underline">
                          <EndpointPath method={row.endpoint.method} path={row.endpoint.path} />
                        </Link>
                      </td>
                      <td className="px-4 py-3 text-right text-slate-500">{row.last_called || "Never"}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            )}
          </div>
        </div>

        {/* Duplicate groups */}
        <div className="bg-white border border-slate-200 rounded-lg p-5">
          <h2 className="text-sm font-semibold text-slate-800">Duplicate API groups</h2>
          <div className="mt-3 space-y-4">
            {duplicates === null && <ShimmerBlock className="h-40" />}
            {duplicates && duplicates.length === 0 && (
              <p className="text-sm text-slate-400">No duplicate groups detected.</p>
            )}
            {duplicates &&
              duplicates.map((group) => (
                <div key={group.id} className="border border-slate-100 rounded-md p-3">
                  <p className="text-xs font-medium text-slate-500 mb-2">{group.group_label || `Group #${group.id}`}</p>
                  <ul className="space-y-1.5">
                    {group.members.map((m) => (
                      <li key={m.endpoint.id} className="flex items-center justify-between">
                        <Link to={`/endpoints/${m.endpoint.id}`} className="hover:underline">
                          <EndpointPath method={m.endpoint.method} path={m.endpoint.path} />
                        </Link>
                        {m.similarity_score != null && (
                          <span className="text-xs text-slate-400">{m.similarity_score}% match</span>
                        )}
                      </li>
                    ))}
                  </ul>
                </div>
              ))}
          </div>
        </div>
      </div>
    </div>
  );
}
