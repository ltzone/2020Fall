#include<omp.h>
#include<iostream>

using namespace std;


int sum(int* arr, int len){
    int sum = 0;
    # pragma omp parallel for num_threads(3) reduction(+:sum)
    for (int i=0;i<len;++i){
        sum += arr[i];
    }
    return sum;
}

template <typename Type>
int Matrix_Mul(Type* Mat_A, Type* Mat_B, Type* Mat_C, int M, int N, int K);


int main(int argc, char* argv[]){
    int a[] = {2,3,4,5,6,7,8,9,10,11};
    cout << sum(a, 10) << endl;
    return 0;
}

template <typename Type>
int Matrix_Mul(Type* Mat_A, Type* Mat_B, Type* Mat_C, int M, int N, int K){
    return 0;
}