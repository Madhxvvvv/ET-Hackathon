/**
 * api.ts — Base API client for the DPSP backend.
 *
 * All fetch wrappers live here. Day 2: replace BASE_URL with the live
 * Render deployment URL via NEXT_PUBLIC_API_URL env var.
 */

const BASE_URL = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000/api/v1";

interface RequestOptions extends RequestInit {
  params?: Record<string, string>;
}

async function request<T>(path: string, options: RequestOptions = {}): Promise<T> {
  const { params, ...init } = options;
  const url = new URL(`${BASE_URL}${path}`);
  if (params) {
    Object.entries(params).forEach(([k, v]) => url.searchParams.set(k, v));
  }
  const res = await fetch(url.toString(), {
    headers: { "Content-Type": "application/json", ...init.headers },
    ...init,
  });
  if (!res.ok) {
    throw new Error(`API ${res.status}: ${res.statusText}`);
  }
  return res.json() as Promise<T>;
}

export const api = {
  get: <T>(path: string, options?: RequestOptions) => request<T>(path, { method: "GET", ...options }),
  post: <T>(path: string, body: unknown, options?: RequestOptions) =>
    request<T>(path, { method: "POST", body: JSON.stringify(body), ...options }),
};

/* ─── Module-specific clients (stubs — filled in Day 2) ─── */

/** POST /currency/detect — returns { label, confidence } */
// eslint-disable-next-line @typescript-eslint/no-unused-vars
export async function detectCurrency(_file: File): Promise<{ label: string; confidence: number }> {
  // TODO Day 2: upload FormData to backend ML endpoint
  throw new Error("Currency detection API not yet integrated.");
}

/** POST /scam-shield/query — returns { answer, sources } */
// eslint-disable-next-line @typescript-eslint/no-unused-vars
export async function queryScamShield(_question: string): Promise<{ answer: string; sources: string[] }> {
  // TODO Day 2: POST to /scam-shield/query and return RAG response
  throw new Error("Scam Shield API not yet integrated.");
}

/** GET /fraud-network/nodes — returns graph data */
export async function getFraudNetwork(): Promise<{ nodes: unknown[]; edges: unknown[] }> {
  // TODO Day 2: fetch Neo4j graph data from backend
  throw new Error("Fraud Network API not yet integrated.");
}
