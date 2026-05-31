"use client";

import { useEffect } from "react";

import { websocketClient } from "@/services/websocket/websocket-client";

import { useMarketStore } from "@/stores/market-store";

export function useMarketStream() {

    const addTick =
        useMarketStore(
            (state) => state.addTick
        );

    const addCandle =
        useMarketStore(
            (state) => state.addCandle
        );

    const addSignal =
        useMarketStore(
            (state) => state.addSignal
        );

    useEffect(() => {

        websocketClient.connect(
            "ws://127.0.0.1:8000/ws/market",

            (message) => {

                const payload =
                    message as {
                        type: string;

                        data: any;
                    };

                // ==========================================
                // Live Tick Stream
                // ==========================================

                if (
                    payload.type ===
                    "tick"
                ) {

                    addTick(
                        payload.data
                    );
                }

                // ==========================================
                // Replay Candle Stream
                // ==========================================

                if (
                    payload.type ===
                    "candle"
                ) {

                    addCandle(
                        payload.data
                    );
                }

                // ==========================================
                // Trading Signals
                // ==========================================

                if (
                    payload.type ===
                    "signal"
                ) {

                    addSignal(
                        payload.data
                    );
                }
            }
        );

        return () => {

            websocketClient.disconnect();
        };

    }, []);
}