#include<iostream>
#include<vector>
#include<fstream>
using namespace std;

pair<int,int> preprocess(vector<int> & s){
    int sum = 0;
    for (int i=0; i<s.size(); ++i){
        if (s[i] < 0){
            s[i] = -s[i];
        }
        sum += s[i];
    }
    int goal = sum / 2;
    return pair<int,int>(sum,goal);
}

int knapsack(vector<int> & s, int goal){
    vector<int> now(goal+1,0);
    vector<int> prev(goal+1,0);
    for (int i=0;i<s.size();++i){
        for (int w=0; w<=goal;++w){
            if (s[i] > w) {
                now[w] = prev[w];
            } else {
                now[w] = max(prev[w], s[i]+prev[w-s[i]]);
            }
        }
        for (int w=0; w<=goal;++w){
            prev[w] = now[w];
        }
    }
    return prev[goal];
}

int solve(vector<int> &s){
    pair<int,int> a = preprocess(s);
    int goal = a.second;
    int sum = a.first;
    int achieve = knapsack(s,goal);
    return (sum-achieve-achieve);
}


int main(){
    int a[] = {1,-6,11,-5};
    vector<int> test1(a, a+4);
    vector<int> input;
    ifstream f("testcase/Data-P1.txt");
    while (! f.eof()){
        int a;
        f >> a;
        input.push_back(a);
    }
    cout << solve(test1) << endl;;
    return 0;

}