package vigenere

func EncryptVigenere(plaintext string, keyword string) string {
	var ciphertext string
	var change rune
	var symbol rune

	for index, char := range plaintext {
		if (char >= 'A' && char <= 'Z') || (char >= 'a' && char <= 'z') {
			change = rune(keyword[index%len(keyword)])

			if 'a' <= char && char <= 'z' {
				change -= 'a'
			} else {
				change -= 'A'
			}

			symbol = rune(char) + change
			if ('A' <= char && char <= 'Z') && (symbol > 'Z') {
				symbol -= 26
			}
			if symbol > 'z' {
				symbol -= 26
			}

			ciphertext += string(symbol)
		} else {
			ciphertext += string(char)
		}
	}

	return ciphertext
}

func DecryptVigenere(ciphertext string, keyword string) string {
	var plaintext string
	var change rune
	var symbol rune

	for index, char := range ciphertext {
		if (char >= 'A' && char <= 'Z') || (char >= 'a' && char <= 'z') {
			change = rune(keyword[index%len(keyword)])

			if 'a' <= char && char <= 'z' {
				change -= 'a'
			} else {
				change -= 'A'
			}

			symbol = rune(char) - change
			if ('a' <= char && char <= 'z') && (symbol < 'a') {
				symbol += 26
			}
			if symbol < 'A' {
				symbol += 26
			}

			plaintext += string(symbol)
		} else {
			plaintext += string(char)
		}
	}

	return plaintext
}
