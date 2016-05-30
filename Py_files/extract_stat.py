#Сбор статистики по обработанным токенам
# -*- coding: utf-8 -*-
import codecs, re, os, json

all_paths = []

def write_data (path, data): # Запись в json
    json_data = json.dumps(data, ensure_ascii=False, indent=1)  
    json_file = codecs.open (path, 'w', 'utf-8')
    json_file.write (json_data)
    json_file.close()
def read_data (path): #Чтание Json
    data_file = codecs.open(path, 'r', 'utf-8')
    data = json.load(data_file)
    data_file.close()
    return data

def create_paths(directory): # С json файлами, содержащими токены
    global all_paths
    for i in os.walk():
        res = i[2]
        if res:
            for j in res:
                all_paths.append(i[0] + "\\" + j)
        

def lang_verb_stat(out_path, name_l, name_v): # Сбор статистики по прилагательным и глаголам
    langs_stat = {}
    verbs_stat = {}
    for f in all_paths:
        new_data = read_data(f)
        for i in new_data:
            for j in i[2]:
                if j[0] in verbs_stat:
                    verbs_stat[j[0]] += 1
                else:
                    verbs_stat.update({j[0]:1})
            for j in i[3]:
                if j[0] in langs_stat:
                    langs_stat[j[0]] += 1
                elif j[0][3:] + u"й" in langs_stat:
                    langs_stat[j[0][3:] + u"й"] += 1
                else:
                    if j[0][:3] == u"по-":
                        langs_stat.update({j[0][3:] + u"й":1})
                    else:
                        langs_stat.update({j[0]:1})

    write_data(out_path + name_l, langs_stat)
    write_data(out_path + name_v, verbs_stat)

def lang_and_verb_stat(out_path, name): #Сбор статистики по сочетанию прилагательного и глагола
    lang_verb_stat = {}
    for f in all_paths:
        new_data = read_data(f)
        for i in new_data:
            loc_langs = []
            for j in i[3]:
                if j[0][:3] == u"по-":
                    if j[0][3:] + u"й" not in lang_verb_stat:
                        lang_verb_stat.update({j[0][3:] + u"й":{}})
                        loc_langs.append(j[0][3:] + u"й")
                else:
                    if j[0] not in lang_verb_stat:
                        lang_verb_stat.update({j[0]:{}})
                        loc_langs.append(j[0])


    for f in all_paths:
        new_data = read_data(f)
        for i in new_data:
            loc_langs = []
            for j in i[3]:
                if j[0][:3] == u"по-":
                    loc_langs.append(j[0][3:] + u"й")
                else:
                    loc_langs.append(j[0])
            for j in loc_langs:
                for k in i[2]:
                    if k[0] in lang_verb_stat[j]:
                        lang_verb_stat[j][k[0]] += 1
                    else:
                        lang_verb_stat[j].update({k[0]:1})
                    
    write_data(out_path + name, lang_verb_stat)

def main (in_directory, out_directory): #На вход подается путь к обрабатываемой директории, и директории, в которую будет производиться запись
    create_paths(in_directory)
    for i in all_paths:
        res = i.split("\\")
        name = res[-1][:-4]
        lang_verb_stat(out_directory, name + "_langs_stat.json", name + "_verbs_stat.json")
        lang_and_verb_stat(out_directory, name +  "_lang_and_verb_stat.json")
main("input", "output")
