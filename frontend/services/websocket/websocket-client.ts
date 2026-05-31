type MessageHandler = (
  data: unknown
) => void;

class WebSocketClient {
  private socket:
    | WebSocket
    | null = null;

  private reconnectTimer:
    | NodeJS.Timeout
    | null = null;

  connect(
    url: string,
    onMessage: MessageHandler
  ) {
    this.socket =
      new WebSocket(url);

    this.socket.onopen = () => {
      console.log(
        "WebSocket connected"
      );
    };

    this.socket.onmessage = (
      event
    ) => {
      try {
        const parsed =
          JSON.parse(
            event.data
          );

        onMessage(parsed);

      } catch (error) {
        console.error(
          "WebSocket parse error",
          error
        );
      }
    };

    this.socket.onclose = () => {
      console.log(
        "WebSocket disconnected"
      );

      this.reconnectTimer =
        setTimeout(() => {
          this.connect(
            url,
            onMessage
          );
        }, 3000);
    };

    this.socket.onerror = (
      error
    ) => {
      console.error(
        "WebSocket error",
        error
      );
    };
  }

  disconnect() {
    if (this.reconnectTimer) {
      clearTimeout(
        this.reconnectTimer
      );
    }

    this.socket?.close();
  }
}

export const websocketClient =
  new WebSocketClient();