#!/bin/bash

# shellcheck disable=SC2164
pip install streamlit
pip install requests
cd frontend
python3 -m streamlit run home.py --server.enableCORS false --server.enableXsrfProtection false
