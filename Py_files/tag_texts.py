import codecs, re, os, json
remove_html = re.compile("\<[^>]*\>")
remove_tg = re.compile("&[A-Za-z#0-9]*?;")
ttag_dir = "d:\\TTAG"

lang_tokens_file = codecs.open("d:\\daniil\\course3\\langs1.txt", "r", "utf-8")
lang_tokens = []
for i in lang_tokens_file:
    lang_tokens.append(i)

verbs_tokens_file = codecs.open("d:\\daniil\\course3\\verbs.txt", "r", "utf-8")
verbs_tokens = []
for i in verbs_tokens_file:
    verbs_tokens.append(i)

other_tokens_file = codecs.open("d:\\daniil\\course3\\other.txt", "r", "utf-8")
other_tokens = []
for i in other_tokens_file:
    other_tokens.append(i)

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

def open_path(path, out):
    texts = []
    for i in os.walk(path):
        res = i[2]
        if res:
            for j in res:
                clr_html(i[0] + "\\" + j)
                tree_tagger(i, j, out)
        
def tree_tagger(i, name, output):
    parts = i[0].split("\\")
    first_parts = "\\".join(parts[:4])
    mid_part = u"\\" + parts[4] + "_tagged\\"
    end_parts = "\\".join(parts[5:-1])
    end_parts += "\\"
    os.system(ttag_dir + "\\tag__ " + i[0] + "\\" + name + " " + output + "\\" + name)#+ first_parts + mid_part + end_parts + name)
def clr_html(path):
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


def main (in_dir, out_dir):
    open_path(in_dir, out_dir)

##def open_path2(path, out="d:\\daniil\\course3\\blog"):
##    stat = read_data("d:\\daniil\\Course3\\langs_stat.json")
##    lang_files = []
##    verb_files = []
##    other_files = []
##    for i in os.walk(path):
##        res = i[2]
##        if res:
##            for j in res:
##                lang, verb, other, stat = search_token(i[0] + "\\" + j, stat)
##                if lang:
##                    lang_files.append(i[0] + "\\" + j)
##                if verb:
##                    verb_files.append(i[0] + "\\" + j)
##                if other:
##                    other_files.append(i[0] + "\\" + j)
##    
##    a = codecs.open(out + "_lang.txt", "w", "utf-8")
##    a.write("\r\n".join(lang_files))
##    a.close()
##    a = codecs.open(out + "_verb.txt", "w", "utf-8")
##    a.write("\r\n".join(verb_files))
##    a.close()
##    a = codecs.open(out + "_other.txt", "w", "utf-8")
##    a.write("\r\n".join(other_files))
##    a.close()
##    write_data("d:\\daniil\\Course3\\langs_stat.json", stat)
##    
##def search_token(path, stat):
##    f_text = codecs.open(path, "r", "utf-8")
##    text = f_text.read()
##    text = text.split("\r\n")
##    lang = False
##    verb = False
##    other = False
##    for i in text:
##        res = i.lower()
##        for j in lang_tokens:
##            if j in res:
##                lang =  True
##                if j in stat:
##                    stat[j] += 1
##                else:
##                    stat.update({j:1})
##        for j in verbs_tokens:
##            if j in res:
##                verb = True
##        for j in other_tokens:
##            if j in res:
##                other = True
##    text.close()
##    return lang, verb, other, stat
#open_path2("d:\\daniil\\Course3\\blog_tagged")

#write_data("d:\\daniil\\Course3\\langs_stat.json", {})
#open_path("d:\\daniil\\Course3\\Texts\\kp", "d:\\daniil\\Course3\\kp_tagged")
#open_path("d:\\daniil\\Course3\\Texts\\paper_balanced", "d:\\daniil\\Course3\\paper_balanced_tagged")
#open_path("d:\\daniil\\Course3\\Texts\\ZhZ\\non_fiction", "d:\\daniil\\Course3\\ZhZ_tagged") 
#clr_html("d:\\daniil\\Course3\\test4.html")

##def open_path3(path):
##    files = []
##    for i in os.walk(path):
##        res = i[2]
##        #print i[0] + i[2][1]
##        if res:
##            #print res
##            for j in res:
##                #clr_html(i[0] + "\\" + j)
##                file_o = codecs.open(i[0] + "\\" + j, "r", "utf-8")
##                res = file_o.read()
##                file_o.close()
##                for k in lang_tokens:
##                    if re.findall(k, res):
##                        files.append(i[0] + "\\" + j)
##    a = codecs.open("d:\\daniil\\Course3\\wtf_langs.txt", "w", "utf-8")
##    a.write("\r\n".join(files))
##    a.close()
                        
#open_path3("d:\\daniil\\Course3\\Texts\\ZhZ")

    
##def open_path4(path, blog_path, ZhZ_path, balanced_path, kp_path):
##    paths = []
##    names = []
##    
##    r_file = codecs.open(blog_path, "r", "utf-8")
##    res = ""
##    for i in r_file:
##        a = i.split("\\")
##        res = re.sub(u"_tagged", u"", a[-1])
##        names.append(res.strip())
##    r_file.close()
##    
##    r_file = codecs.open(ZhZ_path, "r", "utf-8")
##    res = ""
##    for i in r_file:
##        a = i.split("\\")
##        res = re.sub(u"_tagged", u"", a[-1])
##        names.append(res.strip())
##    r_file.close()
##    
##    r_file = codecs.open(balanced_path, "r", "utf-8")
##    res = ""
##    for i in r_file:
##        a = i.split("\\")
##        res = re.sub(u"_tagged", u"", a[-1])
##        names.append(res.strip())
##    r_file.close()
##    
##    r_file = codecs.open(kp_path, "r", "utf-8")
##    res = ""
##    for i in r_file:
##        a = i.split("\\")
##        res = re.sub(u"_tagged", u"", a[-1])
##        names.append(res.strip())
##    r_file.close()
##    #for i in names:
##        #print i
##    for i in os.walk(path):
##        res = i[2]
##        if res:
##            for j in res: 
##                if j in names:
##                    paths.append(i[0] + "\\" + j)
##    a = codecs.open("d:\\daniil\\Course3\\Names\\full_langs.txt", "w", "utf-8")
##    a.write("\r\n".join(paths))
##    a.close()
                    
#open_path4("d:\\daniil\\Course3\\Texts", "d:\\daniil\\Course3\\Names\\blog_lang.txt", "d:\\daniil\\Course3\\Names\\ZhZ_lang.txt", "d:\\daniil\\Course3\\Names\\paper_balanced_lang.txt", "d:\\daniil\\Course3\\Names\\kp_lang.txt")


