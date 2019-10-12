def encrypt_vigenere(plaintext, keyword):
    """
    Encrypts plaintext using a Vigenere cipher.

    >>> encrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> encrypt_vigenere("python", "a")
    'python'
    >>> encrypt_vigenere("ATTACKATDAWN", "LEMON")
    'LXFOPVEFRNHR'
    """
    ciphertext = ''
    for index, char in enumerate(plaintext):
        sub = char

        if 'A' <= char <= 'z':
            change = ord(keyword[index % len(keyword)])
            change -= ord('a') if 'a' <= char <= 'z' else ord('A')

            symbol = ord(char) + change

            if 'a' <= char <= 'z' and symbol > ord('z'):
                symbol -= 26

            elif 'A' <= char <= 'Z' and symbol > ord('Z'):
                symbol -= 26

            sub = chr(symbol)
        ciphertext += sub

    return ciphertext


def decrypt_vigenere(ciphertext, keyword):
    """
    Decrypts a ciphertext using a Vigenere cipher.

    >>> decrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> decrypt_vigenere("python", "a")
    'python'
    >>> decrypt_vigenere("LXFOPVEFRNHR", "LEMON")
    'ATTACKATDAWN'
    """
    plaintext = ''
    for index, char in enumerate(ciphertext):
        sub = char

        if 'A' <= char <= 'z':
            change = ord(keyword[index % len(keyword)])
            change -= ord('a') if 'a' <= char <= 'z' else ord('A')

            symbol = ord(char) - change

            if 'a' <= char <= 'z' and symbol < ord('a'):
                symbol += 26

            elif 'A' <= char <= 'Z' and symbol < ord('A'):
                symbol += 26

            sub = chr(symbol)
        plaintext += sub

    return plaintext
