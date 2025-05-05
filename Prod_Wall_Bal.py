import requests
import json
import urllib3
from prettytable import PrettyTable
import pandas

# Assign the value of file_path globally
file_path = 'Prod_Wall_Bal.xls'
pd = pandas

# Read user IDs and base URLs from Excel
def load_data_from_excel(file_path):
    # Load users data
    exl_user_id = {}
    users_df = pd.read_excel(file_path, sheet_name='Users', dtype=str)
    for _, row in users_df.iterrows():
        exl_opcos = row['ASP-OPCO'].strip()
        user_id = row['User ID']
        if exl_opcos not in exl_user_id:
            exl_user_id[exl_opcos] = []
        exl_user_id[exl_opcos].append(user_id)

    # Load base URLs
    urls_df = pd.read_excel(file_path, sheet_name='BaseUrls')
    base_urls = urls_df['Base_URL'].tolist()

    return base_urls, exl_user_id  # Return correct variable


# Initialize table
table = PrettyTable()
table.field_names = ["ASP-OPCO", "User ID", "Airtel Money Balance", "Airtime Balance"]


# Function to make the API request for wallet balance
def make_request(base_url, user_id, opco):
    global currency, balance
    url = f'{base_url}/api/am-profile/v1/users/{user_id}'

    headers = {
        'ASP-OPCO': opco,
        'X-CLIENT-ID': 'B2C',
        'Content-Type': 'application/json'
    }

    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    response = requests.get(url, headers=headers, verify=False)

    if response.status_code == 200:
        response_json = response.json()  # Parse JSON response
        primary_balances = []
        try:
            wallets = response_json['response']['wallets']
            for wallet in wallets:
                if wallet.get('is_primary') == "Y":
                    currency = wallet['currency']
                    balance = wallet['balance']
                    primary_balances.append(f"{currency} {balance}")  # Add to list

            return primary_balances if primary_balances else None
        except KeyError:
            print(f"Wallet data not found for user ID {user_id} at {base_url} with ASP-OPCO '{opco}'")
    else:
        print(
            f"Failed for user ID {user_id} at {base_url} with ASP-OPCO '{opco}': {response.status_code} - {response.text}")

    return None  # Return None if something went wrong


# Function to get airtime balance for each user
def get_airtime_balance(base_url, user_id, opco):
    url = f'{base_url}/api/subscriber-profile/v4/query-balance?msisdn={user_id}&lob=PREPAID'

    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'asp-api-key': '2e3933d4-9b7c-4d72-945a-a9dcfa7bbf5e',
        'ASP-Locale': 'en-US',
        'ASP-OPCO': opco,
        'ASP-Req-Timestamp': '1743770446'
    }

    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    response = requests.get(url, headers=headers, verify=False)
    Cur_airtime_balance=[]
    if response.status_code == 200:
        response_json = response.json()  # Parse JSON response
        try:
            query_balance_result = response_json.get('queryBalanceResult', [])
            for item in query_balance_result:
                if item.get('balanceDescription') == 'Airtime':
                    airtime_balance = item.get('balance', 0)  # Get the airtime balance
                    currency = item.get('unitType',0)
                    Cur_airtime_balance.append(f"{currency} {airtime_balance}")
                    return Cur_airtime_balance
        except KeyError:
            print(f"Balance data not found for user ID {user_id} at {base_url} with ASP-OPCO '{opco}'")
    else:
        print(
            f"Failed for user ID {user_id} at {base_url} with ASP-OPCO '{opco}': {response.status_code} - {response.text}")

    return None  # Return None if something went wrong


if __name__ == "__main__":
    # Load data from Excel
    base_url, exl_user_id = load_data_from_excel(file_path)
    for base_url in base_url:
        # Extract ASP-OPCO from the base URL
        opco = base_url.split('.')[1].upper()  # Gets 'KE', 'CD', 'UG', 'TZ', 'MW', 'GA'
        user_ids = exl_user_id.get(opco, [])

        print(f"\nMaking requests to base URL: {base_url} with ASP-OPCO: {opco}")

        # Iterate through user IDs for each base URL
        for user_id in user_ids:
            wallet_balances = make_request(base_url, user_id, opco)
            airtime_balance = get_airtime_balance(base_url, user_id, opco)

            if wallet_balances is not None and airtime_balance is not None:
                # Add the data to the table
                table.add_row([opco, user_id, wallet_balances, airtime_balance])


    print("\nSummary of Wallet Balances:")
    print(table)
#added to git update
