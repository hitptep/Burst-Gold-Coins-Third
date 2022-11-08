from queue import LifoQueue
from copy import deepcopy
import pandas as pd
import math

# 字符串转化成字典
def Str_to_dict(str):
    d = {}
    for i in range(len(str)):
        for j in range(len(str[i])):
            if str[i][j] == '-':
                if str[i][0:j] in d.keys():
                    d[str[i][0:j]].append(str[i][j + 2:])
                else:
                    d[str[i][0:j]] = [str[i][j + 2:]]
                break
    return d



# 消除回溯
def recall(samples):
    samplesCopy = deepcopy(samples)
    samples = {}
    change = True
    while change:
        change = False

        for oldLeftKey, rightList in samplesCopy.items():
            # 判断是不是需要合并
            if len(rightList) == 0:
                continue
            dictTmp = {}
            i = 0
            while i < len(rightList):
                if rightList[i][0] in dictTmp.keys():
                    i += 1
                    continue
                oldStartChar = rightList[i][0]
                dictTmp[oldStartChar] = [rightList[i]]
                j = i + 1
                newStartChar = oldLeftKey + '\''
                while newStartChar in dictTmp.keys() or newStartChar in samples.keys():
                    newStartChar += '\''
                while j < len(rightList):  # 继续遍历产生式右侧列表
                    if rightList[j][0] == oldStartChar:
                        change = True
                        if newStartChar not in dictTmp.keys():  # 遇到后面首字母重复的考虑是否已经在字典中建立key
                            dictTmp[newStartChar] = []
                        if oldStartChar + newStartChar not in dictTmp[oldStartChar]:  # 判断是否修改原理对应的字典key的valuelist
                            dictTmp[newStartChar].append(dictTmp[oldStartChar][0][1:])
                            dictTmp[oldStartChar] = [oldStartChar + newStartChar]
                        if rightList[j][1:] != '':  # 判断是否仅仅有这个字符，后面为空
                            dictTmp[newStartChar].append(rightList[j][1:])  # 在新的字典key对应的valuelist中加入新字符串
                        else:
                            dictTmp[newStartChar].append('ε')
                    j += 1
                i = i + 1

            # 将本次得到的dictTmp更新到全局变量字典类型的samples
            samples[oldLeftKey] = []
            for key, valueList in dictTmp.items():
                if len(valueList) == 1:
                    samples[oldLeftKey].extend(valueList)
                else:  # 可能还需要继续
                    samples.update({key: valueList})
        samplesCopy = deepcopy(samples)  # 更新当前全局变量到副本
    samples = dict(sorted(samples.items(), key=lambda x: x[0]))
    return samples


# 非空有限集
def Non_limit1():
    limit_dict = {}
    num = int(input("请输入非空有限集的数目："))
    print("请输入非空有限集：")
    pros=[]
    # 拆分出左递归和非左递归
    for i in range(num):
        pos = 0
        temp = input()
        Vnt = []
        Vnn = []
        l = []
        dicts = {}
        for j in range(len(temp)):
            if temp[j] == '-':
                Vn = temp[0:j]
                pos = j + 2
            elif temp[j] == '|':
                if temp[pos] == Vn:
                    Vnn.append(temp[pos:j])
                    pos = j + 1
                else:
                    Vnt.append(temp[pos:j])
                    pos = j + 1
            elif j == len(temp) - 1:
                if temp[pos] == Vn:
                    Vnn.append(temp[pos:j + 1])
                    pos = j + 1
                else:
                    Vnt.append(temp[pos:j + 1])

        # 如果有左递归，转换成新的产生式
        if len(Vnn) != 0:
            for j in Vnt:
                l.append(Vn + "->" + j + Vn + "'")
            for i in Vnn:
                l.append(Vn + "'->" + i[len(Vn):] + Vn + "'")
            l.append(Vn + "'->" + "ε")
        else:
            for j in Vnt:
                l.append(Vn + "->" + j)
        pros.extend(l)
        # 把字符串转化成字典
        dicts = Str_to_dict(l)
        # 消除回溯
        limit_dict.update(recall(dicts))

    return limit_dict,pros


def First(dicts):
	first = {}
	for key in dicts.keys():
		first[key]=[]
	flag = True
	while flag:
		flag = False
		for key,values in dicts.items():
			for str in values:
				for i in range(len(str)):
					if str[i] == "'":
						continue

					# 是非终结符的情况
					if str[i].isupper():
						# 这个非终结符没有first集
						if len(first[str[i]])==0:
							break
						# 剔除空串，把非终结符的first集加入当前first集
						else:
							temp = str[i]
							while i!=len(str)-1:
								if str[i+1]=="'":
									temp=temp+"'"
									i=i+1
								else:
									break
							len1 = len(first[key])
							first[key].extend(x for x in first[temp] if x not in first[key] and x!='ε')
							len2 = len(first[key])
							if len1 != len2:  # 表明修改过了
								flag = True
							if 'ε'not in first[temp]:
								break
							elif i==len(str)-1 and 'ε'not in first[key]:
								first[key].append('ε')
								break

					# 是终结符的情况
					else:
						if str[i] not in first[key]:
							first[key].append(str[i])
							flag = True
						break
	return first


def Follow(dicts,first,S):
	follow = {}
	for key in dicts.keys():
		follow[key] = []
	follow[S].append('#')
	flag = True
	while flag:
		flag = False
		for key, values in dicts.items():
			for str in values:
				for i in range(len(str)):
					if str[i] == "'":
						continue

					# 是非终结符的情况
					if str[i].isupper():
						temp = str[i]
						while i != len(str) - 1:
							if str[i + 1] == "'":
								temp = temp + "'"
								i = i + 1
							else:
								break
						# 如果后面没有元素，执行规则3
						if i+1==len(str):
							len1 = len(follow[temp])
							follow[temp].extend(x for x in follow[key] if x not in follow[temp])
							len2 = len(follow[temp])
							if len1 != len2:  # 表明修改过了
								flag = True

						# 如果后面有元素，判断是否后一个元素的first集包含空串
						else:
							beta = str[i+1]
							j=i+1
							while j!=len(str)-1:
								if str[j + 1] == "'":
									beta = beta + "'"
									j = j + 1
								else:
									break
							len1 = len(follow[temp])
							if beta in first.keys():
								follow[temp].extend(x for x in first[beta] if x not in follow[temp] and x!='ε')
								if 'ε' in first[beta]:
									follow[temp].extend(x for x in follow[key] if x not in follow[temp])
							elif beta not in follow.keys() and beta not in follow[temp]:
								follow[temp].extend(beta)

							len2 = len(follow[temp])
							if len1 != len2:  # 表明修改过了
								flag = True
	return follow


# 预测分析表
def LL1(Vt,first,follow,df,pros):
	# 遍历每个产生式
	for pro in pros:
		# 获取A字符和alpha
		i = 0
		A = pro[0]
		while i != len(pro) - 1:
			if pro[i + 1] == "'":
				A = A + "'"
				i = i + 1
			else:
				break

		i = i + 3
		alpha = pro[i]
		while i != len(pro) - 1:
			if pro[i + 1] == "'":
				alpha = alpha + "'"
				i = i + 1
			else:
				break

		# 如果首字符是终结符，就直接填入产生式
		if alpha in Vt:
			df.loc[A, alpha] = pro
		elif alpha == 'ε':
			for x in follow[A]:
				df.loc[A, x] = pro
		# 如果产生式首字符的first集含有终结符，填入产生式
		else:
			for a in Vt:
				if a in first[alpha]:
					df.loc[A, a] = pro

			if 'ε' in first[alpha]:
				for a in Vt:
					if a in follow[A]:
						df.loc[A, a] = pro

	return df

# 初始化参数
def Init():
    S = input("请输入文法开始符：")  # 文法开始符
    limit_dict,pros = Non_limit1()  # 非空有限集
    sysbol_str = input("请输入符号串：")
    return S, limit_dict,pros,sysbol_str

# 提取终结符和非终结符
def Vt_Vn(first,follow):
	Vt=[]
	Vn=[]

	Vn.extend([x for x in first.keys()])
	for value in first.values():
		Vt.extend(x for x in value if x not in Vt and x !='ε'and x!='')
	for value in follow.values():
		Vt.extend(x for x in value if x not in Vt and x !='ε'and x!='')
	return Vt,Vn

# 预测分析程序
def Parse(sysbol_str, S, LL, Vn):
	sysbol_str = sysbol_str + '#'
	stack = '#' + S
	dicts = {"符号栈": [stack], "输入串": [sysbol_str], "所用产生式": [" "]}

	while True:
		# 弹出栈顶元素
		stack_top = stack[-1]
		stack = stack[0:len(stack) - 1]
		while stack_top[0] == "'":
			stack_top = stack[-1] + stack_top
			stack = stack[0:len(stack) - 1]

		# 如果stack的栈顶元素是非终结符
		if stack_top in Vn:
			# 获取产生式式
			pro = LL.loc[stack_top, sysbol_str[0]]
			# 如果存在产生式
			if str(pro) != 'nan':
				# 没有遍历完产生式右部
				while pro[-1] != '>':
					temp = pro[-1]
					pro = pro[0:len(pro) - 1]
					while temp[0] == "'":
						temp = pro[-1] + temp
						pro = pro[0:len(pro) - 1]
					if temp != 'ε':
						stack = stack + temp
				# 更新
				dicts["符号栈"].append(stack)
				dicts["输入串"].append(sysbol_str)
				dicts["所用产生式"].append(LL.loc[stack_top, sysbol_str[0]])
			else:
				print("出错了！nan")
				break

		# 如果stack的栈顶元素是终结符
		else:
			# 若等于'#'
			if stack_top == sysbol_str[0]:
				if stack_top == '#':
					print("匹配成功！")
					break
				else:
					sysbol_str = sysbol_str[1:]
					# 更新
					dicts["符号栈"].append(stack)
					dicts["输入串"].append(sysbol_str)
					dicts["所用产生式"].append(" ")
			else:
				print("出错了！")
				print(dicts)
				break

	return dicts

if __name__ == '__main__':
	S,limit_dict,pros,sysbol_str = Init()
	first = First(limit_dict)
	follow = Follow(limit_dict,first,S)
	Vt,Vn = Vt_Vn(first,follow)
	df = pd.DataFrame(index=Vn,columns=Vt)
	LL = LL1(Vt,first,follow,df,pros)
	print(limit_dict)
	print(LL)
	print("First:")
	print(pd.Series(first))
	print("Follow:")
	print(pd.Series(follow))
	print("Vt:"+str(Vt))
	print("Vn:"+str(Vn))
	step_dicts = Parse(sysbol_str,S,LL,Vn)
	step = pd.DataFrame(step_dicts)
	pd.set_option('display.unicode.east_asian_width', True)


	print(step)
