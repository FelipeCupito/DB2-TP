#!/bin/bash

# shellcheck disable=SC2164
cd backendBanks
python3 main.py 8070 5432 "data/user1.json"
