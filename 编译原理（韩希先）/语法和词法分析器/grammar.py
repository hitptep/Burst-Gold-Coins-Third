import copy


class Production:
    def __init__(self, left, right, number):
        self.left = left
        self.right = right
        self.number = number


def isTerminal(value, terminalset):
    if value in terminalset:
        return 1
    return 0


def getFirst(production_list, varset, terminalset):
    first_dic = {}
    # 用来标记first集是否计算完毕，防止重复计算浪费时间
    done = {}
    for var in varset:
        first_dic[var] = set()
        done[var] = 0
    # 所有终结符的first集是他自身
    for var in terminalset:
        first_dic[var] = {var}
        done[var] = 1
    # print("初始化后的done",done)
    # print("初始化的first_dic",first_dic)
    for var in varset:
        if done[var] == 0:
            # print("计算",var)
            getFirstForVar(var, first_dic, varset, terminalset, done)
        # print("计算完毕",var)
        # print("此时的done", done)
        # print("此时的first_dic", first_dic)
        else:
            pass
    return first_dic


def getFirstForVar(var, first_dic, varset, terminalset, done):
    # 已经推导过直接结束

    if done[var] == 1:
        return

    # 对非终结符求first集合,先看右边第一个元素为终结符
    for production in production_list:
        if var in production.left:
            if isTerminal(production.right[0], terminalset):
                first_dic[var].add(production.right[0])
            # 用null表示空字符
            if production.right[0] == "null":
                # print("出现右侧为空")
                first_dic[var].add("null")
    # 右边第一个元素为非终结符
    for production in production_list:
        if var in production.left:
            if isVariable(production.right[0], varset):
                if var == production.right[0]:
                    continue
                if done[production.right[0]] == 0:
                    getFirstForVar(production.right[0], first_dic, varset, terminalset, done)
                if "null" in first_dic[production.right[0]]:
                    first_dic[production.right[0]].remove("null")
                first_dic[var] = first_dic[var] | first_dic[production.right[0]]
            # print("将 ",production.right[0],"的集合 ",first_dic[production.right[0]],"并入",var,"的集合中",first_dic[var],"中","得到",)
            if isVariable(production.right[0], varset) and len(production.right) > 1:

                index = 1
                count = 1
                while isVariable(production.right[index], varset):
                    index = index + 1
                    count = count + 1
                    if index >= len(production.right):
                        break
                i = 0
                while i < count:
                    getFirstForVar(production.right[i], first_dic, varset, terminalset, done)
                    if "null" in first_dic[production.right[i]]:
                        getFirstForVar(production.right[i + 1], first_dic, varset, terminalset, done)
                        first_dic[var] = first_dic[var] | first_dic[production.right[i + 1]]
                    else:
                        break
                    i = i + 1
    # 完成后置为1
    done[var] = 1


def getFollow(varset, terminalset, first_dic, production_list):
    follow_dic = {}
    done = {}
    for var in varset:
        follow_dic[var] = set()
        done[var] = 0
    follow_dic["A1"].add("#")
    # for var in terminalset:
    #     follow_dic[var]=set()
    #     done[var] = 0
    for var in follow_dic:
        getFollowForVar(var, varset, terminalset, first_dic, production_list, follow_dic, done)
    return follow_dic


def getFollowForVar(var, varset, terminalset, first_dic, production_list, follow_dic, done):
    if done[var] == 1:
        return
    for production in production_list:
        if var in production.right:
            ##index这里在某些极端情况下有bug，比如多次出现var，index只会返回最左侧的
            if production.right.index(var) != len(production.right) - 1:
                follow_dic[var] = first_dic[production.right[production.right.index(var) + 1]] | follow_dic[var]
            # 没有考虑右边有非终结符但是为null的情况
            if production.right[len(production.right) - 1] == var:
                if var != production.left[0]:
                    # print(var, "吸纳", production.left[0])
                    getFollowForVar(production.left[0], varset, terminalset, first_dic, production_list, follow_dic,
                                    done)
                    follow_dic[var] = follow_dic[var] | follow_dic[production.left[0]]

    done[var] = 1


def isVariable(value, varset):
    if value in varset:
        return 1
    return 0


def initProduction():
    production_list = []
    production = Production(["A1"], ["A"], 0)
    production_list.append(production)
    production = Production(["A"], ["E", "I", "(", ")", "{", "D", "}"], 1)
    production_list.append(production)
    production = Production(["E"], ["int"], 2)
    production_list.append(production)
    production = Production(["E"], ["float"], 3)
    production_list.append(production)
    production = Production(["D"], ["D", ";", "B"], 4)
    production_list.append(production)
    production = Production(["B"], ["F"], 5)
    production_list.append(production)
    production = Production(["B"], ["G"], 6)
    production_list.append(production)
    production = Production(["B"], ["M"], 7)
    production_list.append(production)
    production = Production(["F"], ["E", "I"], 8)
    production_list.append(production)
    production = Production(["G"], ["I", "=", "P"], 9)
    production_list.append(production)
    production = Production(["P"], ["K"], 10)
    production_list.append(production)
    production = Production(["P"], ["K", "+", "P"], 11)
    production_list.append(production)
    production = Production(["P"], ["K", "-", "P"], 12)
    production_list.append(production)
    production = Production(["I"], ["id"], 13)
    production_list.append(production)
    production = Production(["K"], ["I"], 14)
    production_list.append(production)
    production = Production(["K"], ["number"], 15)
    production_list.append(production)
    production = Production(["K"], ["floating"], 16)
    production_list.append(production)
    production = Production(["M"], ["while", "(", "T", ")", "{", "D", ";", "}"], 18)
    production_list.append(production)
    production = Production(["N"], ["if", "(", "T", ")", "{", "D", ";", "}", "else", "{", "D", ";", "}"], 19)
    production_list.append(production)
    production = Production(["T"], ["K", "L", "K"], 20)
    production_list.append(production)
    production = Production(["L"], [">"], 21)
    production_list.append(production)
    production = Production(["L"], ["<"], 22)
    production_list.append(production)
    production = Production(["L"], [">="], 23)
    production_list.append(production)
    production = Production(["L"], ["<="], 24)
    production_list.append(production)
    production = Production(["L"], ["=="], 25)
    production_list.append(production)
    production = Production(["D"], ["B"], 26)
    production_list.append(production)
    production = Production(["B"], ["N"], 27)
    production_list.append(production)
    return production_list


# 该函数完成production_set在var下的转移
def transf(production_set, var):
    result = []
    for production in production_set:
        if production.right.index(".") == len(production.right) - 1:
            continue;
        index = production.right.index(".") + 1
        if (var == production.right[index]):
            newproduction = copy.deepcopy(production)
            newproduction.right[index], newproduction.right[index - 1] = newproduction.right[index - 1], \
                                                                         newproduction.right[index]
            result.append(newproduction)
    return result


class GraphPoint:

    def __init__(self, begin_production, id):
        self.status = begin_production
        self.transfer = []
        self.id = id

    def add_transfer(self, var, graphPoint):
        self.transfer.append([var, graphPoint])


def isSameStatus(status1, status2):
    if len(status1) != len(status2):
        return 0
    for i in range(0, len(status1)):
        # flag为0，如果status中找到和status1【i】一致的变为1
        flag = 0
        for j in range(0, len(status2)):
            # 右侧不一致，flag2变为1
            str1 = ','.join(status2[j].right)
            str2 = ','.join(status1[i].right)
            if status2[j].left[0] == status1[i].left[0] and str1 == str2:
                flag = 1
                break
        if flag == 0:
            return 0
    return 1


# 用来检验production_set是不是已经存在的point ，如果存在就把point返回
def isInPointset(production_set, pointset):
    for point in pointset:
        if isSameStatus(production_set, point.status):
            return point
    return None


# 生成状态转移图
def generatingGraph(begin_production_set, varset, terminalset, production_list):
    global id
    CLOSURE(varset, terminalset, begin_production_set, production_list)
    beginPoint = GraphPoint(begin_production_set, id)
    id = id + 1



    pointset = [beginPoint]
    set = varset | terminalset
    stack = [beginPoint]
    while len(stack) != 0:
        currentPoint = stack.pop()
        ######

        #####
        for var in set:
            # print("尝试用",var,"进行转移")
            result = transf(currentPoint.status, var)
            if len(result) == 0:
                # print(var,"转移失败！")
                continue
            else:
                # print(var,"可转移！")
                # print("将使用result进行转移！")
                # for onepro in result:
                #     print(onepro.number, " ", onepro.left, "->", onepro.right, "  ")
                # 求出转移后的闭包
                CLOSURE(varset, terminalset, result, production_list)
                nextpoint = isInPointset(result, pointset)
                if nextpoint is None:
                    # print(var,"转移为新状态：")

                    # 新节点压入寻找栈和点集合中，旧节点不能压入，类似于洪范控制
                    nextpoint = GraphPoint(result, id)
                    id = id + 1
                    pointset.append(nextpoint)
                    stack.append(nextpoint)
                # print(nextpoint.id)
                # for onepro in nextpoint.status:
                #     print(onepro.number, " ", onepro.left, "->", onepro.right, "  ")

                currentPoint.add_transfer(var, nextpoint)
            # print("生成一个新状态")
            # for onepro in result:
            #     print(onepro.number," ",onepro.left,"->",onepro.right,"  ")

    return pointset


# 形成闭包
def CLOSURE(varset, terminalset, production_set=[], production_list=[]):
    sizebefore = len(production_list)
    sizeafter = -1

    # 用来测试是不是已经形成闭包，避免进入死循环
    flag = 0
    for production_in_set in production_set:
        if production_in_set.right.index(".") != len(production_in_set.right) - 1:
            if isVariable(production_in_set.right[production_in_set.right.index(".") + 1], varset):
                flag = 1
    if flag == 0:
        return

    while sizeafter != sizebefore:
        for production_in_set in production_set:
            # 点在最右侧就不可能转移
            if (production_in_set.right.index(".") == len(production_in_set.right) - 1):
                continue
            i = production_in_set.right.index(".") + 1;
            # print(i," length",len(production_in_set.right))
            if isTerminal(production_in_set.right[i], terminalset):
                continue;
            templist = []
            for x in production_list:
                # print(i,len(production_in_set.right))
                if x.left[0] == production_in_set.right[i]:
                    y = copy.deepcopy(x)
                    y.right.insert(0, ".")
                    flag = 0
                    for one in production_set:
                        rightflag = 0;
                        if len(one.right) != len(y.right):
                            rightflag = 1
                        else:
                            for j in range(0, len(y.right)):
                                if one.right[j] != y.right[j]:
                                    rightflag = 1
                        if one.left[0] == y.left[0] and rightflag == 0:
                            flag = 1
                    if flag == 0:
                        templist.append(y)
            sizebefore = len(production_set)
            production_set.extend(templist)
            sizeafter = len(production_set)


class Cell:
    def __init__(self):
        self.do = -1
        self.which = -1
        self.done = 0


def getCol(var):
    col_dic = {}
    col_dic["#"] = 0
    col_dic["id"] = 1
    col_dic["number"] = 2
    col_dic["floating"] = 3
    col_dic["float"] = 4
    col_dic["int"] = 5
    col_dic["if"] = 6
    col_dic["else"] = 7
    col_dic["while"] = 8
    col_dic["+"] = 9
    col_dic["-"] = 10
    col_dic["=="] = 11
    col_dic["="] = 12
    col_dic["("] = 13
    col_dic[")"] = 14
    col_dic[";"] = 15
    col_dic[">"] = 16
    col_dic["<"] = 17
    col_dic[">="] = 18
    col_dic["<="] = 19
    col_dic["{"] = 20
    col_dic["}"] = 21
    col_dic["A1"] = 0
    col_dic["A"] = 1
    col_dic["E"] = 2
    col_dic["I"] = 3
    col_dic["D"] = 4
    col_dic["F"] = 5
    col_dic["G"] = 6
    col_dic["M"] = 7
    col_dic["N"] = 8
    col_dic["P"] = 9
    col_dic["K"] = 10
    col_dic["T"] = 11
    col_dic["L"] = 12
    col_dic["B"] = 13
    return col_dic[var]


def initActionAndGoto(pointset, varset, terminalset, begin, follow_dic):
    Action = [[Cell() for i in range(len(terminalset))] for j in range(len(pointset))]
    Goto = [[-1 for i in range(len(varset))] for j in range(len(pointset))]
    for point in pointset:
        # 转移状态
        for tran in point.transfer:
            if isVariable(tran[0], varset):
                if Goto[point.id][getCol(tran[0])] != -1:
                    print("出错404")
                Goto[point.id][getCol(tran[0])] = tran[1].id
            else:
                if Action[point.id][getCol(tran[0])].done == 1:
                    print("出错403")
                Action[point.id][getCol(tran[0])].done = 1
                Action[point.id][getCol(tran[0])].do = "S"
                Action[point.id][getCol(tran[0])].which = tran[1].id
        for production in point.status:
            if production.right.index(".") == len(production.right) - 1 and production.left[0] == begin:
                if Action[point.id][getCol("#")].done == 1:
                    print("出错415")
                Action[point.id][getCol("#")].do = "acc"
                Action[point.id][getCol("#")].done = 1
            if production.right.index(".") == len(production.right) - 1 and production.left[0] != begin:
                # 在follow集中才可归约
                for terminal in terminalset:
                    if terminal in follow_dic[production.left[0]]:
                        Action[point.id][getCol(terminal)].do = "R"
                        Action[point.id][getCol(terminal)].done = 1
                        # 采用该产生式归约
                        Action[point.id][getCol(terminal)].which = production.number

    return Action, Goto


# SLR
def SLR(Action, Goto, source, production_list):
    source.append([0, "#", "结束符"])
    statusstack = [0]
    sentence_stack = ["#"]
    print(source)
    while 1:
        print("*****************************************")
        print("缓冲区剩余元素", source)
        terminal = source.pop(0)

        print("状态栈", statusstack)
        print("句型栈", sentence_stack)
        # 移进
        if Action[statusstack[len(statusstack) - 1]][terminal[0]].do == "S":
            print("动作： 移入操作，从缓冲区中读取", terminal[1], "元素进行移入，并根据Action压入",
                  Action[statusstack[len(statusstack) - 1]][terminal[0]].which, "状态")
            statusstack.append(Action[statusstack[len(statusstack) - 1]][terminal[0]].which)
            sentence_stack.append(terminal[1])
        elif Action[statusstack[len(statusstack) - 1]][terminal[0]].do == "R":
            # 归约
            # 记录归约产生式
            r_production = 0
            for production in production_list:
                if production.number == Action[statusstack[len(statusstack) - 1]][terminal[0]].which:
                    r_production = production
            for i in range(len(r_production.right)):
                statusstack.pop()
                sentence_stack.pop()
            statusstack.append(Goto[statusstack[len(statusstack) - 1]][getCol(r_production.left[0])])
            print("动作： 归约操作，根据Action表利用第", r_production.number, "个产生式归约")
            sentence_stack.append(r_production.left[0])
            source.insert(0, terminal)

        elif Action[statusstack[len(statusstack) - 1]][terminal[0]].do == "acc":

            print("！！！！！！！！！！语义分析完成！！！！！！！！！！！！！！")
            break;
        else:
            print("发生错误，执行紧急恢复，丢弃", terminal);


source = [[5, "int", " 关键字"], [1, "lexicalanalysis", " 标识符"], [13, "(", " 左括号"], [14, ")", " 右括号"],
          [20, "{", " 左大括号"],
          [4, "float", " 关键字"], [1, "a", " 标识符"], [15, ";", " 分号"], [5, "int", " 关键字"], [1, "b", " 标识符"],
          [15, ";", " 分号"], [1, "a", " 标识符"], [12, "=", " 赋值号"], [3, "1.1", " 浮点数"], [15, ";", " 分号"],
          [1, "b", " 标识符"],
          [12, "=", " 赋值号"], [2, "2", " 整数"], [15, ";", " 分号"], [8, "while", "  关键字"], [13, "(", " 左括号"],
          [1, "b", " 标识符"], [17, "<", " 小于号"], [2, "100", " 整数"], [14, ")", " 右括号"], [20, "{", " 左大括号"],
          [1, "b", " 标识符"], [12, "=", " 赋值号"], [1, "b", " 标识符"], [9, "+", " 加 号"], [2, "1", " 整数"],
          [15, ";", " 分号"],
          [1, "a", " 标识符"], [12, "=", " 赋值号"], [1, "a", " 标识符"], [9, "+", " 加号"], [2, "3", " 整数"],
          [15, ";", " 分号"],
          [21, "}", " 右大括号"], [15, ";", " 分号"], [6, "if", " 关键字"], [13, "(", " 左括号"], [1, "a", " 标识符"],
          [16, ">", " 大于号"], [2, "5", " 整数"], [14, ")", " 右括号"], [20, "{", " 左大括号"], [1, "b", " 标识符"],
          [12, "=", " 赋值号"], [1, "b", " 标识符"], [10, "-", " 减号"], [2, "1", " 整数"], [15, ";", " 分号"],
          [21, "}", " 右大括号"],
          [7, "else", " 关键字"], [20, "{", " 左大括号"], [1, "b", " 标识符"], [12, "=", " 赋值号"],
          [1, "b", " 标识符"],
          [9, "+", " 加号"], [2, "1", " 整数"], [15, ";", " 分号"], [15, ";", " 分号"], [15, ";", " 分号"],
          [21, "}", " 右大括号"], [21, "}", " 右大括号"]]
id = 0
varset = {"A1", "A", "E", "I", "D", "F", "G", "M", "P", "K", "T", "L", "B", "N"}
terminalset = {"(", ")", "{", "}", ";", "int", "float", "number", "floating", "while", "if", "else", ">", "<", ">=",
               "<=", "==", "=", "#", "+", "-", "id"}
production_list = initProduction()
first_dic = getFirst(production_list, varset, terminalset)
# for x in first_dic:
#     print(x," : ",first_dic[x])
follow_dic = getFollow(varset, terminalset, first_dic, production_list)
# print("follow:")
# for x in follow_dic:
#     print(x, ":", follow_dic[x])
production = Production(["A1"], [".", "A"], 0)

production_set = [production]
# for x in production_set:
#     print(x.number," ",x.left,"->",x.right,"  ")

pointset = generatingGraph(production_set, varset, terminalset, production_list)
# print(len(pointset))


begin = "A1"
Action, Goto = initActionAndGoto(pointset, varset, terminalset, begin, follow_dic)
print("**********************GOTO***********************************")
for i in range(len(Goto)):
    print(i, end=" ")
    for j in range(len(Goto[i])):
        print("%3d" % Goto[i][j], end=" ")
    print("")

print("**********************Action***********************************")
for i in range(len(Action)):
    print("%2d" % i, end=": ")
    for j in range(len(Action[i])):
        if (Action[i][j].done == 0):
            print("error!", end="   ")
        else:
            print("%3s" % Action[i][j].do, "%2d" % Action[i][j].which, end="   ")
    print("")

SLR(Action, Goto, source, production_list)
