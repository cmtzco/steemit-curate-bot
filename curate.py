from subprocess import call
import threading
import time
import creds




def run_bot(puppet, posting_key):
    call(["python3", "multibot.py", puppet, posting_key])

while True:
    for ea_acct in accounts:
        # pupp_ak = accounts[ea_acct]['active_key']\
        try:
            pupp_pk = accounts[ea_acct]['posting_key']
            t = threading.Thread(target=run_bot, args=(ea_acct, pupp_pk))
            t.start()
        except KeyboardInterrupt:
            print("Quitting...")
            t.close()
            sys.exit(0)

    time.sleep(2500)