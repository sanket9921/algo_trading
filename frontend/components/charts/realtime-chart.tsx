"use client";

import {
    useEffect,
    useRef,
    useState,
} from "react";

import {
    CandlestickData,
    CandlestickSeries,
    ColorType,
    createChart,
    IChartApi,
    ISeriesApi,
    UTCTimestamp,
} from "lightweight-charts";

import {
    fetchHistoricalCandles,
} from "@/services/api/market-api";

import {
    useMarketStore,
} from "@/stores/market-store";

const INSTRUMENT_KEY =
    "NSE_INDEX|Nifty 50";

const TIMEFRAMES = [
    "1m",
    "5m",
    "15m",
];

export function TradingChart() {

    const chartContainerRef =
        useRef<HTMLDivElement | null>(
            null
        );

    const chartRef =
        useRef<IChartApi | null>(
            null
        );

    const candleSeriesRef =
        useRef<
            ISeriesApi<"Candlestick">
            | null
        >(null);

    const candles =
        useMarketStore(
            (state) =>
                state.candles
        );

    const setCandles =
        useMarketStore(
            (state) =>
                state.setCandles
        );

    const currentTimeframe =
        useMarketStore(
            (state) =>
                state.currentTimeframe
        );

    const setTimeframe =
        useMarketStore(
            (state) =>
                state.setTimeframe
        );

    const [
        loading,
        setLoading,
    ] = useState(false);

    // =====================================================
    // Create Chart
    // =====================================================

    useEffect(() => {

        if (
            !chartContainerRef.current
        ) {
            return;
        }

        const chart =
            createChart(
                chartContainerRef.current,
                {

                    layout: {

                        background: {

                            type:
                                ColorType
                                    .Solid,

                            color:
                                "#0f172a",
                        },

                        textColor:
                            "#cbd5e1",
                    },

                    grid: {

                        vertLines: {

                            color:
                                "#1e293b",
                        },

                        horzLines: {

                            color:
                                "#1e293b",
                        },
                    },

                    timeScale: {

                        timeVisible:
                            true,

                        secondsVisible:
                            false,

                        borderColor:
                            "#334155",

                        tickMarkFormatter:
                            (
                                time: number
                            ) => {

                                return new Date(
                                    time * 1000
                                ).toLocaleTimeString(
                                    "en-IN",
                                    {

                                        timeZone:
                                            "Asia/Kolkata",

                                        hour:
                                            "2-digit",

                                        minute:
                                            "2-digit",

                                        hour12:
                                            false,
                                    }
                                );
                            },
                    },

                    localization: {

                        locale:
                            "en-IN",
                    },

                    width:
                        chartContainerRef
                            .current
                            .clientWidth,

                    height: 600,
                }
            );

        const candleSeries =
            chart.addSeries(
                CandlestickSeries,
                {}
            );

        chartRef.current =
            chart;

        candleSeriesRef.current =
            candleSeries;

        chart.timeScale().fitContent();

        const handleResize =
            () => {

                if (
                    !chartContainerRef.current
                ) {
                    return;
                }

                chart.applyOptions({

                    width:
                        chartContainerRef
                            .current
                            .clientWidth,
                });
            };

        window.addEventListener(
            "resize",
            handleResize
        );

        return () => {

            window.removeEventListener(
                "resize",
                handleResize
            );

            chart.remove();
        };

    }, []);

    // =====================================================
    // Load Historical Candles
    // =====================================================

    useEffect(() => {

        async function loadCandles() {

            try {

                setLoading(true);

                const historical =
                    await fetchHistoricalCandles({

                        instrumentKey:
                            INSTRUMENT_KEY,

                        timeframe:
                            currentTimeframe,
                    });

                setCandles(
                    historical
                );

            } catch (error) {

                console.error(
                    "Failed to load candles",
                    error
                );

            } finally {

                setLoading(false);
            }
        }

        loadCandles();

    }, [
        currentTimeframe,
        setCandles,
    ]);

    // =====================================================
    // Sync Candles To Chart
    // =====================================================

    useEffect(() => {

        if (
            !candleSeriesRef.current
        ) {
            return;
        }

        if (
            candles.length === 0
        ) {
            return;
        }

        const formattedCandles:
            CandlestickData<UTCTimestamp>[] =

            candles.map(
                (candle) => {

                    const utcTime =
                        candle.time as UTCTimestamp;

                    return {

                        time:
                            utcTime,

                        open:
                            candle.open,

                        high:
                            candle.high,

                        low:
                            candle.low,

                        close:
                            candle.close,
                    };
                }
            );

        candleSeriesRef.current.setData(
            formattedCandles
        );

        chartRef.current
            ?.timeScale()
            .fitContent();

    }, [candles]);

    return (

        <div className="w-full">

            {/* ====================================== */}
            {/* Header */}
            {/* ====================================== */}

            <div
                className="
                    mb-4
                    flex
                    items-center
                    justify-between
                "
            >

                <div>

                    <h2
                        className="
                            text-xl
                            font-semibold
                            text-white
                        "
                    >
                        NIFTY 50
                    </h2>

                    <p
                        className="
                            text-sm
                            text-slate-400
                        "
                    >
                        Historical +
                        Live Market Data
                    </p>

                </div>

                {/* ================================== */}
                {/* Timeframe Switch */}
                {/* ================================== */}

                <div
                    className="
                        flex
                        gap-2
                    "
                >

                    {TIMEFRAMES.map(
                        (timeframe) => (

                            <button
                                key={
                                    timeframe
                                }

                                onClick={
                                    () =>
                                        setTimeframe(
                                            timeframe
                                        )
                                }

                                className={`
                                    rounded-lg
                                    px-4
                                    py-2
                                    text-sm
                                    font-medium
                                    transition-all

                                    ${
                                        currentTimeframe
                                        ===
                                        timeframe

                                            ? `
                                                bg-blue-600
                                                text-white
                                            `

                                            : `
                                                bg-slate-800
                                                text-slate-300
                                                hover:bg-slate-700
                                            `
                                    }
                                `}
                            >
                                {timeframe}
                            </button>
                        )
                    )}

                </div>
            </div>

            {/* ====================================== */}
            {/* Loading */}
            {/* ====================================== */}

            {loading && (

                <div
                    className="
                        mb-4
                        text-sm
                        text-slate-400
                    "
                >
                    Loading candles...
                </div>
            )}

            {/* ====================================== */}
            {/* Chart */}
            {/* ====================================== */}

            <div
                ref={
                    chartContainerRef
                }

                className="
                    w-full
                    overflow-hidden
                    rounded-2xl
                    border
                    border-slate-800
                "
            />
        </div>
    );
}