// Small reusable renderer for an endpoint's method + path, styled consistently
// wherever it appears across the dashboard (tables, cards, drilldown header).
export default function EndpointPath({ method, path }) {
  const methodColors = {
    GET: "text-blue-600",
    POST: "text-emerald-600",
    PUT: "text-amber-600",
    PATCH: "text-amber-600",
    DELETE: "text-red-600",
  };

  return (
    <span className="font-mono-path text-sm">
      <span className={`font-semibold ${methodColors[method] || "text-slate-600"}`}>{method}</span>{" "}
      <span className="text-slate-700">{path}</span>
    </span>
  );
}
