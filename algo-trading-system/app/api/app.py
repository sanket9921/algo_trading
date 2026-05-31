import asyncio

from contextlib import (
    asynccontextmanager,
)

from fastapi import (
    FastAPI,
    WebSocket,
    WebSocketDisconnect,
)
from fastapi.middleware.cors import (
    CORSMiddleware,
)

from app.api.websocket.manager import (
    connection_manager,
)

from app.bootstrap import (
    ApplicationBootstrap,
)

from app.api.routes.market import (
    router as market_router,
)

from app.api.routes.signals import (
    router as signals_router,
)


@asynccontextmanager
async def lifespan(
    app: FastAPI,
):

    bootstrap = (
        ApplicationBootstrap()
    )

    await bootstrap.initialize()

    yield


api_app = FastAPI(
    title="Algo Trading API",
    lifespan=lifespan,
)

api_app.add_middleware(
    CORSMiddleware,

    allow_origins=[
        "http://localhost:3000",
    ],

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"],
)

api_app.include_router(
    market_router,
    prefix="/api/market",
    tags=["market"],
)

api_app.include_router(
    signals_router,
    prefix="/api/market",
    tags=["signals"],
)

@api_app.websocket(
    "/ws/market"
)
async def websocket_market(
    websocket: WebSocket,
):

    print(
        "Frontend websocket connected"
    )

    await connection_manager.connect(
        websocket
    )

    try:

        while True:

            await asyncio.sleep(1)

    except WebSocketDisconnect:

        print(
            "Frontend websocket disconnected"
        )

        connection_manager.disconnect(
            websocket
        )