import time
from alice_blue import *

api_secret = "ZwIQM6UkaJWTWIQPKP2KNTyVuqWZZ5apm2kOLxK2xnXxJz98bUtRP5JIfnwk2x4k"
app_id = "MmBIvoYyY7"
access_token = AliceBlue.login_and_get_access_token(username="375036", password="mike@1964", twoFA="1964", api_secret= api_secret ,redirect_url='https://ant.aliceblueonline.com/plugin/callback/', app_id=app_id)

alice = AliceBlue(username='375036', password='mike@1964', access_token=access_token)

start_range = 65000
end_range = 70000
buy_diff = 100
sell_diff = 50
end_start = end_range-start_range
buy = []
current_price = 0.0
count = 0
silver_symbol = 'SILVERMIC NOV FUT'
buy_or_not = True


def check_to_buy():

    global buy_price
    global count
    global sell_diff
    global buy_or_not

    pending_orders = alice.get_order_history().get('data').get('pending_orders')  # change this to 'pending_orders'.

    if len(pending_orders) == 0:
        buy_or_not = True

    else:
        m = 0
        count = 0

        while m < len(pending_orders):

            trading_symbol = pending_orders[m].get('trading_symbol')
            price_of_trade = pending_orders[m].get('price')
            transaction_type = pending_orders[m].get('transaction_type')

            if trading_symbol == 'SILVERMIC21NOVFUT' and transaction_type == 'BUY':
                if price_of_trade == buy_price:
                    count = 1

            elif trading_symbol == 'SILVERMIC21NOVFUT' and transaction_type == 'SELL':
                if float(buy_price + sell_diff) == price_of_trade:
                    count = 1

            if count == 1:
                print("Buy or not is turning False")
                buy_or_not = False

            else:
                print("Buy or not is True")
                buy_or_not = True

            m += 1

def place_buy_order():

    check_to_buy()
    global buy_or_not
    print("Buy_Or_Not in place_buy_order is :",buy_or_not)
    global buy_price
    global sell_diff
    sell_price = float(sell_diff)
    global silver_symbol
    global count

    if buy_or_not == True:

        alice.place_order(transaction_type = TransactionType.Buy,
                             instrument = alice.get_instrument_by_symbol('MCX', silver_symbol),
                             quantity = 1,
                             order_type = OrderType.Limit,
                             product_type = ProductType.BracketOrder,
                             price = buy_price,
                             trigger_price = None,
                             stop_loss = 2000.0,
                             square_off = sell_price,
                             trailing_sl = None,
                             is_amo = False)
        buy_or_not = False
        count = 0



while (True):

    socket_opened = False
    def event_handler_quote_update(message):

        global current_price
        current_price = message.get('ltp')

    def open_callback():
        global socket_opened
        socket_opened = True

    alice.start_websocket(subscribe_callback=event_handler_quote_update,
                          socket_open_callback=open_callback,
                          run_in_background=True)
    while(socket_opened==False):
        pass
    alice.subscribe(alice.get_instrument_by_symbol('MCX',silver_symbol), LiveFeedType.COMPACT)
    time.sleep(10)


    m = 1
    while m <= end_start // buy_diff:
        buy.append(float(start_range + m * buy_diff))
        m += 1
    m=0
    while m<len(buy)-1:
        if buy[m] < current_price < buy[m+1]:
            print(buy[m])
            buy_price = buy[m]
        m+=1

    place_buy_order()




