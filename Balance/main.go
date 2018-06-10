package main

import (
	"fmt"
	"math"
	"math/rand"
	"time"
)

type matrix [100][25]float64

func (m matrix) Len() int { return len(m) }

func (m matrix) getFiness() float64 {
	// Gets fitness, F(matrix) = max - min
	var min = math.MaxFloat64
	var max = -1.0
	for _, i := range m {
		for _, cell := range i {
			fmt.Printf("%v ", cell)
			if cell < min {
				min = cell
			}
			if cell > max {
				max = cell
			}
		}
	}
	return max - min
}

func main() {
	seed := rand.New(rand.NewSource(time.Now().UnixNano()))
	var m matrix
	for i := 0; i < 100; i++ {
		for j := 0; j < 25; j++ {
			m[i][j] = float64(seed.Intn(20)) * seed.Float64()
		}
	}
	fmt.Println(m.getFiness())
}
