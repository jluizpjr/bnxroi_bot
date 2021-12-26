#!/bin/bash

while read line; do    
    export $line    
done < keys.env


python3 bnxroi_bot.py
