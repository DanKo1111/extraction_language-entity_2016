# -*- coding: utf-8 -*-
import codecs, re, os, json

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

fix_quotes = re.compile(u'[«»“”„“]')
lang_tokens_file = codecs.open("langs.txt", "r", "utf-8")
lang_tokens = []
for i in lang_tokens_file:
    i_str = i.strip()
    lang_tokens.append(i_str)
    if i_str[-1] == u"й":
        lang_tokens.append(u"по-" + i_str[:-1])
        lang_tokens.append(u"по-древне" + i_str[:-1])
        lang_tokens.append(u"по-старо" + i_str[:-1])
        lang_tokens.append(u"по-пра" + i_str[:-1])
        
    lang_tokens.append(u"древне" + i_str)
    lang_tokens.append(u"старо" + i_str)
    lang_tokens.append(u"пра" + i_str)


verb_tokens_file = codecs.open("verbs.txt", "r", "utf-8")
verb_tokens = []
for i in verb_tokens_file:
    verb_tokens.append(i.strip())

fix_tokens_file = codecs.open("nouns.txt", "r", "utf-8")
fix_tokens = []
for i in fix_tokens_file:
    fix_tokens.append(i.strip())

exceptions = read_data("exceptions.json")

def get_dechyp_tags(path="ttag_dechip.txt"):
    parts = {}
    a = codecs.open(path, "r", "utf-8")
    for i in a:
        res = i.split("\t")
        if len(res) == 20:
            parts.update({res[0]:res[1:]})
    return parts
ttags = get_dechyp_tags()

def dechyp_tag(tag):
    if tag in ttags:
        return ttags[tag]
    else:
        return []

def open_path(path, out = ""):
    all_gramms = []
    for i in os.walk(path):
        res = i[2]
        if res:
            for j in res:
                a = codecs.open(i[0] + "\\" + j, "r", "utf-8-sig")
                f_text = a.read()
                a.close()
                gramms = get_gramm(f_text, i[0] + "\\" + j)
                all_gramms += gramms
                
    lang_verb, lang_fix, verb_fix = sort_gramms(all_gramms)
    write_data(out + "\\adj_verb.json", lang_verb)
    write_data(out + "\\adj_noun.json", lang_fix)
    write_data(out + "\\verb_noun.json", verb_fix)
    
def sort_gramms(gramms):
    lang_verb = []
    lang_fix = []
    verb_fix = []
    for i in gramms:
        if i[2] and i[3]:
           lang_verb.append(i)
        if i[3] and i[4]:
            lang_fix.append(i)
        if i[2] and i[4]:
            verb_fix.append(i)
    return lang_verb, lang_fix, verb_fix        

def get_gramm(f_text, path):
    res = []
    full_text, full_nclr_text = clr_text(f_text)

    for j in xrange(len(full_text)):
        i = 0
        while i < len(full_text[j]) - 6:
            part = full_text[j][i:i+7]
            out, shift = token_type(part, path, full_nclr_text[j])
            if out:
                res.append(out)
            i += shift
        if i >= len(full_text[j]) - 6 and i < len(full_text[j]) - 1:
            out, shift = token_type(full_text[j][i:], path, full_nclr_text[j])
            if out:
                res.append(out)
    return res

def token_type(part, path, text):
    token_verb = []
    token_lang = []
    token_fix = []
    phrase = u""

    f_text = u""
    for i in text:
        a = i.split(u"\t")
        if a:
            f_text += a[0]
            f_text += u" "
    text = f_text

    for i in part:
        its = i.split()
        if len(its) > 2:
            if its[1] == u"SENT":
                break
            phrase += u" "
            phrase += its[0]
            if its[2] in lang_tokens:
                token_lang.append([its[2], its[1]])#
            elif its[2] in verb_tokens:
                token_verb.append([its[2], its[1]])#
            elif its[2] in fix_tokens:
                token_fix.append([its[2], its[1]])#

    part.reverse()
    shift = len(part)
    for i in part:
        its = i.split()
        if len(its) > 2:
            if its[2] in lang_tokens or its[2] in verb_tokens or its[2] in fix_tokens:
                break
            else:
                shift -= 1
    if token_verb and token_lang:
        lang_case = False
        for i in token_lang:
            if i[1] in ttags.keys() and (ttags[i[1]][3] == u"locative" or ttags[i[1]][3] == u"instrumental" or i[0][:3] == u"по-"):
                lang_case = True
        if lang_case:
            return (path, text, token_verb, token_lang, token_fix), shift
        return None, 1
    elif token_lang and token_fix:
        lang_stats = []
        fix_stats = []
        for i in token_lang:
            if i[1] in ttags.keys():
                lang_stats.append([ttags[i[1]][3], ttags[i[1]][10], ttags[i[1]][11]])
        for i in token_fix:
            if i[1] in ttags.keys():
                fix_stats.append([ttags[i[1]][3], ttags[i[1]][10], ttags[i[1]][11]])
        for i in lang_stats:
            if i in fix_stats:
                return (path, text, token_verb, token_lang, token_fix), shift
        return None, 1
    elif token_verb and token_fix:
        fix_case = False
        for i in token_fix:
            if i[1] in ttags.keys() and (ttags[i[1]][3] == u"locative" or ttags[i[1]][3] == u"instrumental"):
                fix_case = True
        if fix_case:
            return (path, text, token_verb, token_lang, token_fix), shift
        return None, 1
    else:
        return None, 1

def clr_text(f_text):
    text = []
    nclr_text = []
    f_text = fix_quotes.sub(u'"', f_text)
    quotes_parts = re.findall(u'"\t-\t".*?"\t-\t"', f_text)
    f_text = re.sub(u'"\t-\t".*?"\t-\t"', u"", f_text)        
    
    t_text = f_text.split(u"\r\n")
    text_parts = []
    next_part = []
    for i in xrange(len(t_text)):
        parts = t_text[i].split()
        if len(parts) > 2:
            if parts[0] == u'"':
                text_parts.append(next_part)
                next_part = []
            elif parts[0] in exceptions.keys() and i < len(t_text) - 2 and t_text[i + 1].split()[0] == exceptions[parts[0]]:
                text_parts.append(next_part)
                next_part = []
            elif parts[0] in exceptions.values() and i > 0 and t_text[i - 1].split()[0] in exceptions.keys() and exceptions[t_text[i - 1].split()[0]] == parts[0]:
                pass
            elif parts[1] == u'SENT':
                text_parts.append(next_part)
                next_part = []
            else:
                next_part.append(t_text[i])
    if next_part:
        text_parts.append(next_part)

    for j in text_parts:
        clear_text_parts = []
        nclr_text_parts = []
        for i in j:
            parts = i.split()
            if len(parts) > 1 and parts[0].strip() != parts[1].strip() and parts[1].strip() != u"-":
                clear_text_parts.append(i)
            nclr_text_parts.append(i)
        text.append(clear_text_parts)
        nclr_text.append(nclr_text_parts)
        
    for j in quotes_parts:
        clear_text_parts = []
        nclr_text_parts = []
        for i in j:
            parts = i.split()
            if len(parts) > 1 and parts[0].strip() != parts[1].strip() and parts[1].strip() != u"-":
                clear_text_parts.append(i)
            nclr_text_parts.append(i)
        text.append(clear_text_parts)
        nclr_text.append(nclr_text_parts)
    return text, nclr_text

def main (in_dir, out_dir):
    open_path(in_dir, out_dir)
#open_path("d:\\daniil\\course3\\paper_balanced_tagged", "d:\\daniil\\course3")
