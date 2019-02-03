import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import mintapi
from utilities.misc import getCredentials, getBrowserDriver

def run(arguments):
    mint = mintapi.Mint(getCredentials("mint")["email"], getCredentials("mint")["password"], mfa_method='sms', headless=False)

    mint.get_accounts()

    # Get extended account detail at the expense of speed - requires an
    # additional API call for each account
    print(mint.get_accounts(True))

    # Get budget information
    print(mint.get_budgets())

    # Get transactions
    print(mint.get_transactions()) # as pandas dataframe
    print(mint.get_transactions_csv(include_investment=False)) # as raw csv data
    print(mint.get_transactions_json(include_investment=False, skip_duplicates=False))

    # Get net worth
    print(mint.get_net_worth())

if __name__ == "__main__":
    run()