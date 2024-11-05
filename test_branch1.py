# -*- coding: utf-8 -*-
# 著作 Azunyan
# コーディング規約は基本的にPEP8に準じて作成します。
# 本コードはOneMax問題を遺伝的アルゴリズムを用いて解くプログラムコードである。
#main.py

import GeneticAlgorithm as ga
import random
from decimal import Decimal


# 遺伝子情報の長さ
GENOM_LENGTH = 500
# 遺伝子集団の大きさ
MAX_GENOM_LIST = 100
# 遺伝子選択数
SELECT_GENOM = 20
# 個体突然変異確率
INDIVIDUAL_MUTATION = 0.1
# 遺伝子突然変異確率
GENOM_MUTATION = 0.01
# 繰り返す世代数
MAX_GENERATION = 5

""" 
day_time_count = {
    "mon1st": 0,
    "mon2nd": 0,
    "mon3rd": 0,
    "mon4th": 0,
    "mon5th": 0,
    "tue1st": 0,
    "tue2nd": 0,
    "tue3rd": 0,
    "tue4th": 0,
    "tue5th": 0,
    "wed1st": 0,
    "wed2nd": 0,
    "wed3rd": 0,
    "wed4th": 0,
    "wed5th": 0,
    "thu1st": 0,
    "thu2nd": 0,
    "thu3rd": 0,
    "thu4th": 0,
    "thu5th": 0,
    "fri1st": 0,
    "fri2nd": 0,
    "fri3rd": 0,
    "fri4th": 0,
    "fri5th": 0
}

grades = {
    "grade1": 0,
    "grade2": 0,
    "grade3": 0,
    "grade4": 0
}

 """
# 学年の前回値を保存する変数
previous_grades = {}
# 学年の基準値
thresholds = {
    "grade1": 244,
    "grade2": 95,
    "grade3": 82,
    "grade4": 48
}
# ゼミの前回値を保存する変数
zemi_previous = None
# 教養演習の前回値を保存する変数
kyouyou_previous = None

def create_genom(length):
    """
    引数で指定された桁のランダムな遺伝子情報を生成、格納したgenomClassで返します。
    :param length: 遺伝子情報の長さ
    :return: 生成した個体集団genomClass
    """
    genome_list = []
    for i in range(length):
        genome_list.append(random.randint(0, 1))
    return ga.genom(genome_list, 0)


def evaluation(ga):
    """評価関数です。今回は全ての遺伝子が1となれば最適解となるので、
    合計して遺伝子と同じ長さの数となった場合を1として0.00~1.00で評価します
    :param ga: 評価を行うgenomClass
    :return: 評価処理をしたgenomClassを返す
    """
    day_time_count = {
        "mon1st": [0, 0, 0, 0, 0],  # 1年生, 2年生, 3年生, 4年生, 全学年
        "mon2nd": [0, 0, 0, 0, 0],
        "mon3rd": [0, 0, 0, 0, 0],
        "mon4th": [0, 0, 0, 0, 0],
        "mon5th": [0, 0, 0, 0, 0],
        "tue1st": [0, 0, 0, 0, 0],
        "tue2nd": [0, 0, 0, 0, 0],
        "tue3rd": [0, 0, 0, 0, 0],
        "tue4th": [0, 0, 0, 0, 0],
        "tue5th": [0, 0, 0, 0, 0],
        "wed1st": [0, 0, 0, 0, 0],
        "wed2nd": [0, 0, 0, 0, 0],
        "wed3rd": [0, 0, 0, 0, 0],
        "wed4th": [0, 0, 0, 0, 0],
        "wed5th": [0, 0, 0, 0, 0],
        "thu1st": [0, 0, 0, 0, 0],
        "thu2nd": [0, 0, 0, 0, 0],
        "thu3rd": [0, 0, 0, 0, 0],
        "thu4th": [0, 0, 0, 0, 0],
        "thu5th": [0, 0, 0, 0, 0],
        "fri1st": [0, 0, 0, 0, 0],
        "fri2nd": [0, 0, 0, 0, 0],
        "fri3rd": [0, 0, 0, 0, 0],
        "fri4th": [0, 0, 0, 0, 0],
        "fri5th": [0, 0, 0, 0, 0]
    }


    grades = {
        "grade1": 0,
        "grade2": 0,
        "grade3": 0,
        "grade4": 0
    }

    # print(ga.getGenom())
    daytime_segments = len(day_time_count)  # キーの数を取得
    for i in range(daytime_segments):  # day_time_countのキーの数だけループ
        segment_start = i * 20  # 20ビットの開始位置
        segment = ga.getGenom()[segment_start:segment_start + 20]  # 20ビットのセグメントを取得

        # 範囲チェック
        if segment_start + 20 <= len(ga.getGenom()):
            daytime_key = list(day_time_count.keys())[i]  # キーを取得
            #print(f"キー: {daytime_key}, 20ビットセグメント: {segment}")
        
        # 学年別に講義数を代入
        daytime_decimal_value = 0
        grade_segments = len(grades)
        for i in range(grade_segments):
            seg_start = i * 5
            seg = segment[seg_start:seg_start + 5]

            if seg_start + 5 <= len(segment):
                grade_key = list(grades.keys())[i]
                decimal_value = binary_changer(seg)
                day_time_count[daytime_key][i] = decimal_value
                daytime_decimal_value += decimal_value
                grades[grade_key] += decimal_value #学年別の講義数に加算
        day_time_count[daytime_key][4] += daytime_decimal_value
    
    grade_point = 0
    zemi_point = 0
    kyouyou_point = 0
    cafeteria_point = 0
    
    grade_point += grade_class_calculate(grades, thresholds)
    zemi_point += zemi_calculate(ga)
    kyouyou_point += kyouyou_calculate(ga)
    cafeteria_point += cafeteria_calculate(day_time_count)
    total_point = grade_point + zemi_point + kyouyou_point + cafeteria_point
    
    if ga.show_results:
        print("-------最終評価--------")
        show(day_time_count, grades, grade_point, zemi_point, kyouyou_point, cafeteria_point, total_point)
    return round(total_point, 2)

# 食堂利用ポイントの設定関数
def cafeteria_calculate(day_time_count):
    point = 0
    for daytime in day_time_count:
        if daytime not in ["mon1st", "tue1st", "wed1st", "thu1st", "fri1st", "mon5th", "tue5th", "wed5th", "thu5th", "fri5th"]:
            if int(day_time_count[daytime][4] * 20 * 0.8) > 368:
                point -= cafeteria_point_cal(day_time_count, daytime) * day_time_count[daytime][4]
            else:
                point += cafeteria_point_cal(day_time_count, daytime) * day_time_count[daytime][4]
    # print(f"付与ポイント：{round(point / 1000, 2)}")
    return point / 1000

# 時間割別の食堂利用者ポイント計算
def cafeteria_point_cal(day_time_count, daytime):
    # 数字の最初の位置を見つける
    for i, char in enumerate(daytime):
        if char.isdigit():
            break

    # part1 = daytime[:i]  # "thu"
    part2 = daytime[i:]  # "2nd"

    grade1 = day_time_count[daytime][0]
    grade2 = day_time_count[daytime][1]
    grade3 = day_time_count[daytime][2]
    grade4 = day_time_count[daytime][3]

    point = 0

    if part2 == "2nd":
        point += grade1 * 0.55
        point += grade2 * 0.3
        point += grade3 * 0.15
        point += grade4 * 0
    elif part2 == "3rd":
        point += grade1 * 0.55
        point += grade2 * 0.24
        point += grade3 * 0.15
        point += grade4 * 0.06
    elif part2 == "4th":
        point += grade1 * 0.41
        point += grade2 * 0.2
        point += grade3 * 0.11
        point += grade4 * 0.28

    return point

# 教養演習ポイントの設定関数
def kyouyou_calculate(ga):
    # 1年生の教養演習を水曜日1限に27個入れる事

    global kyouyou_previous

    kyouyou_class = binary_changer(ga.getGenom()[200:205])
    # print(f"教養演習は{kyouyou_class}個ある")

    if kyouyou_class == 27:
        kyouyou_previous = kyouyou_class
        # print("10ポイント付与")
        return int(10)
    else:
        if kyouyou_previous is None:
            kyouyou_previous = kyouyou_class
            return int(0)
        else:
            if abs(kyouyou_class - 27) < abs(kyouyou_previous - 27):
                kyouyou_previous = kyouyou_class
                # print(f"成績は {kyouyou_class} で、前回値 {kyouyou_previous} 以下です。1ポイント付与")
                return int(1)
            else:
                # print(f"成績は {kyouyou_class} で、前回値 {kyouyou_previous} 以上です。-1ポイント付与")
                return int(-1)

# ゼミポイントの設定関数
def zemi_calculate(ga):
    """ 
    170~175,190~195,390~395ビット目が3年生
    175~180,195~200,395~400ビット目が4年生 
    それぞれ火曜4,5限、木曜5限
    合計90講義の平均30講義あるのが条件
     """
    
    global zemi_previous

    grade3_total = 0
    grade4_total = 0

    grade3_total += binary_changer(ga.getGenom()[170:175])
    grade3_total += binary_changer(ga.getGenom()[190:195])
    grade3_total += binary_changer(ga.getGenom()[390:395])
    grade4_total += binary_changer(ga.getGenom()[175:180])
    grade4_total += binary_changer(ga.getGenom()[195:200])
    grade4_total += binary_changer(ga.getGenom()[395:400])
    total = int((grade3_total + grade4_total) / 3)
    # print(f"ゼミの平均は{total}")
    
    if total == 30:
        zemi_previous = total
        # print("10ポイント付与")
        return int(10)
    else:
        if zemi_previous is None:
            zemi_previous = total
            return int(0)
        else:
            if abs(total - 30) < abs(zemi_previous - 30):
                zemi_previous = total
                # print(f"成績は {total} で、前回値 {zemi_previous} 以下です。1ポイント付与")
                return int(1)
            else:
                # print(f"成績は{total} で、前回値{zemi_previous}又は基準値 以上です。－1ポイント付与")
                return int(-1)

# 学年別開講講義数上限の設定関数
def grade_class_calculate(grades, thresholds):
    global previous_grades
    point = 0
    # print(f"現在の学年別前回値：{previous_grades}")
    for key, value in grades.items():
        threshold = thresholds.get(key, None)
        if threshold is not None:
            if value <= threshold:
                # print(f"{key} の成績は {value} で、基準値 {threshold} 以下です。")
                point += 10
            else:
                # print(f"{key} の成績は {value} で、基準値 {threshold} を超えています。")
                if key not in previous_grades:
                    previous_grades[key] = value
                else:
                    if abs(value - threshold) < abs(previous_grades[key] - threshold):
                        # print(f"{key} の成績は {value} で、前回値の {previous_grades[key]} 以下です。")
                        previous_grades[key] = value
                        point -= abs(value - threshold) / 100
                        
                    else:
                        # print(f"{key} の成績は {value} で、前回値の {previous_grades[key]} 以上です。")
                        point -= abs(value - threshold) / 100
        else:
            print(f"{key} に対する基準値が設定されていません。")
        # print("")
    # print(f"今回の付与ポイントは{round(point, 2)}")
    return point

# 2進数を10進数に変える関数
def binary_changer(binary):
    i = sum(bit * (2 ** i) for i, bit in enumerate(reversed(binary)))
    return i

# 時間割形式で結果を表示する          
def show(day_time_count, grades, grade_point, zemi_point, kyouyou_point, cafeteria_point, total_point):
    for i in range(5):
        if i != 4:
            print(f"{i+1}年生")
        else:
            print("全学年")
        total = 0
        print("      |  mon |  tue |  wed |  thu |  fri |")
        print("------+------+------+------+------+------+")
        for time in ["1st", "2nd", "3rd", "4th", "5th"]:
            print(f"{time:>5}", end=" | ")
            for day in ["mon", "tue", "wed", "thu", "fri"]:
                key = f"{day}{time}"
                if key in day_time_count:
                    total += day_time_count[key][i]
                    print(f"{day_time_count[key][i]:4}", end=" | ")
                else:
                    print("  0 ", end="| ")
            print()
        if i != 4:
            print(f"{i+1}年生の総講義数：{total}")
            print("")
        
    
    daytime_total = 0
    grades_total = 0
    grades_difference = {
        "grade1": 0,
        "grade2": 0,
        "grade3": 0,
        "grade4": 0
    }
    for i in day_time_count:
        daytime_total += day_time_count[i][4]
    for i in grades:
        grades_total += grades[i]
        a = grades[i] - thresholds[i]
        if a > 0:
            grades_difference[i] = f"+{a}"
        elif a < 0:
            grades_difference[i] = f"-{a}"

    print(f"全学年時間割総講義数：{daytime_total}")
    print(f"学年別開講講義数上限基準値：{thresholds}")
    print(f"学年別基準値との差：{grades_difference}")
    print(f"学年別総講義数：{grades}")
    print(f"総学年別講義数：{grades_total}")
    print("-------学年別開講講義数上限評価--------")
    print(f"ポイント：{grade_point}")
    print("-------ゼミ評価--------")
    print(f"ポイント：{zemi_point}　ゼミ数：{day_time_count['tue4th'][2] + day_time_count['tue4th'][3] + day_time_count['tue5th'][2] + day_time_count['tue5th'][3] + day_time_count['thu5th'][2] + day_time_count['thu5th'][3]}")
    print("-------教養演習評価--------")
    print(f"ポイント：{kyouyou_point}　教養演習数：{day_time_count['wed1st'][0]}")
    print("-------食堂利用評価--------")
    print(f"ポイント：{cafeteria_point}")
    print("-------総合評価--------")
    print(f"評価値：{round(total_point, 2)}")
    """ print("")
    print("-------------------------------------------------------")
    print("") """

def days(day):
    if day == [0,0,0]:
        return 'mon'
    elif day == [0,0,1]:
        return 'tue'
    elif day == [0,1,0]:
        return 'wed'
    elif day == [0,1,1]:
        return 'thu'
    elif day == [1,1,1]:
        return 'fri'
    else:
        return 'error'

def times(time):
    if time == [0,0,0]:
        return '1st'
    elif time == [0,0,1]:
        return '2nd'
    elif time == [0,1,0]:
        return '3rd'
    elif time == [0,1,1]:
        return '4th'
    elif time == [1,1,1]:
        return '5th'
    else:
        return 'error'
    
def select(ga, elite):
    """選択関数です。エリート選択を行います
    評価が高い順番にソートを行った後、一定以上
    :param ga: 選択を行うgenomClassの配列
    :return: 選択処理をした一定のエリート、genomClassを返す
    """
    # 現行世代個体集団の評価を高い順番にソートする
    sort_result = sorted(ga, reverse=True, key=lambda u: u.evaluation)
    # 一定の上位を抽出する
    result = [sort_result.pop(0) for i in range(elite)]
    return result


def crossover(ga_one, ga_second):
    """交叉関数です。二点交叉を行います。
    :param ga: 交叉させるgenomClassの配列
    :param ga_one:
    :param ga_second:
    :return: 二つの子孫genomClassを格納したリスト返す
    """
    # 子孫を格納するリストを生成します
    genom_list = []
    # 入れ替える二点の点を設定します→[1:25]
    cross_one = random.randint(0, GENOM_LENGTH)
    cross_second = random.randint(cross_one, GENOM_LENGTH)
    # 遺伝子を取り出します
    one = ga_one.getGenom()
    second = ga_second.getGenom()
    # 交叉させます
    progeny_one = one[:cross_one] + second[cross_one:cross_second] + one[cross_second:]
    progeny_second = second[:cross_one] + one[cross_one:cross_second] + second[cross_second:]
    # genomClassインスタンスを生成して子孫をリストに格納する
    genom_list.append(ga.genom(progeny_one, 0))
    genom_list.append(ga.genom(progeny_second, 0))
    return genom_list


def next_generation_gene_create(ga, ga_elite, ga_progeny):
    """
    世代交代処理を行います
    :param ga: 現行世代個体集団
    :param ga_elite: 現行世代エリート集団
    :param ga_progeny: 現行世代子孫集団
    :return: 次世代個体集団
    """
    # 現行世代個体集団の評価を低い順番にソートする
    next_generation_geno = sorted(ga, reverse=False, key=lambda u: u.evaluation)
    # 追加するエリート集団と子孫集団の合計ぶんを取り除く
    for i in range(0, len(ga_elite) + len(ga_progeny)):
        next_generation_geno.pop(0)
    # エリート集団と子孫集団を次世代集団を次世代へ追加します
    next_generation_geno.extend(ga_elite)
    next_generation_geno.extend(ga_progeny)
    return next_generation_geno


def mutation(ga, induvidual_mutation, genom_mutation):
    """突然変異関数です。
    :param ga: genomClass
    :return: 突然変異処理をしたgenomClassを返す"""
    ga_list = []
    for i in ga:
        # 個体に対して一定の確率で突然変異が起きる
        if induvidual_mutation > (random.randint(0, 100) / Decimal(100)):
            genom_list = []
            for i_ in i.getGenom():
                # 個体の遺伝子情報一つ一つに対して突然変異がおこる
                if genom_mutation > (random.randint(0, 100) / Decimal(100)):
                    genom_list.append(random.randint(0, 1))
                else:
                    genom_list.append(i_)
            i.setGenom(genom_list)
            ga_list.append(i)
        else:
            ga_list.append(i)
    return ga_list


if __name__ == '__main__':

    # 一番最初の現行世代個体集団を生成します。
    current_generation_individual_group = []
    for i in range(MAX_GENOM_LIST):
        current_generation_individual_group.append(create_genom(GENOM_LENGTH))

    for count_ in range(1, MAX_GENERATION + 1):
        # 現行世代個体集団の遺伝子を評価し、genomClassに代入します
        for i in range(MAX_GENOM_LIST):
            evaluation_result = evaluation(current_generation_individual_group[i])
            current_generation_individual_group[i].setEvaluation(evaluation_result)
        # エリート個体を選択します
        elite_genes = select(current_generation_individual_group,SELECT_GENOM)
        # エリート遺伝子を交叉させ、リストに格納します
        progeny_gene = []
        for i in range(0, SELECT_GENOM):
            progeny_gene.extend(crossover(elite_genes[i - 1], elite_genes[i]))
        # 次世代個体集団を現行世代、エリート集団、子孫集団から作成します
        next_generation_individual_group = next_generation_gene_create(current_generation_individual_group,
                                                                       elite_genes, progeny_gene)
        # 次世代個体集団全ての個体に突然変異を施します。
        next_generation_individual_group = mutation(next_generation_individual_group,INDIVIDUAL_MUTATION,GENOM_MUTATION)

        # 1世代の進化的計算終了。評価に移ります

        # 各個体適用度を配列化します。
        fits = [i.getEvaluation() for i in current_generation_individual_group]
        
        # 進化結果を評価します
        min_ = min(fits)
        max_ = max(fits)
        avg_ = round(sum(fits) / len(fits), 2)

        # 現行世代の進化結果を出力します
        print( "-----第{}世代の結果-----".format(count_))
        print( "  Min:{}".format(min_))
        print( "  Max:{}".format(max_))
        print( "  Avg:{}".format(avg_))

        # 現行世代と次世代を入れ替えます
        current_generation_individual_group = next_generation_individual_group

    # 最終結果出力
    elite_genes[0].toggle_show_results()
    evaluation(elite_genes[0])
    # print ("最も優れた個体は{}".format(elite_genes[0].getGenom()))
    