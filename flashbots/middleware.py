from typing import Callable, Coroutine
from web3 import Web3
from web3.middleware import Middleware
from web3.types import RPCEndpoint, RPCResponse
from typing import Any
from .provider import FlashbotProvider

FLASHBOTS_METHODS = [
    "eth_sendBundle",
    "eth_callBundle",
    "eth_cancelBundle",
    "eth_sendPrivateTransaction",
    "eth_cancelPrivateTransaction",
    "flashbots_getBundleStats",
    "flashbots_getUserStats",
    "flashbots_getBundleStatsV2",
    "flashbots_getUserStatsV2",
]


def construct_flashbots_middleware(
    flashbots_provider: FlashbotProvider,
) -> Middleware:
    async def flashbots_middleware(
        make_request: Callable[[RPCEndpoint, Any], Any], w3: Web3
    ) -> Callable[[RPCEndpoint, Any], Coroutine[Any, Any, RPCResponse]]:
        async def middleware(method: RPCEndpoint, params: Any) -> RPCResponse:
            if method not in FLASHBOTS_METHODS:
                return await make_request(method, params)
            else:
                return await flashbots_provider.make_request(method, params)

        return middleware

    return flashbots_middleware
