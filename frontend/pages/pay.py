import json
import requests
import streamlit as st

if 'cbu' not in st.session_state:
    st.session_state.cbu = ""
if 'alias' not in st.session_state:
    st.session_state.alias = ""

st.set_page_config(page_title="💵 Pay")
st.header("💵 Pay")

st.info("Be sure to log in before making a payment.")

tab1, tab2 = st.tabs(["By CBU", "By Alias"])

payment_by_cbu = {}
with tab1:
    with st.form("pay_by_cbu"):
        amount = st.text_input("Amount:")
        password = st.text_input("Password:", type="password")
        to_cbu = st.text_input("Recipient CBU:")
        submitted = st.form_submit_button("Submit")
        if submitted:
            payment_by_cbu["amount"] = float(amount)
            payment_by_cbu["from_cbu"] = st.session_state.cbu
            payment_by_cbu["password"] = password
            payment_by_cbu["to_cbu"] = to_cbu
            payment_json = json.dumps(payment_by_cbu)
            res = requests.post("http://127.0.0.1:8000/transactions/pay-cbu", data=payment_json)
            if res.status_code == 200:
                st.success("Payment completed!")
                url_user = "http://127.0.0.1:8000/users/cbu/" + to_cbu
                res_user = requests.get(url_user)
                user_dict = json.loads(res_user.text)
                name = user_dict["data"]["name"]
                cuit = user_dict["data"]["cuit"]
                alias = user_dict["data"]["alias"]
                with st.expander("Transaction Details"):
                    st.write("Recipent Name: " + name)
                    st.write("Recipent CUIT: " + cuit)
                    st.write("Recipent Alias: " + alias)
                    st.write("Amount: $" + str(amount))
            else:
                st.warning("Payment incomplete. Please check the recipent's CBU")

payment_by_alias = {}
with tab2:
    with st.form("pay_by_alias"):
        amount = st.text_input("Amount:")
        password = st.text_input("Password:", type="password")
        to_alias = st.text_input("Recipient Alias:")
        submitted = st.form_submit_button("Submit")
        if submitted:
            payment_by_alias["amount"] = float(amount)
            payment_by_alias["from_alias"] = st.session_state.alias
            payment_by_alias["password"] = password
            payment_by_alias["to_alias"] = to_alias
            payment_json = json.dumps(payment_by_alias)
            res = requests.post("http://127.0.0.1:8000/transactions/pay-alias", data=payment_json)
            if res.status_code == 200:
                st.success("Payment completed!")
            else:
                st.warning("Payment incomplete. Please check the recipent's CBU")