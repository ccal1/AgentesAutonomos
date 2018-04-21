#ifndef _H_TIMER_
#define _H_TIMER_
#include <chrono>

using namespace std::chrono;

class Timer {
private:
    bool paused;
    high_resolution_clock::time_point timebegin, timeend;
    nanoseconds::rep nanoseconds;
    milliseconds duration;
public:
    Timer(); // Starts automatically on construction
    double getMilliseconds();
    void start();
    void pause();
    bool isPaused();
};

#endif
