#include <pthread.h>
#include <stdio.h>
#include <ctype.h>
#include <limits.h>
#include <string.h>
#include <stdlib.h>
#include <unistd.h> 
#include <sys/types.h>
#include <sys/wait.h>
int value = 0;
void *runner(void *param);

int main(int argc, char *argv[]){
    pid_t pid;
    pthread_t tid;
    pthread_attr_t attr;

    pid = fork();

    if (pid == 0) {
        fork();
        pthread_attr_init(&attr);
        pthread_create(&tid,&attr,runner,NULL);
        // pthread_join(tid,NULL);
    }
    fork();
    sleep(5);
    printf("Create Process\n");
}

void *runner(void *param){
    printf("Create Thread %ld \n",pthread_self());
    pthread_exit(0);
}

