/**
 * Simple shell interface program.
 *
 * Operating System Concepts - Tenth Edition
 * Copyright John Wiley & Sons - 2018
 */
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>
#include <string.h>


#define MAX_LINE		80 /* 80 chars per line, per command */

int main(void)
{
	char *last_args[MAX_LINE/2 + 1];
	char *args[MAX_LINE/2 + 1];	/* command line (of 80) has max of 40 arguments */
	int should_run = 1;
	int last_arg_cnt = 0;

	last_args[last_arg_cnt] = NULL;

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


		if (arg_cnt == 1 && args[0][0] =='!' && args[0][1] == '!'){
			if (last_arg_cnt == 0){
				printf("Error: last command does not exist\n");
				continue;
			}
			printf("History Mode Executing: ");
			/** history mode, copy history storage to current args */
			for (int i=0;i<last_arg_cnt;++i){
				if (i>=1){
					args[i] =(char*) malloc(MAX_LINE*sizeof(char));
				}
				strcpy(args[i],last_args[i]);
				printf("%s ",args[i]);
			}
			printf("\n");
			arg_cnt = last_arg_cnt;
			args[arg_cnt] = NULL;
		} else {
			/* copy current args to history storage */
			for (int i=0;i<arg_cnt;++i){
				if (i>=last_arg_cnt){
					last_args[i] =(char*) malloc(MAX_LINE*sizeof(char));
				}
				strcpy(last_args[i],args[i]);
			}
			for (int i=arg_cnt;i<last_arg_cnt;++i){
				free(last_args[i]);
			}
			last_arg_cnt = arg_cnt;
			last_args[last_arg_cnt] = NULL;
		}

		int should_wait = 1;
		if (args[arg_cnt-1][0] == '&'){
			should_wait = 0;
			free(args[arg_cnt-1]);
			args[--arg_cnt] = NULL;
		}

		int redirect_output = 0;
		char* output_dir = NULL;
		if (arg_cnt > 2 && args[arg_cnt-2][0] == '>'){
			redirect_output = 1;
			output_dir = args[arg_cnt-1];
			free(args[arg_cnt-2]);
			arg_cnt -= 2;
			args[arg_cnt] = NULL;
		}

		int redirect_input = 0;
		char* input_dir = NULL;
		if (arg_cnt > 2 && args[arg_cnt-2][0] == '<'){
			redirect_input = 1;
			input_dir = args[arg_cnt-1];
			free(args[arg_cnt-2]);
			arg_cnt -= 2;
			args[arg_cnt] = NULL;
		}

		if (redirect_input && redirect_output){
			printf("Input and Output can't be simultaneously redirected\n");
			continue;
		}




		pid_t pid = fork();

		if (pid == -1) {
			perror("fork failed");
			exit(EXIT_FAILURE);
		}
		else if (pid == 0) {
			if (redirect_input){
				int input_f = open(input_dir,O_RDONLY);
				dup2(input_f,STDIN_FILENO);
			}
			if (redirect_output){
				int output_f = open(output_dir,O_WRONLY);
				dup2(output_f,STDOUT_FILENO);
			}
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
