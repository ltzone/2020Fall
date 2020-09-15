---
title: 【Artificial Intelligence】1-2 Uninformed Search
url: ai-search
date: 2020-09-11 10:01:41
tags: 
- Artificial Intelligence

categories: 
- Courses

---

<!--more-->

[toc]

## Agents(智能体)

- Perceiving environment through **sensors**
- acting upon environment through **actuators**

### Agents and Environments

- **agent function** maps from percept histories to actions: $f:P^{*}\rightarrow A$
- **agent program** runs on the physical **architecture** to produce $f$

### Rational Agents
- **do the right thing**: cause the agent to be most successful
  - e.g. use which characteristics
- **performance measure** an *objective* criterion for success of an agent's behavior (varied)
- **definition:** for each possible percept sequence, it should select an action that is expected
  - to maximize its performance measure
  - given the evidence provided by the percept sequence and whatever built-in knowledge the agent has (e.g.启发式搜索)
- **autonomous**(自动) agent: if its behavior is determined by its own experience (with ability to learn and adapt)

> PEAS = Performace Measure + Environment + Actuators + Sensors


## Agents that Plan Ahead

### Examples
1. 8-puzzle
   - impt to define transition function
   - 8*4moves of numbers vs. the move of the blank node
2. pacman

### Reflex Agents(条件反射)
- Reflex Agents
  - choose action based on current percept/memory
  - do not consider the future consequences of their actions
  - **consider how the world IS** (instead of will be)
- Can a reflex agent be rational?
  - depends on how to define 'rational'

> Example. reflex pacman got stuck when there is no points nearby to eat

### Planning Agents

- Planning Agents
  - *Ask What If*
  - Decisions based on (hypothesized) consequences of actions
  - Must have a model of how the world evolves in response to actions
  - Must formulate a goal (test)

- Optimal VS Complete Planning
  
- Planning VS Re-Planning
  - planning: when we are simulating future consequences (with time limit)
  - re-planning

## Search Problems

1. A state space
2. A successor function (with action, costs)
3. A start state and a goal test

$$S' = S(s,a)$$

A **solution** is a sequence of actions which transforms the start state to a goal state.

### State Space
- **World State**: includes every last detail of the environment
- **Search State**: keeps only the details needed for planning
  - e.g. {`(x,y)`location, dot `boolean`s}

> States + Actions + Successor + Goal Test


> Problem:  eat all dots while keeping the ghosts perma-scared
> State: (agent position, dot booleans, power paelet booleans, remaining scared time)


### State Space Graphs

- A mathematical representation of a search problem
  - **Nodes** are abstracted world configurations
  - **Arcs** represent successors
  - The **goal test** is a set of goal nodes (maybe only one)
- In a state space graph, each state occurs only once!

### Search Tree
- A “what if” tree of plans and their outcomes
- The start state is the root node
- Children correspond to successors
- Nodes show states, but correspond to PLANS that achieve those states
- *For most problems, we can never actually build the whole tree*

> Each NODE in in the search tree is an entire PATH in the state space graph
> **Lots of repeated structure in the search tree (may be infinite when loop exists in the state graph)**


## Search Solution

### Tree Search
- Expand out potential plans (tree nodes)
- Maintain a **fringe**(边缘：接下来要搜索的结点队列) of partial plans under consideration
- Try to **expand** as few tree nodes as possible
- **Exploration Strategy**: *which fringe nodes to explore?*


### Depth-First Search 
- expand a deepest node first 
- Fringe is a LIFO stack 
- *Not Complete (in case of infinite loops)*
- Not necessarily optimal (least cost)
- Time Complexity: $1+b+b^2+\ldots + b^m = O(b^m)$
- Space Complexity: fringe length$O(bm)$

### Breadth-First Search
- Complete
- Optimal (if all the cost of tiers are same), otherwise not
- Time Complexity: $1+b+b^2+\ldots + b^s = O(b^s)$, where $s$ is the shallowest tier
- Space Complexity: fringe length$O(b^s)$
- **Space is the bigger problem**


