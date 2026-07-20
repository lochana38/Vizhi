import { BrowserRouter, Routes, Route } from "react-router-dom";
import Layout from "./components/Layout";
import OverviewPage from "./pages/OverviewPage";
import SecurityPage from "./pages/SecurityPage";
import PerformancePage from "./pages/PerformancePage";
import UsagePage from "./pages/UsagePage";
import ImportPage from "./pages/ImportPage";
import DrilldownPage from "./pages/DrilldownPage";

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route element={<Layout />}>
          <Route path="/" element={<OverviewPage />} />
          <Route path="/security" element={<SecurityPage />} />
          <Route path="/performance" element={<PerformancePage />} />
          <Route path="/usage" element={<UsagePage />} />
          <Route path="/import" element={<ImportPage />} />
          <Route path="/endpoints/:endpointId" element={<DrilldownPage />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}
