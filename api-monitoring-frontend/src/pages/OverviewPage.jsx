import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import {
  LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer,
  PieChart, Pie, Cell, Legend,
} from "recharts";
import { getKpiCards, getTrafficTrend, getHealthDistribution, getRecentAlerts } from "../api/client";
import KPICard from "../components/KPICard";
import { ShimmerCardGrid, ShimmerBlock } from "../components/Shimmer";
import SeverityBadge from "../components/SeverityBadge";
import AIActionsCard from "../components/AIActionsCard";

const HEALTH_COLORS = { healthy: "#10b981", warning: "#f59e0b", critical: "#ef4444" };

export default function OverviewPage() {
  const [kpi, setKpi] = useState(null);
  const [trend, setTrend] = useState(null);
  const [health, setHealth] = useState(null);
  const [alerts, setAlerts] = useState(null);

  useEffect(() => {
    getKpiCards().then(setKpi).catch(() => setKpi(false));
    getTrafficTrend(30).then(setTrend).catch(() => setTrend([]));
    getHealthDistribution().then(setHealth).catch(() => setHealth(false));
    getRecentAlerts(8).then(setAlerts).catch(() => setAlerts([]));
  }, []);

  const healthPieData = health
    ? [
      { name: "Healthy", value: health.healthy, key: "healthy" },
      { name: "Warning", value: health.warning, key: "warning" },
      { name: "Critical", value: health.critical, key: "critical" },
    ]
    : [];

  return (
    <div>
      <h1 className="text-xl font-semibold text-slate-900">Overview</h1>
      <p className="mt-1 text-sm text-slate-500">Endpoint health, traffic, and recent alerts.</p>

      {/* KPI cards */}
      <div className="mt-6">
        {kpi === null && <ShimmerCardGrid count={4} />}
        {kpi === false && <p className="text-sm text-red-600">Could not load KPI cards.</p>}
        {kpi && (
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <KPICard label="Total Endpoints" value={kpi.total_endpoints} />
            <KPICard label="Active Endpoints" value={kpi.active_endpoints} />
            <KPICard
              label="Health Score"
              value={`${kpi.health_score_percentage}%`}
              tone={kpi.health_score_percentage >= 80 ? "good" : kpi.health_score_percentage >= 50 ? "warning" : "critical"}
            />
            <KPICard label="Unhealthy Endpoints" value={kpi.unhealthy_endpoints} tone={kpi.unhealthy_endpoints > 0 ? "critical" : "good"} />
          </div>
        )}
      </div>

      <div className="mt-6">
        <AIActionsCard />
      </div>


      <div className="mt-6 grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Traffic trend chart */}
        <div className="lg:col-span-2 bg-white border border-slate-200 rounded-lg p-5">
          <h2 className="text-sm font-semibold text-slate-800">Traffic trend (last 30 days)</h2>
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
                  <YAxis tick={{ fontSize: 11 }} />
                  <Tooltip />
                  <Line type="monotone" dataKey="total_calls" stroke="#4f46e5" strokeWidth={2} dot={false} />
                </LineChart>
              </ResponsiveContainer>
            )}
          </div>
        </div>

        {/* Health distribution */}
        <div className="bg-white border border-slate-200 rounded-lg p-5">
          <h2 className="text-sm font-semibold text-slate-800">Health distribution</h2>
          <div className="mt-4 h-64">
            {health === null && <ShimmerBlock className="h-full" />}
            {health === false && <p className="text-sm text-red-600">Could not load.</p>}
            {health && (
              <ResponsiveContainer width="100%" height="100%">
                <PieChart>
                  <Pie data={healthPieData} dataKey="value" nameKey="name" innerRadius={50} outerRadius={80} paddingAngle={2}>
                    {healthPieData.map((entry) => (
                      <Cell key={entry.key} fill={HEALTH_COLORS[entry.key]} />
                    ))}
                  </Pie>
                  <Legend verticalAlign="bottom" height={30} iconSize={8} wrapperStyle={{ fontSize: 12 }} />
                  <Tooltip />
                </PieChart>
              </ResponsiveContainer>
            )}
          </div>
        </div>
      </div>

      {/* Recent alerts feed */}
      <div className="mt-6 bg-white border border-slate-200 rounded-lg p-5">
        <h2 className="text-sm font-semibold text-slate-800">Recent alerts</h2>
        <div className="mt-3 divide-y divide-slate-100">
          {alerts === null && (
            <div className="space-y-3 py-2">
              <ShimmerBlock className="h-8" />
              <ShimmerBlock className="h-8" />
              <ShimmerBlock className="h-8" />
            </div>
          )}
          {alerts && alerts.length === 0 && <p className="text-sm text-slate-400 py-4">No alerts yet.</p>}
          {alerts &&
            alerts.map((alert, i) => (
              <div key={i} className="py-3 flex items-center justify-between gap-3">
                <div className="min-w-0">
                  <p className="text-sm text-slate-800 truncate">
                    <span className="text-xs uppercase text-slate-400 mr-2">{alert.alert_type.replace("_", " ")}</span>
                    {alert.details || alert.severity_or_type}
                  </p>
                  <Link to={`/endpoints/${alert.endpoint_id}`} className="text-xs text-indigo-600 hover:underline">
                    Endpoint #{alert.endpoint_id}
                  </Link>
                </div>
                {alert.alert_type === "security" ? (
                  <SeverityBadge severity={alert.severity_or_type} />
                ) : (
                  <span className="text-xs text-slate-500 whitespace-nowrap">{alert.severity_or_type}</span>
                )}
              </div>
            ))}
        </div>
      </div>
    </div>
  );
}
