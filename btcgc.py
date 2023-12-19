import ecdsa
import hashlib
import base58
from requests import get
import msvcrt

def get_funded_txo_sum(address):
    try:
        response = get(f"https://mempool.space/api/address/38XnPvu9PmonFU9WouPXUjYbW91wa5MerL")

        if response.status_code == 200:
            api_data = response.json()
            funded_txo_sum = api_data.get('chain_stats', {}).get('funded_txo_sum', 0)
            return funded_txo_sum
        else:
            print(f"Falha na requisição: {response.status_code}")
            print(f"Detalhes: {response.text}")
            return 0
    except Exception as e:
        print(f"Erro ao fazer a requisição: {e}")
        return 0

def generate_wallet():
    private_key = ecdsa.SigningKey.generate(curve=ecdsa.SECP256k1)
    public_key = private_key.get_verifying_key().to_string()

    sha256_hash = hashlib.sha256(public_key).digest()
    ripemd160_hash = hashlib.new('ripemd160')
    ripemd160_hash.update(sha256_hash)
    public_key_hash = ripemd160_hash.digest()

    extended_hash = b'\x00' + public_key_hash
    checksum = hashlib.sha256(hashlib.sha256(extended_hash).digest()).digest()[:4]
    extended_hash += checksum

    address = base58.b58encode(extended_hash).decode('utf-8')
    private_key_hex = private_key.to_string().hex()

    return address, private_key_hex

def print_banner(text):
    print(f"{'='*40}")
    print(f"{text:^40}")
    print(f"{'='*40}")

def generate_and_print_wallet():
    wallet_address, private_key = generate_wallet()
    print_banner("Generated BTC GC Wallet")
    print(f"Endereço Bitcoin: {wallet_address}")
    print(f"Chave Privada:    {private_key}")

def generate_and_check_wallet():
    while True:
        wallet_address, private_key = generate_wallet()
        funded_txo_sum = get_funded_txo_sum(wallet_address)

        print_banner("Generated and Checked BTC GC Wallet")
        print(f"Endereço Bitcoin: {wallet_address}")
        print(f"Chave Privada:    {private_key}")
        print(f"Saldo: : {funded_txo_sum}")

        if funded_txo_sum > 0:
            print_banner("Transaction Found! Saving to info.txt")
            with open("info.txt", "w") as file:
                file.write(f"Endereço Bitcoin: {wallet_address}\n")
                file.write(f"Chave Privada:    {private_key}\n")
                file.write(f"Saldo: : {funded_txo_sum}\n")
            break

        if msvcrt.kbhit() and msvcrt.getch().decode('utf-8').lower() == 'p':
            print_banner("Retornando à tela inicial...")
            break

def exibir_menu_principal():
    print_banner("Menu do Gerador e Verificador de Carteira Bitcoin")
    print("\n[1] Gerar Nova Carteira")
    print("[2] Gerar e Verificar Carteira (Pressione P para parar)")
    print("[3] Sair")

def main():
    while True:
        exibir_menu_principal()
        escolha = input("Digite o número da opção desejada: ")

        if escolha == '1':
            generate_and_print_wallet()
        elif escolha == '2':
            generate_and_check_wallet()
        elif escolha == '3':
            print_banner("Saindo... Até logo!")
            break
        else:
            print("Opção inválida. Por favor, tente novamente.")

if __name__ == "__main__":
    main()