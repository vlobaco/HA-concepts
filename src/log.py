from datetime import datetime

def log(actor, message):
    print(f"{(actor + " " * 12)[:12]} | {datetime.now().strftime("%d-%m-%Y %H:%M:%S")} | {message}")
           