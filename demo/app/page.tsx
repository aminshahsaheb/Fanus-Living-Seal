"use client"
import { useState } from "react"
import Lantern from "@/components/Lantern"
import Pipeline from "@/components/Pipeline"
import SignalInput from "@/components/SignalInput"
import SealPanel from "@/components/SealPanel"
import { runFanus } from "@/lib/fanus-api"

export default function Home() {
  const [result, setResult] = useState<any>(null)

  async function execute(signal: string) {
    const res = await runFanus(signal)
    setResult(res)
  }

  return (
    <main className="min-h-screen bg-black text-white p-12 space-y-12">
      <div className="flex flex-col items-center">
        <Lantern confidence={result?.confidence ?? 0.5} />
        <h1 className="text-5xl mt-6">Fanus</h1>
        <p>Living Seal</p>
      </div>
      <Pipeline />
      <SignalInput onSubmit={execute} />
      {result && (
        <SealPanel confidence={result.confidence} conflict={result.conflict} sealState={result.seal_state} />
      )}
    </main>
  )
}
