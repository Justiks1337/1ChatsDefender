from typing import Any

from utils import AbstractHandler


class TestHandler(AbstractHandler):
    async def handle(self, request: Any):
        return False
