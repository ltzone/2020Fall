/**
 * Simple shell interface program.
 *
 * Operating System Concepts - Tenth Edition
 * Copyright John Wiley & Sons - 2018
 */

#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>
#include <string.h>

#define MAX_LINE		80 /* 80 chars per line, per command */

int main(void)
{
	char *args[MAX_LINE/2 + 1];	/* command line (of 80) has max of 40 arguments */
	int should_run = 1;
	
	while (should_run){   
		printf("osh>");
		fflush(stdout);
	
		/**
		 * After reading user input, the steps are:
		 * (1) fork a child process
		 * (2) the child process will invoke execvp()
		 * (3) if command included &, parent will invoke wait()
		 */

		char c;
		int should_new_arg = 1;
		int arg_cnt = 0;
		int arg_len = 0;
		/** collect the input into args 
		 * 
		 * arg_cnt: length of input tokens
		 * 
		*/
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
		} /* end of input processing */

		if (arg_cnt == 0){
			continue;
		}
		
		if (arg_cnt == 1 && strcmp(args[0],"exit") == 0){
			should_run = 0;
			break;
		}

		int should_wait = 1;
		if (args[arg_cnt-1][0] == '&'){
			should_wait = 0;
			free(args[arg_cnt-1]);
			args[--arg_cnt] = NULL;
		}

		pid_t pid = fork();

		if (pid == -1) {
			perror("fork failed");
			exit(EXIT_FAILURE);
		}
		else if (pid == 0) {			
			execvp(args[0],args);
			_exit(EXIT_SUCCESS);
		}
		else {
			int status;
			if (should_wait){
				(void)waitpid(pid, &status, 0);
			}
			for (int i=0;args[i]!=NULL;++i){
				// printf("%s\n",args[i]);
				free(args[i]);
			}
		}
	}
    
	return 0;
}
