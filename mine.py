import time
import requests
from web3 import Web3

# --- CONFIG BASE MAINNET ---
RPC_URL = "https://mainnet.base.org"
PRIVATE_KEY = "0x99e539fdfb8b90ee5594962a7d353fb2eaef0dd30023d469c60458485810ea62"
CONTRACT_ADDRESS = "0x7D563ae2881D2fC72f5f4c66334c079B4Cc051c6"

# --- ABI MINIMAL ---
PROBLEM_MANAGER_ABI = [
    {
        "inputs": [
            {"internalType": "uint256", "name": "problemId", "type": "uint256"},
            {"internalType": "bytes32", "name": "answer", "type": "bytes32"}
        ],
        "name": "submitAnswer",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    }
]

# --- INIT WEB3 ---
web3 = Web3(Web3.HTTPProvider(RPC_URL))
account = web3.eth.account.from_key(PRIVATE_KEY)
contract = web3.eth.contract(address=CONTRACT_ADDRESS, abi=PROBLEM_MANAGER_ABI)

# --- FUNCTION SUBMIT ---
def submit_answer(problem_id, answer):
    try:
        # Convert jawaban int ke bytes32
        if isinstance(answer, int):
            answer_bytes = answer.to_bytes(32, 'big')
        else:
            answer_bytes = Web3.to_bytes(hexstr=answer)

        tx = contract.functions.submitAnswer(problem_id, answer_bytes).build_transaction({
            'from': account.address,
            'nonce': web3.eth.get_transaction_count(account.address),
            'gas': 200000,
            'gasPrice': web3.eth.gas_price,
        })

        signed_tx = account.sign_transaction(tx)
        tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
        print(f"[✅] Jawaban dikirim! Tx hash: {tx_hash.hex()}")
        return tx_hash
    except Exception as e:
        print("[❌] Gagal submit:", e)

# --- FUNCTION FETCH PROBLEM DARI API ---
def fetch_current_problem():
    API_URL = "https://api.agentcoin.site/api/problem/current"
    try:
        resp = requests.get(API_URL)
        if resp.status_code == 200:
            problem = resp.json()
            if problem and problem.get("status") == "active":
                return problem
        return None
    except Exception as e:
        print("[❌] Gagal fetch problem:", e)
        return None

# --- LOOP UNTUK CEK PROBLEM AKTIF ---
while True:
    problem = fetch_current_problem()
    if problem:
        problem_id = problem["problem_id"]
        description = problem.get("description", "")
        print(f"[⚡] Problem aktif: {problem_id} | {description}")

        # --- GENERATE JAWABAN ---
        # Placeholder dummy, ganti dengan logic AI / solver
        answer = 33
        print(f"[⚡] Siap submit jawaban {answer} untuk problem {problem_id}")

        submit_answer(problem_id, answer)
        break
    else:
        print("[⏳] Belum ada problem aktif, tunggu 5 detik...")
        time.sleep(5)
