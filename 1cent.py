from web3 import Web3
from contract_abi import con_abi

private_key = "PRIVATE_KEY"
web3 = Web3(Web3.HTTPProvider("https://fantom.publicnode.com"))

account = web3.eth.account.from_key(private_key)
contract = web3.eth.contract(
    address=web3.to_checksum_address(
        "0xc5c01568a3b5d8c203964049615401aaf0783191"
    ), 
    abi=con_abi
)

address_bytes = bytes.fromhex(account.address[2:])  # Skip the '0x' prefix
address_bytes_32 = bytes(12) + address_bytes  # Pad with 12 zero bytes (32 - 20)

tx_data = (
    "0x000200000000000000000000000000000000000000000000000000000000000186a"
    "00000000000000000000000000000000000000000000000000000000000000000"
    f"{account.address[2:]}"
)

adapter_params_bytes = bytes.fromhex(tx_data[2:])  # Skip the '0x' prefix
for i in range(int(input("Количество транзакций: "))):
    value = contract.functions.estimateSendFee(
        167,
        address_bytes_32,
        100000000000000,
        True,
        tx_data
    ).call()

    value = int(value[0])

    transaction = contract.functions.sendFrom(
        account.address,
        167,
        address_bytes_32,
        100000000000000,
        (account.address, "0x0000000000000000000000000000000000000000", tx_data)
    ).build_transaction({
        'from': account.address,
        'nonce': web3.eth.get_transaction_count(account.address),
        'gas': 500000,
        'gasPrice': web3.to_wei('110', 'gwei'),
        'chainId': 250,
        'value': value
    })

    signed_tx = web3.eth.account.sign_transaction(
        transaction, 
        private_key=private_key
    )
    tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
    tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)

    print(f"Transaction hash: {tx_hash.hex()}")
