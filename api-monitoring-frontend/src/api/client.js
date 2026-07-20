import axios from "axios";

// Change this if your FastAPI backend runs on a different port/host
export const API_BASE_URL = "http://127.0.0.1:8000";

const client = axios.create({
  baseURL: API_BASE_URL,
});

export default client;

// ---- Overview tab ----
export const getKpiCards = () => client.get("/dashboard/kpi-cards").then((r) => r.data);
export const getTrafficTrend = (range = 30) =>
  client.get("/dashboard/traffic-trend", { params: { range } }).then((r) => r.data);
export const getHealthDistribution = () =>
  client.get("/dashboard/health-distribution").then((r) => r.data);
export const getRecentAlerts = (limit = 20) =>
  client.get("/dashboard/recent-alerts", { params: { limit } }).then((r) => r.data);

// ---- Security tab ----
export const getSecurityFindings = (params = {}) =>
  client.get("/security/findings", { params }).then((r) => r.data);
export const getSecuritySummary = () => client.get("/security/summary").then((r) => r.data);
export const resolveSecurityFinding = (findingId) =>
  client.patch(`/security/findings/${findingId}/resolve`).then((r) => r.data);

// ---- Performance tab ----
export const getResponseTimeTrend = (range = 30) =>
  client.get("/performance/response-time-trend", { params: { range } }).then((r) => r.data);
export const getSlowestEndpoints = (limit = 10) =>
  client.get("/performance/slowest-endpoints", { params: { limit } }).then((r) => r.data);
export const getBandwidthUsage = (limit = 10) =>
  client.get("/performance/bandwidth-usage", { params: { limit } }).then((r) => r.data);

// ---- Usage tab ----
export const getTrafficRanking = (limit = 10, order = "desc") =>
  client.get("/usage/traffic-ranking", { params: { limit, order } }).then((r) => r.data);
export const getUnusedEndpoints = (days = 30) =>
  client.get("/usage/unused-endpoints", { params: { days } }).then((r) => r.data);
export const getDuplicateGroups = () => client.get("/duplicates").then((r) => r.data);

// ---- Endpoint drilldown ----
export const getEndpointDrilldown = (endpointId, range = 30) =>
  client.get(`/endpoints/${endpointId}/drilldown`, { params: { range } }).then((r) => r.data);

// ---- Bulk import ----
export const importBulkFile = (file) => {
  const formData = new FormData();
  formData.append("file", file);
  return client
    .post("/bulk-uploads/import", formData, {
      headers: { "Content-Type": "multipart/form-data" },
    })
    .then((r) => r.data);
};

export const getNextActions = (forceRefresh = false) =>
  client.get("/dashboard/next-actions", { params: { force_refresh: forceRefresh } }).then((r) => r.data);

