import unittest
from unittest.mock import MagicMock

from services.query_bus import QueryBus, IRequestHandler, IResponse, IRequest


class QueryBusTestCase(unittest.TestCase):
    def test_handler_execution(self):
        handler = IRequestHandler()
        handler.support = MagicMock(return_value=True)
        handler.handle = MagicMock(return_value=IResponse)
        bus = QueryBus([handler])
        request = IRequest()
        bus.handle(request)
        handler.handle.assert_called_with(request)
