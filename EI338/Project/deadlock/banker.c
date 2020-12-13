#include<stdio.h>
#include<stdlib.h>
#include<string.h>

#define NUMBER_OF_CUSTOMERS 5
#define NUMBER_OF_RESOURCES 4
char MAX_REQUEST_DIR[] = "./max.in";

/* the available amount of each resource */
int available[NUMBER_OF_RESOURCES];

/*the maximum demand of each customer */
int maximum[NUMBER_OF_CUSTOMERS][NUMBER_OF_RESOURCES];

/* the amount currently allocated to each customer */
int allocation[NUMBER_OF_CUSTOMERS][NUMBER_OF_RESOURCES];

/* the remaining need of each customer */
int need[NUMBER_OF_CUSTOMERS][NUMBER_OF_RESOURCES];


int request_resources(int customer_num, int request[]);

void release_resources(int customer_num, int release[]);

int safety_check();

void print_status();

int main(int argc, char **argv){
    /* initialize available and max */
    if (argc != NUMBER_OF_RESOURCES+1){
        printf("Wrong number of resources, input %d, but %d expected\n",argc-1 ,NUMBER_OF_RESOURCES);
        return -1;
    }
    for (int i=0;i<NUMBER_OF_RESOURCES;++i){
        available[i] = atoi(argv[i+1]);
    }

    FILE *fp = fopen(MAX_REQUEST_DIR, "r");
    if (!fp){
        printf("Fail to open file '%s'\n",MAX_REQUEST_DIR);
    }
    for (int i=0;i<NUMBER_OF_CUSTOMERS;++i){
        for (int j=0;j<NUMBER_OF_RESOURCES;++j){
            if (fscanf(fp, "%d,", &maximum[i][j]) != 1){
                printf("The file is not formated correctly.\n");
                fclose(fp);
                return -1;
            }
        }
        fscanf(fp, "\n");
    }

    // for (int i=0;i<NUMBER_OF_CUSTOMERS;++i){
    //     for (int j=0;j<NUMBER_OF_RESOURCES;++j){
    //         printf("%d,", maximum[i][j]);
    //     }
    //     printf("\n");
    // }
    fclose(fp);
    for (int i=0;i<NUMBER_OF_CUSTOMERS;++i){
        for (int j=0;j<NUMBER_OF_RESOURCES;++j){
            allocation[i][j] = 0;
            need[i][j] = maximum[i][j];
        }
    }

    int should_run = 1;

    while (should_run){
        char instr[10];
        printf("banker> ");
        fflush(stdin);
        if (scanf("%s", instr) != 1){
            printf("Empty input.\n");
            continue;
        }
        if (strcmp(instr, "*") == 0){
            print_status();
            continue;
        }
        int customer_num;
        int request[NUMBER_OF_RESOURCES];
        if (scanf("%d", &customer_num) != 1 || customer_num >= NUMBER_OF_CUSTOMERS){
            printf("Invalid Arguments, Customer number expected.\n");
            continue;
        }
        for (int i=0;i<NUMBER_OF_RESOURCES;++i){
            if (scanf("%d", &request[i]) != 1){
                printf("Invalid Arguments, Resource number of %d expected.\n", i);
                continue;
            }
        }

        // printf("%s ",instr);
        // for (int i=0;i<NUMBER_OF_RESOURCES;++i){
        //     printf("%d ",request[i]);
        // }
        // printf("\n");

        if (strcmp(instr,"RQ") == 0){
            if (request_resources(customer_num,request) != 0){
                printf("Request not granted\n");
            } else {
                printf("Request granted\n");
            }
        } else if (strcmp(instr,"RL") == 0){
            release_resources(customer_num,request);
            printf("Released granted\n");
        } else {
            printf("Invalid Instruction, aborted\n");
        }
    }  
    return 0;
}

int request_resources(int customer_num, int request[]){
    /** return 0 if successful and 1 if unsuccessful */
    for (int i=0;i<NUMBER_OF_RESOURCES;++i){
        if (allocation[customer_num][i] + request[i] > maximum[customer_num][i]){
            return 1;
        }
        if (request[i] > available[i]){
            return 1;
        }
        available[i] -= request[i];
        allocation[customer_num][i] += request[i];
        need[customer_num][i] -= request[i];
    }
    if (safety_check() == 1){
        return 0;
    } else {
        for (int i=0;i<NUMBER_OF_RESOURCES;++i){
            available[i] += request[i];
            allocation[customer_num][i] -= request[i];
            need[customer_num][i] += request[i];
        }
        return 1;
    }
}

void release_resources(int customer_num, int release[]){
    for (int i=0;i<NUMBER_OF_RESOURCES;++i){
        if (release[i] > allocation[customer_num][i]){
            release[i] = allocation[customer_num][i];
        }
        available[i] += release[i];
        allocation[customer_num][i] -= release[i];
        need[customer_num][i] += release[i];
    }
}

int safety_check(){
  /**  return 1 if safe and 0 if unsafe
**/
    int work[NUMBER_OF_RESOURCES];
    int finish[NUMBER_OF_CUSTOMERS];
    for (int i=0;i<NUMBER_OF_RESOURCES;++i){
        work[i] = available[i];
    }
    for (int i=0;i<NUMBER_OF_CUSTOMERS;++i){
        finish[i] = 0;
    }
    int finish_cnt = 0;
    while (finish_cnt < NUMBER_OF_CUSTOMERS){
        int chosen_proc = -1;
        for (int i=0;i<NUMBER_OF_CUSTOMERS;++i){
            if (finish[i] == 0){
                int valid_flag = 1;
                for (int j=0;j<NUMBER_OF_RESOURCES;++j){
                    if (need[i][j] > work[j]){
                        valid_flag = 0;
                        break;
                    }
                }
                if (valid_flag == 1){
                    chosen_proc = i;
                    break;
                }
            }
        }
        if (chosen_proc == -1){
            return 0;
        }
        finish_cnt += 1;
        finish[chosen_proc] = 1;
        for (int i=0;i<NUMBER_OF_RESOURCES;++i){
            work[i] += allocation[chosen_proc][i];
        }
    }
    return 1;
}

void print_status(){
    printf("-----available-----\n");
    for (int i=0;i<NUMBER_OF_RESOURCES;++i){
        printf("%d ",available[i]);
    }
    printf("\n");
    printf("-----maximum-----\n");
    for (int i=0;i<NUMBER_OF_CUSTOMERS;++i){
        for (int j=0;j<NUMBER_OF_RESOURCES;++j){
            printf("%d ",maximum[i][j]);
        }
        printf("\n");
    }
    printf("----allocation---\n");
    for (int i=0;i<NUMBER_OF_CUSTOMERS;++i){
        for (int j=0;j<NUMBER_OF_RESOURCES;++j){
            printf("%d ",allocation[i][j]);
        }
        printf("\n");
    }
    printf("-------need-------\n");
    for (int i=0;i<NUMBER_OF_CUSTOMERS;++i){
        for (int j=0;j<NUMBER_OF_RESOURCES;++j){
            printf("%d ",need[i][j]);
        }
        printf("\n");
    }
}