import os
import json
import time
import datetime
import requests
import base58
from solders.keypair import Keypair
from solders.transaction import VersionedTransaction
from solana.rpc.api import Client
from dotenv import load_dotenv

# --- INITIALIZATION ---
load_dotenv()
RPC_URL = os.getenv("SOLANA_RPC_URL") # Твоят Helius RPC URL
PRIVATE_KEY_B58 = os.getenv("SOLANA_PRIVATE_KEY") # Твоят Private Key от Phantom
INTELLIGENCE_LOG = "/root/SolanaProject/ARCHIVE/intelligence_log.csv"

# Jupiter API Endpoints
JUPITER_QUOTE_API = "https://quote-api.jup.ag/v6/quote"
JUPITER_SWAP_API = "https://quote-api.jup.ag/v6/swap"

class MilaTraderV1_1:
    def __init__(self):
        self.solana_client = Client(RPC_URL)
        self.keypair = Keypair.from_bytes(base58.b58decode(PRIVATE_KEY_B58))
        self.pubkey = self.keypair.pubkey()
        
        print(f"--- MILA TRADER v1.1 ACTIVE | WALLET: {self.pubkey} ---")
        print(f"--- STATUS: STANDBY FOR SIGNALS | {datetime.datetime.now()} ---")

    def get_token_quote(self, input_mint, output_mint, amount_sol):
        """Извлича котировка от Jupiter."""
        amount_lamports = int(amount_sol * 1_000_000_000)
        params = {
            "inputMint": input_mint,
            "outputMint": output_mint,
            "amount": amount_lamports,
            "slippageBps": 100 # 1% Slippage за сигурна екзекуция
        }
        try:
            res = requests.get(JUPITER_QUOTE_API, params=params)
            return res.json()
        except Exception as e:
            print(f"[ERROR] Quote failed: {e}")
            return None

    def execute_swap(self, quote_response):
        """Изпълнява суап транзакция през Jupiter."""
        try:
            # 1. Поискване на транзакцията от Jupiter
            payload = {
                "quoteResponse": quote_response,
                "userPublicKey": str(self.pubkey),
                "wrapAndUnwrapSol": True
            }
            res = requests.post(JUPITER_SWAP_API, json=payload)
            swap_data = res.json()
            
            if "swapTransaction" not in swap_data:
                print("[ERROR] Swap transaction not received from Jupiter.")
                return None

            # 2. Декодиране и подписване
            raw_transaction = base58.b58decode(swap_data["swapTransaction"])
            signature = self.keypair.sign_message(VersionedTransaction.from_bytes(raw_transaction).message)
            signed_txn = VersionedTransaction.from_bytes(raw_transaction, [signature])

            # 3. Изпращане към мрежата
            print("[TRADER] Sending transaction to Solana Mainnet...")
            txn_res = self.solana_client.send_raw_transaction(bytes(signed_txn))
            return txn_res
            
        except Exception as e:
            print(f"[CRITICAL ERROR] Execution failed: {e}")
            return None

    def run_automated_logic(self):
        """Наблюдава лога и търгува при засичане на Whale activity."""
        # Примерни монети (Минт адреси)
        SOL_MINT = "So11111111111111111111111111111111111111112"
        USDC_MINT = "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v"

        while True:
            # Тук ще се добави логиката за четене на CSV (от предния модул)
            # В момента скриптът е в режим на готовност за ръчен спусък или сигнал
            
            # ТЕСТОВА ЛОГИКА: Ако искаш да тестваш с 0.01 SOL
            # quote = self.get_token_quote(SOL_MINT, USDC_MINT, 0.01)
            # if quote:
            #     print(f"[TRADER] Found quote: {quote['outAmount']} USDC")
            #     # txn = self.execute_swap(quote)
            
            time.sleep(30)

if __name__ == "__main__":
    trader = MilaTraderV1_1()
    trader.run_automated_logic()