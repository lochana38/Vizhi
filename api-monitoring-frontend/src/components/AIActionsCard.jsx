import { useEffect, useState } from "react";
import { getNextActions } from "../api/client";
import { ShimmerBlock } from "./Shimmer";

const PRIORITY_STYLES = {
  high: "bg-red-50 text-red-700 border-red-200",
  medium: "bg-amber-50 text-amber-700 border-amber-200",
  low: "bg-slate-100 text-slate-600 border-slate-200",
};

export default function AIActionsCard() {
  const [data, setData] = useState(null);
  const [error, setError] = useState(null);
  const [refreshing, setRefreshing] = useState(false);

  const load = (forceRefresh = false) => {
    if (forceRefresh) setRefreshing(true);
    getNextActions(forceRefresh)
      .then((res) => {
        setData(res);
        setError(null);
      })
      .catch((err) => setError(err.response?.data?.detail || "Could not load suggestions."))
      .finally(() => setRefreshing(false));
  };

  useEffect(() => {
    load(false);
  }, []);

  return (
    <div className="bg-white border border-slate-200 rounded-lg p-5">
      <div className="flex items-center justify-between">
        <h2 className="text-sm font-semibold text-slate-800">Suggested next actions</h2>
        <button
          onClick={() => load(true)}
          disabled={refreshing}
          className="text-xs font-medium text-indigo-600 hover:text-indigo-700 disabled:opacity-40"
        >
          {refreshing ? "Refreshing…" : "Refresh"}
        </button>
      </div>

      {data === null && !error && (
        <div className="mt-3 space-y-2">
          <ShimmerBlock className="h-14" />
          <ShimmerBlock className="h-14" />
          <ShimmerBlock className="h-14" />
        </div>
      )}

      {error && <p className="mt-3 text-sm text-red-600">{error}</p>}

      {data && (
        <div className="mt-3 space-y-2">
          {data.actions.map((action, i) => (
            <div key={i} className="border border-slate-100 rounded-md p-3">
              <div className="flex items-center justify-between gap-2">
                <p className="text-sm font-medium text-slate-800">{action.title}</p>
                <span className={`text-xs font-medium px-2 py-0.5 rounded-full border shrink-0 ${PRIORITY_STYLES[action.priority] || PRIORITY_STYLES.low}`}>
                  {action.priority}
                </span>
              </div>
              <p className="mt-1 text-xs text-slate-500">{action.description}</p>
            </div>
          ))}
          <p className="text-xs text-slate-400 pt-1">
            {data.cached ? "Cached result" : "Freshly generated"} via {data.provider} · {new Date(data.generated_at).toLocaleTimeString()}
          </p>
        </div>
      )}
    </div>
  );
}
