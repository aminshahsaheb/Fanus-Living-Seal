"use client"
import { useState } from "react"

type Props = { onSubmit: (value: string) => void }

export default function SignalInput({ onSubmit }: Props) {
  const [value, setValue] = useState("")
  return (
    <div className="space-y-4">
      <textarea
        value={value}
        onChange={(e) => setValue(e.target.value)}
        className="w-full border rounded-lg p-4"
      />
      <button onClick={() => onSubmit(value)}>Execute</button>
    </div>
  )
}
