#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>

#define MAX_LINE		80 /* 80 chars per line, per command */

// int main(){
//     char c[10];
//     c[0] = 'a';
//     c[1] = '\0';
//     printf("%s\n",c);
//     return 0;
// }


int main ()
{
    char *args[MAX_LINE/2 + 1];
    printf("osh>");
    fflush(stdout);
    char c;
    int should_new_arg = 1;
    int arg_cnt = 0;
    int arg_len = 0;
    while (1) {
        c = getchar();
        if (c == '\n'){
            if (arg_cnt > 0)
                args[arg_cnt-1][arg_len++] = '\0';
            args[arg_cnt] = NULL;
            break;
        }
        if (c == ' '){
            if (should_new_arg == 0){
                if (arg_cnt > 0)
                    args[arg_cnt-1][arg_len++] = '\0';
                should_new_arg = 1;
            }
        } else {
            if (should_new_arg){
                char* new_arg;
                new_arg = (char*) malloc(MAX_LINE*sizeof(char));
                args[arg_cnt++] = new_arg;
                arg_len = 0;
                args[arg_cnt-1][arg_len++] = c;
                should_new_arg = 0;
            } else {
                args[arg_cnt-1][arg_len++] = c;
            }
        }
    }
    

    for (int i=0;args[i]!=NULL;++i){
        printf("%s\n",args[i]);
        free(args[i]);
    }
  return 0;
}