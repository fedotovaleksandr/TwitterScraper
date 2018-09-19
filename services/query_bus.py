from abc import ABCMeta, abstractmethod


class IRequest:
    __metaclass__ = ABCMeta


class IResponse:
    __metaclass__ = ABCMeta


class IRequestHandler:
    __metaclass__ = ABCMeta

    @abstractmethod
    def support(self, request: IRequest) -> bool: raise NotImplementedError

    @abstractmethod
    def handle(self, request: IRequest) -> IResponse: raise NotImplementedError


class QueryHandlerNotFoundException(Exception):
    pass


class IQueryBus:
    __metaclass__ = ABCMeta

    @abstractmethod
    def handle(self, request: IRequest) -> IResponse: raise NotImplementedError


class QueryBus(IQueryBus):
    _queryHandlers: [IRequestHandler]

    def __init__(self, queryHandlers: [IRequestHandler]) -> None:
        self._queryHandlers = queryHandlers

    def handle(self, request: IRequest) -> IResponse:
        for handler in self._queryHandlers:
            if handler.support(request):
                return handler.handle(request)
        raise QueryHandlerNotFoundException
