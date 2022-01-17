class Eval:
    def __init__(self, data):
        self.data = data

    def set(self, key, required=True):
        if not self.data:
            return None
        if key not in self.data and required:
            return None
        if required and self.data[key] is None:
            return None
        return self.data[key] if key in self.data else None


class DepositEvent:
    def __init__(self, data):
        valid = Eval(data)
        self.type = valid.set('type')
        self.destination = valid.set('destination')
        self.amount = valid.set('amount')


class WithdrawEvent:
    def __init__(self, data):
        valid = Eval(data)
        self.type = valid.set('type')
        self.origin = valid.set('origin')
        self.amount = valid.set('amount')


class TransferEvent:
    def __init__(self, data):
        valid = Eval(data)
        self.type = valid.set('type')
        self.origin = valid.set('origin')
        self.amount = valid.set('amount')
        self.destination = valid.set('destination')
