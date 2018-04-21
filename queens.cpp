#include <stdlib.h>
#include <set>
#include <vector>
#include <algorithm>
#include <time.h>
#include <iostream>
#include <stdio.h>

#define SIZE 8
#define BITS 3
#define BITS_SIZE 24
#define POPULATION_SIZE 100
#define ITERATIONS 10000
#define GROUP_SIZE 5
#define PARENTS_SIZE 2
#define CHILDREN_SIZE 2

using namespace std;

class Board {
private:
    int genome;
    int fit;

public:
    Board() {
        vector<char> v;
        for(char i = 0 ; i < SIZE; i++) v.push_back(i);
        random_shuffle(v.begin(), v.end());

        genome = 0;
        for(int i = 0; i < SIZE; i ++) {

            genome |= v[i]<<(i * BITS);

        }
        calculateFit();
    }

    Board(int gene) {
        genome = gene;
        calculateFit();
    }

    int getFit() {
        return this->fit;
    }

    int getGenome() {
        return this->genome;
    }

    bool operator < (const Board& other) {
        return fit < other.fit;
    }

    bool operator> (const Board& other) {
        return fit > other.fit;
    }


    void permute(int x, int y) {
        int temp = get(x);
        set_value(x, get(y));
        set_value(y, temp);
    }

    void set_value(int pos, int value) {
        int bitPos = pos * BITS;
        int gene = clean(pos);
        gene |= value << bitPos;
        genome = gene;
    }

    int clean(int pos) {
        int bitPos = pos * BITS;
        return ~(7 << bitPos) & genome;
    }

    int get(int pos) {
        int bitPos = pos * BITS;
        return ((7 << bitPos) & genome) >> bitPos;
    }

    int getUntil(int pos) {
        int bitPos = pos * BITS;
        return genome & ~(-1<<bitPos);
    }

    int diff(int x, int y) {
        return abs(get(x) - get(y));
    }

    int hitsToRight(int pos) {
        int hits = 0;
        for(int i = pos+1; i < SIZE; i++) {
            int posDiff = i - pos;
            hits += ( posDiff == diff(pos, i) );
        }
        return hits;
    }

    void calculateFit() {
        fit = 0;
        for(int i = 0; i < SIZE; i++)
        {
            fit+=hitsToRight(i);
        }
    }

    Board crossOver(Board other, int pos) {
        int used = 0;
        int gene = getUntil(pos);
        for(int i = 0; i < pos; i++) {
            used |= 1<<get(i);
        }

        for(int i = pos, idx = pos * BITS; idx < BITS_SIZE; (++i)%=SIZE) {
            int value = other.get(i);
            if(!((1<<value) & used)) {
                used |= 1 << value;
                gene |= value << idx;
                idx += BITS;
            }
        }
        return Board(gene);
    }

    void geneSwapMutate() {
        int pos1 = rand()%SIZE;
        int pos2 = (pos1 + rand()%(SIZE-1) + 1)%SIZE;

        int gene1 = get(pos1);
        int gene2 = get(pos2);
        
        set_value(pos1, gene2);
        set_value(pos2, gene1);
    }

    void printGenome() {
        for (int i = 0; i < SIZE; i++) {
            cout << get(i) << " ";
        }
        cout << endl;
    }

    void printBoard() {
        cout << getFit() << endl;
        printGenome();
    }
};

Board* getParents(Board*, int*, Board*, int*);
int* getDistinct(int*, int);
Board* replaceParentIfBetter(Board*, int*, Board, int);
Board* offspringGen(Board*, Board*);
Board* mutate(Board*);
Board* substituteParents(Board*, Board*);
void printBoardVec(Board*, int);
Board* replaceParents(Board*, Board*, int*);
int getCrossoverPos();
bool finished(Board*, int*);

int main() {
    // Setting srand argument to generate random sequence
    srand (time(NULL));

    Board *pop = new Board[POPULATION_SIZE];
    int *chosen = new int[GROUP_SIZE];
    Board *parents = new Board[PARENTS_SIZE];
    int *parentsIdx = new int[PARENTS_SIZE];
    Board *offspring = new Board[CHILDREN_SIZE];


    // Generating initial Population
    for(int i = 0; i<POPULATION_SIZE; i++) {
        pop[i] = Board();
    }

    cout << "Print Population" << endl;
    printBoardVec(pop,POPULATION_SIZE);
    cout << endl;

    for(int i = 0; i<ITERATIONS; i++) {
        cout << "iteration: " << i+1 << endl; 

        // Getting parents
        chosen = getDistinct(chosen, GROUP_SIZE);
        parents = getParents(pop, chosen, parents, parentsIdx);
        printBoardVec(parents, PARENTS_SIZE);

        // Generating Offspring
        offspring = offspringGen(parents,offspring);
        printBoardVec(offspring,CHILDREN_SIZE);

        // Applying Mutation
        offspring = mutate(offspring);

        //Sorting Offspring
        sort(offspring, offspring + CHILDREN_SIZE);
        printBoardVec(offspring,CHILDREN_SIZE);

        // Substitution
        parents = substituteParents(parents, offspring);
        printBoardVec(parents, PARENTS_SIZE);

        pop = replaceParents(pop, parents, parentsIdx);
		if(finished(pop, parentsIdx))break;
        cout << endl;

    }

    delete[] pop;
    delete[] chosen;
    delete[] parents;
    delete[] parentsIdx;
    delete[] offspring;

    return 0;
}

Board* getParents(Board* pop, int* chosen, Board* parents, int* parentsIdx) {

    if(pop[chosen[0]] < pop[chosen[1]]) {
        parentsIdx[0] = chosen[0];
        parentsIdx[1] = chosen[1];
    }
    else {
        parentsIdx[1] = chosen[0];
        parentsIdx[0] = chosen[1];
    }

    parents[0] = pop[parentsIdx[0]];
    parents[1] = pop[parentsIdx[1]];

    for(int i = 2; i < GROUP_SIZE; i++) {
        parents = replaceParentIfBetter(parents, parentsIdx, pop[chosen[i]], chosen[i]);
    }
    return parents;
}

Board* replaceParentIfBetter(Board* parents, int *parentsIdx, Board other, int otherIdx) {
    int change = 0;
    for(int i = PARENTS_SIZE - 1; i >= 0 ; i--) {
        if(parents[i] < other){
            change = i+1;
            break;
        }
    }
    Board temp;
    int tempIdx;
    for(int i = change; i < PARENTS_SIZE - 1; i++) {
        temp = parents[i+1];
        parents[i+1] = parents[i];
        parents[i] = other;
        other = temp;
        tempIdx = parentsIdx[i+1];
        parentsIdx[i+1] = parentsIdx[i];
        parentsIdx[i] = otherIdx;
        otherIdx = tempIdx;

    }
    if(change != PARENTS_SIZE) {
        parents[PARENTS_SIZE - 1] = other;
        parentsIdx[PARENTS_SIZE - 1] = otherIdx;
    }

    return parents;
}

int* getDistinct(int* v, int n) {
    int cont = 0;
    int value = rand() % POPULATION_SIZE;
    set<int> chosen;
    while(cont < n)
    {
        if(!chosen.count(value)) {
            v[cont++] = value;
            chosen.insert(value);
        }
        value = rand() % POPULATION_SIZE;
    }
    return v;
}

Board* offspringGen(Board* parents, Board* offspring) {
    int off_index = 0;
    
    for(int j = 0; j < PARENTS_SIZE; j++) {
        
        for (int k = j+1; k < PARENTS_SIZE; k++) {
            int pos = getCrossoverPos();
            offspring[off_index++] = parents[j].crossOver(parents[k],pos);
            
            pos = getCrossoverPos();
            offspring[off_index++] = parents[k].crossOver(parents[j],pos);
        }

    }

    return offspring;
}

Board* mutate(Board* offspring) {
    for (int i = 0; i < CHILDREN_SIZE; i++) {
        if (rand() % 10 <= 3) {
            offspring[i].geneSwapMutate();
        }
    }
    return offspring;
}

Board* substituteParents(Board *parents, Board *offspring) {
    Board* Temp = new Board[PARENTS_SIZE];
    int par_index = 0, off_index = 0, temp_index = 0;

    while (par_index < PARENTS_SIZE && off_index < CHILDREN_SIZE) {
        
        if (parents[par_index] < offspring[off_index]) {

            Temp[temp_index++] = parents[par_index++];
        
        }
        else {

            Temp[temp_index++] = offspring[off_index++];    

        }

    }

    delete[] parents;

    return Temp;
}

Board* replaceParents(Board* pop, Board *parents, int* parentsIdx) {
    for (int i = 0; i < PARENTS_SIZE; i++) {
        pop[parentsIdx[i]] = parents[i];
    }
    return pop;
}

bool finished(Board* pop, int* parentIdx){
	for (int i = 0; i < PARENTS_SIZE; i++){
		if(pop[parentIdx[i]].getFit() == 0) return true;
	}
	return false;
}

void printBoardVec(Board* Array, int sizeArray) {
    for (int i = 0; i < sizeArray; i++) {
        Array[i].printBoard();
    }
}

int getCrossoverPos() {
    int pos = rand() % (SIZE-1) + 1;
    if (rand() % 10 == 9) pos = 0;
    return pos;
}
