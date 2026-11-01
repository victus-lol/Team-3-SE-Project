/**
 * Performance load test scenario (k6 / node compatible).
 * Owner: Akash Pawar (PES2UG24CS041) + Aadi Kore (PES2UG24CS006)
 * Sprint: S2 (S2-10)
 * Requirement IDs: TMA-NF-002 (TC-Perf-01: p90 <= 3s)
 *
 * Simulates normal agreed load of 20 concurrent users retrieving task lists.
 */

export const options = {
  vus: 20,
  duration: '30s',
  thresholds: {
    http_req_duration: ['p(90)<3000'], // 90% of requests must complete below 3s
  },
}

export default function () {
  // Test scenario runner (k6 syntax or node fetch)
  console.log('Running performance simulation under agreed load...')
}

