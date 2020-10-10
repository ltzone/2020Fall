#include<iostream>
#include<vector>
using namespace std;

class Solution{
public:
    int inv_pairs(vector<int> a){
        return inv_pairs_rec(a,0,a.size()-1);
    }

    int inv_pairs_rec(vector<int> & a, int l, int r){
        if (r <= l)
            return 0;
        int mid = (l + r)/2;
        int res = inv_pairs_rec(a, l, mid);
        res += inv_pairs_rec(a, mid+1, r);

        int lptr = l;
        int rptr = mid+1;
        vector<int> merge(r-l+1,0);
        int j = 0;

        while (lptr <= mid && rptr <= r){
            if (a[lptr] > a[rptr]){
                res += mid - lptr + 1;
                merge[j++] = a[rptr++];
            } else {
                merge[j++] = a[lptr++];
            }
        }
        while (lptr <= mid){
            merge[j++] = a[lptr++];
        }
        while (rptr <= r){
            merge[j++] = a[rptr++];
        }
        for (int i=0;i<merge.size();++i){
            a[l+i] = merge[i];
        }

        return res;
    }
};

int main(){
    int size;
    cin >> size;
    vector<int> arr(size,0);
    for (int i=0;i<size;++i)
        cin >> arr[i];
    Solution t;
    cout << t.inv_pairs(arr);
    return 0;
}