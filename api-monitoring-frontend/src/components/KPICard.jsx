export default function KPICard({ label, value, sublabel, tone = "default" }) {
  const toneClasses = {
    default: "text-slate-900",
    good: "text-emerald-600",
    warning: "text-amber-600",
    critical: "text-red-600",
  };

  return (
    <div className="bg-white rounded-lg border border-slate-200 px-5 py-4">
      <p className="text-xs font-medium text-slate-500 uppercase tracking-wide">{label}</p>
      <p className={`mt-2 text-2xl font-semibold ${toneClasses[tone]}`}>{value}</p>
      {sublabel && <p className="mt-1 text-xs text-slate-400">{sublabel}</p>}
    </div>
  );
}
