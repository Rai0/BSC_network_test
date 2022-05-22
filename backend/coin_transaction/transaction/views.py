from django.shortcuts import render
from .services.coin_transaction_services import coin, rpc
from django.http import Http404, HttpResponseRedirect
from .models import transactionModel
from django.http import Http404
from coin_transaction.settings import WIFs, my_address

WIFs=WIFs
my_address=my_address

# Create your views here.
def tx_page (request):
    return render(request=request, template_name='transaction/index.html', context={'transaction':transactionModel.objects.all()})

def make_tx (request):
    tx_as_hax=coin.create_signed_tx (old_address=my_address, address_to=rpc.get_RPC_responce('getnewaddress'), value=1e8, wifs=[WIFs]).as_hex()
    # coin.save_tx (rpc.get_RPC_responce ('sendrawtransaction', params=tx_as_hax))
    coin.send_and_save_tx (tx_as_hax)
    return HttpResponseRedirect ('/')

def tx_description (request, tx):
    try:
        tx = transactionModel.objects.filter(transactionID=tx)[0]
    except Exception as ex: 
        raise Http404 
    if len(tx.description)==0:
        tx.description='this tx has no description'
    context={'id':tx.transactionID, 'description':tx.description}
    return render(request=request, template_name='transaction/tx_description.html', context=context)