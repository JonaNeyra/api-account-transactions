import json

from flask import request, current_app as app
from flask_cors import cross_origin
from application.actions import DepositHandler, WithdrawHandler, TransferHandler
from application.resources import DefaultStorageResource
from application.service import JsonRegister
from application.strategy import (
    AccountDepositTransactioner,
    AccountWithdrawTransactioner,
    AccountTransferTransactioner,
    AccountTransactionable
)
from config.constants import DEPOSIT_TYPE, WITHDRAW_TYPE, TRANSFER_TYPE
from domain.request import DepositEvent, WithdrawEvent, TransferEvent


@app.route('/reset', methods=['POST'])
@cross_origin()
def reset():
    DefaultStorageResource.load().upload_obj(
        json.dumps({}), 'transactions.json'
    )
    return 'OK'


@app.route("/balance", methods=["GET"])
@cross_origin()
def balance():
    account_id = request.args['account_id']
    data = JsonRegister.start()
    total = data.get_account_balance(account_id)

    status = 200
    if balance == 0:
        status = 404

    return str(total), status


@app.route('/event', methods=['POST'])
@cross_origin()
def event():
    status = 201
    if request.json['type'] == DEPOSIT_TYPE:
        req = DepositEvent(request.json)
        data = JsonRegister.start()
        deposit_strategy = AccountDepositTransactioner.config(data)
        deposit_context = AccountTransactionable(deposit_strategy)
        deposit_handler = DepositHandler(deposit_context)
        res = deposit_handler.index(req)
    elif request.json['type'] == WITHDRAW_TYPE:
        req = WithdrawEvent(request.json)
        data = JsonRegister.start()
        withdraw_strategy = AccountWithdrawTransactioner.config(data)
        withdraw_context = AccountTransactionable(withdraw_strategy)
        withdraw_handler = WithdrawHandler(withdraw_context)
        res = withdraw_handler.index(req)
    elif request.json['type'] == TRANSFER_TYPE:
        req = TransferEvent(request.json)
        data = JsonRegister.start()
        transfer_strategy = AccountTransferTransactioner.config(data)
        transfer_context = AccountTransactionable(transfer_strategy)
        transfer_handler = TransferHandler(transfer_context)
        res = transfer_handler.index(req)
    else:
        res = 0

    if res == 0:
        res = str(res)
        status = 404

    return res, status
