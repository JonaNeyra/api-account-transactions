from application.strategy import AccountTransactionable
from domain.request import DepositEvent, WithdrawEvent, TransferEvent


class DepositHandler:
    def __init__(self, strategy_context: AccountTransactionable):
        self.context = strategy_context

    def index(self, event_request: DepositEvent):
        if event_request.destination is None or event_request.amount is None:
            return 0

        return self.context.process(event_request)


class WithdrawHandler:
    def __init__(self, strategy_context: AccountTransactionable):
        self.context = strategy_context

    def index(self, event_request: WithdrawEvent):
        if event_request.origin is None or event_request.amount is None:
            return 0

        return self.context.process(event_request)


class TransferHandler:
    def __init__(self, strategy_context: AccountTransactionable):
        self.context = strategy_context

    def index(self, event_request: TransferEvent):
        if event_request.origin is None or event_request.amount is None or event_request.destination is None:
            return 0

        return self.context.process(event_request)
