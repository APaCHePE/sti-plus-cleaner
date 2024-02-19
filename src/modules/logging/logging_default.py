import json
import time
import os
import logging
from colorama import Fore, Style

def log_final(level, log_data):
    
    if level == os.getenv('WARN'):
        color = Fore.YELLOW
    elif level == os.getenv('ERROR'):
        color = Fore.RED
    else:
        color = Fore.WHITE

    log_message = f'{color}{level.upper()}: {Style.RESET_ALL}'
    log_message += json.dumps(log_data, indent=4, ensure_ascii=False, sort_keys=True)
    print(log_message)

def logger(useCase, timestamp, timestampNow, status, message):
    log_final(useCase, {
        "Timestamp": timestampNow,
        "Consumer-Enterprise-Code": "BANCORIPLEY-CHL",
        "Consumer-Country-Code":"CHL",
        "Channel-Name":"STI-PLUS",
        "Consumer-Sys-Code":"CHL-APP-MOB",
        "Consumer-UserId-Code": "143626873",
        "Trace-Process-Id":"0000000000000056978894719",
        "Trace-Event-Id":"xxxx-xxxx-xxx",
        "Trace-Source-Id":"0000000000000056978894719",
        "App-Code":"ms-customer-get-account",
        "Execution-Time": timestampNow - timestamp * 1000,
        "Status": status, 
        "Message": message
    })