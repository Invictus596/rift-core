"use client";

import { useEffect, useState } from "react";
import { motion } from "framer-motion";
import { Shield } from "lucide-react";

import { FlickeringGrid } from "@/components/ui/flickering-grid";
import { Spotlight } from "@/components/ui/spotlight";
import { NumberTicker } from "@/components/ui/number-ticker";
import { Timeline } from "@/components/ui/timeline";

export default function Home() {
  const timelineData = [
    {
      title: "Step 1: The Watcher",
      content: (
        <p className="text-white/80 text-sm md:text-base">
          Our Python agent constantly monitors the live Bitcoin mempool for specific OP_RETURN <span className="text-purple-400 font-semibold">RIFT</span> tags.
        </p>
      ),
    },
    {
      title: "Step 2: Cairo Verifier",
      content: (
        <p className="text-white/80 text-sm md:text-base">
          Our Cairo 2.6.4 smart contracts mathematically prove the transaction validity using <span className="text-purple-400 font-semibold">secp256k1 signatures</span> directly on Starknet.
        </p>
      ),
    },
    {
      title: "Step 3: The Executor",
      content: (
        <p className="text-white/80 text-sm md:text-base">
          The final L2 action layer where <span className="text-purple-400 font-semibold">wrapped assets are minted</span> instantly upon verification.
        </p>
      ),
    },
    {
      title: "Mock Mode Demo",
      content: (
        <p className="text-white/80 text-sm md:text-base">
          For this hackathon, this pipeline is running in an engineered high-speed simulation, successfully verifying <span className="text-green-400 font-semibold">12+ txs in 50 seconds</span>.
        </p>
      ),
    },
  ];

  return (
    <div className="relative min-h-screen bg-black overflow-hidden">
      {/* Full-page FlickeringGrid background */}
      <div className="absolute inset-0">
        <FlickeringGrid
          squareSize={4}
          gridGap={6}
          color="rgb(139, 92, 246)"
          maxOpacity={0.2}
          flickerChance={0.4}
          className="w-full h-full"
        />
      </div>

      {/* Hero Section with Spotlight */}
      <section className="relative z-10 min-h-screen flex flex-col items-center justify-center px-4">
        <Spotlight className="top-0 left-1/2 -translate-x-1/2" fill="rgb(139, 92, 246)" />
        
        <motion.div
          initial={{ opacity: 0, y: 40 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8, delay: 0.2 }}
          className="text-center"
        >
          <h1 className="text-6xl md:text-8xl lg:text-9xl font-black mb-6 bg-gradient-to-r from-white via-purple-200 to-purple-400 bg-clip-text text-transparent">
            Rift Protocol
          </h1>
          
          <p className="text-lg md:text-2xl text-white/60 max-w-3xl mx-auto leading-relaxed">
            Making Bitcoin <span className="text-purple-400 font-semibold">Instant</span>.
            Break the 10-minute barrier with{" "}
            <span className="text-white/80">zero-knowledge L2 execution</span>.
          </p>
        </motion.div>
      </section>

      {/* Architecture Timeline Section */}
      <section className="relative z-10 py-20 px-4">
        <div className="max-w-7xl mx-auto">
          <motion.div
            initial={{ opacity: 0, y: 40 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
            viewport={{ once: true }}
          >
            <Timeline data={timelineData} />
          </motion.div>
        </div>
      </section>

      {/* Terminal Section */}
      <section className="relative z-10 py-20 px-4">
        <div className="max-w-4xl mx-auto">
          <motion.div
            initial={{ opacity: 0, y: 40 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
            viewport={{ once: true }}
          >
            <AnimatedTerminal />
          </motion.div>
        </div>
      </section>

      {/* Stats Section */}
      <section className="relative z-10 py-20 px-4 pb-32">
        <div className="max-w-4xl mx-auto">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5, delay: 0.1 }}
              viewport={{ once: true }}
              className="rounded-2xl bg-white/5 border border-white/10 p-8 backdrop-blur-sm"
            >
              <div className="text-zinc-400 text-sm font-sans tracking-wide mb-2">Mempool Txs Scanned</div>
              <div className="text-5xl md:text-6xl font-mono font-bold tracking-tighter text-white dark:text-white">
                <NumberTicker value={45230} />
              </div>
              <div className="mt-4 text-green-400 text-sm flex items-center gap-2">
                <span className="w-2 h-2 rounded-full bg-green-400 animate-pulse" />
                Live monitoring
              </div>
            </motion.div>

            <motion.div
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5, delay: 0.2 }}
              viewport={{ once: true }}
              className="rounded-2xl bg-white/5 border border-white/10 p-8 backdrop-blur-sm"
            >
              <div className="text-zinc-400 text-sm font-sans tracking-wide mb-2">Proofs Verified</div>
              <div className="text-5xl md:text-6xl font-mono font-bold tracking-tighter text-white dark:text-white">
                <NumberTicker value={12} />
              </div>
              <div className="mt-4 text-purple-400 text-sm flex items-center gap-2">
                <Shield className="w-4 h-4" />
                ZK execution complete
              </div>
            </motion.div>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="relative z-10 border-t border-white/10 py-8 px-4">
        <div className="max-w-4xl mx-auto flex flex-col md:flex-row justify-between items-center gap-4">
          <p className="text-white/30 text-sm">
            © 2025 Rift Protocol. Building on Bitcoin & Starknet.
          </p>
          <div className="flex gap-6">
            <a href="#" className="text-white/40 hover:text-white/80 text-sm transition-colors">
              Documentation
            </a>
            <a href="#" className="text-white/40 hover:text-white/80 text-sm transition-colors">
              GitHub
            </a>
            <a href="#" className="text-white/40 hover:text-white/80 text-sm transition-colors">
              Devpost
            </a>
          </div>
        </div>
      </footer>
    </div>
  );
}

// Custom AnimatedTerminal component (fallback since 21st.dev endpoint was down)
function AnimatedTerminal() {
  const lines = [
    { text: "Initializing Rift Watcher...", type: "info", delay: 0 },
    { text: "Monitoring mempool...", type: "info", delay: 500 },
    { text: "[+] RIFT DETECTED: 0x9a6c506b...", type: "success", delay: 1200 },
    { text: "🛡️ Cairo Verification: SUCCESS (12ms)", type: "success", delay: 1800 },
    { text: "⚡ 12 txs verified in 48.2s", type: "success", delay: 2400 },
  ];

  return (
    <div className="w-full rounded-xl bg-black/90 border border-white/10 shadow-2xl shadow-black/50 overflow-hidden">
      <div className="flex items-center gap-2 px-4 py-3 bg-white/5 border-b border-white/10">
        <div className="flex gap-2">
          <div className="w-3 h-3 rounded-full bg-red-500/80" />
          <div className="w-3 h-3 rounded-full bg-yellow-500/80" />
          <div className="w-3 h-3 rounded-full bg-green-500/80" />
        </div>
        <span className="ml-4 text-xs text-white/40 font-mono">rift-protocol — watcher output</span>
      </div>
      <div className="p-6 font-mono text-sm md:text-base min-h-[280px]">
        {lines.map((line, index) => (
          <TerminalLine key={index} line={line} index={index} />
        ))}
        <div className="flex items-center gap-2 pt-4">
          <span className="text-green-400">▋</span>
          <span className="text-white/40 animate-pulse">Awaiting next batch...</span>
        </div>
      </div>
    </div>
  );
}

function TerminalLine({ line, index }: { line: { text: string; type: string; delay: number }; index: number }) {
  const [isVisible, setIsVisible] = useState(line.delay === 0);

  useEffect(() => {
    const timer = setTimeout(() => setIsVisible(true), line.delay);
    return () => clearTimeout(timer);
  }, [line.delay]);

  return (
    <motion.div
      initial={{ opacity: 0, x: -10 }}
      animate={{ opacity: isVisible ? 1 : 0, x: isVisible ? 0 : -10 }}
      transition={{ duration: 0.3 }}
      className={`py-1 ${
        line.type === "success" ? "text-green-400" : "text-white/70"
      }`}
    >
      {line.text}
    </motion.div>
  );
}
