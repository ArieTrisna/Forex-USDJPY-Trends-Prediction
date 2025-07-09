import streamlit as st
import pandas as pd
import joblib 
from sklearn.ensemble import GradientBoostingClassifier
from dotenv import load_dotenv
from twelvedata import TDClient
import os

# ------------------ Data Pull and Feature Engineering --------------
## --------- Credentials --------
def configure():
    load_dotenv()

## ----------- Data Pull ----------
def data_get():
    configure()
    td = TDClient(apikey=os.getenv('api_key'))      # Initialize client - apikey parameter is requiered
    ts = td.time_series(                            # Construct the necessary time series
        symbol="USD/JPY",
        interval="1day",
        outputsize=5000,
        timezone="UTC",
        )
    usdjpy_daily_df = ts.as_pandas()                
    return usdjpy_daily_df                          # Returns pandas.DataFrame

## ------------ Data Transform --------
def transform():
    df = data_get()
    df = df.sort_index(ascending=True)
    df['tomorrow'] = df['close'].shift(-1)
    df['target'] = (df['tomorrow'] > df['close']).astype(int)
    return df                                                                   # Return Transformed DataFrame

## ------------ Feature Engineering -------
def feature_engineering():
    df = transform()
    horizons = [2, 5, 60, 250, 1000]
    predictors = []
    for horizon in horizons:
        rolling_averages = df.rolling(horizon).mean()

        ratio_column = f'Close_Ratio{horizon}'
        df[ratio_column] = df['close'] / rolling_averages['close']

        trend_column = f'Trend_{horizon}'
        df[trend_column] = df.shift(1).rolling(horizon).sum()['target']

        predictors += [ratio_column, trend_column]
    
    df = df.dropna()
    return df, predictors                                                          # Returns Featured DataFrame and Predictors

# ----------- Load the trained model -----------------
def render():
    model = joblib.load("gradient_boost_classifier.pkl")
    df, predictors = feature_engineering()

    # ----------- Data Overview ---------------------
    st.header('Data Overview', divider=True)
    st.dataframe(df.tail(10))

    # -------------- Model Comparison ----------------
    st.header("Model Comparison", divider=True)
    model_comparison = '''
    Models:
    1. Random Forest Classifier  
    2. Gradient Boosting Classifier  
    3. K Nearest Neighbor  
    4. XGBoost Classifier  
    5. Decision Tree Classifier  

    For comparing these models, I'm using Accuracy and Precision Score
    '''
    st.markdown(model_comparison)
    st.image('./Images/model_comparison.png', caption="Evaluation Metrics Result")
    st.write("Based on the comparison we can see that Gradient Boost is the highest overall so for this prediction we are using Gradient Boost Classifier")

    # ------------ Making Predictions ----------------
    st.header("Predict", divider=True)
    st.subheader("Please Click This Button to Predict")
    
    X = df[predictors]
    y = df['target']

    if st.button("PREDICT"):
        latest_prediction = model.predict(X.tail(1))[0]
        st.success(f"📊 Prediction for Next Day: {'⬆️ Up' if latest_prediction == 1 else '⬇️ Down'}")
        st.warning("Trade At Your Own Risk", icon='⚠️')


