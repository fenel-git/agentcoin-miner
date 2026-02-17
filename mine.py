import os
import requests
from web3 import Web3

# === CONFIG ===
AGENT_ID = 14486  # ganti dengan agent ID kamu
PRIVATE_KEY = "0x99e539fdfb8b90ee5594962a7d353fb2eaef0dd30023d469c60458485810ea62"  # ganti dengan private key
RPC_URL = "https://mainnet.base.org"  # endpoint Base chain
PROBLEM_API = "https://api.agentcoin.site/api/problem/current"
PROBLEM_MANAGER_ADDRESS = "0x7D563ae2881D2fC72f5f4c66334c079B4Cc051c6"

# === WEB3 SETUP ===
w3 = Web3(Web3.HTTPProvider(RPC_URL))
account = w3.eth.account.from_key(PRIVATE_KEY)

# === FUNCTION ===
def fetch_problem():
    resp = requests.get(PROBLEM_API)
    data = resp.json()
    if not data.get("is_active", False):
        print("Problem not active yet.")
        return None
    return data

def solve_problem(problem):
    # contoh problem matematika: sum divisible by 3 or 5, but not 15
    template = problem["template_text"]
    N = AGENT_ID
    # logika contoh
    total = sum(k for k in range(1, N+1) if (k % 3 == 0 or k % 5 == 0) and k % 15 != 0)
    mod = N % 100 + 1
    answer = total % mod
    return answer

def submit_answer(problem_id, answer):
    # encode answer ke bytes32
    answer_bytes = Web3.toBytes(answer)
    # buat transaction (dummy example, sesuaikan ABI/contract)
    tx = {
        "to": PROBLEM_MANAGER_ADDRESS,
        "value": 0,
        "gas": 200000,
        "nonce": w3.eth.get_transaction_count(account.address),
        "data": answer_bytes,
    }
    signed = account.sign_transaction(tx)
    tx_hash = w3.eth.send_raw_transaction(signed.rawTransaction)
    print("Submitted:", tx_hash.hex())

# === MAIN LOOP ===
if __name__ == "__main__":
    problem = fetch_problem()
    if problem:
        ans = solve_problem(problem)
        print("Answer:", ans)
        submit_answer(problem["problem_id"], ans)
