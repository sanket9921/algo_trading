export interface HistoricalSignal {

    signal_type: string;

    strategy_name: string;

    price: number;

    timestamp: number;
}

export async function
fetchHistoricalSignals() {

    const response =
        await fetch(
            "http://127.0.0.1:8000/api/market/signals"
        );

    if (!response.ok) {

        throw new Error(
            "Failed to fetch signals"
        );
    }

    return (
        await response.json()
    ) as HistoricalSignal[];
}