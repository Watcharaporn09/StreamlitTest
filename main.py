import streamlit as st
import pandas as pd
import datetime as dt

from pathlib import Path


st.sidebar.header('Input Features')

def input_features():
    age = st.sidebar.number_input("Age (yrs)", value = 0)
    hema = st.sidebar.radio("Hematemesis",["Yes","No"])
    hb = st.sidebar.number_input("Hemoglobin level (g/dL)", value = 0.00)

    data = {'Age': age,
            'Hematemesis': hema,
            'Hemoglobin': hb}

    features = pd.DataFrame(data, index=[0])
    return features


df = input_features()

st.write('Input values from sidebar')
st.dataframe(df)

st.write(df.eq(0).any().any())

# Current Directory of Output file
myfile = Path('./out.csv')


if st.sidebar.button('Predict'):
    # Check whether there is a zero in the dataframe or not.
    # If there is a zero in the dataframe, Do nothing.
    if df.eq(0).any().any():
        st.write('Some values are Zeros')
    else:
        st.write('Ready for Prediction')

        outdf = pd.DataFrame([{'Timestamp': dt.datetime.now()}])
        outdf = pd.concat([outdf, df], axis=1)

        # Assume the predicted value and the probabilities for all classes
        outdf['Predicted Value'] = 1
        outdf['Prob for Negative class'] = 0.4
        outdf['Prob for Positive class'] = 0.6

        st.write(outdf)

        if myfile.is_file():
            st.write('File Existed')
            outdf.to_csv('out.csv', mode='a', index=False, header=False)
        else:
            st.write('File Not Found!')
            outdf.to_csv('out.csv', index=False)

        collecteddf = pd.read_csv('out.csv')

        st.download_button(
            label="Download CSV",
            data=collecteddf.to_csv().encode("utf-8"),
            file_name="collecteddata.csv",
            mime="text/csv"
        )

