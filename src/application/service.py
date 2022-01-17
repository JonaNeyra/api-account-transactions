import json
from application.resources import DefaultStorageResource
from config.constants import DEPOSIT_TYPE, WITHDRAW_TYPE


class JsonRegister:
    ACCOUNT_TRANSACTIONS_KEY = 'transactions'

    def __init__(self, data):
        self.data = data

    @classmethod
    def start(cls):
        obj = DefaultStorageResource.load().client.get_object(
            Bucket=DefaultStorageResource.bucket,
            Key=DefaultStorageResource.default_key
        )
        content = obj['Body']
        transactions = json.loads(content.read())
        return cls(transactions)

    def get_account_balance(self, account_id: int):
        balance = 0
        if account_id not in self.data:
            return balance

        for transaction_review in self.data[account_id][self.ACCOUNT_TRANSACTIONS_KEY]:
            if transaction_review['type'] == DEPOSIT_TYPE:
                balance = balance + transaction_review['amount']
            if transaction_review['type'] == WITHDRAW_TYPE:
                balance = balance - transaction_review['amount']

        return balance

    def get_data(self):
        return self.data

    def get_account(self, account_id):
        if account_id not in self.data:
            return 0
        return self.data[account_id]

    def set_account(self, account_id):
        if account_id in self.data:
            return self

        transactions = {self.ACCOUNT_TRANSACTIONS_KEY: []}
        self.data[account_id] = transactions

        return self

    def add_transaction(self, account_id, transaction: dict):
        transaction_list = self.data[account_id][self.ACCOUNT_TRANSACTIONS_KEY]
        transaction_list.append(transaction)

        self.data[account_id][self.ACCOUNT_TRANSACTIONS_KEY] = transaction_list

        return self

    def is_account(self, account_id):
        return account_id in self.data

    def save(self):
        DefaultStorageResource.load().upload_obj(
            json.dumps(self.data, indent=2), 'transactions.json'
        )
