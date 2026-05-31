export interface HistoricalCandle {

    time: number;

    open: number;

    high: number;

    low: number;

    close: number;

    volume: number;
}

interface FetchHistoricalCandlesParams {

    instrumentKey: string;

    timeframe?: string;

    fromDate?: string;

    toDate?: string;
}

export async function
fetchHistoricalCandles(
    params: FetchHistoricalCandlesParams
) {

    const query =
        new URLSearchParams({

            instrument_key:
                params.instrumentKey,

            timeframe:
                params.timeframe ?? "1m",

            ...(params.fromDate && {
                from_date:
                    params.fromDate,
            }),

            ...(params.toDate && {
                to_date:
                    params.toDate,
            }),
        });

    const response =
        await fetch(
            `http://127.0.0.1:8000/api/market/candles?${query.toString()}`
        );

    if (!response.ok) {

        throw new Error(
            "Failed to fetch candles"
        );
    }

    const candles =
    (
        await response.json()
    ) as HistoricalCandle[];

    const uniqueCandles =
        Array.from(
            new Map(
                candles.map(
                    (candle) => [
                        candle.time,
                        candle,
                    ]
                )
            ).values()
        );

    uniqueCandles.sort(
        (a, b) =>
            a.time - b.time
    );

    return uniqueCandles;
}