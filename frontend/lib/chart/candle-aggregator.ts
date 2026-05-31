import { ChartCandle } from "@/types/chart";

interface TickData {
  lastPrice: number;

  timestamp: string;
}

export class CandleAggregator {
  private currentCandle:
    | ChartCandle
    | null = null;

  update(
    tick: TickData
  ): ChartCandle {

    const tickDate =
      new Date(
        tick.timestamp
      );

    const candleTime =
      Math.floor(
        tickDate.getTime() /
          60000
      ) * 60;

    if (
      !this.currentCandle ||
      this.currentCandle.time !==
        candleTime
    ) {

      this.currentCandle = {
        time: candleTime,

        open:
          tick.lastPrice,

        high:
          tick.lastPrice,

        low:
          tick.lastPrice,

        close:
          tick.lastPrice,
      };

      return this.currentCandle;
    }

    this.currentCandle.high =
      Math.max(
        this.currentCandle.high,
        tick.lastPrice
      );

    this.currentCandle.low =
      Math.min(
        this.currentCandle.low,
        tick.lastPrice
      );

    this.currentCandle.close =
      tick.lastPrice;

    return this.currentCandle;
  }
}