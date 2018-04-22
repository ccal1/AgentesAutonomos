#ifndef BOARD_H
#define BOARD_H


#define SIZE 8
#define BITS 3
#define BITS_SIZE 24
#define MAX_ERROR ((SIZE * (SIZE -1)) / 2)

using namespace std;

#include <iostream>
#include <time.h>
#include <math.h>
#include <vector>
#include <set>
#include <stdlib.h>
#include <algorithm>

class Board {
private:
    int genome;
    int fit;
	int getNthSetBit(int, int);
	void setValue(int, int);
	void calculateFit();
	int hitsToRight(int);
	int diff(int, int);
	int getUntil(int);
	int clean(int);
	int countBits(int);
	void geneSwap(int pos1, int pos2);
	  
public:
	Board();
	Board(int);
	int getFit();
	double exponentialFit();
	double parabolicFit();
	double linearFit(); 
	int getGenome();
	bool operator < (const Board&); 
	bool operator > (const Board&);
	int get(int);
	Board crossOver(Board, int); 
	void geneSwapMutate();
	void printGenome();
	void printBoard();
	void smartMutate();
	void someHitSwapMutate();
	int findHitsBitmask();
	void hitsPermutationMutate();
};

#endif
