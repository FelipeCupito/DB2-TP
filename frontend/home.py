import streamlit as st
import requests
import json

if 'cbu' not in st.session_state:
    st.session_state.cbu = ""
if 'to_cbu' not in st.session_state:
    st.session_state.to_cbu = ""
if 'amount' not in st.session_state:
    st.session_state.amount = ""

st.title("🏦 Banco")

cbu = st.text_input(label="CBU:")
login = st.button("Ingresar ➡")
if login:
    url = "http://127.0.0.1:8000/users/" + cbu
    res = requests.get(url)
    if res.status_code != 200:
        st.warning("Usuario no encontrado. Por favor verifique el CBU ingresado.")
    else:
        st.session_state.cbu = cbu
        res_dict = json.loads(res.text)
        name = res_dict["name"]
        welcome_msg = "Hola, " + name + "!"
        st.write(welcome_msg)

if st.session_state.cbu:
    cols = st.columns(2)
    with cols[0]:
        balance = st.button("Consultar Balance 💰")
        if balance:
            st.session_state.cbu = cbu
            url = "http://127.0.0.1:8000/users/" + st.session_state.cbu + "/balance"
            amount = requests.get(url)
            st.write("$" + amount.text)
    cols = st.columns(2)
    with cols[0]:
        st.session_state.to_cbu = st.text_input("CBU Destinatario:")
    with cols[1]:
        st.session_state.amount = st.text_input("Monto:")
    pay = st.button("Pagar 💵")
    if pay:
        url_pay = "http://127.0.0.1:8000/transactions/" + st.session_state.cbu + "/pay"
        url_charge = "http://127.0.0.1:8000/transactions/" + st.session_state.to_cbu + "/charge"
        params = {"amount": float(st.session_state.amount)}
        res_pay = requests.post(url_pay, params=params)
        res_charge = requests.post(url_charge, params=params)
        if res_pay.status_code != 200 or res_charge.status_code != 200:
            st.warning("Pago no realizado. Consultar saldo y/o verifique el CBU del destinatario.")
        else:
            st.success("Pago realizado!")
