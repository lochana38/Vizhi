import { NavLink, Outlet } from "react-router-dom";

const navItems = [
  { to: "/", label: "Overview", end: true },
  { to: "/security", label: "Security" },
  { to: "/performance", label: "Performance" },
  { to: "/usage", label: "Usage" },
  { to: "/import", label: "Import Data" },
];

export default function Layout() {
  return (
    <div className="min-h-screen flex bg-slate-50">
      <aside className="w-60 shrink-0 bg-slate-950 text-slate-300 flex flex-col">
        <div className="px-5 py-6 border-b border-slate-800">
          <p className="text-white font-semibold tracking-tight">API Monitor</p>
          <p className="text-xs text-slate-500 mt-0.5">Endpoint health &amp; risk</p>
        </div>
        <nav className="flex-1 px-3 py-4 space-y-1">
          {navItems.map((item) => (
            <NavLink
              key={item.to}
              to={item.to}
              end={item.end}
              className={({ isActive }) =>
                `block rounded-md px-3 py-2 text-sm font-medium transition-colors ${
                  isActive
                    ? "bg-slate-800 text-white"
                    : "text-slate-400 hover:bg-slate-900 hover:text-slate-200"
                }`
              }
            >
              {item.label}
            </NavLink>
          ))}
        </nav>
      </aside>

      <main className="flex-1 min-w-0">
        <div className="max-w-7xl mx-auto px-8 py-8">
          <Outlet />
        </div>
      </main>
    </div>
  );
}
