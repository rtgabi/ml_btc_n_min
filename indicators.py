import pandas as pd

# create dataframe
def create_df(data: list):
    df=pd.DataFrame(data, columns=['open_timestamp', 'open', 'high', 'low', 'close',
                                   'volume', 'close_timestamp', 'quote_asset_volume',
                                   'n_trades', 'taker_buy_base_asset_vol', 'taker_buy_quote_asset_vol',
                                   'ignore'])
    
    df.drop(columns=['quote_asset_volume', 'taker_buy_base_asset_vol',
                     'taker_buy_quote_asset_vol', 'ignore'], inplace=True)
    
    for i in ['open', 'close', 'low', 'high', 'volume']:
        df[i]=pd.to_numeric(df[i])
    
    return df

# add ema(s)
def add_ema(df: pd.DataFrame, *emas: int):
    for ema in emas:
        df[f'ema_{ema}']=df['close'].ewm(span=ema, min_periods=ema).mean()

# compute rsi
def rsi(df: pd.DataFrame, period: int=14):
    price_diff=df['close'].diff()
    gain=(price_diff.where(price_diff>0, 0)).rolling(window=period).mean()
    loss=(-price_diff.where(price_diff<0, 0)).rolling(window=period).mean()

    rs=gain/loss
    df['rsi']=100-(100/(1+rs))

# compute macd
def macd(df:pd.DataFrame, short: int=12, long: int=26, signal: int=9):
    short_ema=df['close'].ewm(span=short, adjust=False).mean()
    long_ema=df['close'].ewm(span=long, adjust=False).mean()

    df['macd_line']=short_ema-long_ema
    df['signal_line']=df['macd_line'].ewm(span=signal, adjust=False).mean()

# compute bollinger bands
def bollinger_bands(df: pd.DataFrame, period: int=20):
    copy=df.copy()
    copy['sma']=df['close'].rolling(window=period).mean()
    df['upper_band']=copy['sma']+(df['close'].rolling(window=period).std()*2)
    df['lower_band']=copy['sma']+(df['close'].rolling(window=period).std()*2)

# compute stochastic oscillator
def stochastic_oscillator(df: pd.DataFrame, k_period=14, d_period=3):
    high=df['high'].rolling(window=k_period).max()
    low=df['low'].rolling(window=k_period).min()
    df['k']=100*((df['close']-low)/(high-low))
    df['d']=df['k'].rolling(window=d_period).mean()

# compute average true range
def wwma(values: pd.Series, alpha: int):
    return values.ewm(alpha=1/alpha, min_periods=alpha, adjust=False).mean()

def atr(df: pd.DataFrame, period=14):
    copy=df.copy()
    high=copy['high']
    low=copy['low']
    close=copy['close']

    copy['tr_0']=abs(high-low)
    copy['tr_1']=abs(high-low.shift())
    copy['tr_2']=abs(low-close.shift())

    tr=copy[['tr_0', 'tr_1', 'tr_2']].max(axis=1)
    df['atr']=wwma(tr, period)

# compute chaikin money flow
def chaikin_money_flow(df: pd.DataFrame, period=20):
    copy=df.copy()
    copy['money_flow_multiplier']=((copy['close']-copy['low'])-(copy['high']-copy['close']))/(copy['high']-copy['low'])
    copy['money_flow_volume']=copy['money_flow_multiplier']*copy['volume']
    
    df['cmf']=copy['money_flow_volume'].rolling(window=period).sum()/copy['volume'].rolling(window=period).sum()