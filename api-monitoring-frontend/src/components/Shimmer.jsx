export function ShimmerBlock({ className = "" }) {
  return <div className={`shimmer rounded-md ${className}`} />;
}

export function ShimmerCardGrid({ count = 4 }) {
  return (
    <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
      {Array.from({ length: count }).map((_, i) => (
        <ShimmerBlock key={i} className="h-24" />
      ))}
    </div>
  );
}
