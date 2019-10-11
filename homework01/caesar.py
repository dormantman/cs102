def encrypt_caesar(plaintext):
    """
    Encrypts plaintext using a Caesar cipher.

    >>> encrypt_caesar("PYTHON")
    'SBWKRQ'
    >>> encrypt_caesar("python")
    'sbwkrq'
    >>> encrypt_caesar("Python3.6")
    'Sbwkrq3.6'
    >>> encrypt_caesar("")
    ''
    """
    ciphertext = ""
    for char in plaintext:
        if "A" <= char <= "z":
            symbol = ord(char) + 3

            if "A" <= char <= "Z" < chr(symbol):
                symbol -= 26

            elif chr(symbol) > "z":
                symbol -= 26

            char = chr(symbol)
        ciphertext += char

    return ciphertext


def decrypt_caesar(ciphertext):
    """
    Decrypts a ciphertext using a Caesar cipher.

    >>> decrypt_caesar("SBWKRQ")
    'PYTHON'
    >>> decrypt_caesar("sbwkrq")
    'python'
    >>> decrypt_caesar("Sbwkrq3.6")
    'Python3.6'
    >>> decrypt_caesar("")
    ''
    """
    plaintext = ""
    for char in ciphertext:
        if "A" <= char <= "z":
            enc = ord(char) - 3

            if enc < ord("A"):
                enc += 26

            if "a" <= char <= "z" and enc < ord("a"):
                enc += 26

            char = chr(enc)
        plaintext += char

    return plaintext


print(encrypt_caesar("Python3.6"))
print(decrypt_caesar("SBWKRQ"))
print(decrypt_caesar("Sbwkrq3.6"))
