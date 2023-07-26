import json
import streamlit as st
import requests
import pandas as pd

if 'cbu' not in st.session_state:
    st.session_state.cbu = ""
if 'alias' not in st.session_state:
    st.session_state.alias = ""
if 'to_cbu' not in st.session_state:
    st.session_state.to_cbu = ""
if 'amount' not in st.session_state:
    st.session_state.amount = ""

transactions = {
    "Date": [],
    "Alias": [],
    "Name": [],
    "CBU": [],
    "Amount": []
}

st.set_page_config(page_title="🏠 Home")
st.title("🧚Pixie")

st.subheader("The N°1 payment platform in Argentina" )

cbu = st.text_input(label="CBU:")
login = st.button("Enter ➡")
if login:
    url = "http://127.0.0.1:8000/users/cbu/" + cbu
    res = requests.get(url)
    res_dict = json.loads(res.text)
    if res.status_code != 200 or res_dict["data"] is None:
        st.warning("User not found. Please verify the CBU.")
    else:
        st.session_state.cbu = cbu
        name = res_dict["data"]["name"]
        cuit = res_dict["data"]["cuit"]
        alias = res_dict["data"]["alias"]
        st.session_state.alias = alias
        welcome_msg = "Hello, " + name + "!"
        cuit_msg = "CUIT: " + cuit
        alias_msg = "Alias: " + alias
        st.write(welcome_msg)
        st.write(cuit_msg)
        st.write(alias_msg)
        url = "http://127.0.0.1:8000/users/" + st.session_state.cbu + "/balance"
        res = requests.get(url)
        res_dict = json.loads(res.text)
        balance = res_dict["data"]
        if balance is None:
            st.write("Balance: $0" )
        else:
            st.write("Balance: $" + str(balance))
        with st.expander("Transaction History"):
            url_hist = "http://127.0.0.1:8000/transactions/" + st.session_state.cbu + "/history"
            res_hist = requests.get(url_hist)
            hist_dict = json.loads(res_hist.text)
            history = hist_dict["data"]
            if history is None:
                st.write("No transactions")
            else:
                for i in range(0, len(hist_dict["data"])):
                    transaction = hist_dict["data"][i]
                    transactions["Date"].append(transaction["date"])
                    transactions["Alias"].append(transaction["to_user"]["alias"])
                    transactions["Name"].append(transaction["to_user"]["name"])
                    transactions["CBU"].append(transaction["to_user"]["cbu"])
                    transactions["Amount"].append(transaction["amount"])
                transactions_df = pd.DataFrame.from_dict(transactions)
                st.table(transactions_df)
                