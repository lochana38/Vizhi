const styles = {
  high: "bg-red-50 text-red-700 border-red-200",
  medium: "bg-amber-50 text-amber-700 border-amber-200",
  low: "bg-slate-100 text-slate-600 border-slate-200",
};

export default function SeverityBadge({ severity }) {
  const cls = styles[severity] || styles.low;
  return (
    <span className={`inline-block px-2 py-0.5 rounded-full text-xs font-medium border ${cls}`}>
      {severity}
    </span>
  );
}
