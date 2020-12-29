---
title: 【System Engineering】Final Review
url: se2-review
date: 2020-12-25 12:56:03
tags: 
- System Engineering

categories: 
- Courses

---

For CA notes, online notes are not complete, please see slides. OS notes are complete. Happy reviewing!

Updated on Dec 26, 2020 10:00 PM

|   Chapter  	|   Key Concepts                                                                                                                        	|
|------------	|---------------------------------------------------------------------------------------------------------------------------------------	|
|   CA-1     	|   Formula for Amdahl’s Law, Performance, Flynn’s Taxonomy                                                                             	|
|   CA-2     	|   All topics about MIPS                                                                                                               	|
|   CA-3     	|   Structure, Block Organization and Calculation about cache miss, memory access, CPU time, Miss Penalty                               	|
|   CA-4     	|   Pipelining, Three Hazards, Solution, Quantitive Analysis                                                                            	|
|   OS-1     	|   The general organization of a computer system and the role of interrupts                                                            	|
|   OS-2     	|   OS Services, System Calls, System Services                                                                                          	|
|   OS-3     	|   Process, PCB, Process Scheduling, Context Switch, Multitasking on Mobile, Process Creation/Termination, Interprocess Communication  	|
|   OS-4     	|   Multicore Programming, Multithreading Models                                                                                        	|
|   OS-5     	|   Scheduling Criteria, Algorithms (FCFS/SJF/RR/Priority)                                                                              	|
|   OS-6     	|   Producer-Consumer Problem, Race Condition, Critical Problem, Mutex, Semaphores, Monitors                                            	|
|   OS-7     	|   Three Problems and solution: Bounded-Buffer, Reader-Writer and Dining-Philosopher                                                   	|
|   OS-8     	|   4 conditions, Resource-Allocation Graph, Deadlock Prevention, Deadlock Avoidance, Banker’s Algorithm                                	|
|   OS-9     	|   Memory space mapping, MMU, Contiguous Memory Allocation, Paging, TLB, Page Tables                                                   	|
|   OS-10    	|   Virtual Memory, Demand Paging, Page Replacement                                                                                     	|

<!--more-->

[toc]





| Week   	| Slides       	| Date    	|
|--------	|-------------	|----------	|
| Week1  	| OS1         	| 9月11日  	|
| Week2  	| OS1 + CA1   	| 9月18日  	|
| Week3  	| CA1 + OS2   	| 9月25日  	|
| Week4  	| break       	| 10月2日  	|
| Week5  	| OS2         	| 10月9日  	|
| Week6  	| CA2         	| 10月16日 	|
| Week7  	| CA3         	| 10月23日 	|
| Week8  	| CA3+OS4     	| 10月30日 	|
| Week9  	| OS4         	| 11月6日  	|
| Week10 	| OS5         	| 11月13日 	|
| Week11 	| CA4         	| 11月20日 	|
| Week12 	| OS5+OS6     	| 11月27日 	|
| Week13 	| OS6+OS7+OS8 	| 12月4日  	|
| Week14 	| OS8+OS9     	| 12月11日 	|
| Week15 	| OS9+OS10    	| 12月18日 	|
| Week16 	| OS10        	| 12月25日 	|

## 题型
- 名词解释
  - e.g. what is OS
  - e.g. Functions
- 简答题
  - Explain the principle
  - Algorithm (Scheduling, Banker ...)
  - Interepret on Examples
- 计算
  - Architecture topics
    - Some Formula Given

## CA1 - Fundamentals of Quantitive Design and Analysis

### Introduction

- Pipelined Instruction Execution
- Limits to pipelining
- Levels of the Memory Hierarchy

### Quantitive Principles of Computer Design
- Amdahl's Law
  - Speedup = ?
  - Amdahl's Law Example
  - Calculate speedup
- Processor performance equation
  - CPU time = $? \times ? \times ?$
  - Examples on Page 47/48
  - Calculate speedup
- Principles of Computer Design
  - CPU time
  - CPI
  - CPU clock cycles
  - ...
  - Example on Page 50/51: Compute CPI

### Computer Architecture
- Flynn's Taxonomy
  - SISD
  - SIMD
  - MISD
  - MIMD





### ~~Omitted~~
- Classes of Computers
- Trends in Technology
- Power in Integrated Circuits 
- Trends in Cost Dependability
- Performance
- Fallacies and Pitfalls



## OS1 - Introduction

### Outlined

- Describe the general organization of a computer system and the role of interrupts


### ~~Omitted~~

A lot


## CA2 - Instrtucion Set Principles (Appendix A)


### Outlined

- Structural and Data Hazards  (to be found in CA3)
- MIPS data types [Section A.9]
  - Bytes, Half-words, Words, Doublewords and their usage
- Instruction Layout for MIPS
  - Type
    - I-Type
    - R-Type
    - J-Type
  - Fields
    - Reg-reg
    - Reg-Imm
    - Branch
    - Jump/Call
- MIPS addressing modes [Figure A.23] [Section A.3]
  - Register direct
  - Displacement
  - Immediate
  - Byte addressable & 64 bit address 
  - R0 $\leftarrow$ always contains value 0
  - Displacement = 0 $\Rightarrow$ register indirect
  - R0 + Displacement = 0 $\Rightarrow$ absolute addressing

### ~~Omitted~~

A lot, general concepts not required, only MIPS related topics


## OS2 - Operating System Structures


### Outlined
- Identify services provided by an operating system
- Illustrate how system calls are used to provide operating system services

### Operating System Services
- What function do OS provide?
- One set of services helpful to user?
  - UI
  - Program
  - IO
  - FS
  - Communications
  - Error Detect
- Another set efficient operation
  - Resource Allocation
  - Logging
  - Protection and security
- A view of OS services
  
### System Calls
- Written in ?
- API
- Example: copy files
- Types of system calls
  - Process Ctl
  - File Management
  - Device Management
  - Information maintain
  - Communication
  - Protection

### System Services

### ~~Omitted~~
- System Calls
  - OS Examples
    - Arduino
    - FreeBSD
- Linkers and Loaders
- Why Applications are Operating System Specific
- Operating-System Design and Implementation
  - Design
  - Implementation
- Operating System Structure
  - Monolithic Structure - Original UNIX
  - Layered Approach
  - Microkernals
  - Modules
  - Hybrid Systems
  - Android
- Building and Booting an Operating System
  - Building
  - System Boot
- Operating System Debugging


## CA3 - Memory Hierarchy Design (Chapter 2)


### Introduction
- Why memory hierachy
- Structure Diagram

### Memory Hierarchy Basics
- How Miss occurs and resolved
- Block Organization Methods
  - ...
- Write to Cache methods
  - ...
- Miss rate
- Causes of misses
  - ...3
- Average Memory Access Time
  - Formula
  - Calculation
  - Example on Appendix B-4: calculation formulas
  - Example on B-5: calculate time on cache hits/miss

### Block
- Cache Miss?
- Write?
- Miss Latency
- CPU time considering Memory stalls
  - Example on B-17: Average Memory Access Time and Process Performance, Calculte impact
- Miss Penalty calculation
  - Example on B-20: Miss Penalty and Out of order execution processors
    - _Not touched on lecture, pay attention_

### More Exercises
- Example on Page 80: Calculate Memory Access Time
- Example on Page 82: block organization on power requirement
  - _Not touched on lecture, pay attention_
- Example on Page 83: calculate penalty of multiple stage of caches L2+L3...



### ~~Omitted~~
- Six Basic Cache Optimization
  - Perspectives
  - Optimization Strategys
  - Advanced Optimizations
  - Summary
- Memory Technology
  - Types: SRAM and DRAM
  - Optimization
- Flash Memory
- Memory Dependability
- Virtual Memory

## OS3 - Processes

### Outlined Objectives

- Identify the separate components of a process and illustrate how they are represented and scheduled in an operating system.
- Describe how processes are created and terminated in an operating system, including developing programs using the appropriate system calls that perform these operations.
- Describe and contrast interprocess communication using shared memory and message passing.

### Process Concept

- What is Process
- Multiple Parts
  - text section, pc, ...
- passive? active
- Process in memory
- Process State
  - Draw Diagram of Process State
- PCB components

### Threads
- Concepts, detail in OS4


### Process Scheduling
- Concepts
  - What is the purpose?
  - Structure?
    - ready queue, wait queue
    - Data strucure?
    - what happens on a CPU switch
- Context Switch
  - Explain
- Multitasking on Mobile Systems
  - Difference, foreground, background
  - _Pay attention_




### Operations on Processes
- Process Creation
  - parent, children, tree
  - pid?
  - resource sharing options, execution options what?
  - address space option?
  - UNIX examples
- Process Termination
  - what system call
  - parent authority is what
- Cascading Termination
  - cascading?
  - status information
  - zombie & orphan


### Interprocess Communication
- independent or cooperating, meaning
- Two models of IPC, draw diagrams
- Shared memory, detail in OS6,7 sync methods
  - Producer Consumer Problem
- Message Passing
  - explain
  - Direct Communication
    - how
    - properties of communication link


### ~~Omitted~~
- Operations on Processes
  - Android Process Importance Hierarchy
  - Multiprocess Architecture – Chrome Browser
- IPC in Message-Passing Systems
  - Indirect Communication
  - Synchronization
  - Buffering
- Examples of IPC Systems
  - POSIX
  - MACH
  - Windows
- Communication in Client-Server Systems
  - Pipes
    - Ordinary Pipes
    - Named Pipes
  - Sockets
    - Socket Types
    - Socket Usage
  - Remote Procedure Calls


## CA4 - Pipelining (Appendix C)

### Outline

- Structural and Data Hazards 
- Forwarding
- Branch Schemes
- Exceptions and Interrupts


### Pipelining, Structural and Data Hazards, Forwarding

- 5 Steps of a (pre-pipelined) MIPS Datapath
  - graph draw
  - pipeline latches
  - visualizing
- Code SpeedUp Equation for pipelining
- Hazards: 3 kinds, detail
- One Memory Port/Structual Hazards
  - bubble
  - Dual port vs. Single port
    - Calculation
- Data Hazard (if no forwarding)
  - Three generic data hazards
    - RAW
    - WAR
    - WAW
  - Forwarding
    - datapath figure
    - visualizing
  - LW-ALU Data Hazard Even with Forwarding
    - visualizing
    - detection


### Control Hazard
- old simple design put branch completion in stage 4
  - How three cycle stall is generated?
  - overhead calculation
  - solution
- New Pipelined mips datapath, faster branch
- 4 Alternative Solutions
  - stall until
  - predict not taken
  - predict taken
  - delayed branch
- scheduling branch delay slots
- evaluation of solutions
- Another problem with pipelining
  - exception
  - interrupt
  - precise interrupt problem
    - _pay attention_
- And in conclusion: control and pipelining
  - remember the key points!

### ~~Omitted~~

Almost no, just review all the slides in lec4-CA :)


## OS4 - Threads and Concurrency

### Outlined Objectives
- Identify the basic components of a thread, and contrast threads and processes
- Describe the benefits and challenges of designng multithreaded applications

### Overview
- Motivation
- Single and Multithreaded Programming
  - draw diagram
- Multithreaded Server Architecture
  - draw diagram
- Benefits
  - ... 4


### Multicore Programming
- definition
  - challenges
- parallelism vs. concurrency
- type of parallelism
  - data
  - task
  - illustrate diff through diagram
- Amdahl's Law

### Multithreading Models
- Many to One
- One to One
- Many to Many
- Two level Model
- principle, diagram, example, difference, usage and limitation 


### ~~Omitted~~
- Thread Libraries
  - PThreads
    - Generate multiple threads
  - Java Threads
  - Java Executor Framework
- Implicit Threading
- Thread Pools
  - Fork-Join Parallelism
  - OpenMP
  - Grand Central Dispatch
  - Intel Threading Building Blocks (TBB)
- Threading Issues
  - Semantics of fork() and exec()
  - Signal Handling
  - Thread Cancellation
    - Thread Cancellation in Java
  - Thread Local Storage
- Scheduler Activations
  - Operating System Examples
  - Windows Threads
  - Linux Threads



## OS5 - CPU Scheduling

### Outlined Objective
- Describe various CPU scheduling algorithms
- Assess CPU scheduling algorithms based on scheduling criteria

### Basic Concepts
- goal, Burst Cycle, CPU burst, IO burst
- histogram of frequency vs duration
- CPU scheduler
  - what
  - may take place where?
  - non preemptive or preemptive occasions
- Dispatcher
  - function?
  - dispatch latency?

### Scheduling Criteria
- CPU utilization
- throughput
- turnaround time
- waiting time
- response time

### Scheduling Algorithms
- Optimization Goals
  - ... 5 (correspond to above criteria)
- FCFS
  - example
  - Convoy Effect
- SJF
  - Determining Length of Next CPU Burst
    - How?
  - Preemptive version:
    - Example of Shortest-remaining-time-first
  - Prediction diagram
  - Example of Exponential Averaging
- RR
  - time quantum
  - example
  - turnaround time **varies** with the time quantum (why)
- Priority Scheduling
  - starvation and aging
  - w/wo RR
  - multilevel queue
    - diagram implementation

### ~~Omitted~~
- Thread Scheduling
  - Pthread Scheduling
- Multi-Processor Scheduling
  - SMP symmetric multiprocessing
  - Multicore Processors
  - Multithread Multicore System
  - NUMA and CPU scheduling
- Real-Time CPU Scheduling
  - Priority-based Scheduling
  - Rate Montonic Scheduling
  - Earliest Deadline First Scheduling (EDF)
  - Proportional Share Scheduling
  - POSIX Real-Time Scheduling
- Operating Systems Examples
  - Linux Scheduling Through V2.5
  - Linux Scheduling in Version 2.6.23 +
  - Windows Scheduling
- Algorithm Evaluation
  - Deterministic Evaluation
  - Queueing Models 排队论
  - Simulations
  - Implementation


## OS6 - Synchronization Tools

### Outelined Objectives
- Describe the critical-section problem and illustrate a race condition
- Demonstrate how mutex locks, semaphores, monitors, and condition variables can be used to solve the critical section problem
  - _objective as requried, but not outlined in detail below, pay attention!_

### Background
- Producer
- Consumer
- Race Condition : client and server
- Race Condition Example : fork


### The Critical-Section Problem
- Solution to Critical Section Problem
- Critical-Section Handling in OS
- Peterson’s Solution
- Remark
- Example


### Maybe Also Review
- Mutex Locks
  - Definitions
- Semaphores
  - Usage
  - Implementation
  - Implementation with no Busy Waiting
  - Problems with Semaphores
- Monitors
  - Schematic view of a Monitor
  - Condition Variables
  - Alternatives to implementing condition variables
  - Monitor Implementation Using Semaphores
  - Usage: Resuming Processes within a Monitor
  - Application: Single Resource allocation
    - A Monitor to Allocate Single Resource


### ~~Omitted~~
- Hardware Support for Synchronization
  - Memory Barriers
  - Hardware Instructions
  - Test_and_set Instruction
  - compare_and_swap Instruction
  - Atomic Variables
- Liveness
  - DeadLock
  - Other forms of deadlock:
  - Priority Inheritance Protocol

## OS7 - Synchronization Examples


### Outlined Objectives
- Explain the bounded-buffer, readers-writers, and dining philosophers synchronization problems.
- Describe the tools used by Linux and Windows to solve synchronization problems.

### Classical Problems
- Bounded-Buffer Problem
  - Producer Process
- Readers-Write Problem
  - Solution
- Dining-Philosophers Problem
  - First Attempt : Semaphore Solution
  - Monitor Solution


### ~~Omitted~~
- Kernel Synchronization – Windows
- Linux Synchronization
- POSIX Synchronization
- Java Synchronization
- Alternative Approaches


## OS8 - Deadlocks

### Outlined Objectives
- Illustrate how deadlock can occur when mutex locks are used
- Define the four necessary conditions that characterize deadlock
- Identify a deadlock situation in a resource allocation graph
- Evaluate the four different approaches for preventing deadlocks]
- Apply the banker’s algorithm for deadlock avoidance

### System Model

### Deadlock in Multithreaded Applications

### Deadlock Characterization

- Resource-Allocation Graph
- Basic Facts
 
### Methods for Handling Deadlocks


### Deadlock Prevention
- Circular Wait
- Deadlock Avoidance
- Safe State
- Basic Facts
- Avoidance Algorithms
- Banker’s Algorithm
  - Data Structures for the Banker’s Algorithm
  - Safety Algorithm
  - Resource-Request Algorithm for Process Pi
  - Example


### ~~Omitted~~

- Avoidance Algorithms
  - Resource-Allocation Graph Scheme
- Deadlock Detection
  - Single Instance of Each Resource Type
  - Several Instances of a Resource Type
  - Detection Algorithm
    - Example
  - Detection-Algorithm Usage
- Recovery from Deadlock
  - Resource Preemption

## OS9 - Main Memory

### Outlined Objectives

- To provide a detailed description of various ways of organizing memory hardware
- To discuss various memory-management techniques,


### Background
- Logical vs. Physical Address Space
- Memory-Management Unit (MMU)
  - Example of MMU

### Contiguous Memory Allocation
- Hardware Support for Relocation and Limit Registers
- Variable Partition
- Solution for Dynamic Storage-Allocation Problem
- ~~~Fragmentation~~~


### Paging
- Address Translation Scheme
- Paging Hardware
- Paging – Calculating Internal Fragmentation


### Implementation of Page Table
- Translation Look-Aside Buffer
- Paging Hardware with TLB
- Effective Access Time
- ~~~Memory Protection~~~
- ~~~Shared Pages~~~


### Structure of the Page Table
- Hierarchical Page Tables
- Two-Level Paging Example
- ~~64-bit Logical Address Space~~



### ~~Omitted~~
- Background
  - Protection
  - Hardware Address Protection
  - Address Binding
  - Binding of Instructions and Data to Memory
  - Multistep Processing of a User Program
  - Dynamic Loading
  - Dynamic Linking
- Structure of Page Table
  - Hashed Page Tables
  - Inverted Page Table
- Swapping
  - Context Switch Time including Swapping
  - Swapping on Mobile Systems
  - Swapping with Paging
- Example: The Intel 32 and 64-bit Architectures
  - Page Address Translation
  - IA-32 Page Address Extensions
  - Intel x86-64
- Example: ARMv8 Architecture


## OS10 - Virtual Memory

### Outlined Objectives
- Define virtual memory and describe its benefits.

### Background
- Virtual memory
  - Virtual Memory That is Larger Than Physical Memory
- Virtual-address Space
  
### Demand Paging
- Performance of Demand Paging
  - Example
- Demand Paging Optimizations


### Copy-On-Write


### Page Replacement
- ~~~What Happens If there is no free frame~~~
- ~~~Page Replacement Concepts~~~
- ~~~Basic Page Replacement~~~
- Page and Frame Replacement Algorithms
  - First-In-First-Out (FIFO) Algorithm
  - FIFO Illustrating Belady’s Anomaly
  - Optimal Algorithm
  - Least Recently Used (LRU) Algorithm
  - LRU Implementation
  - LRU Approximation Algorithms


### ~~Omitted~~
- Demand Paging
  - Basic Concepts
  - Valid-Invalid Bit
  - Example: Page Table When Some Pages Are Not in Main Memory
  - Steps in Handling Page Fault
  - Aspects of Demand Paging
  - Instruction Restart
  - Free-Frame Lost
  - Stages in Demand Paging – Worse Case
- Page Replacement
  - Enhanced Second-Chance Algorithm
  - Counting Algorithms
  - Page-Buffering Algorithms
  - Applications and Page Replacement
- Allocation of Frames
  - Fixed Allocation
  - Reclaiming Pages
  - Non-Uniform Memory Access
- Thrashing
  - Demand Paging and Thrashing
  - Working-Set Model
  - Implementaion: Keeping Track of the Working Set
  - Page-Fault Frequency
  - Working Sets and Page Fault Rates
- Allocating Kernel Memory
  - Buddy System
  - Slab Allocator
- Other Considerations