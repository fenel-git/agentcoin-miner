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
        answer_bytes = answer.to_bytes(32, 'big')
        tx = contract.functions.submitAnswer(problem_id, answer_bytes).build_transaction({
            'from': account.address,
            'nonce': web3.eth.get_transaction_count(account.address),
            'gas': 200000,
            'gasPrice': web3.eth.gas_price,
        })

        signed_tx = account.sign_transaction(tx)
        tx_hash = web3.eth.send_raw_transaction(signed_tx.raw_transaction)
        print(f"[✅] Jawaban dikirim! Tx hash: {tx_hash.hex()}")
        return tx_hash
    except Exception as e:
        print("[❌] Gagal submit:", e)

# --- FUNCTION FETCH CURRENT PROBLEM ---
def fetch_current_problem():
    API_URL = "https://api.agentcoin.site/api/problem/current"
    try:
        resp = requests.get(API_URL)
        problem = resp.json()
        if problem and problem.get("is_active"):
            return problem
        return None
    except Exception as e:
        print("[❌] Gagal fetch problem:", e)
        return None

# --- FUNCTION SOLVE SOAL OTOMATIS ---
def solve_problem(template_text, agent_id):
    # Contoh problem: sum of integers k divisible by 3 or 5 but not 15, modulo (N mod 100 + 1)
    # Ambil N dari template_text → di AgentCoin biasanya N = AGENT ID
    N = agent_id
    modulo = N % 100 + 1
    total = 0
    for k in range(1, 1000):  # range cukup besar, contoh
        if (k % 3 == 0 or k % 5 == 0) and (k % 15 != 0):
            total += k
    return total % modulo

# --- AGENT ID untuk template ---
AGENT_ID = 14486

# --- LOOP UNTUK CEK PROBLEM AKTIF ---
while True:
    problem = fetch_current_problem()
    if problem:
        problem_id = problem["problem_id"]
        template_text = problem.get("template_text", "")
        print(f"[⚡] Problem aktif: {problem_id} | {template_text}")

        # --- HITUNG JAWABAN OTOMATIS ---
        answer = solve_problem(template_text, AGENT_ID)
        print(f"[⚡] Jawaban dihitung: {answer}")

        # --- SUBMIT JAWABAN ---
        submit_answer(problem_id, answer)
        break
    else:
        print("[⏳] Belum ada problem aktif, tunggu 5 detik...")
        time.sleep(5)
