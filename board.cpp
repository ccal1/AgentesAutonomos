#include "board.h"

Board::Board() {
    vector<char> v;
    for(char i = 0 ; i < SIZE; i++) v.push_back(i);
    random_shuffle(v.begin(), v.end());

    genome = 0;
    for(int i = 0; i < SIZE; i ++) {

        genome |= v[i]<<(i * BITS);

    }
    calculateFit();
}

Board::Board(int gene) {
    genome = gene;
    calculateFit();
}

int Board::getFit() {
    return this->fit;
}

int Board::getGenome() {
    return this->genome;
}

bool Board::operator < (const Board& other) {
    return fit < other.fit;
}

bool Board::operator> (const Board& other) {
    return fit > other.fit;
}


void Board::permute(int x, int y) {
    int temp = get(x);
    set_value(x, get(y));
    set_value(y, temp);
}

void Board::set_value(int pos, int value) {
    int bitPos = pos * BITS;
    int gene = clean(pos);
    gene |= value << bitPos;
    genome = gene;
}

int Board::clean(int pos) {
    int bitPos = pos * BITS;
    return ~(7 << bitPos) & genome;
}

int Board::get(int pos) {
    int bitPos = pos * BITS;
    return ((7 << bitPos) & genome) >> bitPos;
}

int Board::getUntil(int pos) {
    int bitPos = pos * BITS;
    return genome & ~(-1<<bitPos);
}

int Board::diff(int x, int y) {
    return abs(get(x) - get(y));
}

int Board::hitsToRight(int pos) {
    int hits = 0;
    for(int i = pos+1; i < SIZE; i++) {
        int posDiff = i - pos;
        hits += ( posDiff == diff(pos, i) );
    }
    return hits;
}

void Board::calculateFit() {
    fit = 0;
    for(int i = 0; i < SIZE; i++)
    {
        fit+=hitsToRight(i);
    }
}

Board Board::crossOver(Board other, int pos) {
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

void Board::geneSwapMutate() {
    int pos1 = rand()%SIZE;
    int pos2 = (pos1 + rand()%(SIZE-1) + 1)%SIZE;

    int gene1 = get(pos1);
    int gene2 = get(pos2);
    
    set_value(pos1, gene2);
    set_value(pos2, gene1);
}

void Board::printGenome() {
    for (int i = 0; i < SIZE; i++) {
        cout << get(i) << " ";
    }
    cout << endl;
}

void Board::printBoard() {
    cout << getFit() << endl;
    printGenome();
}
