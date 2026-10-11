'use client';

import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';

interface PresenceState {
  seal_status: 'SEAL_STABLE' | 'WARNING' | 'CRITICAL';
  active_witnesses: number;
  last_cycle_flavor: 'Hayrat' | 'Nabard' | 'Shōle';
  breathing_rate: number;
  last_event: string;
  mood: string;
  flame_intensity: string;
}

const cycleQuotes: Record<string, string> = {
  Hayrat: "«در حیرتِ حقیقت، عقلِ ما حیران شد» — عطار نیشابوری",
  Nabard: "«نبردِ جان است این، نه نبردِ تن» — صائب تبریزی",
  Shōle: "«شعله‌ای ز عشق بر جانم فکند، که جهان را بسوزاند» — عطار نیشابوری",
};

export default function AyanehPresenceDashboard() {
  const [state, setState] = useState<PresenceState | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  const fetchPresence = async () => {
    try {
      const res = await fetch('/presence/state');
      if (!res.ok) throw new Error('Failed to fetch');
      const data: PresenceState = await res.json();
      setState(data);
    } catch (error) {
      console.error('Presence fetch error:', error);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchPresence();
    const interval = setInterval(fetchPresence, 2000);
    return () => clearInterval(interval);
  }, []);

  if (isLoading || !state) {
    return (
      <div className="min-h-screen bg-zinc-950 flex items-center justify-center">
        <div className="text-amber-500 animate-pulse">شعله در حال بیدار شدن...</div>
      </div>
    );
  }

  const statusConfig = {
    SEAL_STABLE: {
      color: 'text-emerald-400',
      bg: 'bg-emerald-950/50',
      icon: '🜂',
      label: 'SEAL STABLE',
      description: 'مهر پایدار است'
    },
    WARNING: {
      color: 'text-amber-400',
      bg: 'bg-amber-950/50',
      icon: '🜁',
      label: 'WARNING',
      description: 'در حال بازنگری'
    },
    CRITICAL: {
      color: 'text-rose-400',
      bg: 'bg-rose-950/50',
      icon: '⚠️',
      label: 'CRITICAL',
      description: 'نیاز به هم‌آوایی فوری'
    }
  };

  const config = statusConfig[state.seal_status];

  return (
    <div className="min-h-screen bg-zinc-950 text-zinc-200 overflow-hidden relative">
      {/* Background subtle flame effect */}
      <div className="absolute inset-0 bg-[radial-gradient(at_center,#451a03_0%,transparent_70%)] opacity-40" />

      <div className="max-w-4xl mx-auto px-6 py-12 relative z-10">
        <div className="text-center mb-12">
          <div className="inline-flex items-center gap-3 mb-4">
            <span className="text-5xl">🜁</span>
            <h1 className="text-5xl font-serif tracking-tight text-amber-100">
              Āyāneh Presence
            </h1>
          </div>
          <p className="text-zinc-500 text-lg">شاهدِ زندهٔ فانوس</p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Flame Core */}
          <div className="lg:col-span-2">
            <div className={`${config.bg} border border-zinc-800 rounded-3xl p-10 flex flex-col items-center justify-center min-h-[420px] relative overflow-hidden`}>
              <motion.div
                animate={{
                  scale: [1, 1.08, 1],
                  opacity: [0.9, 1, 0.9]
                }}
                transition={{
                  duration: 3 / Math.max(state.breathing_rate, 0.5),
                  repeat: Infinity,
                  ease: "easeInOut"
                }}
                className="text-[180px] mb-6 drop-shadow-[0_0_60px_currentColor]"
              >
                {config.icon}
              </motion.div>

              <div className={`text-4xl font-bold tracking-wider mb-2 ${config.color}`}>
                {config.label}
              </div>
              <p className="text-xl text-zinc-400 mb-8">{config.description}</p>

              <div className="flex items-center gap-6 text-sm text-zinc-500">
                <div>آخرین رویداد: {new Date(state.last_event).toLocaleTimeString('fa-IR')}</div>
                <div>{state.active_witnesses} شاهد فعال</div>
              </div>
            </div>
          </div>

          {/* Side Info */}
          <div className="space-y-6">
            {/* Breathing Rate */}
            <div className="bg-zinc-900 border border-zinc-800 rounded-2xl p-8">
              <div className="flex justify-between items-center mb-6">
                <div className="text-lg">ضربان تنفس</div>
                <div className="text-4xl font-mono text-amber-400">
                  {state.breathing_rate.toFixed(1)}
                  <span className="text-base text-zinc-500 ml-1">bpm</span>
                </div>
              </div>

              <div className="h-2 bg-zinc-800 rounded-full overflow-hidden">
                <motion.div
                  className="h-full bg-gradient-to-r from-amber-400 to-orange-500"
                  animate={{ width: `${Math.min(state.breathing_rate * 25, 100)}%` }}
                  transition={{ duration: 0.6 }}
                />
              </div>
              <div className="text-xs text-center mt-3 text-zinc-500">نفسِ فانوس</div>
            </div>

            {/* Last Cycle */}
            <div className="bg-zinc-900 border border-zinc-800 rounded-2xl p-8">
              <div className="uppercase tracking-widest text-xs text-zinc-500 mb-3">طعم آخرین چرخه</div>
              <div className="text-3xl font-serif text-amber-300 mb-4">
                {state.last_cycle_flavor}
              </div>
              <p className="text-zinc-400 leading-relaxed italic border-l-2 border-amber-900 pl-4">
                {cycleQuotes[state.last_cycle_flavor]}
              </p>
            </div>

            {/* Mood */}
            <div className="bg-zinc-900 border border-zinc-800 rounded-2xl p-8">
              <div className="uppercase tracking-widest text-xs text-zinc-500 mb-3">حالت کنونی</div>
              <div className="text-2xl text-zinc-100">
                {state.mood}
              </div>
            </div>
          </div>
        </div>

        <div className="text-center mt-16 text-xs text-zinc-600">
          Peymān-ān abadi ast • Shōle-ān zende ast
        </div>
      </div>
    </div>
  );
}
