#!/bin/bash

# ============================================
# File        : setup.sh
# Project     : Fang
# Author      : Aromal
# Description : Installs required dependencies
#               and launches the Fang tool.
# Version     : 1.0.2
# ============================================

cmd=$(command -v python3 ||  command -v python )

if [ -z "$cmd" ]; then
   echo "[x] Python not installed"
   
   read -p "[*] Do you want to install python [Y/n]: " choice

   if [[ "$choice" == "Y" ||  "$choice" == "y" || -z "$choice" ]]; then
       
        sudo apt update
        sudo apt install -y python3 python3-pip

        cmd=$(command -v python3)

        "$cmd" -m pip install -r ./requirements.txt
        "$cmd" main.py

    else
        echo "[x] Installation cancelled"
        exit 1
    fi

else 
   $cmd main.py
fi

