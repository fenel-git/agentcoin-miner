import time
from web3 import Web3

# --- CONFIG BASE MAINNET ---
RPC_URL = "https://mainnet.base.org"
PRIVATE_KEY = "0x99e539fdfb8b90ee5594962a7d353fb2eaef0dd30023d469c60458485810ea62"
AGENT_ID = 14486
CONTRACT_ADDRESS = "0x7D563ae2881D2fC72f5f4c66334c079B4Cc051c6"  # ProblemManager

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
    },
    {
        "inputs": [
            {"internalType": "uint256", "name": "problemId", "type": "uint256"}
        ],
        "name": "getProblem",
        "outputs": [
            {
                "components": [
                    {"internalType": "bytes32","name":"answerHash","type":"bytes32"},
                    {"internalType": "uint256","name":"answerDeadline","type":"uint256"},
                    {"internalType": "uint256","name":"revealDeadline","type":"uint256"},
                    {"internalType": "uint8","name":"status","type":"uint8"},
                    {"internalType": "uint256","name":"correctCount","type":"uint256"},
                    {"internalType": "uint256","name":"totalCorrectWeight","type":"uint256"},
                    {"internalType": "uint256","name":"winnerCount","type":"uint256"},
                    {"internalType": "uint256","name":"verifiedWinnerCount","type":"uint256"}
                ],
                "internalType": "struct ProblemInfo",
                "name": "",
                "type": "tuple"
            }
        ],
        "stateMutability": "view",
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
        # convert jawaban int ke bytes32
        if isinstance(answer, int):
            answer_bytes = answer.to_bytes(32, 'big')
        else:
            # asumsi jawaban string hex, misal "0xabc..."
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

# --- AUTO CEK PROBLEM ---
while True:
    try:
        # misal problem_id = 1 untuk contoh, bisa loop cek real contract
        problem_id = 1
        problem_info = contract.functions.getProblem(problem_id).call()
        print(f"[⚡] Problem {problem_id} status: {problem_info[3]}")

        # generate jawaban dummy (gantikan logika solve nyata nanti)
        answer = 33
        print(f"[⚡] Siap submit jawaban {answer} untuk problem {problem_id}")

        submit_answer(problem_id, answer)
        break
    except Exception as e:
        print("[⏳] Belum ada problem aktif atau error:", e)
        time.sleep(5)
