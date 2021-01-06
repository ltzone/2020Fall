#include<iostream>
#include<vector>
#include<fstream>
using namespace std;



static int* now = new int[10000000];
static int* prev_col = new int[10000000];

pair<int,int> preprocess(int* s, int len){
    int sum = 0;
    for (int i=0; i<len; ++i){
        if (s[i] < 0){
            s[i] = -s[i];
        }
        sum += s[i];
    }
    int goal = sum / 2;
    return pair<int,int>(sum,goal);
}

int knapsack(int* s, int goal, int len){
    for (int i=0;i<=goal;++i){
        now[i] = 0;
    }
    for (int i=0;i<len;++i){
        for (int w=1; w<=goal;++w){
            if (s[i] > w) {
                now[w] = prev_col[w];
            } else {
                now[w] = max(prev_col[w], s[i]+prev_col[w-s[i]]);
            }
        }
        for (int w=0; w<=goal;++w){
            prev_col[w] = now[w];
        }
    }
    return prev_col[goal];
}

int solve(int* s, int len){
    pair<int,int> a = preprocess(s,len);
    int goal = a.second;
    int sum = a.first;
    int achieve = knapsack(s,goal,len);
    return (sum-achieve-achieve);
}


int main(){
    ifstream f("testcase/Data-P1.txt");
    int tmp[10000];
    for (int i=0;i<10000;++i){
        f >> tmp[i];
    }
    cout << solve(tmp,10000) << endl;;
    return 0;

}