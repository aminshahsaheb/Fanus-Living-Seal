"use client"
import { motion } from "framer-motion"

type Props = { confidence: number }

export default function Lantern({ confidence }: Props) {
  const scale = 1 + confidence * 0.25
  return (
    <motion.div
      animate={{ scale }}
      transition={{ duration: 1 }}
      className="w-40 h-40 rounded-full bg-yellow-400/40 blur-xl"
    />
  )
}
