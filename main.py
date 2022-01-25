# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settin

#from coinbase.wallet.client import Client

# from time import sleep
import time
# import numpy as np
import talib
# from ta.volatility import BollingerBands, AverageTrueRange
# from talib import SMA
import matplotlib.pyplot as plt
plt.style.use('bmh')
# import yfinance as yf
# import pandas_datareader as pdr
import ccxt
import pandas as pd
from StockSymbols import symbols_kraken








#Globals
SYMBOLS_GLOBAL = symbols_kraken
COMPLETED_TRADES = {}
PROFIT_PERCENT_LIST = []
BOUGHT_STOCKS = {}
BOUGHT_QUANTITIES = {}
trades_so_far = 0

#Buy price vs Sell price
THRESHOLD_PASSED_TF = {}
THRESHOLD_MAX_VS_NOW = {}
#Max price vs Sell price






#Start of TA-lib practice with Apple Stocks
# aapl = yf.download('AAPL', '2019-1-1', '2019-12-27')



# aapl['Simple MA'] = ta.SMA(aapl['Close'],14)
# aapl['EMA'] = ta.EMA(aapl['Close'], timeperiod = 14)
#
# print(aapl['Simple MA'])
# print(aapl['EMA'])

#Using padas datareader to get data
#BTC = pdr.get_data_yahoo('BTC')
#BTC.head()
# print(BTC['Close'])

#https://developers.coinbase.com/docs/wallet/guides/buy-sell



# exchange = ccxt.coinbasepro({
#     'apiKey':"",
#     'secret':""
# })

exchange = ccxt.kraken({
        'apiKey':",
        'secret':""
})

#markets = exchange.load_markets()




#Trying out 'Techniacal Analysis Library in Python Tutorial' (Youtube)





#pulling from coinbase exchange
#bars = exchange.fetch_ohlcv('ETH/USD','1d')



#Convertin ccxt raw data into dataframe
#df = pd.DataFrame(bars, columns=['timestamp','open','high','low','close','volume'])
# print("Df")
# print(df)
# current_price = df[-1:]
# current_price2 = current_price['close']
# print("Current price")
# print(current_price2)

#using data frame to create bollinger bands from ta

    #Creating SMA, Sma 2 works as it goes by day, Sma 1 goes by minutes and does not work as needed.
#bb_indicator = BollingerBands(df['close'])
#SMA150_2 = talib.SMA(BTC['Close'].values,150)




#print(talib.get_functions())

#df['upper_band'] = bb_indicator.bollinger_hband()
#df['lower_band'] = bb_indicator.bollinger_lband()
#df['moving_average'] = bb_indicator.bollinger_mavg()


#atr_indicator = AverageTrueRange(df['high'],df['low'],df['close'])
#df['atr'] = atr_indicator.average_true_range()
#print(df)

#percentage change function
def percentage_change(start_price, buy_price):
    start_price = float(start_price)
    buy_price = float(buy_price)
    numeric_change = buy_price - start_price
    percent_change = numeric_change / start_price * 100
    return percent_change



def buylive(stock_symbol, current_price, pertradebudget):
    global trades_so_far
    print("BUYING:", stock_symbol)
    print("cur price:", current_price)
    print("pertradebud:", pertradebudget)
    bought = False
    attempts = 1
    while not bought and attempts < 5:
        try:
            quant_to_buy = (pertradebudget/current_price)
            quant_to_buy = round(quant_to_buy,2)
            print("Quant to buy", quant_to_buy)
            if quant_to_buy <= 0:
                return
            order = exchange.create_market_buy_order(stock_symbol,quant_to_buy)
            print("Order:",order)
            BOUGHT_STOCKS[stock_symbol] = [current_price, 0]

            BOUGHT_QUANTITIES[stock_symbol] = quant_to_buy
            trades_so_far += 1
            bought = True

        except:
            print("FAILED TO BUY :", quant_to_buy, "of", stock_symbol)
            print("Attempt Number:",attempts)
            attempts += 1

def moving_average_indicatorTF(stock_symbol, stock_data, current_price):
    print("Checking moving average")

    # SMA100_full = talib.SMA(stock_data['close'].values, 100)
    # SMA150_full = talib.SMA(stock_data['close'].values, 150)
    # SMA100_end = SMA100_full[-1:]
    # SMA150_end = SMA150_full[-1:]
    # SMA50_full = talib.SMA(stock_data['close'].values, 50)
    # SMA50_end = SMA50_full[-1:]
    SMA1_full = talib.SMA(stock_data['close'].values,10)
    SMA1_end = SMA1_full[-1:]


    if current_price > SMA1_end:
        print("Current price above moving average...")
        print("Current price:", current_price)
        print("Moving average:", SMA1_end)
        return True
    else:
        return False

def moving_average_strategy(symbols,tradenum,budget):
    print("Starting 'moving_average_strategy' buy strategy...")

    i = 0
    budget = budget - 1
    pertradebudget = budget / tradenum
    print("budget:", budget)
    print("tradenum:", tradenum)
    print("pertradebud:", pertradebudget)

    while i < len(symbols) and trades_so_far < tradenum:
        print("Trades so far", trades_so_far)
        print("Tradenum", tradenum)
        stock_symbol = symbols[i]
        print(stock_symbol)
        print("...")

        raw_data = exchange.fetch_ohlcv(stock_symbol, '1m')
        stock_data = pd.DataFrame(raw_data, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        current_row = stock_data[-1:]
        current_price_full = current_row['close']

        stock_data_low = stock_data['low']
        stock_data_high = stock_data['high']

        # 299 is the usual, but keys will vary, so we need the key of the dictanary, to access to element
        dic_key = list(current_price_full.keys())[0]

        current_price = current_price_full[dic_key]

        if moving_average_indicatorTF(stock_symbol, stock_data, current_price) == True:
            buylive(stock_symbol,current_price,pertradebudget)


        #print("PAUSING moving_average_strategy, could not pull moving average or could not buy")

        i += 1

    return trades_so_far




def rolling_bollinger(stock_symbol):
    #VERY INCOMPLETE, WAS WORKING ON MA FUNC
    raw_data = exchange.fetch_ohlcv(stock_symbol, '1m')

    stock_data = pd.DataFrame(raw_data, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    current_row = stock_data[-1:]
    current_price_full = current_row['close']

    stock_data_low = stock_data['low']
    stock_data_high = stock_data['high']

    # 299 is the usual, but keys will vary, so we need the key of the dictanary, to access to element
    dic_key = list(current_price_full.keys())[0]

    current_price = current_price_full[dic_key]

    condition_1 = False
    condition_2 = False

    SMA100_full = talib.SMA(stock_data['close'].values, 100)
    SMA150_full = talib.SMA(stock_data['close'].values, 150)
    SMA100_end = SMA100_full[-1:]
    SMA150_end = SMA150_full[-1:]
    SMA50_full = talib.SMA(stock_data['close'].values, 50)
    SMA50_end = SMA50_full[-1:]

    """"Basis of Conditions: 
        Entry: If the current price is close to, or slightly past the support line
        BUY. 
        If support line price is 99.8% of the current price, BUY 
        Exit: Exits are pretty much the same with the threshold"""

    upperband, middleband, lowerband = talib.BBANDS(stock_data['close'].values, 20, 2, 2)
    lowerband_end = lowerband[-1:]
    upperband_end = upperband[-1:]
    print("Upperband:")
    print(upperband)
    print("Lowerband")
    print(lowerband)
    print("Lowerband end")
    print(lowerband_end)
#screener

#the Mark Minervini Trend is not being used and is not very effective especially considering the alterations that must
#be made in order for it to operate
#does not have split 3 budget implemntaion
def screener_Mark_Minervini_Trend(symbols):
    i = 0
    picked_stock_list = []


    while i < len(symbols):

        stock_symbol = symbols[i]

        print(stock_symbol)
        print("...")

        raw_data = exchange.fetch_ohlcv(stock_symbol, '1d')
        stock_data = pd.DataFrame(raw_data, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        current_row = stock_data[-1:]
        current_price_full = current_row['close']

        stock_data_low = stock_data['low']
        stock_data_high = stock_data['high']


        #299 is the usual, but keys will vary, so we need the key of the dictanary, to access to element
        dic_key = list(current_price_full.keys())[0]

        current_price = current_price_full[dic_key]
        condition_1 = False
        condition_2 = False
        condition_3 = False
        condition_4 = False
        condition_5 = False
        condition_6 = False
        condition_7 = False

        condition_0 = True

        #Condition 1: Current Price > 150 SMA and > 200 SMA

        SMA100_full = talib.SMA(stock_data['close'].values, 100)
        SMA150_full = talib.SMA(stock_data['close'].values, 150)
        SMA100_end = SMA100_full[-1:]
        SMA150_end = SMA150_full[-1:]



        if current_price > SMA100_end and current_price > SMA150_end:
            condition_1 = True



        #Condition 2: 150 SMA and > 200 SMA

        if SMA100_end > SMA150_end:
            condition_2 = True

        #Condition 3: 200 SMA trending up for at least 1 month (ideally 4-5 months)
        SMA150_neg_one_month = SMA150_full[-30:]


        if SMA150_neg_one_month[0] < SMA150_end:
            condition_3 = True




        #Condition 4: 50 SMA> 150 SMA and 50 SMA> 200 SMA
        SMA50_full = talib.SMA(stock_data['close'].values, 50)
        SMA50_end = SMA50_full[-1:]

        if SMA50_end > SMA100_end and SMA50_end > SMA150_end:
            condition_4 = True




        #Condition 5: Current Price > 50 SMA

        if current_price > SMA50_end:
            condition_5 = True
        #Condition 6: Current Price is at least 30% above 52 week low (higher the better)

        the52weeklow = 10000000000

        for j in range(len(stock_data_low)):
            if stock_data_low[j] < the52weeklow:
                the52weeklow = stock_data_low[j]

        the52weeklow30percent = the52weeklow * 1.3

        if current_price > the52weeklow30percent:
            condition_6 = True



        #Condition 7: Current Price is within 25% of 52 week high
        the52weekhigh = 0

        for o in range(len(stock_data_high)):
            if stock_data_high[o] < the52weekhigh:
                the52weekhigh = stock_data_low[o]

        the52weekhigh75percent = the52weekhigh * 0.75
        if current_price >= the52weekhigh75percent:
            condition_7 = True

        if condition_0: #and condition_2 and condition_3 and condition_4 and condition_5 and condition_6 and condition_7:
         #This condition decides if this stock should be bought
         #BUY



            print("Con 0 satisfied")

            print(stock_symbol)
            picked_stock_list.append(stock_symbol)
            BOUGHT_STOCKS[stock_symbol]= [current_price,0]
            #Better way would be to call a quick function that buys the stock with this symbol
            #buystock(stock_symbol)
                #this function should add stock symbol to bought stocks if successful in buying at price
                #when adding to BUY_STOCKS, add the stock symbol as key, cur price as element

        i += 1

#screener_Mark_Minervini_Trend(symbols)
#^ test the screener



def biggest_percent_changers(symbols):
    print("Starting biggest_percent_changers")
    percent_change_list = []
    increment = 1
    for symb in symbols:
        print("Looping through symbols", increment)
        increment += 1
        try:
            raw_data = exchange.fetch_ohlcv(symb, '1m')

            stock_data = pd.DataFrame(raw_data, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
            # Timestamps are in 60 sec incremets, 720 timestamps, which is 12 hours


            first_row = stock_data[(int(len(stock_data)-(len(stock_data) / 3))):]
            #currently set up so that the first row is back 4 hours (line 480 should be)
            current_row = stock_data[-1:]

            current_price_full = current_row['close']
            first_price_full = first_row['close']

            dic_key_cur = list(current_price_full.keys())[0]
            dic_key_first = list(first_price_full.keys())[0]

            current_price = current_price_full[dic_key_cur]
            first_price = first_price_full[dic_key_first]

            change = percentage_change(first_price,current_price)

            percent_change_list.append({'symbol':symb,'percentchange':change})
        except:
            print("PAUSING SEARCH 'biggest_percent_changers' API not accessed or symbol not found")

    newlist = sorted(percent_change_list, key = lambda d: d['percentchange'], reverse=True)
    print("Final sorted list by percent change:", newlist)
    return newlist




#Buying the biggest percent changers
def buying_biggest_percent_changers(symbols, tradenum, budget):
    #WORK IN PROGRESS

    print("Starting 'buying_biggest_percent_changers' buy strategy...")
    print("Trades so far:", trades_so_far)
    budget = budget - 1
    pertradebudget = budget / tradenum
    print("budget:", budget)
    print("tradenum:", tradenum)
    print("pertradebud:", pertradebudget)

    symbols_to_buy = []

    percent_changers_list = biggest_percent_changers(symbols)

    for i in range(int(tradenum)):
        dic = percent_changers_list[i]
        dic_symbol = dic['symbol']
        dic_percent = dic['percentchange']

        if dic_percent > 1:
            symbols_to_buy.append(dic_symbol)

    print("FOUND SYMBOLS TO BUY:", symbols_to_buy)
    for symb in symbols_to_buy:

        try:
            raw_data = exchange.fetch_ohlcv(symb, '1m')

            stock_data = pd.DataFrame(raw_data, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
            current_row = stock_data[-1:]
            current_price_full = current_row['close']

            dic_key = list(current_price_full.keys())[0]
            current_price = current_price_full[dic_key]

            buylive(symb,current_price,pertradebudget)


        except:
            print("FAILED TO BUY", symb, "moving on to next")

    return trades_so_far



#OG StRat
def bouncing_off_support(symbols, tradenum, budget):
    print("Starting 'bouncing_off_support' buy strategy...")



    i = 0
    picked_stock_list = []
    budget = budget - 1
    pertradebudget = budget / tradenum
    print("budget:", budget)
    print("tradenum:",tradenum)
    print("pertradebud:",pertradebudget)


    while i < len(symbols) and trades_so_far < tradenum:
        print("Trades so far",trades_so_far)
        print("Tradenum",tradenum)
        stock_symbol = symbols[i]
        print(stock_symbol)
        print("...")

        try:
            raw_data = exchange.fetch_ohlcv(stock_symbol, '1m')

            stock_data = pd.DataFrame(raw_data, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
            current_row = stock_data[-1:]
            current_price_full = current_row['close']

            stock_data_low = stock_data['low']
            stock_data_high = stock_data['high']

            # 299 is the usual, but keys will vary, so we need the key of the dictanary, to access to element
            dic_key = list(current_price_full.keys())[0]

            current_price = current_price_full[dic_key]




            condition_1 = False
            condition_2 = False

            SMA100_full = talib.SMA(stock_data['close'].values, 100)
            SMA150_full = talib.SMA(stock_data['close'].values, 150)
            SMA100_end = SMA100_full[-1:]
            SMA150_end = SMA150_full[-1:]
            SMA50_full = talib.SMA(stock_data['close'].values, 50)
            SMA50_end = SMA50_full[-1:]

            """"Basis of Conditions: 
                Entry: If the current price is close to, or slightly past the support line
                BUY. 
                If support line price is 99.8% of the current price, BUY 
                Exit: Exits are pretty much the same with the threshold"""

            upperband, middleband, lowerband = talib.BBANDS(stock_data['close'].values, 20, 2, 2)
            lowerband_end = lowerband[-1:]

            #Condition 1

            if (current_price * .997) <= lowerband_end:
                if current_price < (lowerband_end * 0.98):
                    print("Current price too far less than 2% under the lowBB")
                else:
                    print("CONDITION_1 : SATISFIED")
                    print("Current Price: ", current_price)
                    print("Lowerband: ", lowerband_end)
                    condition_1 = True

            #Condition 2

            if current_price > SMA50_end:
                print("CONDITION_2 : SATISFIED")
                condition_2 = True


            if condition_1 and condition_2:
             #This condition decides if this stock should be bought
             #BUY

                print("Current Price is higher than SMA50")
                print("price: ", current_price, "sma50: ", SMA50_end)


                print("Con 1 and Con 2 satisfied")

                print(stock_symbol)
                picked_stock_list.append(stock_symbol)


                #UNCOMMENT THIS WHEN GOING LIVE
                #exchange.create_market_buy_order(stock_symbol, stock_quantity)
                #BOUGHT_QUANTITIES[stock_symbol] = stock_quantity

                #BOUGHT_STOCKS[stock_symbol]= [current_price,0]
                    #Sets the starting price, sell price should be updated
                #Better way would be to call a quick function that buys the stock with this symbol
                #buystock(stock_symbol)
                    #this function should add stock symbol to bought stocks if successful in buying at price
                    #when adding to BUY_STOCKS, add the stock symbol as key, cur price as element

                buylive(stock_symbol,current_price,pertradebudget)


            i += 1
        except:
            print("PAUSING BUY: Could not retrieve API data from internet")
    return trades_so_far






#SELLER PAPER FUNCTION

def seller_paper(stock_symbol):
    raw_data = exchange.fetch_ohlcv(stock_symbol, '1m')
    stock_data = pd.DataFrame(raw_data, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    current_row = stock_data[-1:]
    current_price_full = current_row['close']
    dic_key = list(current_price_full.keys())[0]
    current_price = current_price_full[dic_key]

    (BOUGHT_STOCKS[stock_symbol])[1] = current_price

    buy_price = (BOUGHT_STOCKS[stock_symbol])[0]
    sell_price = (BOUGHT_STOCKS[stock_symbol])[1]
    profit = percentage_change(buy_price,sell_price)

    print("Percentage profit made from ", stock_symbol, ": ", profit)
    print("Bought at: ", buy_price)
    print("Sell at: ", sell_price)
    PROFIT_PERCENT_LIST.append(profit)
    COMPLETED_TRADES[stock_symbol] = [buy_price,sell_price]

def seller_live(stock_symbol):
    print("Selling:",stock_symbol)
    raw_data = exchange.fetch_ohlcv(stock_symbol, '1m')
    stock_data = pd.DataFrame(raw_data, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    current_row = stock_data[-1:]
    current_price_full = current_row['close']
    dic_key = list(current_price_full.keys())[0]
    current_price = current_price_full[dic_key]

    (BOUGHT_STOCKS[stock_symbol])[1] = current_price

    quantity = BOUGHT_QUANTITIES[stock_symbol]
    #need to figure out how to get quantities
    order = exchange.create_market_sell_order(stock_symbol,quantity)
    print("Order:", order)
    del BOUGHT_QUANTITIES[stock_symbol]

    buy_price = (BOUGHT_STOCKS[stock_symbol])[0]
    sell_price = (BOUGHT_STOCKS[stock_symbol])[1]
    profit = percentage_change(buy_price, sell_price)

    print("Percentage profit made from ", stock_symbol, ": ", profit)
    print("Bought at: ", buy_price)
    print("Sell at: ", sell_price)
    PROFIT_PERCENT_LIST.append(profit)
    COMPLETED_TRADES[stock_symbol] = [buy_price, sell_price]


#don't actually sell for now, just subtract the buy price from the sell price
#and take a fake profit.


#Threshold function
def threshold_function(stock_symbol):
    if (THRESHOLD_MAX_VS_NOW[stock_symbol])[0] > ((((THRESHOLD_MAX_VS_NOW[stock_symbol])[1]) * 0.996)):
        #SELL
        #add now price to BOUGHT STOCks, call selling paper


        print("Satisfies sell command: PASSED THRESHOLD FUNCTION")
        seller_live(stock_symbol)
        #perform sell fucntion
    #this can be improved, as price goes on a run, may want to sell after less of a drop down







#selling_scanner()


def gen_selling_scanner(buy_time):
    print("Buy time: ",buy_time )
    sell_time = buy_time + 36000
    print("Sell time:", sell_time)
    stop_loss_notification = False
    for p in BOUGHT_STOCKS:
        THRESHOLD_MAX_VS_NOW[p] = [0,0]
        print(THRESHOLD_MAX_VS_NOW[p])
        print(p)
    for k in BOUGHT_STOCKS:
        THRESHOLD_PASSED_TF[k] = False
    while sell_time > time.time():
        print("Performing Scan")

        print(BOUGHT_STOCKS)
        print(PROFIT_PERCENT_LIST)

        if time.time() >= buy_time + 1800 and not stop_loss_notification:
            print("STOP LOSS in market time commitment fulfilled, now allowing stop loss conditions to satisfy")
            stop_loss_notification = True

        for i in BOUGHT_STOCKS:
            cur_time = time.time()
            sell_command = False

            threshold_passed = THRESHOLD_PASSED_TF[k]
            stock_symbol = i
            starting_price = (BOUGHT_STOCKS[stock_symbol])[0]

                #Gets the new current price
            try:
                raw_data = exchange.fetch_ohlcv(stock_symbol, '1m')
                stock_data = pd.DataFrame(raw_data, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
                current_row = stock_data[-1:]
                current_price_full = current_row['close']
                dic_key = list(current_price_full.keys())[0]
                current_price = current_price_full[dic_key]

                print(stock_symbol)
                print("start price:", starting_price)
                print("current price:", current_price)


                if current_price >= (starting_price * 1.015):
                    THRESHOLD_PASSED_TF[stock_symbol] = True
                    print("Added to ",stock_symbol,"to threshold")

                    #Profit has been achieved, run till it starts to drop
                    #call threshold function next , only on the current stock, check if price has dropped since max.
                if THRESHOLD_PASSED_TF[stock_symbol] is True:
                    (THRESHOLD_MAX_VS_NOW[stock_symbol])[1] = current_price

                    print("Updated threshold NOW price on:", stock_symbol)
                    if current_price > (THRESHOLD_MAX_VS_NOW[stock_symbol])[0]:
                        (THRESHOLD_MAX_VS_NOW[stock_symbol])[0] = current_price

                        print("Updated threshold MAX price on:", stock_symbol)

                    #going to need a new threshold function for these
                    print("Entering threshold_fucntion...")
                    threshold_function(stock_symbol)
                elif current_price <= (starting_price * 0.99) and (buy_time + 900) < cur_time:
                    #this condition is the stop loss, currently having it run for 30 minutes before calling it quits
                    sell_command = True
                    print("Satisfies sell command: STOP LOSS")
                elif cur_time > (buy_time + 43200) and threshold_passed == False:
                    #Sells all non threshold stocks after 12 hours
                    sell_command = True
                    print("Satisfies sell command: 12 hours passed THRESHOLD == FALSE")

                if sell_command:
                    #perform sell action
                    #make this a new function

                    print("Sell", stock_symbol)


                    # print("Before updated sell price",BOUGHT_STOCKS[stock_symbol])
                    # (BOUGHT_STOCKS[stock_symbol])[1] = current_price
                    # print("After",BOUGHT_STOCKS[stock_symbol])
                    # TESTING DELETE THIS ^

                    seller_live(stock_symbol)
            except:
                print("PAUSING SELL: Could not retrieve API data from internet")
        if len(BOUGHT_STOCKS) == 0:
            print("All bought stocks have been SOLD without clearsell, ending selling_scanner...")
            return
        for i in COMPLETED_TRADES:
            #this clears the stock from BOUGHT_STOCKS if it has already been sold
            if i in BOUGHT_STOCKS:
                del BOUGHT_STOCKS[i]

def clearsell_inventory():
    print("NOTICE: ")
    print("Timer has run out, force selling all remaining stocks")
    print("....")
    print(".....")
    for i in BOUGHT_STOCKS:
        #seller_paper(i)
        seller_live(i)
    # for i in COMPLETED_TRADES:
    #         # this clears the stock from BOUGHT_STOCKS if it has already been sold
    #     if i in BOUGHT_STOCKS:
    #         del BOUGHT_STOCKS[i]
    print("All bought stocks have been SOLD, ending selling_scanner...")
#setting up coinbas client
#client = Client("g4g00cgecr7JswC6","Vjsnz6auhlwDxAGMMxuwFVXIEMYORmyH")
#payment_method = client.get_payment_methods()[0] //Used to grab payment ID to actually make the purchase

#Take user input
# user_limit_order = float(input("Enter a price for you coin limit order (USD): "))
# user_amount_spent = float(input("Enter how much you want to spend (USD): "))

#Creating the loop
#currency_code = 'USD'

#start_price = client.get_spot_price(currency = currency_code)


# while(True):
#
#     #Reset currents and find percentage change
#     buy_price = client.get_buy_price(currency = currency_code)
#     percentage_gainloss = percentage_change(start_price.amount,buy_price.amount)
#
#     #print bitcoin current price, and percentage change
#     print("Bitcoin is " + str(buy_price) + "\nPercent change in last 60 seconds: " + format(percentage_gainloss, ".3f") + '%')
#
#     if(float(buy_price.amount) <= user_limit_order):
#
#         print("Bought $" + str(user_amount_spent) + " or " + str(user_amount_spent / float(buy_price.amount )) + " bitcoin at " + buy_price.amount)
#     sleep(60)
#
#     start_price = buy_price

def start_day(symbols):
    print("Starting new day...")

    print(symbols)
    balance_before = exchange.fetch_balance()['info']
    print("Balance",balance_before)
    trade_num = 0
    while trade_num == 0:
        trade_num = bouncing_off_support(symbols, float(1),float(15))
    buy_time = time.time()
    gen_selling_scanner(buy_time)
    if len(BOUGHT_STOCKS) > 0:
        clearsell_inventory()
    print("BOUGHT_STOCKS:",BOUGHT_STOCKS)
    sum = 0
    count = 0
    for i in PROFIT_PERCENT_LIST:
        sum = sum + i
        count += 1
    average_profit = sum / count
    print("Average percentage profit: ", average_profit)
    balance_after = exchange.fetch_balance()['info']
    print("Balance Before:", balance_before)
    print("Balance After:", balance_after)
    print("FINISHED")

    return average_profit


def main():
    global COMPLETED_TRADES, PROFIT_PERCENT_LIST, BOUGHT_STOCKS, BOUGHT_QUANTITIES, trades_so_far
    start_time = time.time()
    daycount = 1

    symbols = SYMBOLS_GLOBAL
    while time.time() < (start_time +86400):
        COMPLETED_TRADES = {}
        PROFIT_PERCENT_LIST = []
        BOUGHT_STOCKS = {}
        BOUGHT_QUANTITIES = {}
        trades_so_far = 0
        print("Day:",daycount)
        symbols_to_send = symbols
        profit = start_day(symbols_to_send)
        if profit < 0:
            print("Profit failed, removing these stocks:", BOUGHT_STOCKS)
            for i in BOUGHT_STOCKS:
                print("Symbols before remove", symbols)
                symbols.remove(i)
                print("Symbols after remove", symbols)
        daycount += 1

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
