package caesar

func EncryptCaesar(plaintext string, shift int) string {
	var ciphertext string

	shift = shift % 26
	for _, char := range plaintext {
		if (char >= 'A' && char <= 'Z') || (char >= 'a' && char <= 'z') {
			if (char+rune(shift) > 'Z' && char <= 'Z') || (char+rune(shift) > 'z') {
				char = char - 26
			}
			char = char + rune(shift)
		}
		ciphertext += string(char)
	}

	return ciphertext
}

func DecryptCaesar(ciphertext string, shift int) string {
	var plaintext string

	shift = shift % 26
	for _, char := range ciphertext {
		if (char >= 'A' && char <= 'Z') || (char >= 'a' && char <= 'z') {
			if (char-rune(shift) < 'A' && char >= 'A') || (char-rune(shift) < 'a' && char >= 'a') {
				char = char + 26
			}
			char = char - rune(shift)
		}
		plaintext += string(char)
	}

	return plaintext
}
