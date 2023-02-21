USER_NAME = "pradylearner@gmail.com"
PWD="#chartink123"

telegram_bot_api_id = '5210233677:AAF2-qncOC1J87VTe4jfRv7OFBATALl36V8'
telegram_chat_id = '@eodsignals'


C_LNK = "https://chartink.com/screener/"
C_PR_URL = 'https://chartink.com/screener/process'

eod_queries = { "Potential Movers " :"( {33489} ( ( {33489} ( ( {33489} ( ( latest open - latest close ) <= ( latest high - latest low ) * 0.2 and latest open >= latest close ) ) or ( {33489} ( ( latest close - latest open ) <= ( latest high - latest low ) * 0.2 and latest close >= latest open ) ) ) ) and ( {33489} ( ( {33489} ( ( 1 day ago open - 1 day ago close ) <= ( 1 day ago high - 1 day ago low ) * 0.2 and 1 day ago open >= 1 day ago close ) ) or ( {33489} ( ( 1 day ago close - 1 day ago open ) <= ( 1 day ago high - 1 day ago low ) * 0.2 and 1 day ago close >= 1 day ago open ) ) ) ) and latest high > latest low and latest volume > 10000 and latest close > 100 and latest close < 1500 ) ) ",
"Evening Star ":"( {cash} ( latest open > latest close and latest open < 1 day ago close and 1 day ago open > 1 day ago close and 1 day ago close > 2 days ago close and 2 days ago close > 3 days ago close and 3 days ago open < 3 days ago close ) ) ",
"Bearish Engulfing " : "( {33489} ( 1 day ago close > 1 day ago open and latest close < 1 day ago open and latest open > 1 day ago close ) ) ",
"Bullish Engulfing " : "( {cash} ( 1 day ago close < 1 day ago open and latest close > 1 day ago open and latest open < 1 day ago close and latest close > 50 and latest volume > 50000 and abs ( latest close - 1 candle ago close / 1 candle ago close * 100 ) < 2.5 ) ) ",
"Morning Star ": "( {cash} ( latest open < latest close and latest open > 1 day ago close and 1 day ago open < 1 day ago close and 1 day ago close < 2 days ago close and 2 days ago open > 2 days ago close and 2 days ago close < 3 days ago close and 3 days ago open > 3 days ago close ) ) "
}  
bullrun = {"Bull Charge":"( {57960} ( [0] 5 minute close > 1 day ago high and latest low > 1 day ago close and latest open > 1 day ago close and latest volume > latest sma ( latest volume , 20 ) * 1.2 and 1 day ago open > 1 day ago close and 1 day ago close > 1 day ago low * 0.95 and latest volume > 70000 and latest close > 50 and latest close < 900 ) )   "}
                
bullEng = {"Engulfing Bull": "( {33489} ( [0] 15 minute close >  [0] 15 minute open and [-1] 15 minute open > [-1] 15 minute close and  [0] 15 minute open < [-1] 15 minute close and [0] 15 minute close > [-1] 15 minute open and latest volume > 50000 ) ) "} 

bearEng = {"Engulfing Bear":"( {33489} ( [0] 15 minute close < [0] 15 minute open and [-1] 15 minute open < [-1] 15 minute close and  [0] 15 minute open > [-1] 15 minute close and [0] 15 minute close < [-1] 15 minute open and latest volume > 50000 ) ) " }