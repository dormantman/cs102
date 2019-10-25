package main

import (
	"fmt"
	"io/ioutil"
	"path/filepath"
	"math/rand"
)

func readSudoku(filename string) ([][]byte, error) {
	data, err := ioutil.ReadFile(filename)
	if err != nil {
		return nil, err
	}
	grid := group(filter(data), 9)
	return grid, nil
}

func filter(values []byte) []byte {
	filtered_values := make([]byte, 0)
	for _, v := range values {
		if (v >= '1' && v <= '9') || v == '.' {
			filtered_values = append(filtered_values, v)
		}
	}
	return filtered_values
}

func display(grid [][]byte) {
	for i := 0; i < len(grid); i++ {
		for j := 0; j < len(grid); j++ {
			fmt.Print(string(grid[i][j]))
		}
		fmt.Println()
	}
}

func toByte(n int) byte {
    nums := []byte{'1', '2', '3', '4', '5', '6', '7', '8', '9'}
    return nums[n - 1]
}

func group(values []byte, n int) [][]byte {
    var result[][]byte;

    for i := 0; i < len(values); i += n {
        result = append(result, values[i:i+n])
    }
    
	return result
}

func getRow(grid [][]byte, row int) []byte {
    return grid[row]
}

func getCol(grid [][]byte, col int) []byte {
    var col_data []byte

    for row := 0; row < len(grid); row++ {
        col_data = append(col_data, grid[row][col])
    }

    return col_data
}

func getBlock(grid [][]byte, row int, col int) []byte {
    var block []byte

    var row_count = row / 3 * 3
    var col_count = col / 3 * 3

    for row := row_count; row < row_count + 3; row++ {
        for col := col_count; col < col_count + 3; col++ {
            block = append(block, grid[row][col])
        }
    }

    return block
}

func findEmptyPosition(grid [][]byte) (int, int) {
    for row := 0; row < len(grid); row++ {
        for col := 0; col < len(grid[0]); col++ {
            if grid[row][col] == byte('.') {
                return row, col
            }
        }
    }
    return -1, -1
}

func contains(values []byte, search byte) bool {
	for _, v := range values {
		if v == search {
			return true
		}
	}
	return false
}

func findPossibleValues(grid [][]byte, row int, col int) []byte {
    set := make(map[byte]bool)

    for num := 1; num <= 9; num++ {
        set[toByte(num)] = true
    }

    for _, num := range getRow(grid, row) {
        set[num] = false
    }

    for _, num := range getCol(grid, col) {
        set[num] = false
    }

    for _, num := range getBlock(grid, row, col) {
        set[num] = false
    }

    var result []byte

    for num := 1; num <= 9; num++ {
        if set[toByte(num)] {
            result = append(result, toByte(num))
        }
    }

    return result
}

func solve(grid [][]byte) ([][]byte, bool) {
    row, col := findEmptyPosition(grid)
    if (row == -1) && (col == -1) {
        return grid, true
    }

    values := findPossibleValues(grid, row, col)

    for _, value := range values {
        grid[row][col] = byte(value)

        solution, result := solve(grid)
        if result {
            return solution, true
        }

        grid[row][col] = byte('.')
    }

    return grid, false

}

func compareArrays(a1 []byte, a2 []byte) bool {
    for i := 0; i <= len(a1); i++ {
        if a1[i] != a2[i] {
            return false
        }
    }
    return true
}

func checkSolution(grid [][]byte) bool {
    var correct []byte

    for i := 1; i <= 9; i++ {
        correct = append(correct, byte(i))
    }

    for row := 0; row < len(grid); row++ {
        if !compareArrays(getRow(grid, row), correct) {
            return false
        }
    }

    for col := 0; col < len(grid); col++ {
        if !compareArrays(getCol(grid, col), correct) {
            return false
        }
    }

    for _, row := range []int{0, 3, 6} {
        for _, col := range []int{0, 3, 6} {
            block := getBlock(grid, row, col)
            if !compareArrays(block, correct) {
                return false
            }
        }
    }

    return true
}

func generateSudoku(N int) [][]byte {
    var grid [][]byte

    for i := 0; i < 9; i++ {
        var row []byte

        for j := 0; j < 9; j++ {
            row = append(row, byte('.'))
        }

        grid = append(grid, row)
    }

    if N > 81 {
        N = 0
    } else {
        N = 81 - N
    }

    for N != 0 {
        row := rand.Intn(8)
        col := rand.Intn(8)
        if grid[row][col] != byte('.') {
            grid[row][col] = byte('.')
            N -= 1
        }
    }

    return grid
}

func main() {
	puzzles, err := filepath.Glob("puzzle*.txt")
	if err != nil {
		fmt.Printf("Could not find any puzzles")
		return
	}
	for _, fname := range puzzles {
		go func(fname string) {
			grid, _ := readSudoku(fname)
			solution, _ := solve(grid)
			fmt.Println("Solution for", fname)
			display(solution)
		}(fname)
	}
	var input string
	fmt.Scanln(&input)
}
