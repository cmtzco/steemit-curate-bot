from piston.steem import *
from piston.account import Account
from piston.exceptions import InvalidWifError, PostDoesNotExist
from pistonapi.exceptions import VoteWeightTooSmall
import threading
import random
import traceback
import time
import sys

upvote_history = []
MAX_THREADS = 4
running_threads = []
lock = threading.Lock()

def curation_delay_vote(wif_key, account_to_vote_with, identifier, time_to_wait, vote_weight):
    time.sleep(time_to_wait)
    steem = Steem(wif=wif_key)
    steem.vote(identifier, vote_weight, account_to_vote_with)
    print("[INFO][CURATE][VOTE] Voted from {}".format(account_to_vote_with))


def multifeed(puppet, puppet_posting_key):

    upvote_history = []
    pupp = Account(puppet)
    print("{}'s VOTING POWER: {}".format(puppet, pupp.voting_power()))
    vests = str(Account(puppet).get_balances()['VESTS']).split(" ")[0]
    if float(vests) >= 100000:
        vote_weight = 5
    else: 
        vote_weight = 100

    if pupp.voting_power() >= 70:
        print("{} : Waiting for new posts by {}".format(puppet, my_subscriptions))
        steem = Steem(wif=puppet_posting_key)

        for comment in steem.stream_comments():
            try:
                if comment.author in my_subscriptions:

                        if comment.identifier in upvote_history:
                            print("Comment has been previously voted on: {}".format(comment.identifier))


                        print("New post by @{} {}".format(comment.author, url_builder(comment)))

                        try:
                            print("Voting from {} account".format(puppet))
                            curation_time = random.randint(1800, 2200)
                            dice = random.randint(1, 100)
                            print("Curation time {} for {}, with chance of {}".format(curation_time, puppet, dice))
                            if dice > 77:
                                print("Time to wait {} for {} to vote.".format(curation_time, puppet))
                                t = threading.Thread(target=curation_delay_vote,
                                                    args=(puppet_posting_key, puppet, comment.identifier, curation_time, vote_weight))
                                t.start()
                                upvote_history.append(comment.identifier)
                            else:
                                print("Failed dice:{}".format(dice))
                        except BroadcastingError as e:
                            print("Upvoting failed...")
                            print("We have probably reached the upvote rate limit. {}".format(e))
                        except VoteWeightTooSmall: 
                            print("Low Vote Weight for: {}".format(puppet))
                            pass
                        except Exception as er:
                            print("Error:{}".format(er))
            except PostDoesNotExist: 
                print("Post Does not exist")
                pass

    else:
        print("Skipping vote from {} due to low voting power: {}".format(puppet, pupp.voting_power()))
        sys.exit(0)


def feed():
    print("Waiting for new posts by %s\n" % my_subscriptions)
    steem = Steem(wif=posting_key)
    for comment in steem.stream_comments():

        if comment.author in my_subscriptions:
            if len(comment.title) > 0:
                if comment.identifier in upvote_history:
                    continue

                print("New post by @%s %s" % (comment.author, url_builder(comment)))

                try:
                    comment.vote(100, account)
                    print("====> Upvoted")
                    upvote_history.append(comment.identifier)
                except BroadcastingError as e:
                    print("Upvoting failed...")
                    print("We have probably reached the upvote rate limit.")
                    print(str(e))



def url_builder(comment):
    return "https://steemit.com/%s/%s" % (comment.category, comment.identifier)

if __name__ == "__main__":
    while True:
        try:
            from creds import *
            puppet = sys.argv[1]
            posting_key = sys.argv[2]
            print("Running Feed: {}".format(puppet))
            multifeed(puppet, posting_key)
        except (KeyboardInterrupt, SystemExit):
            print("Quitting...")
            break
        except Exception as err:
            print('### Exception Occurred: Restarting:   {}'.format(err))
            print("{}:   Unexpected error: {}".format(puppet, sys.exc_info()[0]))
            traceback.print_exc()

            

