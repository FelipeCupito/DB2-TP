#!/bin/bash

chmod +x backendPixie/setup.sh
chmod +x backendBanks/setup.sh
chmod +x run_bank1.sh
chmod +x run_bank2.sh
chmod +x run_pixie.sh


# shellcheck disable=SC2164
cd backendPixie
./setup.sh &

# shellcheck disable=SC2103
cd ..

# shellcheck disable=SC2164
cd backendBanks
./setup.sh &

