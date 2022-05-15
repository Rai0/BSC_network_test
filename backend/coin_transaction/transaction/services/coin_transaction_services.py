import requests
import json
from pycoin.networks.bitcoinish import create_bitcoinish_network

# данные для RPC-доступы: 
ip = '45.32.232.25'
port = '3669'
user = 'bcs_tester'
password = 'iLoveBCS'

class coinTransactionService:
    headers = {'content-type': "application/json",}

    def get_RPC_responce (self, url, port, rpcuser, rpcpassword, method, params = None, headers = headers):
        url = 'http://' +  ip + ':' +  port + '/'
        payload = json.dumps({"method":  method, "params":  params})
        response = requests.request("POST", url, data = payload, headers =  headers, auth = ( rpcuser,  rpcpassword))
        json_response = json.loads(response.text)
        return json_response
        return (json_response ['result']) 

    def create_network (self):
        network = create_bitcoinish_network (symbol = '', network_name = '', subnet_name = '',
                                            wif_prefix_hex="80", address_prefix_hex="19",
                                            pay_to_script_prefix_hex="32", bip32_prv_prefix_hex="0488ade4",
                                            bip32_pub_prefix_hex="0488B21E", bech32_hrp="bc", bip49_prv_prefix_hex="049d7878",
                                            bip49_pub_prefix_hex="049D7CB2", bip84_prv_prefix_hex="04b2430c",
                                            bip84_pub_prefix_hex="04B24746", magic_header_hex = "F1CFA6D3", default_port=3666)

coin = coinTransactionService ()

if __name__ == '__main__':
    print (coin.get_RPC_responce (ip, port, user, password, 'getblockchaininfo'))
    coin.create_network ()