# coding=utf-8
import jieba

# 数据分组
question_list = []
answers_list = []


def gen_group_labeled():
    data_file = open('./data/BoP2017-DBQA.dev.txt')
    score_file = open('./data/Sample.test.output.txt')
    current_question = ''
    question_num = 0
    while True:
        data = data_file.readline()
        # score = score_file.readline()
        score = 0
        if data:
            input_data = data.split("\t")
            question = input_data[1]
            if question != current_question:
                current_question = question
                question_list.append(current_question)
                answers_list.append([[int(input_data[0]), int(score), input_data[2]]])  # 对错 分值 答案
                question_num += 1
            else:
                answers_list[question_num - 1].append([int(input_data[0]), int(score), input_data[2]])
        else:
            break
    data_file.close()
    score_file.close()


def gen_group():
    data_file = open('./data/data.txt')
    score_file = open('./data/Sample.test.output.txt')
    current_question = ''
    question_num = 0
    while True:
        data = data_file.readline()
        # score = score_file.readline()
        score = 0
        if data:
            input_data = data.split("\t")
            question = input_data[0]
            if question != current_question:
                current_question = question
                question_list.append(current_question)
                answers_list.append([[0, int(score), input_data[1]]])  # 对错 分值 答案
                question_num += 1
            else:
                answers_list[question_num - 1].append([0, int(score), input_data[1]])
        else:
            break
    data_file.close()
    score_file.close()


# MRR计算
def calc_a_mrr(answers):
    rank = 0
    sorted_answers = sorted(answers, key=lambda answer: answer[1], reverse=True)
    for i, answer in enumerate(sorted_answers):
        if answer[0] == 1:
            rank += 1 / (i + 1)
    rank /= len(answers)
    return rank


def calc_all_mrr():
    rank = 0
    for answers in answers_list:
        rank += calc_a_mrr(answers)
    return rank


ccount = 0
acount = 0


# 计算score
def calc_score(question, answers):
    global ccount, acount
    question_words = list(jieba.cut(question, cut_all=False))
    word_weights = []
    answer_scores = []

    answer_words_list = []
    for answer in answers:
        answer_words_list.append(list(jieba.cut(answer[2], cut_all=False)))

    word_appear_time = 0
    for question_word in question_words:
        for answer_words in answer_words_list:
            if question_word in answer_words:
                word_appear_time += 1
        word_weights.append(1 / ((word_appear_time + 1) * (word_appear_time + 1)))
        word_appear_time = 0

    score = 0
    for i, answer_words in enumerate(answer_words_list):
        for j, question_word in enumerate(question_words):
            if question_word in answer_words:
                score += word_weights[j]
        # score /= len(answer_words)
        answer_scores.append([answers[i][0], score])
        score = 0
    answer_scores = sorted(answer_scores, key=lambda answer_score: answer_score[1], reverse=True)

    temp = ''
    for answer_score in answer_scores:
        temp += str(answer_score[0])
    if answer_scores[0][0] == 1 or answer_scores[1][0] or answer_scores[2][0]:
        ccount += 1
    acount += 1
    print(temp)


gen_group_labeled()
for i in range(0, len(question_list)):
    calc_score(question_list[i], answers_list[i])

print(ccount / acount)
