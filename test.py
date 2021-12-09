fr = open('record2.txt','r', encoding='UTF-8')
dic = {}
for line in fr:
    value = line.strip().split(':')
    dic[value[0]] = value[1]
fr.close()
print(dic)

