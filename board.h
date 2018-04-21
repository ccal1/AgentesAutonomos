#define SIZE 8
#define BITS 3
#define BITS_SIZE 24

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

public:
	 Board();
	 Board(int);
	 int getFit();
	 int getGenome();
	 bool operator < (const Board&); 
	 bool operator > (const Board&);
	 int get(int);
	 void permute(int, int);
	 void set_value(int, int );
	 int clean(int);
	 int getUntil(int);
	 int diff(int, int);
	 int hitsToRight(int);
	 void calculateFit();
	 Board crossOver(Board, int); 
     void geneSwapMutate();
     void printGenome();
	 void printBoard();     
};
