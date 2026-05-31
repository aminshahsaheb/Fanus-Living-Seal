"use client"

import { motion } from "framer-motion"

const nodes = ["INPUT", "GATE", "FILTER", "RFC", "ENGINE", "SEAL", "OUTPUT"]

type Props = { activeNode?: string }

export default function Pipeline({ activeNode }: Props) {
  return (
    <div className="flex gap-4 flex-wrap justify-center">
      {nodes.map((n, i) => (
        <motion.div
          key={n}
          initial={{ opacity: 0.3 }}
          animate={{ opacity: activeNode === n ? 1 : [0.3, 1, 0.3] }}
          transition={{ repeat: Infinity, duration: 2, delay: i * 0.2 }}
          className={`border px-4 py-2 rounded-xl ${activeNode === n ? "border-yellow-400 bg-yellow-400/20" : "border-white/20"}`}
        >
          {n}
        </motion.div>
      ))}
    </div>
  )
}
