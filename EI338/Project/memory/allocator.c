#include<stdio.h>
#include<stdlib.h>
#include<string.h>

#define PROC_NAME_SIZE 20

typedef struct MemBlock {
    int beg;
    int size;
    struct MemBlock* next;
    char name[PROC_NAME_SIZE];
    int status; // 0 unused, 1 in use
} mem_block;

mem_block* mem_head = NULL;

int request_memory(char* proc_name, int request_size, char mode);

int request_memory_first_fit(char* proc_name, int request_size);
int request_memory_best_fit(char* proc_name, int request_size);
int request_memory_worst_fit(char* proc_name, int request_size);

int release_memory(char* proc_name);

void print_status();

void compact_mem();

void init_data(){
    request_memory("P1",100,'F');
    request_memory("P2",210,'W');
    request_memory("P3",400,'F');
    request_memory("P4",220,'B');
    request_memory("P5",230,'F');
}

int main(int argc, char **argv){
    if (argc != 2){
        printf("Wrong Argument Number, input %d, but 1 (memory size) expected\n",argc-1);
        return -1;
    }

    /* initialize */
    mem_head = malloc(sizeof(mem_block));
    mem_head->beg = 0;
    if (sscanf(argv[1],"%d",&(mem_head->size)) != 1){
        printf("Input Size should be a number\n");
        return -1;
    };
    mem_head->next = NULL;
    strcpy(mem_head->name,"Unused");
    mem_head->status = 0;

    // init_data();

    int should_run = 1;

    while (should_run){
        char instr[10];
        printf("allocator> ");
        fflush(stdin);
        if (scanf("%s", instr) != 1){
            printf("Empty input.\n");
            continue;
        }
        if (strcmp(instr, "STAT") == 0){
            print_status();
            continue;
        }
        if (strcmp(instr, "X") == 0){
            should_run = 0;
            break;
        }
        if (strcmp(instr, "C") == 0){
            compact_mem();
            continue;
        }
        if (strcmp(instr, "RQ") == 0){
            char proc_name[PROC_NAME_SIZE];
            int request_size;
            char alloc_mode;
            if (scanf("%s %d %c", proc_name, &request_size, &alloc_mode) != 3){
                printf("Error RQ format, expected process name + request size + alloc mode\n");
                continue;
            }
            int alloc_status = request_memory(proc_name, request_size, alloc_mode);
            if (alloc_status == 0){
                printf("Memory Allocation Granted\n");
            } else {
                printf("Memory Allocation Failed\n");
            }
        }
        if (strcmp(instr, "RL") == 0){
            char proc_name[PROC_NAME_SIZE];
            if (scanf("%s", proc_name) != 1){
                printf("Error RL format, process name expected\n");
                continue;
            }
            int release_number = release_memory(proc_name);
            printf("Released %d blocks of memory of %s\n", release_number, proc_name);
        }
    }  
    return 0;
}


void print_status(){
    mem_block* current_block = mem_head;
    while (current_block != NULL){
        printf("Addresses [%d:%d]\t", current_block->beg, current_block->beg+current_block->size-1);
        if (current_block->status == 0){
            printf("%s\n",current_block->name);
        } else {
            printf("Process %s\n",current_block->name);
        }
        current_block = current_block->next;
    }
    return;
}

void compact_mem(){
    mem_block* current_block = mem_head;
    int free_mem = 0;
    int used_mem = 0;
    while (current_block != NULL && current_block->status == 0){
        mem_head = current_block->next;
        free_mem += current_block->size;
        free(current_block);
        current_block = mem_head;
    }

    mem_block* prev_block = current_block;
    current_block->beg = used_mem;
    used_mem += current_block->size;
    current_block = current_block->next;

    while (current_block != NULL){
        if (current_block->status == 0){
            free_mem += current_block->size;
            mem_block* tmp = current_block;
            current_block = current_block->next;
            free(tmp);
        } else {
            current_block->beg = used_mem;
            used_mem += current_block->size;
            prev_block->next = current_block;
            prev_block = current_block;
            current_block = current_block->next;
        }
    }
    prev_block->next = malloc(sizeof(mem_block));
    prev_block->next->beg = used_mem;
    strcpy(prev_block->next->name,"Unused");
    prev_block->next->next = NULL;
    prev_block->next->size = free_mem;
    prev_block->next->status = 0;
    return;
}


int request_memory(char* proc_name, int request_size, char mode){
    switch (mode)
    {
    case 'F':
    case 'f':
        return request_memory_first_fit(proc_name, request_size);
    case 'B':
    case 'b':
        return request_memory_best_fit(proc_name, request_size);
    case 'W':
    case 'w':
        return request_memory_worst_fit(proc_name, request_size);
    default:
        return -1;
    }
    return -1;
}

void split_block(char* proc_name, int request_size, mem_block* current_block){
    mem_block* new_hole = malloc(sizeof(mem_block));
    new_hole->next = current_block->next;
    new_hole->size = current_block->size - request_size;
    new_hole->beg = current_block->beg + request_size;
    strcpy(new_hole->name, "Unused");
    new_hole->status = 0;

    current_block->next = new_hole;
    current_block->size = request_size;
    strcpy(current_block->name, proc_name);
    current_block->status = 1;
}

int request_memory_first_fit(char* proc_name, int request_size){
    mem_block* current_block = mem_head;
    while (current_block != NULL){
        if (current_block->status == 0 && current_block->size >= request_size){
            break;
        }
        current_block = current_block -> next;
    }
    if (current_block == NULL){
        return -1;
    }
    split_block(proc_name, request_size, current_block);
    return 0;
}

int request_memory_best_fit(char* proc_name, int request_size){
    mem_block* best_block = NULL;
    mem_block* current_block = mem_head;
    while(current_block != NULL){
        if (current_block->status == 0 && current_block->size >= request_size){
            if (best_block == NULL){
                best_block = current_block;
            } else if (best_block->size > current_block->size){
                best_block = current_block;
            }
        }
        current_block = current_block -> next;
    }
    if (best_block == NULL){
        return -1;
    }
    split_block(proc_name, request_size, best_block);
    return 0;
}

int request_memory_worst_fit(char* proc_name, int request_size){
    mem_block* worst_block = NULL;
    mem_block* current_block = mem_head;
    while(current_block != NULL){
        if (current_block->status == 0 && current_block->size >= request_size){
            if (worst_block == NULL){
                worst_block = current_block;
            } else if (worst_block->size < current_block->size){
                worst_block = current_block;
            }
        }
        current_block = current_block -> next;
    }
    if (worst_block == NULL){
        return -1;
    }
    split_block(proc_name, request_size, worst_block);
    return 0;
}


int release_memory(char* proc_name){
    int release_cnt = 0;
    mem_block* current_block = mem_head;
    while (current_block != NULL){
        if (strcmp(current_block->name,proc_name) == 0){
            current_block->status = 0;
            strcpy(current_block->name,"Unused");
            release_cnt += 1;
        }
        current_block = current_block -> next;
    }
    current_block = mem_head;
    while (current_block->next != NULL){
        if (current_block->status == 0 && current_block->next->status == 0){
            current_block->size += current_block->next->size;
            mem_block* tmp = current_block->next;
            current_block->next = current_block->next->next;
            free(tmp);
            continue; /* don't step forward, check again for consecutive */
        }
        current_block = current_block -> next;
    }
    return release_cnt;
}
