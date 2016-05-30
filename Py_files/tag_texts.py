#Обработка текстовых файлов при помощи treetagger
import codecs, re, os, json
remove_html = re.compile("\<[^>]*\>")
remove_tg = re.compile("&[A-Za-z#0-9]*?;")
ttag_dir = "d:\\TTAG" #Путь к тритаггеру

lang_tokens_file = codecs.open("langs.txt", "r", "utf-8") # Токены языков
lang_tokens = []
for i in lang_tokens_file:
    lang_tokens.append(i)

verbs_tokens_file = codecs.open("verbs.txt", "r", "utf-8") # Токены глаголов
verbs_tokens = []
for i in verbs_tokens_file:
    verbs_tokens.append(i)

other_tokens_file = codecs.open("nouns.txt", "r", "utf-8") # Токены существительных
other_tokens = []
for i in other_tokens_file:
    other_tokens.append(i)

def write_data (path, data): # Запись в json
    json_data = json.dumps(data, ensure_ascii=False, indent=1)  
    json_file = codecs.open (path, 'w', 'utf-8')
    json_file.write (json_data)
    json_file.close()
def read_data (path): #Чтение json
    data_file = codecs.open(path, 'r', 'utf-8')
    data = json.load(data_file)
    data_file.close()
    return data     

def open_path(path, out): # Перебор всех файлов директории
    texts = []
    for i in os.walk(path):
        res = i[2]
        if res:
            for j in res:
                clr_html(i[0] + "\\" + j)
                tree_tagger(i, j, out)
        
def tree_tagger(i, name, output): #Запуск тритаггера, получает на вход путь к обрабатываемому файлу, и путь к результату
    parts = i[0].split("\\")
    first_parts = "\\".join(parts[:4])
    mid_part = u"\\" + parts[4] + "_tagged\\"
    end_parts = "\\".join(parts[5:-1])
    end_parts += "\\"
    os.system(ttag_dir + "\\tag__ " + i[0] + "\\" + name + " " + output + "\\" + name)#+ first_parts + mid_part + end_parts + name)
def clr_html(path): # Очистка от html
    res = codecs.open(path, "r", "cp1251")
    text = res.read()
    text = text.split("<!-- ====================== WITHOUT ANY TABLES ====================== -->")
    if len(text) > 1:
        text = text[1]
    else:
        text = text[0]
    text = remove_html.sub("", text)
    text = remove_tg.sub("", text)
    res.close()
    res = codecs.open(path, "w", "utf-8")
    res.write(text)
    res.close()


def main (in_dir, out_dir): #Функция получает на вход путь к обрабатываемой директории и путь к директории, куда будет производиться запись
    open_path(in_dir, out_dir)

main("input", "output")
