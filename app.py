# Dependencies
import streamlit as st

# ------------------ Streamlit Layout -------------------
import desc
import technical
import prediction

st.title("Forex USD/JPY Pair Price Direction Prediction")
tab1, tab2, tab3 = st.tabs(["🗎Description", "📊Technical Indicator", "🔎Prediction"])

with tab1:
    desc.render()

with tab2:
    technical.render()

with tab3:
    prediction.render()




# if st.button('Load'):
#     df = feature_engineering()
#     st.dataframe(df.tail(5))
#     st.write(predictors)

# if st.button("Predict"):
#     prediction = model.predict(df[predictors])
#     if prediction[0] == 1:
#         st.success("Prediction: Price will go UP 📈")
#     else:
#         st.error("Prediction: Price will go DOWN 📉")
