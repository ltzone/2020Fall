#include<omp.h>
#include<iostream>
#include<fstream>

using namespace std;

template <typename Type>
Type* Matrix_Mul_Serial(Type* Mat_A, Type* Mat_B, int M, int N, int K);

int* generate_matrix(int M, int N, int rangeL, int rangeR);

template <typename Type>
void output_matrix(Type* Mat, int M, int N, const char * output_dir);

template <typename Type>
Type* input_matrix(int M, int N, const char * input_dir);

template<typename Type>
Type* Matrix_Mul_Parallel_Loop(Type* Mat_A, Type* Mat_B, int M, int N, int K);

int main(int argc, char* argv[]){
    int m = 1000, n = 1000, k = 1000;
    int l = 0, r = 5;
    int* mat1 = generate_matrix(m,n,l,r);
    int* mat2 = generate_matrix(n,k,l,r);

    double t1,t2;
    t1 = omp_get_wtime();
    // int* mat_res = Matrix_Mul_Serial(mat1, mat2, m, n, k);
    int* mat_res = Matrix_Mul_Parallel_Loop(mat1, mat2, m, n, k);
    t2 = omp_get_wtime();
    cout << "Time: " << t2 - t1 << endl;
    // output_matrix(mat_res, m, k,"serial_result.mat");
    delete [] mat_res;

    return 0;
}

template<typename Type>
Type* Matrix_Mul_Parallel_Loop(Type* Mat_A, Type* Mat_B, int M, int N, int K){
    Type* res = new Type [M * K];
    for (int i=0;i<M*K;++i){
        res[i] = 0;
    }

    # pragma omp parallel for num_threads(8)
    for (int i=0;i<M;++i){
        for (int j=0;j<K;++j){
            for (int k=0;k<N;++k){
                res[i*K+j] += (Mat_A[i*N+k] * Mat_B[k*K+j]);
            }
        }
    }

    return res;
}

template <typename Type>
Type* Matrix_Mul_Serial(Type* Mat_A, Type* Mat_B, int M, int N, int K){
    Type* res = new Type[M*K];
    for (int i=0;i<M*K;++i){
        res[i] = 0;
    }
    for (int i=0;i<M;++i){
        for (int j=0;j<K;++j){
            for (int k=0;k<N;++k){
                res[i*K+j] += (Mat_A[i*N+k] * Mat_B[k*K+j]);
            }
        }
    }
    return res;
}

int* generate_matrix(int M, int N, int rangeL, int rangeR){
    int n = M * N;
    int* res = new int [n];
	for (int i = 0; i < n; i++)
	    res[i] = rand() % (rangeR - rangeL + 1) + rangeL;
	return res;
}


template <typename Type>
void output_matrix(Type* Mat, int M, int N, const char * output_dir){
    ofstream outfile;
    outfile.open(output_dir, ios::out | ios::trunc);
    for (int i=0;i<M;++i){
        for (int j=0;j<N;++j){
            outfile << Mat[i*N+j] << ' ';
        }
        outfile << endl;
    }
    outfile.close();
}

template <typename Type>
Type* input_matrix(int M, int N, const char * input_dir){
    ifstream infile;
    int n = M * N;
    Type* res = new Type [n];
    infile.open(input_dir);
    for (int i=0;i<M;++i){
        for (int j=0;j<N;++j){
            infile >> res[i*N+j];
        }
    }
    infile.close();
    return res;
}
