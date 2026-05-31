import { create } from "zustand";

import {
  CandleData,
  SignalData,
  TickData,
} from "@/types/market";

interface MarketStore {

  ticks: TickData[];

  candles: CandleData[];

  signals: SignalData[];

  currentTimeframe: string;

  // ==========================================
  // Tick Actions
  // ==========================================

  addTick: (
    tick: TickData
  ) => void;

  // ==========================================
  // Candle Actions
  // ==========================================

  setCandles: (
    candles: CandleData[]
  ) => void;

  addCandle: (
    candle: CandleData
  ) => void;

  clearCandles: () => void;

  setTimeframe: (
    timeframe: string
  ) => void;

  // ==========================================
  // Signal Actions
  // ==========================================

  addSignal: (
    signal: SignalData
  ) => void;

  setSignals: (
    signals: SignalData[]
  ) => void;

  clearSignals: () => void;
}

export const useMarketStore =
  create<MarketStore>(
    (set) => ({

      // ==========================================
      // State
      // ==========================================

      ticks: [],

      candles: [],

      signals: [],

      currentTimeframe: "1m",

      // ==========================================
      // Tick Updates
      // ==========================================

      addTick: (tick) =>

        set((state) => ({

          ticks: [
            ...state.ticks.slice(-200),
            tick,
          ],
        })),

      // ==========================================
      // Historical Candle Preload
      // ==========================================

      setCandles: (
        candles
      ) =>

        set({

          candles:
            [...candles].sort(
              (a, b) =>
                a.time - b.time
            ),
        }),

      // ==========================================
      // Live / Replay Candle Updates
      // ==========================================

      addCandle: (candle) =>

        set((state) => {

          const existingIndex =
            state.candles.findIndex(
              (existing) =>
                existing.time
                ===
                candle.time
            );

          // ======================================
          // Replace Existing Candle
          // ======================================

          if (
            existingIndex !== -1
          ) {

            const updated =
              [...state.candles];

            updated[
              existingIndex
            ] = candle;

            return {
              candles: updated,
            };
          }

          // ======================================
          // Append New Candle
          // ======================================

          return {

            candles: [

              ...state.candles,

              candle,

            ].sort(
              (a, b) =>
                a.time - b.time
            ),
          };
        }),

      clearCandles: () =>

        set({
          candles: [],
        }),

      setTimeframe: (
        timeframe
      ) =>

        set({
          currentTimeframe:
            timeframe,
        }),

      // ==========================================
      // Signal Updates
      // ==========================================

      addSignal: (signal) =>

        set((state) => ({

          signals: [
            ...state.signals,
            signal,
          ],
        })),

      setSignals: (
        signals
      ) => set({
        signals,
      }),

      clearSignals: () =>

        set({
          signals: [],
        }),
    })
  );