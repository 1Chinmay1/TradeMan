from time import sleep
import os,sys,json
import datetime as dt

DIR_PATH = os.getcwd()
sys.path.append(DIR_PATH)

import Brokers.place_order_calc as place_order_calc
import MarketUtils.InstrumentBase as InstrumentBase
import Strategies.StrategyBase as StrategyBase
import MarketUtils.general_calc as general_calc
import Brokers.place_order as place_order

_,mpwizard_json = place_order_calc.get_strategy_json('MPWizard')
instrument_obj = InstrumentBase.Instrument()
strategy_obj = StrategyBase.Strategy.read_strategy_json(mpwizard_json)

class MPWInstrument:
    def __init__(self, name, token, trigger_points, price_ref):
        self.name = name
        self.token = token
        self.trigger_points = trigger_points
        self.price_ref = price_ref
    
    def get_name(self):
        return self.name
    
    def get_token(self):
        return self.token
    
    def get_trigger_points(self):
        return self.trigger_points
    
    def get_price_ref(self):
        return self.price_ref

class OrderMonitor:
    def __init__(self, json_data, max_orders):
        self.mood_data = json.loads(json_data)
        self.instruments = self._create_instruments(self.mood_data['EntryParams'])
        self.orders_placed_today = 0
        self.max_orders_per_day = max_orders
        self.today_date = dt.date.today()
        self.done_for_the_day = False
        self.indices_triggered_today = set()
        self.message_sent = {
            instrument.get_name(): {level: False for level in instrument.get_trigger_points().keys()}
            for instrument in self.instruments
        }
        self.instrument_monitor = place_order_calc.monitor()
        self.instrument_monitor.set_callback(self.handle_trigger)
        self._add_tokens_to_instrument_monitor()

    def _add_tokens_to_instrument_monitor(self):
        for instrument in self.instruments:
            self.instrument_monitor.add_token(
                token=str(instrument.get_token()),
                trigger_points=instrument.get_trigger_points(),
                # Add additional parameters if needed
            )

    @staticmethod
    def _load_json_data(json_data):
        return json.loads(json_data)
    
    def _reset_daily_counters(self):
        self.today_date = dt.date.today()
        self.orders_placed_today = 0
        self.done_for_the_day = False
        self.indices_triggered_today = set()

    def create_single_instrument(self,instruments_data):
        name =instruments_data['Name']
        token = instruments_data['Token']
        trigger_points = instruments_data['TriggerPoints']
        price_ref = instruments_data['PriceRef']
        instrument = MPWInstrument(name, token, trigger_points,price_ref)
        return instrument

    
    def _create_instruments(self, instruments_data):
        instruments = []
        for name, data in instruments_data.items():
            # Skip entries that do not have the 'TriggerPoints' key
            if 'TriggerPoints' not in data or 'PriceRef' not in data:
                continue
            
            token = self.mood_data['GeneralParams']['IndicesTokens'].get(name)
            if token is None:
                print(f"Warning: Token not found for instrument {name}")
                continue

            trigger_points = data['TriggerPoints']
            price_ref = data['PriceRef']
            instrument = MPWInstrument(name, token, trigger_points,price_ref)
            instruments.append(instrument)
        return instruments

    def _check_price_crossing(self, prev_ltp, ltp, levels):
        """Check if the price has crossed a certain level."""
        for level_name, level_price in levels.items():
            if prev_ltp is None:
                continue
            if prev_ltp < level_price <= ltp:
                return "UpCross", level_name
            elif prev_ltp > level_price >= ltp:
                return "DownCross", level_name
        return None, None

    def create_order_details(self,name,cross_type,ltp,price_ref):
        mood_data_entry = self._get_mood_data_for_instrument(name)
        if not mood_data_entry:
            return #TODO add try exception for all the points of failure.

        option_type = self._determine_option_type(cross_type, mood_data_entry)
        if not option_type:
            return
        
        strikeprc = general_calc.round_strike_prc(ltp,name)
        expiry_date = instrument_obj.get_expiry_by_criteria(name,strikeprc,option_type,'current_week')
        exchange_token = instrument_obj.get_exchange_token_by_criteria(name,strikeprc,option_type,expiry_date)
        order_details = [
        {  
        "strategy": strategy_obj.get_strategy_name(),
        "exchange_token" : exchange_token,     
        "segment" : strategy_obj.get_general_params().get('Segment'),
        "transaction_type": strategy_obj.get_general_params().get('TransactionType'),  
        "order_type" : strategy_obj.get_general_params().get('OrderType'), 
        "product_type" : strategy_obj.get_general_params().get('ProductType'),
        "price_ref" : price_ref,
        "order_mode" : ["Main","TSL"],
        "trade_id" : "MP3_entry" #TODO fetch the order_tag from {strategy_name}.json
        }]
        return order_details

    def _process_instrument(self, ltp, instrument, prev_ltp, message_sent):
        """Process an instrument's data and handle trading signals."""
        if self.orders_placed_today >= self.max_orders_per_day:
            print("Daily signal limit reached. No more signals will be generated today.")
            return
        
        token = instrument.get_token()
        levels = instrument.get_trigger_points()
        name = instrument.get_name()
        price_ref = instrument.get_price_ref()

        #check if the index has been triggered today
        if name in self.indices_triggered_today:
            return
        
        cross_type, level_name = self._check_price_crossing(prev_ltp[name], ltp, levels)
        if cross_type and not self.message_sent[instrument.get_name()][level_name]:
            order_to_place = self.create_order_details(name,cross_type,ltp,price_ref)
            # place_order.place_order_for_strategy(strategy_obj.get_strategy_name(),order_to_place)  
            print(f"{cross_type} at {ltp} for {name}!")
            
            
            # place_order.place_order_for_broker("MPWizard", order_details, monitor=self.monitor)
            self.indices_triggered_today.add(name) 
            
            message = f"{cross_type} {self._get_mood_data_for_instrument(name)['IBLevel']} {self.mood_data['GeneralParams']['TradeView']} at {ltp} for {name}!"
            print(message)
            # discord.discord_bot(message,"MPWizard") 
            self.orders_placed_today += 1
            self.message_sent[name][level_name] = True
        prev_ltp[name] = ltp

    def _get_mood_data_for_instrument(self, name):
        return self.mood_data['EntryParams'].get(name)

    def _determine_option_type(self, cross_type, mood_data_entry):
        """Determine the option type based on cross type and mood data."""
        ib_level = mood_data_entry['IBLevel']
        instru_mood = self.mood_data['GeneralParams']['TradeView']

        if ib_level == 'Big':
            return 'PE' if cross_type == 'UpCross' else 'CE'
        elif ib_level == 'Small':
            return 'PE' if cross_type == 'DownCross' else 'CE'
        elif ib_level == 'Medium':
            return 'PE' if instru_mood == 'Bearish' else 'CE'
        else:
            print(f"Unknown IB Level: {ib_level}")
        return None
    
    def process_orders(self,instrument, cross_type, ltp):
        index_tokens = strategy_obj.get_general_params().get("IndicesTokens")
        token_to_index = {str(v): k for k, v in index_tokens.items()}
        index_name = token_to_index.get(instrument)
        print(index_name)
        if index_name:
            obj = self.create_single_instrument(self.mood_data['EntryParams'][index_name])
            name = obj.get_name()
            price_ref = obj.get_price_ref()

            
            if self.orders_placed_today >= self.max_orders_per_day:
                print("Daily signal limit reached. No more signals will be generated today.")
                return
            order_to_place = self.create_order_details(name,cross_type,ltp,price_ref)
            place_order.place_order_for_strategy(strategy_obj.get_strategy_name(),order_to_place)  

            self.indices_triggered_today.add(name) 
            self.orders_placed_today += 1
            if name in self.message_sent:
                for level in self.message_sent[name]:
                    self.message_sent[name][level] = True 
        else:
            print("Index name not found for token:", instrument)



    def handle_trigger(self, instrument,data):
        ltp = self.instrument_monitor.fetch_ltp(instrument)
        
        
        if data['type'] == 'trigger':
            cross_type = 'UpCross' if data['name'] == 'IBHigh' else 'DownCross'
            self.process_orders(instrument, cross_type, ltp)
            
        elif data['type'] == 'target':
            # print(f"Target reached for {instrument.get_name()} at {ltp}.")
            order_details = data.get('order_details')
            if order_details:
                new_target, new_limit_prc = place_order.place_tsl(order_details)
                data['target'] = new_target
                data['limit'] = new_limit_prc
                print(f"New target set to {new_target} and new limit price set to {new_limit_prc}.")
            else:
                print("No order details available to update target and limit prices.")
                
        elif data['type'] == 'limit':
            print(f"Limit reached for {instrument.get_name()} at {ltp}. Handling accordingly.")
            # Handle limit reached scenario here
        

    def monitor_index(self):
        print("Monitoring started...")
        # while True:
        if dt.date.today() != self.today_date:
            self._reset_daily_counters()
            self.message_sent = {
                instrument.get_name(): {level: False for level in instrument.get_trigger_points().keys()}
                for instrument in self.instruments
            }
        self.instrument_monitor.start_monitoring()

        sleep(10)