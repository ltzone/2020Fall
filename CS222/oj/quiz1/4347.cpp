#include<iostream>
#include <algorithm>


using namespace std;

typedef struct Task {
    double start = 0;
    double end = 25;
} task;

bool task_cmp (task i,task j){
    return (i.end < j.end);
}


int main(){
    int size;
    cin >> size;

    task* schedules = new task [size];
    for (int i=0; i<size;++i){
        double t;
        cin >> t;
        if (t >= 0 && t <= 24)
            schedules[i].start = t;
    }
    for (int i=0; i<size;++i){
        double t;
        cin >> t;
        if (t >= 0 && t <= 24 && t > schedules[i].start)
            schedules[i].end = t;
    }

    sort(schedules, schedules+size, task_cmp);

    // for (int i=0; i<size;++i){
    //     cout << schedules[i].start << " " << schedules[i].end << endl;
    // }

    double end_work = -1;
    int cnt = 0;

    for (int i=0; i<size; ++i){
        if (schedules[i].start >= end_work){
            cnt++;
            end_work = schedules[i].end;
        }
    }

    delete [] schedules;

    cout << cnt << endl;
    return 0;
}