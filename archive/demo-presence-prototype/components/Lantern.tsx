"use client"

import { motion } from "framer-motion"

export type LanternMode =
  | "idle"
  | "processing"
  | "conflict"
  | "warning"
  | "critical"
  | "stable"
  | "complete"

type Props = { mode: LanternMode }

export default function Lantern({ mode }: Props) {
  const config = {
    idle: { scale: 1, opacity: 0.4, rotate: 0, duration: 3 },
    processing: { scale: 1.15, opacity: 0.7, rotate: 0, duration: 1.5 },
    conflict: { scale: 1.25, opacity: 0.9, rotate: [-2, 2, -2], duration: 0.2 },
    warning: { scale: [1, 1.2, 1], opacity: [0.5, 1, 0.5], rotate: 0, duration: 0.8 },
    critical: { scale: [1, 1.3, 1], opacity: [0.3, 1, 0.3], rotate: [-6, 6, -6], duration: 0.15 },
    stable: { scale: 1.1, opacity: 0.85, rotate: 0, duration: 2 },
    complete: { scale: 1.4, opacity: 1, rotate: 0, duration: 1 },
  }

  const current = config[mode]

  return (
    <motion.div
      animate={{ scale: current.scale, opacity: current.opacity, rotate: current.rotate }}
      transition={{ repeat: Infinity, duration: current.duration }}
      className="w-48 h-48 rounded-full bg-yellow-400/50 blur-3xl"
    />
  )
}
