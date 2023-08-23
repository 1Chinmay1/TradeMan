import os
import json
import logging
from datetime import datetime
from kiteconnect import KiteConnect
from pya3 import *

script_dir = os.path.dirname(os.path.abspath(__file__))   
parent_dir = os.path.abspath(os.path.join(script_dir, '..'))

def load_credentials(filepath):
    with open(filepath, 'r') as file:
        return json.load(file)

def place_zerodha_order(trading_symbol, transaction_type, trade_type, strike_price, index, users, broker='zerodha'):
    # filepath = os.path.join(parent_dir, 'Utils', 'users', f'{users}.json')
    # if not os.path.exists(filepath):
    #     print("file not exist")
    #     return
    # user_details = load_credentials(filepath)

    # if broker not in user_details:
    #     return

    # api_key = user_details[broker]['api_key']
    # access_token = user_details[broker]['access_token']
    # kite = KiteConnect(api_key=api_key)
    # kite.set_access_token(access_token)

    # if index == 'NIFTY':
    #     qty = user_details[broker]['Siri_qty']['NIFTY_qty']
    # elif index == 'BANKNIFTY':
    #     qty = user_details[broker]['Siri_qty']['BANKNIFTY_qty']
    # elif index == 'FINNIFTY':
    #     qty = user_details[broker]['Siri_qty']['FINNIFTY_qty']

    # if transaction_type == 'BUY':
    #     order_type = kite.TRANSACTION_TYPE_BUY
    # elif transaction_type == 'SELL':
    #     order_type = kite.TRANSACTION_TYPE_SELL
    # else:
    #     logging.info(f"Invalid trade type for user {users}.")
    #     return

    # try:
    #     entry_margin = round(kite.margins(segment="equity")['available']['live_balance'],2)           
    #     order_id = kite.place_order(variety=kite.VARIETY_REGULAR,
    #                                 exchange=kite.EXCHANGE_NFO,
    #                                 tradingsymbol=trading_symbol,
    #                                 transaction_type=order_type,
    #                                 quantity=qty,
    #                                 product=kite.PRODUCT_MIS,
    #                                 order_type=kite.ORDER_TYPE_MARKET)


    #     logging.info(f"Order placed for user {users}. ID is: {order_id}")
        
    #     # Fetch avg_prc using the order_id
    #     order_history = kite.order_history(order_id=order_id)
    #     for i in order_history:
    #         if i['status'] == 'COMPLETE':
    #             avg_prc = (i['average_price'])

    #     # avg_prc = order_history[-1]['average_price']  # Assuming last entry contains the final average price
    #     print(f"Average price for user {users} is: {avg_prc}")
    #     order_trade_type = trade_type
    #     if str(strike_price) not in trading_symbol:
    #         order_trade_type = "HedgeOrder"

    #     exit_margin = round(kite.margins(segment="equity")['available']['live_balance'],2)
    #     margin_used = round(entry_margin - exit_margin,2)

    #     # Create a new dict for the order
    #     order_dict = {
    #         "margin_used": margin_used,
    #         "order_id": order_id,
    #         "trade_type": order_trade_type,
    #         "qty": qty,
    #         "avg_prc": avg_prc,
    #         "timestamp": str(datetime.now()),
    #         "strike_price": strike_price,
    #         "tradingsymbol": trading_symbol[0]
    #     }

    #     # Create a new list for each trade_type if it doesn't exist
    #     if 'orders' not in user_details[broker]:
    #         user_details[broker]['orders'] = {}
    #     if 'Siri' not in user_details[broker]['orders']:
    #         user_details[broker]['orders']['Siri'] = {}
    #     if trade_type not in user_details[broker]['orders']['Siri']:
    #         user_details[broker]['orders']['Siri'][trade_type] = []

    #     # Add the order_dict to the corresponding trade_type list
    #     user_details[broker]['orders']['Siri'][trade_type].append(order_dict)

    # except Exception as e:
    #     message = f"Order placement failed for user {users}: {e}"
    #     # mpwizard_discord_bot(message)
    #     logging.info(message)

    # with open(filepath, 'w') as file:
    #     json.dump(user_details, file, indent=4)  # Save the updated user_details back to json file
    # return float(avg_prc)
    print(trading_symbol, transaction_type, trade_type, strike_price, index, users, broker)
    return 10.0


def place_aliceblue_order(trading_symbol, transaction_type, trade_type, strike_price, index, users, broker='aliceblue'):
    # filepath = os.path.join(parent_dir, 'Utils', 'users', f'{users}.json')
    # if not os.path.exists(filepath):
    #     print("file not exist")
    #     return
    # user_details = load_credentials(filepath)

    # if broker not in user_details:
    #     return
    
    # username = str(user_details[broker]['username'])
    # api_key = user_details[broker]['api_key']
    # alice = Aliceblue(username, api_key = api_key)
    # session_id = alice.get_session_id()

    # if index == 'NIFTY':
    #     qty = user_details[broker]['Siri_qty']['NIFTY_qty']
    # elif index == 'BANKNIFTY':
    #     qty = user_details[broker]['Siri_qty']['BANKNIFTY_qty']
    # elif index == 'FINNIFTY':
    #     qty = user_details[broker]['Siri_qty']['FINNIFTY_qty']

    # if transaction_type == 'BUY':
    #     order_type = TransactionType.Buy
    # elif transaction_type == 'SELL':
    #     order_type = TransactionType.Sell
    # else:
    #     logging.info(f"Invalid trade type for user {users}.")
    #     return
    
    # try:
    #     entry_margin = (float(alice.get_balance()[0]['net']))
    #     order_id = alice.place_order(transaction_type = order_type,
    #                                     instrument = trading_symbol,
    #                                     quantity = qty ,
    #                                     order_type = OrderType.Market,
    #                                     product_type = ProductType.Intraday,
    #                                     price = 0.0,
    #                                     trigger_price = None,
    #                                     stop_loss = None,
    #                                     square_off = None,
    #                                     trailing_sl = None,
    #                                     is_amo = False)
    #     logging.info(f"Order placed for user {users}. ID is: {order_id['NOrdNo']}")

    #     # Fetch avg_prc using the order_id
    #     avg_prc = alice.get_order_history(order_id['NOrdNo'])['Avgprc']
    #     order_trade_type = trade_type
    #     if str(strike_price) not in trading_symbol[3]:
    #         order_trade_type = "HedgeOrder"

    #     exit_margin = (float(alice.get_balance()[0]['net']))
    #     margin_used = (entry_margin - exit_margin)

    #     # Create a new dict for the order
    #     order_dict = {
    #         "margin_used": margin_used,
    #         "order_id": order_id['NOrdNo'],
    #         "trade_type": order_trade_type,
    #         "qty": qty,
    #         "avg_prc": avg_prc,
    #         "timestamp": str(datetime.now()),
    #         "strike_price": strike_price,
    #         "tradingsymbol": trading_symbol[3]
    #     }

    #     # Create a new list for each trade_type if it doesn't exist
    #     if 'orders' not in user_details[broker]:
    #         user_details[broker]['orders'] = {}
    #     if 'Siri' not in user_details[broker]['orders']:
    #         user_details[broker]['orders']['Siri'] = {}
    #     if trade_type not in user_details[broker]['orders']['Siri']:
    #         user_details[broker]['orders']['Siri'][trade_type] = []


    #     # Add the order_dict to the corresponding trade_type list
    #     user_details[broker]['orders']['Siri'][trade_type].append(order_dict)

    # except Exception as e:
    #     message = f"Order placement failed for user {users}: {e}"
    #     # mpwizard_discord_bot(message)
    #     logging.info(message)

    # with open(filepath, 'w') as file:
    #     json.dump(user_details, file, indent=4)  # Save the updated user_details back to json file
    # return float(avg_prc)
    print(trading_symbol, transaction_type, trade_type, strike_price, index, users, broker)
    return 10.0


def place_stoploss_zerodha(trading_symbol, transaction_type, trade_type, strike_price, index, limit_prc, users, broker='zerodha'):
    # filepath = os.path.join(parent_dir, 'Utils', 'users', f'{users}.json')
    # if not os.path.exists(filepath):
    #     print("file not exist")
    #     return
    # user_details = load_credentials(filepath)

    # if broker not in user_details:
    #     return

    # api_key = user_details[broker]['api_key']
    # access_token = user_details[broker]['access_token']
    # kite = KiteConnect(api_key=api_key)
    # kite.set_access_token(access_token)

    # print("price",limit_prc)
    # #check if the limit_prc is negative if it is negative print a message
    # if limit_prc < 0:
    #     limit_prc = 10.0
    #     message = f"Check the stoploss for {users}"
    #     # mpwizard_discord_bot(message)

    # trigger_prc = limit_prc+1

    # if index == 'NIFTY':
    #     qty = user_details[broker]['MPWizard_qty']['NIFTY_qty']
    # elif index == 'BANKNIFTY':
    #     qty = user_details[broker]['MPWizard_qty']['BANKNIFTY_qty']
    # elif index == 'FINNIFTY':
    #     qty = user_details[broker]['MPWizard_qty']['FINNIFTY_qty']


    # if transaction_type == 'BUY':
    #     order_type = kite.TRANSACTION_TYPE_BUY
    # elif transaction_type == 'SELL':
    #     order_type = kite.TRANSACTION_TYPE_SELL
    # else:
    #     logging.info(f"Invalid trade type for user {users}.")
    #     return
    # try:           
    #     order_id = kite.place_order(variety=kite.VARIETY_REGULAR,
    #                                 exchange=kite.EXCHANGE_NFO,
    #                                 price=round(limit_prc,1),
    #                                 tradingsymbol=trading_symbol,
    #                                 transaction_type=order_type,
    #                                 quantity=qty,
    #                                 trigger_price=round(trigger_prc,1),
    #                                 product=kite.PRODUCT_MIS,
    #                                 order_type=kite.ORDER_TYPE_SL)


    #     logging.info(f"Order placed for user {users}. ID is: {order_id}")

    #     # Fetch avg_prc using the order_id
    #     order_history = kite.order_history(order_id=order_id)
    #     avg_prc = order_history[-1]['average_price']  # Assuming last entry contains the final average price

    #     order_trade_type = trade_type
    #     if trading_symbol:
    #         print("trading symbol",trading_symbol[0])

    #     # Create a new dict for the order
    #     order_dict = {
    #         "order_no": order_id,
    #         "trade_type": order_trade_type,
    #         "qty": qty,
    #         "avg_prc": avg_prc,
    #         "timestamp": str(datetime.now()),
    #         "strike_price": strike_price,
    #         "tradingsymbol": trading_symbol
    #     }

    # except Exception as e:
    #     message = f"Order placement failed for user {users}: {e}"
    #     # mpwizard_discord_bot(message)
    #     logging.info(message)

    # with open(filepath, 'w') as file:
    #     json.dump(user_details, file, indent=4)  # Save the updated user_details back to json file
    
    # if order_id is None:
    #     # mpwizard_discord_bot(f"Order placement failed for user {users}.")
    #     order_id = 0
    
    # return order_id
    print(trading_symbol, transaction_type, trade_type, strike_price, index, limit_prc, users, broker)
    return 10.0


def place_stoploss_aliceblue(trading_symbol, transaction_type, trade_type, strike_price, index, limit_prc, users, broker='aliceblue'):
    # filepath = os.path.join(parent_dir, 'Utils', 'users', f'{users}.json')
    # if not os.path.exists(filepath):
    #     print("file not exist")
    #     return
    # user_details = load_credentials(filepath)

    # if broker not in user_details:
    #     return
    
    # if limit_prc < 0:
    #     limit_prc = 10.0
    #     message = f"Check the stoploss for {users}"
    #     # mpwizard_discord_bot(message)

    # trigger_prc = limit_prc+1

    # username = str(user_details[broker]['username'])
    # api_key = user_details[broker]['api_key']
    # alice = Aliceblue(username, api_key = api_key)
    # session_id = alice.get_session_id()
    # if index == 'NIFTY':
    #     qty = user_details[broker]['MPWizard_qty']['NIFTY_qty']
    # elif index == 'BANKNIFTY':
    #     qty = user_details[broker]['MPWizard_qty']['BANKNIFTY_qty']
    # elif index == 'FINNIFTY':
    #     qty = user_details[broker]['MPWizard_qty']['FINNIFTY_qty']

    # if transaction_type == 'BUY':
    #     order_type = TransactionType.Buy
    # elif transaction_type == 'SELL':
    #     order_type = TransactionType.Sell
    # else:
    #     logging.info(f"Invalid trade type for user {users}.")
    #     return
    # try:
    #     order_id = alice.place_order(transaction_type = order_type,
    #                                     instrument = trading_symbol,
    #                                     quantity = qty ,
    #                                     order_type = OrderType.StopLossLimit,
    #                                     product_type = ProductType.Intraday,
    #                                     price = round(limit_prc,1), #####limit price
    #                                     trigger_price = round(trigger_prc,1),#########trigger price
    #                                     stop_loss = None,
    #                                     square_off = None,
    #                                     trailing_sl = None,
    #                                     is_amo = False)
        
    #     logging.info(f"Order placed for user {users}. ID is: {order_id['NOrdNo']}")
    #     order_no = order_id['NOrdNo']
    #     # Fetch avg_prc using the order_id
    #     avg_prc = alice.get_order_history(order_id['NOrdNo'])['Avgprc']

    #     order_trade_type = trade_type
    #     if str(strike_price) not in trading_symbol[3]:
    #         order_trade_type = "HedgeOrder"

    #     # Create a new dict for the order
    #     order_dict = {
    #         "order_no": order_no,
    #         "trade_type": order_trade_type,
    #         "qty": qty,
    #         "avg_prc": avg_prc,
    #         "timestamp": str(datetime.now()),
    #         "strike_price": strike_price,
    #         "tradingsymbol": trading_symbol[3]
    #     }

    # except Exception as e:
    #     message = f"Order placement failed for user {users}: {e}"
    #     # mpwizard_discord_bot(message)
    #     logging.info(message)

    # with open(filepath, 'w') as file:
    #     json.dump(user_details, file, indent=4)  # Save the updated user_details back to json file
    # return order_no
    print(trading_symbol, transaction_type, trade_type, strike_price, index, limit_prc, users, broker)
    return 10.0