export interface TickData {
  instrumentKey: string;
  lastPrice: number;
  timestamp: string;
}

export interface CandleData {
  time: any;
  instrumentKey: string;

  timeframe: string;

  open: number;

  high: number;

  low: number;

  close: number;

  volume: number;

  startTime: string;

  endTime: string;
}

export interface SignalData {
  instrumentKey: string;

  signalType: "BUY" | "SELL";

  strategyName: string;

  price: number;

  timestamp: string;
}