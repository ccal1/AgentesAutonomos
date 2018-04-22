#include <stdlib.h>
#include <set>
#include <vector>
#include <algorithm>
#include <time.h>
#include <iostream>
#include <stdio.h>
#include "board.h"
#include "timer.h"

#define EXEC_NUMBER 40
#define POPULATION_SIZE 100
#define ITERATIONS 1000
#define GROUP_SIZE 5
#define PARENTS_SIZE 2
#define CHILDREN_SIZE 2

#define SMART_MUTATE 1
#define GENE_SWAP_MUTATE 2
#define HIT_SWAP_MUTATE 3
#define MUTATION GENE_SWAP_MUTATE


using namespace std;

struct statStruc {
    Timer timer;
    vector<pair<double,double> > statistics;
    vector<int> bestBoard;
    int numInter;
    
    statStruc() {}
    statStruc(Timer timer_, vector<pair<double,double> > statistics_, vector<int> bestBoard_, int numInter_) : timer(timer_), statistics(statistics_), bestBoard(bestBoard_), numInter(numInter_) {}

};

struct resultsStruc {
    pair<double,double> timerStat;
    vector<pair<double,double> > resultStat;
    vector<pair<double,double> > bestBoardStat;

    resultsStruc() {}
    resultsStruc(pair<double,double> timerStat_, vector<pair<double,double> > resultStat_, vector<pair<double,double> > bestBoardStat_) : timerStat(timerStat_), resultStat(resultStat_), bestBoardStat(bestBoardStat_) {}
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
pair<double, double> generateStatistics(Board*, int);
statStruc geneticAlgorithm();
resultsStruc generateResults (vector<statStruc>);

int main() {
    // Setting srand argument to generate random sequence
    vector<statStruc> Results(EXEC_NUMBER);
    resultsStruc finalResults;

    for (unsigned int i = 0; i < Results.size(); i++) {
        Results[i] = geneticAlgorithm();
    }

    finalResults = generateResults(Results);

    cout<<"Time Average: "<<finalResults.timerStat.first<<"\n";
    cout<<"Time Standard Deviation: "<<finalResults.timerStat.second<<"\n";
    cout<<"\nAverage:\n";
    for(unsigned int i = 0; i<finalResults.resultStat.size(); i++){
        cout<<finalResults.resultStat[i].first<< " ";
    }
    cout<<"\n\n";
    
    cout<<"Standard Deviation:\n";
    for(unsigned int i = 0; i<finalResults.resultStat.size(); i++){
        cout<< finalResults.resultStat[i].second << " ";
    }
    cout<<"\n\n";
    
    cout<<"Best by iteration Average: \n";
    for(unsigned int i = 0; i < finalResults.bestBoardStat.size(); i++){
        cout<< finalResults.bestBoardStat[i].first << " ";
    }
    cout<<"\n";

    cout<<"Best by iteration Standard Deviation: \n";
    for(unsigned int i = 0; i < finalResults.bestBoardStat.size(); i++){
        cout<< finalResults.bestBoardStat[i].second << " ";
    }
    cout<<"\n";

    Results.clear();

    return 0;
}

statStruc geneticAlgorithm () {
    srand (time(NULL));
    Timer timer = Timer(), timerEnd;
    Board *pop = new Board[POPULATION_SIZE];
    int *chosen = new int[GROUP_SIZE];
    Board *parents = new Board[PARENTS_SIZE];
    int *parentsIdx = new int[PARENTS_SIZE];
    Board *offspring = new Board[CHILDREN_SIZE];
    vector<pair<double, double> > statistics;
    vector<int> bestBoard;
    bool end = false;
    int numInter = 0;


    // Generating initial Population
    for(int i = 0; i<POPULATION_SIZE; i++) {
        pop[i] = Board();
    }

    //Sorting population
    sort(pop,pop+POPULATION_SIZE);

    //cout << "Print Population" << endl;
    //printBoardVec(pop,POPULATION_SIZE);
    //cout << endl;

    for(int i = 0; i<ITERATIONS; i++) {
        //cout << "iteration: " << i+1 << endl; 

        // Getting parents
        chosen = getDistinct(chosen, GROUP_SIZE);
        parents = getParents(pop, chosen, parents, parentsIdx);
        // timer.pause();
        // printBoardVec(parents, PARENTS_SIZE);
        // timer.start();

        // Generating Offspring
        offspring = offspringGen(parents,offspring);
        // timer.pause();
        // printBoardVec(offspring,CHILDREN_SIZE);
        // timer.start();
        
        // Applying Mutation
        offspring = mutate(offspring);

        //Sorting Offspring
        sort(offspring, offspring + CHILDREN_SIZE);
        // timer.pause();
        // printBoardVec(offspring,CHILDREN_SIZE);
        // timer.start();
        
        // Substitution
        parents = substituteParents(parents, offspring);
        // timer.pause();
        // printBoardVec(parents, PARENTS_SIZE);
        // timer.start();

        pop = replaceParents(pop, parents, parentsIdx);

        //Sorting population
        timer.pause(); 
        sort(pop,pop+POPULATION_SIZE);
        statistics.push_back(generateStatistics(pop, POPULATION_SIZE));
        bestBoard.push_back(pop[0].getFit());
        timer.start();

        if(pop[0].getFit() == 0 && !end)  {
            timer.pause();
            timerEnd = timer;
            numInter = i;
            end = true;
        }
        // cout << endl;

    }
    
    // Iteration Statistics Print
    // cout<<"Time: "<<timer.getNanoseconds()<<"\n";
    // cout<<"\nAverage:\n";
    // for(int i = 0; i<statistics.size(); i++){
    //     cout<<statistics[i].first<< " ";
    // }
    // cout<<"\n\n";
    
    // cout<<"Standard Deviation:\n";
    // for(int i = 0; i<statistics.size(); i++){
    //     cout<< statistics[i].second << " ";
    // }
    // cout<<"\n\n";
    
    // cout<<"Best by iteration:\n";
    // for(int i = 0; i<bestBoard.size(); i++){
    //     cout<< bestBoard[i] << " ";
    // }
    // cout<<"\n";

    delete[] pop;
    delete[] chosen;
    delete[] parents;
    delete[] parentsIdx;
    delete[] offspring;

    return statStruc(timerEnd, statistics, bestBoard, numInter);
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
            if(MUTATION == GENE_SWAP_MUTATE) offspring[i].geneSwapMutate();
            else if(MUTATION == SMART_MUTATE) offspring[i].smartMutate();
            else if(MUTATION == HIT_SWAP_MUTATE) offspring[i].someHitSwapMutate();
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

pair<double, double> generateStatistics(Board * pop, int n) {
    double sum = 0;
    for(int i = 0; i<n; i++) {
        sum += pop[i].getFit();
    }
    double avg = sum/n;

    double deltaSum = 0;
    for(int i = 0; i < n; i++) {
        double delta = avg - pop[i].getFit();
        deltaSum += sqrt(delta * delta);
    }
    double stdDeviation = deltaSum/n;
    return pair<double, double>(avg, stdDeviation);
}

resultsStruc generateResults (vector<statStruc> Results) {
    pair<double,double> timerStat(0,0);
    vector<pair<double,double> > resultStat(ITERATIONS,pair<double,double>(0,0));
    vector<pair<double,double> > bestBoardStat(ITERATIONS,pair<double,double>(0,0));

    // Calculations for Timer
    for (unsigned int i = 0; i < Results.size(); i++) {
        timerStat.first += Results[i].timer.getNanoseconds();
    }
    timerStat.first = timerStat.first/Results.size();

    for(unsigned int i = 0; i < Results.size(); i++) {
        double delta = timerStat.first - Results[i].timer.getNanoseconds();
        timerStat.second += sqrt(delta * delta);
    }
    timerStat.second = timerStat.second/Results.size();

    // Calculations for statistics
    for (int i = 0; i < ITERATIONS; i++) {
        for (unsigned int j = 0; j < Results.size(); j++) {
            resultStat[i].first += Results[j].statistics[i].first;
        }
        resultStat[i].first = resultStat[i].first/Results.size();

        for(unsigned int j = 0; j < Results.size(); j++) {
            double delta = Results[j].statistics[i].first - resultStat[i].first;
            resultStat[i].second += sqrt(delta * delta);
        }
        resultStat[i].second = resultStat[i].second/Results.size();
    }

    // Calculations for bestBoard
    for (int i = 0; i < ITERATIONS; i++) {
        for (unsigned int j = 0; j < Results.size(); j++) {
            bestBoardStat[i].first += Results[j].bestBoard[i];
        }
        bestBoardStat[i].first = bestBoardStat[i].first/Results.size();

        for(unsigned int j = 0; j < Results.size(); j++) {
            double delta = Results[j].bestBoard[i] - bestBoardStat[i].first;
            bestBoardStat[i].second += sqrt(delta * delta);
        }
        bestBoardStat[i].second = bestBoardStat[i].second/Results.size();
    }

    return resultsStruc(timerStat, resultStat, bestBoardStat);
}