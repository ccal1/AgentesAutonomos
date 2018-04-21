#include "timer.h"

using namespace std::chrono;

Timer::Timer() {
    this->timebegin = high_resolution_clock::now();
    this->duration = nanoseconds(0);
    this->paused = false;
}

double Timer::getMilliseconds() {
    if (!this->paused) {
        pause();
        start();
    }
    return duration.count()/1000000.0;
}

double Timer::getNanoseconds() {
    if (!this->paused) {
        pause();
        start();
    }
    return duration.count();
}

void Timer::start() {
    this->paused = false;
    this->timebegin = high_resolution_clock::now();
}

void Timer::pause() {
    if(!this->paused) {
        duration += duration_cast<nanoseconds>(high_resolution_clock::now() - this->timebegin);    
    }
    this->paused = true;
}

bool Timer::isPaused(){
    return this->paused;
}
