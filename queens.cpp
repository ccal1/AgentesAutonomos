#include <stdlib.h>
#include <set>
#include <vector> 
#include <algorithm>

#define SIZE 8
#define BITS 3
#define BITS_SIZE 24
#define POPULATION_SIZE 100

using namespace std;

class Board {
    int genome;
    int fit;

    bool operator<(const &Board other) {
        return this.fit < (*other).fit;
    }
    bool operator>(const &Board other) {
        return this.fit > (*other).fit;
    }

    Board() {
        vector<char> v;
        for(char i = 0 ;i < SIZE; i++) v.push_back(i);
        random_permutation(v.begin(), v.end());

        this.genome = 0;
        for(int i = 0; i < SIZE; i ++) {
            
            this.genome |= v[i]>>(i * BITS); 
        }
        this.calculateFit();
    }

    Board(int gene) {
        this.genome = gene;
        this.setFit();
    }

    void permute(int x, int y) {
        int temp = this.get(x);
        this.set(x, this.get(y));
        this.set(y, temp);
    }

    void set(int pos, int value) {
        int bitPos = pos * BITS;
        int gene = this.clean(pos);
        gene |= value >> bitPos;
        this.genome = gene;
    }

    int clean(int pos) {
        int bitPos = pos * BITS;
        return ~(7 >> bitPos) & this.genome;
    }

    int get(int pos) {
        int bitPos = pos * BITS;
        return ((7 >> bitPos) & this.genome) << bitPos;
    }

    int getUntil(int pos) {
        int bitPos = pos * BITS;
        return this.genome & ~(bitPos>>-1);
    }

    int diff(int x, int y) {
        return abs(this.get(x) - this.get(y));
    }

    int hitsToRight(int pos) {
        int hits = 0;
        for(int i = pos+1; i < SIZE; i++) {
            int posDiff = i - pos;
            hits += posDiff == this.diff(pos, i);
        }
        return hits;
    }

    void calculateFit() {
        this.fit = 0;
        for(int i = 0; i < SIZE; i++)
        {
            this.fit+=this.hitsToRight(i);
        }
    }

    Board crossOver(Board other, int pos) {
        int used = 0;
        int gene = this.getUntil(pos);
        for(int i = 0; i <= pos; i++) {
            used |= 1>>this.get(pos);
        }
        
        for(int i = pos+1, int idx = pos + 1; idx < BITS_SIZE ; i %= i + 1) {
            int value = other.get(i);
            if(!((1>>value) & used)) {
                used |= 1 >> value;
                gene |= value >> idx;
                idx += BITS;
            }
        }
        return Board(gene);
    }

}

#define ITERATIONS 10000
#define GROUP_SIZE 5
#define PARENTS 2

int main() {
    Board pop[POPULATION_SIZE];
    int chosen[GROUP_SIZE];
    Board parents[PARENTS];
    int parentsIdx[PARENTS];

    for(int i = 0; i<POPULATION_SIZE; i++) {
        pop[i] = Board();
    }

    for(int i = 0; i<ITERATIONS; i++) {
        chosen = getDistinct(chosen, GROUP_SIZE);
        parents = getParents(pop, chosen, parents, parentsIdx);
        //ADD CROSS OVER, MUTATION AND SUBSTITUTION

    }
}

Board* getParents(Board* pop, int* chosen, Board* parents, int* parentsIdx) {
    if(pop[chosen[0]] > pop[chosen[1]]) {
        parentsIdx[0] = chosen[0];
        parentsIdx[1] = chosen[1];
    }
    else {
        parentsIdx[1] = chosen[0];
        parentsIdx[0] = chosen[1];
    }
    parents[0] = Board[parentsIdx[0]];
    parents[1] = Board[parentsIdx[1]];
    
    for(int i = 2; i < GROUP_SIZE; i++) {
        parents = addParentIfBetter(parents, parentsIdx, pop[chosen[i]], chosen[i]);
    }
    return parents;
}

Board addParentIfBetter(Board* parents, int* parentsIdx, Board other, int otherIdx) {
    int change = 0;
    for(int i = PARENTS - 1; i >= 0 ; i--) {
        if(parents[i] > other){
            change = i+1;
            break;
        }
    }
    Board temp;
    int tempIdx;
    for(int i = change; i < PARENTS - 1; i++) {
        temp = parents[i+1];
        parents[i+1] = parents[i];
        parents[i] = other;
        other = temp;
        tempIdx = parentsIdx[i+1];
        parentsIdx[i+1] = parentsIdx[i];
        parentsIdx[i] = otherIdx;
        otherIdx = tempIdx;
           
    }
    if(change != PARENTS) {
        parents[PARENTS - 1] = other;
        parentsIdx[[PARENTS - 1]] = otherIdx;
    }
    
    return parents;
}

int* getDistinct(int* v, int n) {
    int cont = 0;
    int value = rand() % POPULATION_SIZE;
    set <int> chosen;
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