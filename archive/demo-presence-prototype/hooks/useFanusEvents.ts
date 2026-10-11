"use client"

import { useEffect } from "react"

export function useFanusEvents(
  executionId: string,
  onEvent: (type: string, payload: any) => void
) {
  useEffect(() => {
    if (!executionId) return

    const source = new EventSource(`/api/v1/executions/${executionId}/events`)

    source.onmessage = (event) => {
      const data = JSON.parse(event.data)
      onEvent(data.type, data.payload)
    }

    source.onerror = () => {
      source.close()
    }

    return () => {
      source.close()
    }
  }, [executionId])
}
