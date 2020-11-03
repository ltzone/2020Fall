#include<iostream>
#include<vector>
#include<fstream>
using namespace std;

class Solution{
public:
    vector<int> game(vector<int> & v){
        vector<vector<int> > dp;
        for (int i=0;i<v.size();++i){
            dp.push_back(vector<int>(v.size(),0));
        }

        for(int i=v.size()-1;i>=0;--i){
            dp[i][i] = v[i];
            if(i+1<v.size())
                dp[i][i+1] = max(v[i],v[i+1]);
            for(int j=i+2;j<v.size();++j){
                int next1 = dp[i+1][j-1];
                if (i+2 < v.size()){
                    next1 = min(next1, dp[i+2][j]);
                }
                int next2 = dp[i+1][j-1];
                if (j-2 >= i){
                    next2 = min(next2, dp[i][j-2]);
                }
                dp[i][j] = max(v[i]+next1, v[j]+next2);
            }
        }
        cout << dp[0][v.size()-1] << endl;

        // recover
        vector<int> trace;
        int i=0,j=v.size()-1;
        while(i < v.size()-2 && j - i >= 2){
            int val = dp[i][j];
            int take_right = min(dp[i][j-2],dp[i+1][j-1]);
            int take_left = min(dp[i+2][j],dp[i+1][j-1]);
            if (val == take_right + v[j]){
                trace.push_back(v[j]);
                if (dp[i][j-2] < dp[i+1][j-1]){
                    j-=2;
                } else {
                    i++;j--;
                }
            } else if (val == take_left + v[i]){
                trace.push_back(v[i]);
                if (dp[i+2][j] < dp[i+1][j-1]){
                    j+=2;
                } else {
                    i++;j--;
                }
            }
        };
        if (i == j){
            trace.push_back(v[i]);
            return vector<int>(trace.rbegin(),trace.rend());
        } else{
            trace.push_back(max(v[i], v[j]));
            return vector<int>(trace.rbegin(),trace.rend());
        }
    }
};

int main(){
    // int a[] = {8,15,3,7};
    // vector<int> test1(a, a+4);
    vector<int> input;
    ifstream f("testcase/Data-P4.txt");
    while (! f.eof()){
        int a;
        f >> a;
        input.push_back(a);
    }
    Solution s;
    vector<int> result = s.game(input);

    ofstream ans("result/Ans-P4.txt",ofstream::trunc);

    for (int i=0;i<result.size();++i){
        ans << result[i] << " ";
    }
    ans << endl;
    ans.close();
    return 0;
}

// ans: 247411