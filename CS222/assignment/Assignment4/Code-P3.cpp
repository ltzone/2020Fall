#include<iostream>
#include<string>
#include<fstream>
#include<sstream>
#include<vector>
using namespace std;

class Solution{
private:
    string dna1;
    string dna2;
    vector<pair<int,int> > p; 
    int loss(char a){
        switch (a) {
            case 'A':
                return 1;
            case 'T':
                return 2;
            case 'C':
                return 3;
            case 'G':
                return 1;
            default:
                return 0;
        }
    }

    int loss_seq(string & a, int beg, int end){
        int i = beg;
        int sum = 0;
        while (i <= end){
            sum += loss(a[i]);
            i++;
        }
        return sum;
    }

    int edit(char a, char b){
        if (a==b)
            return 0;
        if (a>b)
            return edit(b,a);
        if (a == 'A'){
            switch (b){
                case 'C': return 1;
                case 'G': return 5;
                case 'T': return 1;
                default: return 0;
            }
        } else if (a == 'C'){
            switch (b){
                case 'G': return 1;
                case 'T': return 1;
                default: return 0;
            }
        } else if (a == 'G' && b == 'T'){
            return 9;
        }
        return 0;
    }

public:
    int f_end1;
    int f_end2;
    Solution(string & f1, string & f2):dna1(f1),dna2(f2){
        while ((dna1[dna1.size()-1] != 'A') &&
               (dna1[dna1.size()-1] != 'T') &&
               (dna1[dna1.size()-1] != 'C') &&
               (dna1[dna1.size()-1] != 'G')){
                   dna1.pop_back();
               }
        while ((dna2[dna2.size()-1] != 'A') &&
               (dna2[dna2.size()-1] != 'T') &&
               (dna2[dna2.size()-1] != 'C') &&
               (dna2[dna2.size()-1] != 'G')){
                   dna2.pop_back();
               }
        f_end1 = dna1.size()-1; f_end2 = dna2.size()-1;
        cout << dna1.size()-1 << " " << dna2.size() -1 << endl;
        cout << dna1[dna1.size()-1] <<" " << dna2[dna2.size()-1] << endl;
    }

    vector<pair<int,int> > simpleAlignment(int beg1, int end1, int beg2, int end2){
        int len1 = end1 - beg1 + 1;
        int len2 = end2 - beg2 + 1;
        vector<vector<int> > dp(len1 + 1, vector<int>(len2 + 1, INT32_MAX));
        dp[0][0] = 0;
        for (int i=0; i<=len1; ++i){
            dp[i][0] = loss_seq(dna1,beg1,beg1+i-1);
        }
        for (int j=0; j<=len2; ++j){
            dp[0][j] = loss_seq(dna2,beg2,beg2+j-1);
        }
        for (int i=1; i<=len1; ++i){
            for (int j=1; j<=len2; ++j){
                int edit_cost = edit(dna1[beg1+i-1],dna2[beg2+j-1]) + dp[i-1][j-1];
                int cut1_cost = loss(dna1[beg1+i-1]) + dp[i-1][j];
                int cut2_cost = loss(dna2[beg2+j-1]) + dp[i][j-1];
                dp[i][j] = min(edit_cost,min(cut1_cost, cut2_cost));
            }
        }
        int i=len1, j=len2;
        vector<pair<int,int> > result;
        while (i > 0 && j > 0){
            int val = dp[i][j];
            if (dp[i-1][j-1]+edit(dna1[beg1+i-1],dna2[beg2+j-1]) == val){
                i--;j--;
            } else if (dp[i-1][j] + loss(dna1[beg1+i-1]) == val){
                i--;
            } else {
                j--;
            }
            result.push_back(pair<int,int>(beg1+i,beg2+j));
        }
        while (i > 0){
            i--;
            result.push_back(pair<int,int>(beg1+i,beg2));
        }
        while (j > 0){
            j--;
            result.push_back(pair<int,int>(beg1,beg2+j));
        }
        vector<pair<int,int> > res_reversed(result.rbegin(),result.rend());
        return res_reversed;
    }

    pair<string, string> originalAlignment(int beg1, int end1, int beg2, int end2){
        int len1 = end1 - beg1 + 1;
        int len2 = end2 - beg2 + 1;
        vector<vector<int> > dp(len1 + 1, vector<int>(len2 + 1, INT32_MAX));
        dp[0][0] = 0;
        for (int i=0; i<=len1; ++i){
            dp[i][0] = loss_seq(dna1,beg1,beg1+i-1);
        }
        for (int j=0; j<=len2; ++j){
            dp[0][j] = loss_seq(dna2,beg2,beg2+j-1);
        }
        for (int i=1; i<=len1; ++i){
            for (int j=1; j<=len2; ++j){
                int edit_cost = edit(dna1[beg1+i-1],dna2[beg2+j-1]) + dp[i-1][j-1];
                int cut1_cost = loss(dna1[beg1+i-1]) + dp[i-1][j];
                int cut2_cost = loss(dna2[beg2+j-1]) + dp[i][j-1];
                dp[i][j] = min(edit_cost,min(cut1_cost, cut2_cost));
            }
        }
        cout << dp[len1][len2];
        // int i=len1, j=len2;
        // string res1, res2;
        // while (i > 0 && j > 0){
        //     int val = dp[i][j];
        //     if (dp[i-1][j-1]+edit(dna1[beg1+i-1],dna2[beg2+j-1]) == val){
        //         res1.push_back(dna1[beg1+i-1]);
        //         res2.push_back(dna2[beg2+j-1]);
        //         i--;j--;
        //     } else if (dp[i-1][j] + loss(dna1[beg1+i-1]) == val){
        //         res1.push_back('-');
        //         res2.push_back(' ');
        //         i--;
        //     } else {
        //         res1.push_back(' ');
        //         res2.push_back('-');
        //         j--;
        //     }
        // }
        // while (i > 0){
        //     res2.push_back(' ');
        //     res1.push_back('-');i--;
        // }
        // while (j > 0){
        //     res1.push_back(' ');
        //     res2.push_back('-');j--;
        // }
        // string res1_reversed(res1.rbegin(),res1.rend());
        // string res2_reversed(res2.rbegin(),res2.rend());
        // cout << dp[len1][len2] << endl;
        // return pair<string,string>(res1_reversed,res2_reversed);
        return pair<string,string>();
    }

    vector<int> spaceEfficientAlignment(int beg1, int end1, int beg2, int end2){
        int len1 = end1 - beg1 + 1;
        int len2 = end2 - beg2 + 1;
        vector<vector<int> > dp(2, vector<int>(len1 + 1, INT32_MAX));
        int loss_sum = 0;
        dp[0][0] = 0;
        for (int i=1;i<=len1;++i){
            loss_sum += loss(dna1[beg1+i-1]);
            dp[0][i] = loss_sum;
        }
        dp[1][0] = 0;
        for (int j=1; j<=len2; ++j){
            dp[1][0] += loss(dna2[beg2+j-1]);
            for (int i=1;i<=len1;++i){
                int edit_cost = edit(dna1[beg1+i-1],dna2[beg2+j-1]) + dp[0][i-1];
                int cut1_cost = loss(dna1[beg1+i-1]) + dp[1][i-1];
                int cut2_cost = loss(dna2[beg2+j-1]) + dp[0][i];
                dp[1][i] = min(edit_cost,min(cut1_cost, cut2_cost));
            }
            for (int i=0;i<=len1;++i){
                dp[0][i] = dp[1][i];
            }
        }
        vector<int > tmp_res(++dp[0].begin(),dp[0].end());
        return tmp_res;
        return dp[0];
    }
    vector<int> backwardSpaceEfficientAlignment(int beg1, int end1, int beg2, int end2){
        int len1 = end1 - beg1 + 1;
        int len2 = end2 - beg2 + 1;
        vector<vector<int> > dp(2, vector<int>(len1 + 1, INT32_MAX));
        int loss_sum = 0;
        dp[0][0] = 0;
        for (int i=1;i<=len1;++i){
            loss_sum += loss(dna1[end1-i+1]);
            dp[0][i] = loss_sum;
        }
        dp[1][0] = 0;
        for (int j=1; j<=len2; ++j){
            dp[1][0] += loss(dna2[end2-j+1]);
            for (int i=1;i<=len1;++i){
                int edit_cost = edit(dna1[end1-i+1],dna2[end2-j+1]) + dp[0][i-1];
                int cut1_cost = loss(dna1[end1-i+1]) + dp[1][i-1];
                int cut2_cost = loss(dna2[end2-j+1]) + dp[0][i];
                dp[1][i] = min(edit_cost,min(cut1_cost, cut2_cost));
            }
            for (int i=0;i<=len1;++i){
                dp[0][i] = dp[1][i];
            }
        }
        vector<int > res_reversed(dp[0].rbegin(),--dp[0].rend());
        return res_reversed;
        // return dp[0];
    }

    vector<pair<int,int> > divideAndConquerAlignment(int beg1, int end1, int beg2, int end2){
        int len1 = end1 - beg1 + 1;
        int len2 = end2 - beg2 + 1;
        if (len1 <= 2 || len2 <= 2){
            return simpleAlignment(beg1, end1, beg2, end2);
        }
        int mid2 = (beg2 + end2) / 2;
        vector<int> left_cost = spaceEfficientAlignment(beg1, end1, beg2, mid2);
        vector<int> right_cost = backwardSpaceEfficientAlignment(beg1, end1, mid2, end2);
        int q = 0; int min = INT32_MAX;
        for (int i=0;i<left_cost.size();++i){
            if (left_cost[i] + right_cost[i] < min){
                min = left_cost[i] + right_cost[i];
                q = i;
            }
        }
        q += beg1;
        // if (len1 == 3001){
        //     cout << min << endl;
        // }
        // cout << q << "," << mid2 << endl;
        vector<pair<int,int> > left_result = divideAndConquerAlignment(beg1,q,beg2,mid2);
        vector<pair<int,int> > right_result = divideAndConquerAlignment(q,end1,mid2,end2);
        left_result.insert(left_result.end(), right_result.begin(), right_result.end());
        return left_result;
    }

    pair<string,string> format_output(vector<pair<int, int> > result, int end1, int end2){
        string res1, res2;
        result.push_back(pair<int,int>(end1+1,end2+1));
        for (int i=0;i<result.size()-1;++i){
            pair<int,int> item = result[i];
            pair<int,int> next = result[i+1];
            if ((item.first == next.first) && ((item.second + 1) == next.second)) {
                res1.push_back(' ');
                res2.push_back('-');
            } else if (((item.first + 1) == next.first) && (item.second == next.second)){
                res1.push_back('-');
                res2.push_back(' ');
            } else if ((item.first + 1 == next.first) && (item.second + 1 == next.second)){
                res1.push_back(dna1[item.first]);
                res2.push_back(dna2[item.second]);
            }
        }
        return pair<string, string>(res1,res2);
    }

    pair<string,string> solution(){
        int end1 = dna1.size()-1, end2 = dna2.size()-1;
        // int end1 = 20,  end2 = 20;
        // int end1 = 3000, end2 = 2990;
        // cout << end1  << " " << end2 << endl;
        vector<pair<int,int> > tmp = divideAndConquerAlignment(0,end1,0,end2);
        return format_output(tmp, end1, end2);
    }
};

int main(){
    ifstream t1("testcase/Data-P3a.txt");
    ifstream t2("testcase/Data-P3b.txt");
    stringstream f1, f2;
    f1 << t1.rdbuf();
    f2 << t2.rdbuf();
    string dna1(f1.str()),dna2(f2.str());
    Solution s(dna1, dna2);
    ofstream ans1("result/Ans-P3a.txt",ofstream::trunc);
    ofstream ans2("result/Ans-P3b.txt",ofstream::trunc);
    pair<string,string> efficient_result = s.solution();
    ans1 << efficient_result.first << endl;
    ans2 << efficient_result.second << endl;
    ans1.close();
    ans2.close();
    return 0;
}