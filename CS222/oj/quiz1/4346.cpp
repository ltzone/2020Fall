#include<vector>
#include<iostream>
using namespace std;

class Solution {
public:
    int candy(vector<int>& ratings) {
        if (ratings.size() == 0)
            return 0;
        int sum = 0;
        vector<int> left2right(ratings.size(),1);
        vector<int> right2left(ratings.size(),1);
        for (int i=1; i<ratings.size(); i++){
            if (ratings[i] > ratings[i - 1]){
                left2right[i] = left2right[i-1] * 2;
            }
        }
        for (int i=ratings.size()-2;i>=0;i--){
            if (ratings[i] > ratings[i + 1]) {
                right2left[i] = right2left[i + 1] * 2;
            }
        }
        for (int i=0; i< ratings.size();i++){
            sum += max(left2right[i], right2left[i]);
        }
        return sum;
    }
};

int main(){
    int size;
    cin >> size;
    if (size <= 1){
        cout << 0;
        return 0;
    }
    if (size%2 == 0){
        vector<int> a(size/2,0);
        vector<int> b(size/2,0);
        int i=0;
        while (i<size){
            if (i%2 == 1){
                cin >> a[i/2];
            } else {
                cin >> b[i/2];
            }
            ++i;
        }
        Solution s;
        cout << s.candy(a) + s.candy(b);
    } else {
        vector<int> a(size/2,0);
        vector<int> b(size/2 + 1,0);
                int i=0;
        while (i<size){
            if (i%2 == 1){
                cin >> a[i/2];
            } else {
                cin >> b[i/2];
            }
            ++i;
        }
        Solution s;
        cout << s.candy(a) + s.candy(b);
    }
    return 0;
}
