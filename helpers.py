from jina import Document, DocumentArray, Client
import pandas as pd
import streamlit as st


def get_data(index_path):
    da = DocumentArray.load(index_path)
    df = da.to_dataframe()

    df["doc_id"] = df["id"].apply(lambda x: x[:8])
    df["datetime"] = df["tags"].apply(lambda x: x.get("dt"))
    df["known_label"] = df["tags"].apply(lambda x: x.get("known_label"))
    df["port"] = df["tags"].apply(lambda x: int(x.get("port")))
    df["protocol"] = df["tags"].apply(lambda x: int(x.get("protocol")))
    df["known_label"] = df["known_label"].map(lambda x: "Benign" if x == 0.0 else "Attack")
    df["predicted"] = get_predictions()
    df['is_wrong'] = df.apply(lambda x: x['predicted'] != x['known_label'], axis=1)
    return df

def filter_by_date(df, start_date, end_date):
    df_filtered = df.loc[(df.Timestamp.dt.date >= start_date) & (df.Timestamp.dt.date <= end_date)]
    return df_filtered

def get_client():
    return Client(port="12345")

def get_predictions():
    """
    ***Need to have query_flow.py running in seperate file for this fxn to work.***
    """
    client = get_client()
    results =  client.post("/predict", return_results=True)
    return [doc.tags.get("preds") for doc in results]

def set_bg_hack_url(url: str) -> None:
    '''
    A function to unpack an image from url and set as bg.
    Returns
    -------
    The background.
    '''
        
    st.markdown(
         f"""
         <style>
         .stApp {{
             background: url({url});
             background-size: cover
         }}
         </style>
         """,
         unsafe_allow_html=True
     )

