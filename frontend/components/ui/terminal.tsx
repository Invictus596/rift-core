"use client";

import { useEffect, useRef, useState } from "react";
import { cn } from "@/lib/utils";

interface TerminalLine {
  text: string;
  type: "info" | "success" | "warning";
  timestamp: string;
}

export function Terminal({ className }: { className?: string }) {
  const [lines, setLines] = useState<TerminalLine[]>([]);
  const scrollRef = useRef<HTMLDivElement>(null);

  const getTimestamp = () => {
    return new Date().toLocaleTimeString("en-US", {
      hour12: false,
      hour: "2-digit",
      minute: "2-digit",
      second: "2-digit",
      fractionalSecondDigits: 3,
    });
  };

  const addLine = (text: string, type: "info" | "success" | "warning" = "info") => {
    setLines((prev) => [...prev.slice(-50), { text, type, timestamp: getTimestamp() }]);
  };

  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [lines]);

  useEffect(() => {
    const riftTags = [
      "RIFT:STARKNET_DEPOSIT",
      "RIFT:ZK_PROOF_SUBMIT",
      "RIFT:BTC_LOCK",
      "RIFT:EXECUTION_REQ",
      "RIFT:STATE_UPDATE",
    ];

    const btcAddresses = [
      "bc1qxy2kgdygjrsqtzq2n0yrf2493p83kkfjhx0wlh",
      "bc1qar0srrr7xfkvy5l643lydnw9re59gtzzwf5mdq",
      "bc1q34aq5drpuwy3wgl9lhup9892qp6svr8ldzyy7c",
      "bc1qeklem3cn0th0w6avdhxguec6hxq5j5q8y8z7xh",
    ];

    const txIds = [
      "a1b2c3d4e5f6...",
      "f6e5d4c3b2a1...",
      "9f8e7d6c5b4a...",
      "4a5b6c7d8e9f...",
      "1a2b3c4d5e6f...",
    ];

    let phase = "init";
    let txCount = 0;
    const maxTxs = 15;

    const runSimulation = async () => {
      await sleep(500);
      addLine("Initializing Rift Protocol mempool monitor...", "info");

      await sleep(300);
      addLine("Connecting to Bitcoin node (testnet)...", "info");

      await sleep(400);
      addLine("Connected. Monitoring mempool for RIFT tags...", "success");

      await sleep(500);
      phase = "scanning";

      while (txCount < maxTxs) {
        await sleep(Math.random() * 2000 + 500);

        const address = btcAddresses[Math.floor(Math.random() * btcAddresses.length)];
        const txId = txIds[Math.floor(Math.random() * txIds.length)];
        const riftTag = riftTags[Math.floor(Math.random() * riftTags.length)];
        const amount = (Math.random() * 2 + 0.1).toFixed(4);

        addLine(`[MEMPOOL] New tx detected: ${txId}`, "info");
        addLine(`  From: ${address.slice(0, 16)}...`, "info");
        addLine(`  Amount: ${amount} BTC`, "info");

        await sleep(150);

        if (Math.random() > 0.3) {
          addLine(`  ⚡ RIFT TAG DETECTED: ${riftTag}`, "success");
          addLine(`  → Queuing for ZK proof generation`, "success");
          txCount++;
        } else {
          addLine(`  No RIFT tag - skipping`, "warning");
        }

        addLine("", "info");

        if (txCount >= 8 && phase === "scanning") {
          phase = "processing";
          addLine("━━━ ZK PROOF BATCH PROCESSING ━━━", "success");
        }
      }

      await sleep(800);
      addLine(`━━━ DEMO COMPLETE ━━━`, "success");
      addLine(`Detected ${maxTxs} RIFT transactions in ~50 seconds`, "success");
      addLine(`Ready for Starknet execution layer...`, "info");
    };

    runSimulation();
  }, []);

  return (
    <div
      className={cn(
        "relative w-full h-full min-h-[400px] rounded-xl overflow-hidden",
        "bg-black/90 border border-white/10",
        "shadow-2xl shadow-black/50",
        "font-mono text-sm",
        className
      )}
    >
      <div className="flex items-center gap-2 px-4 py-3 bg-white/5 border-b border-white/10">
        <div className="flex gap-2">
          <div className="w-3 h-3 rounded-full bg-red-500/80" />
          <div className="w-3 h-3 rounded-full bg-yellow-500/80" />
          <div className="w-3 h-3 rounded-full bg-green-500/80" />
        </div>
        <span className="ml-4 text-xs text-white/40">rift-protocol — mempool monitor</span>
      </div>

      <div
        ref={scrollRef}
        className="h-[calc(100%-48px)] overflow-y-auto p-4 space-y-1 scrollbar-thin scrollbar-thumb-white/10 scrollbar-track-transparent"
      >
        {lines.map((line, i) => (
          <div key={i} className="flex gap-3">
            <span className="text-white/30 shrink-0">[{line.timestamp}]</span>
            <span
              className={cn(
                line.type === "success" && "text-green-400",
                line.type === "warning" && "text-yellow-400/80",
                line.type === "info" && "text-white/70"
              )}
            >
              {line.text || "\u00A0"}
            </span>
          </div>
        ))}
        <div className="flex items-center gap-2 pt-2">
          <span className="text-green-400">▋</span>
          <span className="text-white/40 animate-pulse">Listening for mempool transactions...</span>
        </div>
      </div>
    </div>
  );
}

function sleep(ms: number) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}
