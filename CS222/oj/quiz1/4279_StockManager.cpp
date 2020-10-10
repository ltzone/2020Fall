#include<iostream>
#include<vector>
using namespace std;

int main(){
    int size;
    cin >> size;
    vector<int> prices(size,0);
    for (int i=0;i<size;++i){
        cin >> prices[i];
    }
    if (prices.size() == 0){
        cout << 0;
        return 0;
    }
    int buy = 0;
    int sell = 0;
    int profit = 0;
    int i = 0;
    while (i < prices.size()-1){
        while (i<prices.size()-1 && prices[i] >= prices[i+1]){
            i++;
        }
        buy = prices[i];
        while (i<prices.size()-1 && prices[i] <= prices[i+1]){
            i++;
        }
        sell = prices[i];
        profit+= sell - buy;
    }
    cout << profit;
    return 0;
}