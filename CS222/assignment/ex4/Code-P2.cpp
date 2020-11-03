#include<iostream>
#include<vector>
#include<fstream>
using namespace std;

int bookshelf(vector<int> & thick, vector<int> & width){
    int len = thick.size();
    vector<vector<int> > dp;
    for (int i=0;i<=len;++i)
        dp.push_back(vector<int>(2*len+1,9999));
    dp[0][0]=0;
    for (int i=1;i<=len;++i){
        for(int j=0;j<2*len+1;++j){
            dp[i][j] = dp[i-1][j] + width[i-1];
            if (j >= thick[i-1]){
                dp[i][j] = min(dp[i][j], dp[i-1][j-thick[i-1]]);
            }
        }
    }
    int j;
    for (j=0; j<2*len; ++j){
        if (dp[len][j] <= j)
            break;
    }
    return j;
}

int main(){

    ifstream f("testcase/Data-P2.txt");
    int len;
    f >> len;
    vector<int> thick;
    vector<int> width;
    for (int i=0;i<len;++i){
        int t, w;
        f >> t >> w;
        thick.push_back(t);
        width.push_back(w);
    }

    // int thick_in[] = {1,1,2,2,1};
    // int width_in[] = {12,3,15,5,1};
    // vector<int> thick(thick_in, thick_in + 5);
    // vector<int> width(width_in, width_in + 5);
    cout << bookshelf(thick,width) << endl;
    return 0;
}