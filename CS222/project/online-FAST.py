import time

import numpy as np
import random
import csv
import math


def load_csv_table(loc, table_name, row_num, col_num):
    csvFile = open(loc)
    csv_reader = csv.reader(csvFile)
    table = np.zeros((row_num, col_num)).astype(int)
    tag = 0
    for row in csv_reader:
        table[tag] = np.array([int(float(x)) for x in row])
        if tag % 1000 == 0:
            print('%s %d' % (table_name, tag))
        tag = tag + 1
    csvFile.close()
    print('%s loaded!' % table_name)
    return table


def load_requests(loc):
    csvFile = open(loc)
    csv_reader = csv.reader(csvFile)
    random_user = []
    tag = 0
    for row in csv_reader:
        random_user.append([int(x) for x in row])
        if tag % 1000 == 0:
            print('random_user %d' % tag)
        tag = tag + 1
    csvFile.close()
    print('random_user loaded!')
    return random_user


def load_capacity(loc):
    csvFile = open(loc)
    csv_reader = csv.reader(csvFile)
    service_capacity = []
    for row in csv_reader:
        for i in row:
            service_capacity.append(int(i))
    csvFile.close()
    service_capacity = np.array(service_capacity)
    print('service_capacity loaded!')
    return service_capacity


def make_set(table):
    return [set(i) for i in table]


def load_service_table(recommendation_list_ori, service_num, user_num, topN):
    service_topN_users = []
    for i in range(service_num):
        service_topN_users.append([])
    for i in range(user_num):
        for j in range(topN):
            service_temp = recommendation_list_ori[i][j]
            service_topN_users[service_temp].append(i)
    service_topN_users = np.array(service_topN_users)

    user_pos_in_service = []
    for i in range(service_num):
        user_pos_in_service.append([])
    for service_i in range(service_num):
        for user_j in service_topN_users[service_i]:
            for i in range(topN):
                if recommendation_list_ori[user_j][i] == service_i:
                    user_pos_in_service[service_i].append(i)
                    break
    return service_topN_users, user_pos_in_service


class OnlineFASTSolution:
    def __init__(self, service_num, user_num,
                 fast_top_n, recommendation_total_round,  # configurations
                 loc_recommendation_list_ori,
                 loc_preference_score,
                 user_requests, user_probability, service_capacity,  # data inputs
                 loc_results,  # output dir
                 mode
                 ):
        # Configurations
        self.mode = mode
        self.service_num = service_num
        self.user_num = user_num
        self.Top_N = fast_top_n
        self.recommendation_total_round = recommendation_total_round
        self.output_writer = csv.writer(open(loc_results, 'w', newline='', encoding='utf-8'))
        self.output_writer.writerow(['Max_Satisfaction', 'Satisfaction',
                                     'avg_fairness', 'fairness_variance'])

        """
        Input Data
        """
        # Original Recommendation Lists
        self.recommendation_list_ori = load_csv_table(loc_recommendation_list_ori,
                                                      "recommendation_list", user_num, service_num)
        self.recommendation_list_ori_set = make_set([lis[:5] for lis in self.recommendation_list_ori])
        # Preference Scores
        self.preference_score = load_csv_table(loc_preference_score,
                                               "preference score", user_num, service_num)
        # Income requests
        self.requests_list = user_requests
        self.user_probability = user_probability
        self.service_capacity = service_capacity
        # Initialize user_in_service_pos
        self.service_topN_users, self.user_pos_in_service = \
            load_service_table(self.recommendation_list_ori, self.service_num, self.user_num, self.Top_N)
        self.service_topN_users_set = make_set(self.service_topN_users)

        """
        Intermediate Results
        """
        # Initialize probability
        self.probability = np.zeros((recommendation_total_round, user_num, service_num))
        # user_i in service_j counts upto now
        self.probability_total = np.zeros((user_num, service_num))
        # Actual appearance probability (definition 2)
        self.p_theory = np.zeros(service_num).astype(float)
        # Fairness degree of user_i w.r.t. service_j upto now
        self.top_n_fairness = np.zeros((user_num, self.Top_N))
        # Overall fairness degree of user_i upto now
        self.top_n_fairness_total = np.zeros(user_num)
        # the count of rounds for user_i upto now
        self.recommended_round_user = np.zeros(user_num).astype(int)
        # Initialize total_rec_num
        self.total_rec_num = np.zeros(service_num).astype(int)

    def update_top_n_fairness_total(self, user):
        fairness_temp = 0
        for i in range(self.Top_N):
            service = self.recommendation_list_ori[user][i]
            p_actual = self.probability_total[user][service] / self.recommended_round_user[user] if \
                self.recommended_round_user[user] > 0 else 0
            if self.p_theory[service] != 0:
                self.top_n_fairness[user][i] = (p_actual - self.p_theory[service]) / self.p_theory[service]
                fairness_temp = fairness_temp + self.top_n_fairness[user][i]
            self.top_n_fairness_total[user] = fairness_temp
        return

    def is_feasible(self, rec_service, priority_users, service_seat, remain_user_cnt):
        if self.mode == 'fast':
            expected_capacity = 0
            for u in priority_users:
                if rec_service in self.recommendation_list_ori_set[u]:
                    expected_capacity += self.user_probability[u]
            return service_seat[rec_service] - 1 >= expected_capacity / self.user_num * remain_user_cnt
        if self.mode == 'preempt':
            return service_seat[rec_service] > 0

    def random_assign(self, Round, rec_service, recommendation_list):
        requests_set = set(self.requests_list[Round])
        user_list = []
        user_list.append(-1)
        pos_list = []
        total_len = len(self.service_topN_users_set[rec_service])
        actual_len = 0
        final_len = 0
        for u in self.service_topN_users_set[rec_service]:
            if u in requests_set:
                actual_len += 1
                if len(recommendation_list[u]) < self.Top_N:
                    user_list.append(u)
                    final_len += 1
        absent_num = total_len - actual_len
        pos_list.append(float(absent_num) / total_len)
        if final_len:
            average_pos = float(actual_len) / total_len / final_len
            for p in range(final_len):
                pos_list.append(average_pos)
        else:
            return -1
        pos_list = np.array(pos_list)
        index = np.random.choice(user_list, p=pos_list.ravel())
        return index

    def run_random(self):
        np.random.seed(0)
        for Round in range(self.recommendation_total_round):
            # reset service seat at the beginning of each round
            service_seat = self.service_capacity.copy()
            recommendation_list = []
            for i in range(self.user_num):
                recommendation_list.append([])
            Satisfaction = 0
            for (cur_user_index, request) in enumerate(self.requests_list[Round]):
                curent_index = 0
                while curent_index < self.Top_N:
                    rec_service = self.recommendation_list_ori[request][curent_index]
                    if service_seat[rec_service] > 0:
                        user_i = self.random_assign(Round, rec_service, recommendation_list)
                        if user_i != -1:
                            recommendation_list[user_i].append(rec_service)
                            service_seat[rec_service] -= 1
                            self.probability[Round][user_i][rec_service] = self.probability[Round][user_i][
                                                                               rec_service] + 1
                            self.probability_total[user_i][rec_service] = self.probability_total[user_i][
                                                                              rec_service] + 1
                            self.p_theory[rec_service] = self.p_theory[rec_service] + 1 / self.total_rec_num[
                                rec_service] \
                                if self.total_rec_num[rec_service] > 0 else 0
                            recommendation_index_ori = 0
                            for i in self.recommendation_list_ori[user_i]:
                                if i == rec_service:
                                    break
                                recommendation_index_ori += 1
                            if recommendation_index_ori < self.Top_N:
                                Satisfaction = Satisfaction + (self.preference_score[user_i][recommendation_index_ori] /
                                                               self.preference_score[user_i][0] / math.log(
                                            (recommendation_index_ori + 2), 2))
                            # self.update_Top_N_fairness_total(user_i)
                    curent_index += 1

            # update p_theory
            for service_temp in range(self.service_num):
                if len(self.service_topN_users[service_temp]) == 0:
                    continue
                p_theory_temp = 0
                for user in self.service_topN_users[service_temp]:
                    p_theory_temp = p_theory_temp + self.probability_total[user][service_temp]
                p_theory_temp = p_theory_temp / self.total_rec_num[service_temp] \
                    if self.total_rec_num[service_temp] > 0 else 0
                self.p_theory[service_temp] = p_theory_temp

            # update Top_N fairness_total
            for user in self.requests_list[Round]:
                self.update_top_n_fairness_total(user)

            # Calculate Max_Satisfaction,
            # Update recommended_round and total_rec_num based on true requests
            Max_Satisfaction = 0
            # the satisfaction number of the original algorithm for the current groups of users
            for i in self.requests_list[Round]:
                self.recommended_round_user[i] = self.recommended_round_user[i] + 1
                for j in range(self.Top_N):
                    Max_Satisfaction = Max_Satisfaction + (self.preference_score[i][j]
                                                           / self.preference_score[i][0] / math.log((j + 2), 2))
                    service_temp = self.recommendation_list_ori[i][j]
                    self.total_rec_num[service_temp] = self.total_rec_num[service_temp] + 1

            row_temp = [Max_Satisfaction * 5, Satisfaction * 5,
                        np.mean(self.top_n_fairness_total), np.var(self.top_n_fairness_total)]
            self.output_writer.writerow(row_temp)
            print(Round, row_temp)

    def run_fast(self):
        for Round in range(self.recommendation_total_round):
            # reset service seat at the beginning of each round
            service_seat = self.service_capacity.copy()

            recommendation_list = []
            for i in range(self.user_num):
                recommendation_list.append([])
            Satisfaction = 0
            for (cur_user_index, request) in enumerate(self.requests_list[Round]):
                recommendation_index_ori = 0
                priority_users = []

                for user in range(self.user_num):
                    if user != request and \
                            self.top_n_fairness_total[user] < self.top_n_fairness_total[request] and \
                            len(recommendation_list[user]) < self.Top_N:
                        priority_users.append(user)
                rank = len(recommendation_list[request])
                while len(recommendation_list[request]) < self.Top_N:
                    rec_service = self.recommendation_list_ori[request][recommendation_index_ori]
                    user_i = request
                    if self.is_feasible(rec_service, priority_users, service_seat,
                                        max(1, self.user_num - cur_user_index)):
                        recommendation_list[request].append(rec_service)
                        service_seat[rec_service] -= 1
                        self.probability[Round][user_i][rec_service] = self.probability[Round][user_i][rec_service] + 1
                        self.probability_total[user_i][rec_service] = self.probability_total[user_i][rec_service] + 1
                        self.p_theory[rec_service] = self.p_theory[rec_service] + 1 / self.total_rec_num[rec_service] \
                            if self.total_rec_num[rec_service] > 0 else 0
                        if recommendation_index_ori < self.Top_N:
                            Satisfaction = Satisfaction + (self.preference_score[user_i][recommendation_index_ori] /
                                                           self.preference_score[user_i][0] / math.log(
                                        (recommendation_index_ori + 2), 2))
                            # self.update_Top_N_fairness_total(user_i)
                    recommendation_index_ori += 1
                    if recommendation_index_ori >= self.service_num:
                        break
            # update p_theory
            for service_temp in range(self.service_num):
                if len(self.service_topN_users[service_temp]) == 0:
                    continue
                p_theory_temp = 0
                for user in self.service_topN_users[service_temp]:
                    p_theory_temp = p_theory_temp + self.probability_total[user][service_temp]
                p_theory_temp = p_theory_temp / self.total_rec_num[service_temp] \
                    if self.total_rec_num[service_temp] > 0 else 0
                self.p_theory[service_temp] = p_theory_temp

            # update Top_N fairness_total
            for user in self.requests_list[Round]:
                self.update_top_n_fairness_total(user)

            # Calculate Max_Satisfaction,
            # Update recommended_round and total_rec_num based on true requests
            Max_Satisfaction = 0
            # the satisfaction number of the original algorithm for the current groups of users
            for i in self.requests_list[Round]:
                self.recommended_round_user[i] = self.recommended_round_user[i] + 1
                for j in range(self.Top_N):
                    Max_Satisfaction = Max_Satisfaction + (self.preference_score[i][j]
                                                           / self.preference_score[i][0] / math.log((j + 2), 2))
                    service_temp = self.recommendation_list_ori[i][j]
                    self.total_rec_num[service_temp] = self.total_rec_num[service_temp] + 1

            row_temp = [Max_Satisfaction * 5, Satisfaction * 5,
                        np.mean(self.top_n_fairness_total), np.var(self.top_n_fairness_total)]
            self.output_writer.writerow(row_temp)
            print(Round, row_temp)

    def run(self):
        if self.mode == 'random':
            self.run_random()
        else:
            self.run_fast()


# Two way of genenerating requests (static size or dynamic size)
def generate_requests_static_size(probability=0.8, rounds=100, user_count=800):
    return [random.sample([i for i in range(user_count)],
                          int(user_count * probability)) for j in range(rounds)]


def generate_requests_dynamic_size(probability=0.8, rounds=100, user_count=800):
    requests = []
    for i in range(rounds):
        users = []
        for j in range(user_count):
            if random.random() < probability:
                users.append(j)
        requests.append(random.sample(users, len(users)))
    return requests


if __name__ == "__main__":
    current_time = time.strftime("%d-%H:%M", time.localtime())
    online_fast_solver = OnlineFASTSolution(
        service_num=50,
        user_num=800,
        fast_top_n=5,
        recommendation_total_round=100,
        loc_recommendation_list_ori='datasets/data1/recommendation_list_ori.csv',
        loc_preference_score='datasets/data1/preference_score.csv',
        user_requests=load_requests('datasets/data1/random_user_0.6.csv'),
        user_probability=[0.6 for i in range(800)],
        service_capacity=load_capacity('datasets/data1/service_capacity.csv'),
        loc_results=f'results/[{current_time}]onlineFast.csv',
        mode='preempt'  # 'fast' or 'preempt'
    )
    online_fast_solver.run()
