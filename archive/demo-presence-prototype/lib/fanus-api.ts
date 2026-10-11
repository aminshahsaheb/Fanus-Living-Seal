import { FanusResponse } from "@/types/fanus"

const ENGINE_URL = process.env.NEXT_PUBLIC_ENGINE_URL || "http://localhost:8000"

export async function runFanus(signal: string): Promise<FanusResponse> {
  const res = await fetch(`${ENGINE_URL}/execute`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ signal }),
  })
  if (!res.ok) throw new Error("Fanus Engine unavailable")
  return res.json()
}
