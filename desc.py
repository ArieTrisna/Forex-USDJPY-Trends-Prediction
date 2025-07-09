import streamlit as st

def render():
    ## ------- Explain What is Forex --------------
    st.header("What is Forex?", divider=True)
    st.image('./Images/pexels-energepic-com-27411-159888.jpg')

    forex_explanation = '''
    Forex, a portmanteau of foreign and exchange, is where banks, businesses, governments, investors, and individuals buy or sell currencies. Whenever you purchase something in another currency or exchange cash to get the local money of your vacation destination, you’re taking part in the forex or foreign exchange (FX) market. Businesses and individuals often do this while investors trade currencies to profit from fluctuating exchange rates.  
    Forex is the largest and most liquid market in the world. Participants in this global electronic marketplace traded about $7.5 trillion per day in 2022, far exceeding the daily trading volumes of the world stock market.
    '''
    st.markdown(f'<div style="text-align: justify;">{forex_explanation}</div>', unsafe_allow_html=True)

    ## -------- Pairing ---------
    st.header("Forex Pair", divider=True)
    forex_pair = '''
    In the forex market, currencies are traded in pairs. That means when you buy one currency you are simultaneously selling another one—and vice versa.
    For each currency pair, there is an exchange rate, indicating how much of the quote currency is needed to buy one unit of the base currency.
    '''
    st.markdown(f'<div style="text-align: justify;">{forex_pair}</div>', unsafe_allow_html=True)

    st.subheader("USD/JPY Pair", divider=True)
    st.image('./Images/pexels-luoqing-29916107.jpg')
    usdjpy_pair = '''
    So for this project I'm using USD/JPY Pair for a moment to analyze and build a model that can predict if the price will go up or down in the future using classification model.

    1 = up  
    0 = down
    '''
    st.markdown(usdjpy_pair)