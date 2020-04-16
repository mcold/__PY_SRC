#coding: utf-8

file = 'jcloze.java'
with open(file, "r") as f:
    l_txt = f.readlines()
    #l_txt = txt.split()
    l_res = list()
    for i in range(len(l_txt)):

        line = l_txt[i]
        res = line.strip()
        count = 0
        for j in range(len(line)):
            if line[j] == ' ':
                count = count + 1
            else:
                break
        if int(count/4) > 0:
            res = u'<p style="text-indent:' + str(int(count/4)) + u'0%;">' + res + u'\n'
            l_res.append(res)
            continue
        if not res == '':
            res = res + u'\n'
            l_res.append(res)
            continue
        #l_res.append(res)

f = open('res.txt', "wb")
for i in range(len(l_res)):
    f.write(l_res[i].encode('utf-8'))

