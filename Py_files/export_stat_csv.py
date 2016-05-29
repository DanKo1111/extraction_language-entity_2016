# -*- coding: utf-8 -*-
import codecs, os, json

def write_data (path, data):
    json_data = json.dumps(data, ensure_ascii=False, indent=1)  
    json_file = codecs.open (path, 'w', 'utf-8')
    json_file.write (json_data)
    json_file.close()
def read_data (path):
    data_file = codecs.open(path, 'r', 'utf-8')
    data = json.load(data_file)
    data_file.close()
    return data

def rewrite_csv(in_path, out_path):
    #print in_path, out_path
    data = read_data(in_path)
    text = u""
    for i in data:
        #print type(data)
        #print type(i)
        if type(data[i]) != type({}):
            text += i
            text += ";"
            text += unicode(data[i])
            text += u"\r\n"
        else:
            for j in data[i]:
                text += i
                text += u";"
                text += j
                text += u";"
                text += unicode(data[i][j])
                text += u"\r\n"
    #print text
    a = codecs.open(out_path, "w", "utf-8")
    a.write(text)
    a.close()
def main(path, out):
    for i in os.walk(path):
        res = i[2]
        if res:
            for j in res:
                #print j
                #print i[0] + "\\" + j
                #print i[0] + "\\" + j[-4:] + "csv"
                rewrite_csv(i[0] + "\\" + j, out + "\\" + j[:-4] + "csv")
main("D:\\Daniil\\Course3\\stat", "D:\\Daniil\\Course3\\csv2")
