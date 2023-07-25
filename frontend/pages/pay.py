"""    
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
"""    