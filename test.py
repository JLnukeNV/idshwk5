# test.py is a python file to train model for detecting DGA domain
from sklearn.ensemble import RandomForestClassifier
import numpy as np

domainlist = []


class Domain:
    def __init__(self, _name, _label, _length, _firstLength, _averageLength, _numbers):
        self.name = _name
        self.label = _label
        self.length = _length
        self.firstLength = _firstLength
        self.averageLength = _averageLength
        self.numbers = _numbers

    def returnData(self):
        return [self.firstLength, self.numbers]  # 更改传入的特征以得到更准确模型

    def returnLabel(self):
        return self.label   # notdga 0     dga 1


def preprocess(filename):
    # wfile = open("processed.txt", 'w')
    with open(filename) as f:
        for line in f:

            numbers = 0
            for i in line:
                if i.isdigit():
                    numbers += 1

            segment = line.split(".")

            m = segment[len(segment) - 1].split(",")
            m[1] = m[1].strip()
            m[1] = m[1].replace('\n', '').replace('\r', '')
            if m[1] == "notdga":
                dga = 0
            else:
                dga = 1
            length = 0
            i = 0
            name = ""
            while i <= len(segment) - 1:
                if i <= len(segment) - 2:
                    length += len(segment[i])
                    if i > 0:
                        name += '.'
                    name += segment[i]
                else:
                    length += len(m[0])
                    name += '.' + m[0]
                i += 1
            averageLength = length - len(m[0])
            firstLength = len(segment[0])
            domainlist.append(Domain(name, dga, length, firstLength, averageLength, numbers))
            # newline = [line.replace('\n', '').replace('\r', ''), str(length), str(slength), str(numbers)]
            # wfile.write(c.join(newline) + "\n")

    # wfile.close()


def test(filename):
    wfile = open("result.txt", 'w')
    with open(filename) as f:
        for line in f:
            line = line.strip()
            if line.startswith("#") or line == "":
                continue
            # 特征提取
            numbers = 0
            for i in line:
                if i.isdigit():
                    numbers += 1

            tokens = line.split(".")
            i = 0
            length = 0
            while i < len(tokens) - 1:
                length += len(tokens[i])
                i += 1
            # averageLength = length/(len(tokens) - 1)
            firstLength = len(tokens[0])
            a = clf.predict([[firstLength, numbers]])
            if a == np.array([1]):
                str = ",dga\n"
            else:
                str = ",notdga\n"
            wfile.write(line + str)

    wfile.close()


if __name__ == '__main__':
    # 预处理
    preprocess("train.txt")

    # 训练模型
    featureMatrix = []
    labelList = []
    for item in domainlist:
        featureMatrix.append(item.returnData())
        labelList.append(item.returnLabel())
    clf = RandomForestClassifier(random_state=0)
    clf.fit(featureMatrix, labelList)

    # 测试并输出结果
    test("test.txt")
