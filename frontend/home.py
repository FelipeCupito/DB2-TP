# import streamlit as st
# import requests
# import json
# import pandas as pd

# # Define page configuration
# st.set_page_config(page_title="User Authentication and Dashboard")

# # Define session states
# if 'authenticated' not in st.session_state:
#     st.session_state.authenticated = False
# if 'cbu' not in st.session_state:
#     st.session_state.cbu = ""
# if 'alias' not in st.session_state:
#     st.session_state.alias = ""
# if 'password' not in st.session_state:
#     st.session_state.password = ""
# if 'transaction_data' not in st.session_state:
#     st.session_state.transaction_data = {}
# if 'user_data' not in st.session_state:
#     st.session_state.user_data = {}

# # Get list of banks
# url = "http://127.0.0.1:8000/banks/all"
# res = requests.get(url)
# res_dict = json.loads(res.text)
# banks = [bank["name"] for bank in res_dict["data"]]

# # Helper function for authentication
# def authenticate_user(cbu, password):
#     url = f"http://127.0.0.1:8000/users/cbu/{cbu}?password={password}"
#     res = requests.get(url)
#     res_dict = json.loads(res.text)
#     if res.status_code == 200 and res_dict["data"] is not None:
#         st.session_state.authenticated = True
#         st.session_state.cbu = cbu
#         st.session_state.password = password
#         st.session_state.user_data = res_dict["data"]
#         return True
#     else:
#         return False

# # Helper function to register a new user
# def register_user(name, cuit, cbu, alias, alias_type, bank_name, password):
#     new_user = {
#         "name": name,
#         "cuit": cuit,
#         "cbu": cbu,
#         "alias": alias,
#         "alias_type": alias_type,
#         "bank_name": bank_name,
#         "password": password
#     }
#     url = "http://127.0.0.1:8000/users/register"
#     res = requests.post(url, json=new_user)
#     return res.json()

# # Helper function to get public user details by CBU
# def get_public_user_details_by_cbu(cbu):
#     url = f"http://127.0.0.1:8000/users/public/cbu/{cbu}"
#     res = requests.get(url)
#     return res.json()

# # Helper function to get public user details by Alias
# def get_public_user_details_by_alias(alias):
#     url = f"http://127.0.0.1:8000/users/public/alias/{alias}"
#     res = requests.get(url)
#     return res.json()

# # Helper function to reload user data
# def reload_user_data():
#     url = f"http://127.0.0.1:8000/users/cbu/{st.session_state.cbu}?password={st.session_state.password}"
#     res = requests.get(url)
#     st.session_state.user_data = res.json()["data"]

# # User login page
# def login_page():
#     st.header("Login")
#     cbu = st.text_input("CBU")
#     password = st.text_input("Password", type="password")
#     if st.button("Login"):
#         if authenticate_user(cbu, password):
#             st.success("Logged in successfully")
#             st.experimental_rerun()
#         else:
#             st.error("Invalid CBU or Password")

# # User registration page
# def register_page():
#     st.header("Register")
#     name = st.text_input("Name:")
#     cuit = st.text_input("CUIT:")
#     cbu = st.text_input("CBU")
#     alias_type = st.selectbox("Alias Type:", options=["email", "phone", "nickname"])
#     alias = st.text_input("Alias")
#     bank_name = st.selectbox("Bank Name:", options=banks)
#     password = st.text_input("Password", type="password")
#     if st.button("Register"):
#         ret = register_user(name, cuit, cbu, alias, alias_type, bank_name, password)
#         if ret["response_type"] == "success":
#             st.success("User registered successfully. Redirecting to login page...")
#             st.experimental_rerun()
#         else:
#             st.error(ret["description"])

# # User dashboard
# def user_dashboard():
#     st.header(f"Welcome, {st.session_state.user_data['name']}!")
#     st.write(f"CUIT: {st.session_state.user_data['cuit']}")
#     st.write(f"Alias: {st.session_state.user_data['alias']}")
    
#     # Correct URL for balance
#     url = f"http://127.0.0.1:8000/users/{st.session_state.cbu}/balance?password={st.session_state.password}"
#     res = requests.get(url)
#     res_dict = json.loads(res.text)
#     balance = res_dict["data"]
#     st.write(f"Balance: ${balance}")

#     if st.button("Logout"):
#         st.session_state.authenticated = False
#         st.experimental_rerun()

#     st.subheader("Transaction History")
#     with st.expander("View Transaction History"):
#         url_hist = f"http://127.0.0.1:8000/transactions/{st.session_state.cbu}/history"
#         res_hist = requests.get(url_hist)
#         hist_dict = json.loads(res_hist.text)
#         history = hist_dict["data"]
#         if not history:
#             st.write("No transactions")
#         else:
#             transactions = {"Date": [], "Alias": [], "Name": [], "CBU": [], "Amount": []}
#             for transaction in history:
#                 if transaction["from_user"]["cbu"] == st.session_state.cbu:
#                     # Sent transaction
#                     transactions["Date"].append(transaction["date"])
#                     transactions["Alias"].append(transaction["to_user"]["alias"])
#                     transactions["Name"].append(transaction["to_user"]["name"])
#                     transactions["CBU"].append(transaction["to_user"]["cbu"])
#                     transactions["Amount"].append(-transaction["amount"])  # Negative for sent transactions
#                 elif transaction["to_user"]["cbu"] == st.session_state.cbu:
#                     # Received transaction
#                     transactions["Date"].append(transaction["date"])
#                     transactions["Alias"].append(transaction["from_user"]["alias"])
#                     transactions["Name"].append(transaction["from_user"]["name"])
#                     transactions["CBU"].append(transaction["from_user"]["cbu"])
#                     transactions["Amount"].append(transaction["amount"])  # Positive for received transactions
#             transactions_df = pd.DataFrame.from_dict(transactions)
#             st.table(transactions_df)

#     st.subheader("Make a Payment")
#     tab1, tab2 = st.tabs(["By CBU", "By Alias"])
#     with tab1:
#         with st.form("pay_by_cbu"):
#             amount = st.text_input("Amount:")
#             password = st.text_input("Password:", type="password")
#             to_cbu = st.text_input("Recipient CBU:")
#             submitted = st.form_submit_button("Submit")
#             if submitted:
#                 user_details = get_public_user_details_by_cbu(to_cbu)
#                 if user_details["response_type"] == "success":
#                     st.session_state.transaction_data = {
#                         "amount": float(amount),
#                         "from_cbu": st.session_state.cbu,
#                         "password": password,
#                         "to_cbu": to_cbu,
#                         "recipient_details": user_details["data"]
#                     }
#                     st.experimental_rerun()
#                 else:
#                     st.warning("Recipient CBU not found")

#     with tab2:
#         with st.form("pay_by_alias"):
#             amount = st.text_input("Amount:")
#             password = st.text_input("Password:", type="password")
#             to_alias = st.text_input("Recipient Alias:")
#             submitted = st.form_submit_button("Submit")
#             if submitted:
#                 user_details = get_public_user_details_by_alias(to_alias)
#                 if user_details["response_type"] == "success":
#                     st.session_state.transaction_data = {
#                         "amount": float(amount),
#                         "from_alias": st.session_state.user_data["alias"],
#                         "password": password,
#                         "to_alias": to_alias,
#                         "recipient_details": user_details["data"]
#                     }
#                     st.experimental_rerun()
#                 else:
#                     st.warning("Recipient Alias not found")

#     if st.session_state.transaction_data:
#         st.subheader("Confirm Payment")
#         recipient = st.session_state.transaction_data["recipient_details"]
#         st.write(f"Recipient Name: {recipient['name']}")
#         st.write(f"Recipient CUIT: {recipient['cuit']}")
#         if st.button("Confirm Payment"):
#             payment_data = st.session_state.transaction_data.copy()
#             del payment_data["recipient_details"]
#             if "to_cbu" in payment_data:
#                 url = "http://127.0.0.1:8000/transactions/pay-cbu"
#             else:
#                 url = "http://127.0.0.1:8000/transactions/pay-alias"
#             res = requests.post(url, json=payment_data)
#             res_json = res.json()
#             if res.status_code == 200:
#                 st.success("Payment completed!")
#                 st.session_state.transaction_data = {}
#                 reload_user_data()  # Refresh user data after payment
#                 st.experimental_rerun()
#             else:
#                 st.warning("Payment failed.")
#                 st.warning(res_json["description"])

# # Main application logic
# if st.session_state.authenticated:
#     user_dashboard()
# else:
#     login_or_register = st.selectbox("Login or Register", ["Login", "Register"])
#     if login_or_register == "Login":
#         login_page()
#     else:
#         register_page()



import streamlit as st
import requests
import json
import pandas as pd

# Define page configuration
st.set_page_config(page_title="User Authentication and Dashboard")

# Define session states
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'cbu' not in st.session_state:
    st.session_state.cbu = ""
if 'alias' not in st.session_state:
    st.session_state.alias = ""
if 'password' not in st.session_state:
    st.session_state.password = ""
if 'transaction_data' not in st.session_state:
    st.session_state.transaction_data = {}
if 'user_data' not in st.session_state:
    st.session_state.user_data = {}

# Get list of banks
url = "http://127.0.0.1:8000/banks/all"
res = requests.get(url)
res_dict = json.loads(res.text)
banks = []
for i in range(0,len(res_dict["data"])):
    banks.append(res_dict["data"][i]["name"])

# Helper function for authentication
def authenticate_user(cbu, password):
    url = f"http://127.0.0.1:8000/users/cbu/{cbu}?password={password}"
    res = requests.get(url)
    res_dict = json.loads(res.text)
    if res.status_code == 200 and res_dict["data"] is not None:
        st.session_state.authenticated = True
        st.session_state.cbu = cbu
        st.session_state.password = password
        st.session_state.user_data = res_dict["data"]
        return True
    else:
        return False

# Helper function to register a new user
def register_user(name, cuit, cbu, alias, alias_type, bank_name, password):
    new_user = {
        "name": name,
        "cuit": cuit,
        "cbu": cbu,
        "alias": alias,
        "alias_type": alias_type,
        "bank_name": bank_name,
        "password": password
    }
    url = "http://127.0.0.1:8000/users/register"
    res = requests.post(url, json=new_user)
    return res.json()

# Helper function to get public user details by CBU
def get_public_user_details_by_cbu(cbu):
    url = f"http://127.0.0.1:8000/users/public/cbu/{cbu}"
    res = requests.get(url)
    return res.json()

# Helper function to get public user details by Alias
def get_public_user_details_by_alias(alias):
    url = f"http://127.0.0.1:8000/users/public/alias/{alias}"
    res = requests.get(url)
    return res.json()

# Helper function to reload user data
def reload_user_data():
    url = f"http://127.0.0.1:8000/users/cbu/{st.session_state.cbu}?password={st.session_state.password}"
    res = requests.get(url)
    st.session_state.user_data = res.json()["data"]

# User login page
def login_page():
    st.header("Login")
    cbu = st.text_input("CBU")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if authenticate_user(cbu, password):
            st.success("Logged in successfully")
            st.experimental_rerun()
        else:
            st.error("Invalid CBU or Password")

# User registration page
def register_page():
    st.header("Register")
    name = st.text_input("Name:")
    cuit = st.text_input("CUIT:")
    cbu = st.text_input("CBU")
    alias_type = st.selectbox("Alias Type:", options=["email", "phone", "nickname"])
    alias = st.text_input("Alias")
    bank_name = st.selectbox("Bank Name:", options=banks)
    password = st.text_input("Password", type="password")
    if st.button("Register"):
        ret = register_user(name, cuit, cbu, alias, alias_type, bank_name, password)
        if ret["response_type"] == "success":
            st.success("User registered successfully. Redirecting to login page...")
            # st.experimental_rerun()
        else:
            st.error(ret["description"])

# User dashboard
def user_dashboard():
    st.header(f"Welcome, {st.session_state.user_data['name']}!")
    st.write(f"CUIT: {st.session_state.user_data['cuit']}")
    st.write(f"Alias: {st.session_state.user_data['alias']}")
    
    # Correct URL for balance
    url = f"http://127.0.0.1:8000/users/{st.session_state.cbu}/balance?password={st.session_state.password}"
    res = requests.get(url)
    res_dict = json.loads(res.text)
    if res_dict["response_type"] == "error":
        st.write(f"Balance: Not available")
        st.write(f"Error: {res_dict['description']}")
    else:
        balance = res_dict["data"]
        st.write(f"Balance: ${balance}")

    if st.button("Logout"):
        st.session_state.authenticated = False
        st.experimental_rerun()
        
    st.subheader("Transaction History")
    with st.expander("View Transaction History"):
        url_hist = f"http://127.0.0.1:8000/transactions/{st.session_state.cbu}/history"
        res_hist = requests.get(url_hist)
        hist_dict = json.loads(res_hist.text)
        history = hist_dict["data"]
        if not history:
            st.write("No transactions")
        else:
            transactions = {"Date": [], "Alias": [], "Name": [], "CBU": [], "Amount": []}
            for transaction in history:
                if transaction["from_user"]["cbu"] == st.session_state.cbu:
                    # Sent transaction
                    transactions["Date"].append(transaction["date"])
                    transactions["Alias"].append(transaction["to_user"]["alias"])
                    transactions["Name"].append(transaction["to_user"]["name"])
                    transactions["CBU"].append(transaction["to_user"]["cbu"])
                    transactions["Amount"].append(-transaction["amount"])  # Negative for sent transactions
                elif transaction["to_user"]["cbu"] == st.session_state.cbu:
                    # Received transaction
                    transactions["Date"].append(transaction["date"])
                    transactions["Alias"].append(transaction["from_user"]["alias"])
                    transactions["Name"].append(transaction["from_user"]["name"])
                    transactions["CBU"].append(transaction["from_user"]["cbu"])
                    transactions["Amount"].append(transaction["amount"])  # Positive for received transactions
            transactions_df = pd.DataFrame.from_dict(transactions)
            st.table(transactions_df)
            
    st.subheader("Make a Payment")
    tab1, tab2 = st.tabs(["By CBU", "By Alias"])
    with tab1:
        with st.form("pay_by_cbu"):
            amount = st.text_input("Amount:")
            password = st.text_input("Password:", type="password")
            to_cbu = st.text_input("Recipient CBU:")
            submitted = st.form_submit_button("Submit")
            if submitted:
                user_details = get_public_user_details_by_cbu(to_cbu)
                if user_details["response_type"] == "success":
                    st.session_state.transaction_data = {
                        "amount": float(amount),
                        "from_cbu": st.session_state.cbu,
                        "password": password,
                        "to_cbu": to_cbu,
                        "recipient_details": user_details["data"]
                    }
                    st.experimental_rerun()
                else:
                    st.warning("Recipient CBU not found")

    with tab2:
        with st.form("pay_by_alias"):
            amount = st.text_input("Amount:")
            password = st.text_input("Password:", type="password")
            to_alias = st.text_input("Recipient Alias:")
            submitted = st.form_submit_button("Submit")
            if submitted:
                user_details = get_public_user_details_by_alias(to_alias)
                if user_details["response_type"] == "success":
                    st.session_state.transaction_data = {
                        "amount": float(amount),
                        "from_alias": st.session_state.user_data["alias"],  # Cambiamos de from_cbu a from_alias
                        "password": password,
                        "to_alias": to_alias,
                        "recipient_details": user_details["data"]
                    }
                    st.experimental_rerun()
                else:
                    st.warning("Recipient Alias not found")

    if st.session_state.transaction_data:
        st.subheader("Confirm Payment")
        recipient = st.session_state.transaction_data["recipient_details"]
        st.write(f"Recipient Name: {recipient['name']}")
        st.write(f"Recipient CUIT: {recipient['cuit']}")
        if st.button("Confirm Payment"):
            payment_data = st.session_state.transaction_data.copy()
            del payment_data["recipient_details"]
            if "to_cbu" in payment_data:
                url = "http://127.0.0.1:8000/transactions/pay-cbu"
            else:
                url = "http://127.0.0.1:8000/transactions/pay-alias"
            res = requests.post(url, json=payment_data)
            res_json = res.json()
            if res.status_code == 200:
                st.success("Payment completed!")
                st.session_state.transaction_data = {}
                reload_user_data()  # Refresh user data after payment
                st.experimental_rerun()
            else:
                st.warning("Payment failed.")
                st.warning(res_json["description"])

# Main application logic
if st.session_state.authenticated:
    user_dashboard()
else:
    login_or_register = st.selectbox("Login or Register", ["Login", "Register"])
    if login_or_register == "Login":
        login_page()
    else:
        register_page()