import json
import requests
import streamlit as st

st.set_page_config(page_title="🧑🏻 Create User")
st.header("🧑🏻 Create User")

new_user = {}

url = "http://127.0.0.1:8000/banks/all"
res = requests.get(url)
res_dict = json.loads(res.text)
banks = []
for i in range(0,len(res_dict["data"])):
    banks.append(res_dict["data"][i]["name"])

with st.form("create_user"):
    st.write("Complete the following fields:")
    alias = st.text_input("Alias:")
    alias_type = st.selectbox("Alias Type:", options=["email", "phone", "nickname"])
    bank_name = st.selectbox("Bank Name:", options=banks)
    cbu = st.text_input("CBU:")
    cuit = st.text_input("CUIT:")
    name = st.text_input("Name:")
    password = st.text_input("Password:", type="password")

   # Every form must have a submit button.
    submitted = st.form_submit_button("Submit")
    if submitted:
        new_user["alias"] = alias
        new_user["alias_type"] = alias_type
        new_user["bank_name"] = bank_name
        new_user["cbu"] = cbu
        new_user["cuit"] = cuit
        new_user["name"] = name
        new_user["password"] = password
        json_user = json.dumps(new_user)
        res = requests.post("http://127.0.0.1:8000/users/register", data=json_user)
        if res.status_code == 200:
            st.success("User successfully created!")
        else:
            st.warning("User not created. Please check values.")