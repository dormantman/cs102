package rsa

import (
	"errors"
	"math"
	"math/big"
	"math/rand"
)

type Key struct {
	key int
	n   int
}

type KeyPair struct {
	Private Key
	Public  Key
}

func isPrime(n int) bool {
	if n > 1 {
		for i := 2; i <= int(math.Floor(math.Pow(float64(n), 0.5))); i++ {
			if n%i == 0 {
				return false
			}
		}
		return true
	}
	return false
}

func gcd(a int, b int) int {
	for b != 0 {
		a, b = b, a%b
	}
	return a
}

func multiplicativeInverse(e int, phi int) int {
	var dt [][]int

	dt = append(dt, []int{phi, e, phi % e, phi / e, -1, -1})
	for i := 0; dt[i][2] != 0; i++ {
		phi, e := dt[i][1], dt[i][2]
		dt = append(dt, []int{phi, e, phi % e, phi / e, -1, -1})
	}

	dt[len(dt)-1][4] = 0
	dt[len(dt)-1][5] = 1
	for i := len(dt) - 2; i >= 0; i-- {
		dt[i][4], dt[i][5] = dt[i+1][5], dt[i+1][4]-dt[i+1][5]*dt[i][3]
	}

	d := dt[0][5] % phi
	if d < 0 {
		return d + phi
	} else {
		return d
	}
}

func GenerateKeypair(p int, q int) (KeyPair, error) {
	if !isPrime(p) || !isPrime(q) {
		return KeyPair{}, errors.New("Both numbers must be prime.")
	} else if p == q {
		return KeyPair{}, errors.New("p and q can't be equal.")
	}

	n := p * q
	phi := (p - 1) * (q - 1)

	e := rand.Intn(phi-1) + 1
	g := gcd(e, phi)
	for g != 1 {
		e = rand.Intn(phi-1) + 1
		g = gcd(e, phi)
	}

	d := multiplicativeInverse(e, phi)
	return KeyPair{Key{e, n}, Key{d, n}}, nil
}

func Encrypt(pk Key, plaintext string) []int {
	cipher := []int{}
	n := new(big.Int)
	for _, ch := range plaintext {
		n = new(big.Int).Exp(
			big.NewInt(int64(ch)), big.NewInt(int64(pk.key)), nil)
		n = new(big.Int).Mod(n, big.NewInt(int64(pk.n)))
		cipher = append(cipher, int(n.Int64()))
	}
	return cipher
}

func Decrypt(pk Key, cipher []int) string {
	plaintext := ""
	n := new(big.Int)
	for _, ch := range cipher {
		n = new(big.Int).Exp(
			big.NewInt(int64(ch)), big.NewInt(int64(pk.key)), nil)
		n = new(big.Int).Mod(n, big.NewInt(int64(pk.n)))
		plaintext += string(rune(int(n.Int64())))
	}
	return plaintext
}
