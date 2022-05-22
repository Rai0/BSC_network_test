import requests
import json
from pycoin.networks.bitcoinish import create_bitcoinish_network
from pycoin.coins.tx_utils import create_signed_tx
from random import randint
from transaction.models import transactionModel

class connectRPC:
    """connect to RPC"""

    # данные для RPC-доступы: 
    headers={'content-type': "application/json",}
    ip='45.32.232.25'
    port='3669'
    user='bcs_tester'
    password='iLoveBCS'

    def get_RPC_responce (self, method, ip=ip, port=port, rpcuser=user, rpcpassword=password, params=None, headers=headers, rezal_filter='result'):
        """return json responce"""
        url = 'http://' +  ip + ':' +  port + '/'
        payload = json.dumps({"method":method, "params":[params]})
        response = requests.request("POST", url, data = payload, headers=headers, auth=( rpcuser,  rpcpassword))
        json_response = json.loads(response.text)
        return (json_response [rezal_filter]) 

class coinTransactionService:
    # class for create and sing tx
    def _create_network (self):
        network = create_bitcoinish_network (symbol = '', network_name = '', subnet_name = '',
                                            wif_prefix_hex="80", address_prefix_hex="19",
                                            pay_to_script_prefix_hex="32", bip32_prv_prefix_hex="0488ade4",
                                            bip32_pub_prefix_hex="0488B21E", bech32_hrp="bc", bip49_prv_prefix_hex="049d7878",
                                            bip49_pub_prefix_hex="049D7CB2", bip84_prv_prefix_hex="04b2430c",
                                            bip84_pub_prefix_hex="04B24746", magic_header_hex = "F1CFA6D3", default_port=3666)
        return network

    def _create_spendable(self, coin_value, script, tx_hash, tx_out_index):
        return dict(
                coin_value=coin_value,
                script_hex=script,
                tx_hash_hex=tx_hash,
                tx_out_index=tx_out_index,
                block_index_available=0,
                does_seem_spent=False,
                block_index_spent=0
            )

    def _get_spendables_from_utxo(self, old_address):
        """return list of spendables"""
        # get utxo from api
        utxo=requests.get(f"https://bcschain.info/api/address/{old_address}/utxo").json()
        spendables=[]
        for tx in utxo:
            spendables.append(self._create_spendable(tx["value"], tx["scriptPubKey"], tx["transactionId"], tx["outputIndex"]))
        return spendables

    def create_signed_tx(self,  old_address: str, address_to: str, value: int, wifs: list):
        """return signed tx"""
        network=self._create_network()
        spendables=self._get_spendables_from_utxo(old_address)
        return create_signed_tx(network, spendables, [(address_to, value), old_address], wifs, fee=int(value/1000))

    def save_tx (self, transactionID: str) -> None:
        """func for save tx to db"""
        tx=transactionModel(transactionID=transactionID)
        tx.save ()

coin=coinTransactionService ()
rpc=connectRPC()