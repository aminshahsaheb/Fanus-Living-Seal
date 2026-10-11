"use client"

import { useState } from "react"
import Lantern, { LanternMode } from "@/components/Lantern"
import Pipeline from "@/components/Pipeline"
import SignalInput from "@/components/SignalInput"
import SealPanel from "@/components/SealPanel"
import { useFanusEvents } from "@/hooks/useFanusEvents"

export default function Home() {
  const [executionId, setExecutionId] = useState("")
  const [lanternMode, setLanternMode] = useState<LanternMode>("idle")
  const [activeNode, setActiveNode] = useState("INPUT")
  const [result, setResult] = useState<any>(null)

  useFanusEvents(executionId, (type, payload) => {
    switch (type) {
      case "RFC_START":
        setActiveNode("RFC")
        setLanternMode("processing")
        break
      case "CONFLICT_DETECTED":
        setLanternMode("conflict")
        break
      case "SEAL_WARNING":
        setLanternMode("warning")
        break
      case "SEAL_CRITICAL":
        setLanternMode("critical")
        break
      case "SEAL_STABLE":
        setActiveNode("SEAL")
        setLanternMode("stable")
        break
      case "OUTPUT_READY":
        setActiveNode("OUTPUT")
        setLanternMode("complete")
        break
    }
  })

  async function execute(signal: string) {
    const res = await fetch("/api/v1/execute", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ signal }),
    })
    const data = await res.json()
    setExecutionId(data.execution_id)
  }

  return (
    <main className="min-h-screen bg-black text-white p-12 space-y-12">
      <div className="flex flex-col items-center">
        <Lantern mode={lanternMode} />
        <h1 className="text-5xl mt-6">Fanus</h1>
        <p>Living Seal</p>
      </div>

      <Pipeline activeNode={activeNode} />

      <SignalInput onSubmit={execute} />

      {result && (
        <SealPanel confidence={result.confidence} conflict={result.conflict} sealState={result.seal_state} />
      )}
    </main>
  )
}
