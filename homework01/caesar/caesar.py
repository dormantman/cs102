def encrypt_caesar(plaintext, shift):
    ciphertext = ""
    for char in plaintext:
        if "A" <= char <= "z":
            symbol = ord(char) + shift % 26

            if "A" <= char <= "Z" < chr(symbol):
                symbol -= 26

            elif chr(symbol) > "z":
                symbol -= 26

            char = chr(symbol)
        ciphertext += char

    return ciphertext


def decrypt_caesar(ciphertext, shift):
    plaintext = ""
    for char in ciphertext:
        if "A" <= char <= "z":
            enc = ord(char) - shift % 26

            if enc < ord("A"):
                enc += 26

            if "a" <= char <= "z" and enc < ord("a"):
                enc += 26

            char = chr(enc)
        plaintext += char

    return plaintext
