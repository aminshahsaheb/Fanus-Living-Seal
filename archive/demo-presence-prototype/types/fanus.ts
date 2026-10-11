export interface FanusResponse {
  input: string
  output: string
  confidence: number
  conflict: number
  seal_state: "stable" | "warning" | "critical"
  reasoning_depth: number
}
