## CS222 Project Code

This project is based on paper [FAST: A Fairness Assured Service Recommendation Strategy Considering Service Capacity Constraint](https://link.springer.com/chapter/10.1007/978-3-030-65310-1_21)


### How to run the code

The solution has been encapsulated in a solution class called OnlineFASTSolution, by changing the configurations you can simulate the online-FAST algorithm on different datasets.

- As has been noted in our paper, there are three alogrithms to compare, online-FAST, preempt and random, you can specify them in the configuration
- You should download the dataset from [here](https://zenodo.org/record/3661863#.X_W4oS21HX8), and use the utility functions to load the following tables into the program.
  - loc_recommendation_list_ori
  - loc_preference_score
  - service_capacity
- You can either choose to generate userset with the utility function or load them from the dataset provided [here](https://zenodo.org/record/3661863#.X_W4oS21HX8).
- make sure that the service number, user number coincide with the input dataset.

The output results will be put into a csv file.