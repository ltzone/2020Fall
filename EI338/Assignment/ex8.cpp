#include<omp.h>
#include<iostream>
#include<fstream>

using namespace std; 


int* generate_array(int len, int randl, int randr){
    int* gen = new int [len];
    for (int i=0; i<len; ++i){
        gen[i] = rand() % (randr - randl + 1) + randl;
    }
    return gen;
}

int serial_sum(int* arr, int len){
    int sum = 0;
    for (int i=0; i<len; ++i){
        sum += arr[i];
    }
    return sum;
}

void parallel_runner(int* arr, int len, int* result);

int parallel_sum(int* arr, int len){
    int sum = 0;
    // # pragma omp parallel for num_threads(4) reduction(+:sum)
    // for (int i=0; i<len; ++i){
    //     sum += arr[i];
    // }
    #pragma omp parallel num_threads(4)
    parallel_runner(arr,len,&sum);
    return sum;
}

void parallel_runner(int* arr, int len, int* result){
    int my_thread = omp_get_thread_num();
    int thread_count = omp_get_num_threads();
    int local_sum = 0;
    for (int i=0;i*thread_count+my_thread<len;++i){
        local_sum += arr[i*thread_count+my_thread];
    }
    #pragma omp critical
    *result += local_sum;
    return;
}


int main(int argc, char* argv[]){
    int m = 10, l = 0, r = 5;
    // generate a random array with 1000 elements ranging from 0 to 4;
    int* arr = generate_array(m,l,r);

    double t1,t2,t3;
    t1 = omp_get_wtime();
    int sum_res1 = serial_sum(arr, m);
    t2 = omp_get_wtime();
    int sum_res2 = parallel_sum(arr, m);
    t3 = omp_get_wtime();
    cout << "Serial Time: " << t2 - t1 << "\tResult: " << sum_res1 << endl;
    cout << "Parallel Time: " << t3 - t2 << "\tResult: " << sum_res2 << endl;
    cout << (t2 - t1) /(t3 - t2) << endl;
    delete [] arr;
    return 0;
}