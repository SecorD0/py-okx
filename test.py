import os

from dotenv import load_dotenv

from py_okx.OKXClient import OKXClient
from py_okx.models import OKXCredentials, Chains


class Asset:
    @staticmethod
    def currencies() -> None:
        print('\n--- currencies ---')
        currencies = okx_client.asset.currencies(token_symbol='ETH')
        for token_symbol, chains in currencies.items():
            print(f'\n{token_symbol}')
            for chain, currency_dict in chains.items():
                print(f'\t{chain}: {currency_dict}')

        print('---')
        currencies = okx_client.asset.currencies()
        for token_symbol, chains in currencies.items():
            print(f'\n{token_symbol}')
            for chain, currency_dict in chains.items():
                print(f'\t{chain}: {currency_dict}')

    @staticmethod
    def balances() -> None:
        print('\n--- balances ---')
        balances = okx_client.asset.balances(token_symbol='USDT')
        for token_symbol, balance in balances.items():
            print(f'{token_symbol}: {balance}')

        print('---')
        balances = okx_client.asset.balances()
        for token_symbol, balance in balances.items():
            print(f'{token_symbol}: {balance}')

    @staticmethod
    def withdrawal_history() -> None:
        print('\n--- withdrawal_history ---')
        withdrawal_history = okx_client.asset.withdrawal_history()
        for wdId, withdrawal in withdrawal_history.items():
            print(f'{wdId}: {withdrawal}')

    @staticmethod
    def withdrawal() -> None:
        print('\n--- withdrawal ---')
        withdrawal_token = okx_client.asset.withdrawal(
            token_symbol='USDT', amount=100, toAddr=toAddr, fee=0.1, chain=Chains.ArbitrumOne
        )
        print(withdrawal_token)

    @staticmethod
    def cancel_withdrawal() -> None:
        print('\n--- cancel_withdrawal ---')
        response = okx_client.asset.cancel_withdrawal(wdId=wdId)
        print(response)


def main() -> None:
    print('--------- Asset ---------')
    asset = Asset()
    asset.currencies()
    asset.balances()
    asset.withdrawal_history()
    asset.withdrawal()
    asset.cancel_withdrawal()


if __name__ == '__main__':
    load_dotenv()
    credentials = OKXCredentials(
        api_key=str(os.getenv('API_KEY')) if os.getenv('API_KEY') else '',
        secret_key=str(os.getenv('SECRET_KEY')) if os.getenv('SECRET_KEY') else '',
        passphrase=str(os.getenv('PASSPHRASE')) if os.getenv('PASSPHRASE') else ''
    )
    if credentials.completely_filled():
        okx_client = OKXClient(
            credentials=credentials, entrypoint_url=str(os.getenv('ENTRYPOINT_URL')), proxy=str(os.getenv('PROXY'))
        )
        toAddr = str(os.getenv('TO_ADDR'))
        wdId = str(os.getenv('WD_ID'))

        main()

    else:
        print('Specify all variables in the .env file!')
