"use client";

import { TradingChart } from "@/components/charts/realtime-chart";

import { useMarketStream } from "@/hooks/use-market-stream";

export default function HomePage() {

  useMarketStream();

  return (
    <main className="p-4">

      <h1 className="mb-4 text-3xl font-bold">
        Algo Trading Workstation
      </h1>

      <TradingChart />

    </main> 
  );
}