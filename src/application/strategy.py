from __future__ import annotations
from abc import ABC, abstractmethod
from application.service import JsonRegister
from config.constants import WITHDRAW_TYPE, DEPOSIT_TYPE
from domain.request import DepositEvent, WithdrawEvent, TransferEvent


class AccountTransactionable:
    def __init__(self, transactioner: AccountTransactioner):
        self._transactioner = transactioner

    @property
    def verifier(self) -> AccountTransactioner:
        return self._transactioner

    @verifier.setter
    def verifier(self, transactioner: AccountTransactioner):
        self._transactioner = transactioner

    def process(self, event):
        return self._transactioner.op(event)


class AccountTransactioner(ABC):
    @classmethod
    @abstractmethod
    def config(cls, register: JsonRegister):
        pass

    @abstractmethod
    def op(self, event):
        pass


class AccountDepositTransactioner(AccountTransactioner):
    def __init__(self, register: JsonRegister):
        self.register = register

    @classmethod
    def config(cls, register: JsonRegister):
        return cls(register)

    def op(self, event: DepositEvent):
        type = event.type
        amount = int(event.amount)
        destination = event.destination
        transaction = {'type': type, 'amount': amount}
        if not self.register.is_account(destination):
            self.register.set_account(destination)
            self.register.add_transaction(destination, transaction)
            self.register.save()
        else:
            self.register.add_transaction(destination, transaction)
            self.register.save()

        return {
            'destination': {
                "id": destination,
                'balance': self.register.get_account_balance(destination)
            }
        }


class AccountWithdrawTransactioner(AccountTransactioner):
    def __init__(self, register):
        self.register = register

    @classmethod
    def config(cls, register: JsonRegister):
        return cls(register)

    def op(self, event: WithdrawEvent):
        type = event.type
        amount = int(event.amount)
        origin = event.origin
        transaction = {'type': type, 'amount': amount}
        if self.register.is_account(origin):
            self.register.add_transaction(origin, transaction)
            self.register.save()
        else:
            return 0

        return {
            'origin': {
                "id": origin,
                'balance': self.register.get_account_balance(origin)
            }
        }


class AccountTransferTransactioner(AccountTransactioner):
    def __init__(self, register):
        self.register = register

    @classmethod
    def config(cls, register: JsonRegister):
        return cls(register)

    def op(self, event: TransferEvent):
        amount = int(event.amount)
        origin = event.origin
        destination = event.destination
        if not self.register.is_account(origin):
            return 0

        if not self.register.is_account(destination):
            self.register.set_account(destination)

        if self.register.is_account(origin):
            transfer = {'type': WITHDRAW_TYPE, 'amount': amount}
            self.register.add_transaction(origin, transfer)
            accept_transfer = {'type': DEPOSIT_TYPE, 'amount': amount}
            self.register.add_transaction(destination, accept_transfer)

        return {
            'origin': {
                "id": origin,
                'balance': self.register.get_account_balance(origin)
            },
            'destination': {
                "id": destination,
                'balance': self.register.get_account_balance(destination)
            }
        }
