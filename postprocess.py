import os
import json 
import time 

'''
this script extract all pair translate from folder contains json have translation pair 
and postprocess them 
'''

OUTPUT_FILE_VIE_KHMER = 'final_output/vi_khmer.txt'
OUTPUT_FILE_ONLY_VIE = 'final_output_only/vie.txt'
OUTPUT_FILE_ONLY_KHMER = 'final_output_only/khmer.txt'
os.makedirs('final_output', exist_ok=True)
os.makedirs('final_output_only', exist_ok=True)

OUTPUT_FILE_EN_KHMER = 'final_output/en_khmer.txt'
JSON_FOLDER_PATH = './output/' + '27' # fix this, value
import copy
def refine_sentence(text):
    text = text.replace('\n', ' ')
    text = text.replace('\t', ' ')
    text = text.replace('\\ n', ' ')
    text = text.replace('\\ ', ' ')
    text = text.replace('}"', ' ')
    return text


def double_check_wrong_translate(en_khme_dict):
    '''
    sometimes delay translate might lead to not finish translation (can lead to wrong translation completely) 
    so delay does exist but ratio is so low that can be ignored for now (about 4/100 is wrong translation)
    rest is that we filter even correct one but missing some character (but all this number is so tiny , it can be ignored)
    not gonna filter all wrong translation but at least we did out best here lol
    '''
    correct_pair_dict = {}
    wrong_pair_dict = {}
    must_have_char_ls = ['?', '...']
    for en, khme in en_khme_dict.items():
        is_valid = True
        for char in must_have_char_ls:
            if khme.count(char) != en.count(char):
                is_valid = False
                wrong_pair_dict[en] = khme
                # print ('---- wrong pair ----')
                # print (en, khme)
                break 
            else:
                continue 
        if is_valid: correct_pair_dict[en] = khme

    return correct_pair_dict, wrong_pair_dict


def spot_maybe_wrong_translate(en_khme_dict):
    '''
    during crawling , an old result can be stuck and write as translation for another word next 
    any translation relate to that corrupted khme will be wrong
    '''
    unique_kme = set()
    wrong_pair_dict = {}
    correct_pair_dict = {}
    corrupt_kme = set()
    
    for en, khme in en_khme_dict.items():
        if khme not in unique_kme:
            unique_kme.add(khme)
        else:
            wrong_pair_dict[en] = khme
            corrupt_kme.add(khme)


    non_corrupt_kme = unique_kme - corrupt_kme
    print ('----first check info----')
    print ('unique kme is ', len(unique_kme))
    print ('corrupt kme is ', len(corrupt_kme))
    print ('non corrupt kme is ', len(non_corrupt_kme))

    for en, khme in en_khme_dict.items():
        if khme in non_corrupt_kme:
            correct_pair_dict[en] = khme

    return correct_pair_dict, wrong_pair_dict
        
def check_file(output_file):
    with open (output_file, 'r', encoding="utf-8") as f:
        lines = f.readlines()
        for line in lines:
            if len(line.strip().split('\t')) != 2:
                raise Exception('wrong line dont have at least 2 contents', line)
            contents = line.strip().split('\t')
            first, second = contents
            if first == '' or second == '':
                raise Exception('wrong line with empty content ', line)
    print ('txt file is all good')

def create_vn_khmer_dataset(train_vi, 
                            train_en,
                            en_khme_dict,
                            vi_khme_dict,
                            exist_en, 
                            lost_en,
                            lost_vi
                            ):
    
    train_vi = copy.deepcopy(train_vi)
    train_en = copy.deepcopy(train_en)
    en_khme_dict = en_khme_dict = copy.deepcopy(en_khme_dict)
    vi_khme_dict = vi_khme_dict = copy.deepcopy(vi_khme_dict)
    exist_en = exist_en = copy.deepcopy(exist_en)

    for vi_text, en_text in zip(train_vi, train_en):
        if en_text in en_khme_dict.keys():
            # match once only , in case their train dataset contains duplicate
            if en_text not in exist_en:
                exist_en.add(en_text)
            else:
                continue
            khme_text = en_khme_dict[en_text]
            # decrease cause same vietnamese sentence , only pick 1 vie text
            if vi_text in vi_khme_dict.keys():
                lost_vi += 1
                continue
            vi_khme_dict[vi_text] = refine_sentence(khme_text)

    print ('at first we have en ', len(en_khme_dict))
    print ('lost vi ', lost_vi)
    print ('lost en ', lost_en)
    if  len(en_khme_dict) - lost_vi - lost_en != len(vi_khme_dict):
        raise Exception('hmmmm, something wrong but i dunno lol, never encounter before . bascially lost_en is calculate in this way , \
                        in code \
                        for en_text in en_khme_dict.keys():\
                        if en_text not in train_en_set:\
                            lost_en += 1')
    print ('real left number of sentences', len(vi_khme_dict))

    empty_line = 0
    with open (OUTPUT_FILE_VIE_KHMER, 'w', encoding="utf-8") as f:
        for key, value in vi_khme_dict.items():
            if key == '' or value == '':
                empty_line += 1
                continue
            f.write(refine_sentence(key))
            f.write('\t')
            f.write(refine_sentence(value))
            f.write('\n')
    print ('empty line remove', empty_line)
    check_file(OUTPUT_FILE_VIE_KHMER)

def create_en_khmer_dataset(train_vi, 
                            train_en,
                            en_khme_dict,
                            vi_khme_dict,
                            exist_en, 
                            lost_en,
                            lost_vi
):
    train_vi = copy.deepcopy(train_vi)
    train_en = copy.deepcopy(train_en)
    en_khme_dict = en_khme_dict = copy.deepcopy(en_khme_dict)
    vi_khme_dict = vi_khme_dict = copy.deepcopy(vi_khme_dict)
    exist_en = exist_en = copy.deepcopy(exist_en)
    new_en_khme_dict = {}
    for _, en_text in zip(train_vi, train_en):
        if en_text in en_khme_dict.keys():
            # match once only , in case their train dataset contains duplicate
            if en_text not in exist_en:
                exist_en.add(en_text)
            else:
                continue
            khme_text = en_khme_dict[en_text]
            new_en_khme_dict[en_text] = refine_sentence(khme_text)

    print ('at first we have en ', len(en_khme_dict))
    print ('lost en ', lost_en)
    print ('new_en_khme_dict ', len(new_en_khme_dict))
    if  len(en_khme_dict) - lost_en != len(new_en_khme_dict):
        raise Exception('hmmmm, something wrong but i dunno lol, never encounter before . bascially lost_en is calculate in this way , \
                        in code \
                        for en_text in en_khme_dict.keys():\
                        if en_text not in train_en_set:\
                            lost_en += 1')
    print ('real left number of sentences', len(new_en_khme_dict))

    empty_line = 0
    with open (OUTPUT_FILE_EN_KHMER, 'w', encoding="utf-8") as f:
        for key, value in new_en_khme_dict.items():
            if key == '' or value == '':
                empty_line += 1
                continue
            f.write(refine_sentence(key))
            f.write('\t')
            f.write(refine_sentence(value))
            f.write('\n')
    print ('empty line remove', empty_line)
    check_file(OUTPUT_FILE_EN_KHMER)



vi_khme_dict = {}
en_khme_dict = {}
for filename in os.listdir(JSON_FOLDER_PATH):
    fullpath = os.path.join(JSON_FOLDER_PATH, filename)
    with open(fullpath, 'r', encoding="utf-8") as f:
        data = json.load(f)
        en_khme_dict.update(data) # same key will get overwritten , thats ok 

correct_pair_dict, wrong_pair_dict = spot_maybe_wrong_translate(en_khme_dict)
better_correct_pair_dict, another_wrong_pair_dict = double_check_wrong_translate(correct_pair_dict)
print ('--------------------------------------------')
print ('before first check', len(en_khme_dict.keys()))
print ('after first check', len(correct_pair_dict.keys()))
print ('after double check', len(better_correct_pair_dict.keys()))
print ('--------------------------------------------')

en_khme_dict = better_correct_pair_dict
wrong_pair_dict.update(another_wrong_pair_dict)
with open ('final_output/need_translate_again.json', 'w', encoding="utf-8") as f:
    json.dump(wrong_pair_dict, f,ensure_ascii=False, indent=4)

train_vi_path = r'C:\Users\Admin\CODE\work\text2text\crawl\PhoMT\PhoMT\detokenization\train\train.vi'
train_en_path = r'C:\Users\Admin\CODE\work\text2text\crawl\PhoMT\PhoMT\detokenization\train\train.en'
with open (train_vi_path, 'r', encoding="utf-8") as f:
    lines = f.readlines()
    train_vi = [line.strip() for line in lines]

with open (train_en_path, 'r', encoding="utf-8") as f:
    lines = f.readlines()
    train_en = [line.strip() for line in lines]


'''
in here, 
i only keep 1 en sentence for 1 khmer sentence

i only keep 1 en sentence for 1 vietnamese sentence

no doing 1 sentence can have variations translation
'''
exist_en = set()
lost_en = 0
lost_vi = 0
train_en_set = set(train_en)
# if my collect en doesnt exist in the train file 
for en_text in en_khme_dict.keys():
    if en_text not in train_en_set:
        lost_en += 1


'''
for now , for quality assurance , I do , 
- 1 unique khme in all translation of khome can be kept
- en text come from train_en_path can be kept (in fear i might get translate some outsider en text to khme)
- 1 vn can be kept
so we can understand that 1 unique vn map to 1 unique khme, and en text middleman must exist in train_en_path
'''


print ('---------------------for vi-khmer--------------------------------')

create_vn_khmer_dataset(train_vi, 
                        train_en,
                        en_khme_dict,
                        vi_khme_dict,
                        exist_en, 
                        lost_en,
                        lost_vi
                        )
print ('---------------------for en-khmer--------------------------------')
exist_en = set()
lost_en = 0
lost_vi = 0
train_en_set = set(train_en)
# if my collect en doesnt exist in the train file 
for en_text in en_khme_dict.keys():
    if en_text not in train_en_set:
        lost_en += 1
create_en_khmer_dataset(train_vi, 
                        train_en,
                        en_khme_dict,
                        vi_khme_dict,
                        exist_en, 
                        lost_en,
                        lost_vi
                        )
with open (OUTPUT_FILE_ONLY_VIE, 'w', encoding="utf-8") as f_vie:
    with open (OUTPUT_FILE_ONLY_KHMER, 'w', encoding="utf-8") as f_khmer:
        with open (OUTPUT_FILE_VIE_KHMER, 'r', encoding="utf-8") as f_total:
            lines = f_total.readlines()
            for line in lines:
                try:
                    if len(line.strip().split('\t')) != 2:
                        raise Exception('wrong line dont have at least 2 contents', line)
                    contents = line.strip().split('\t')
                    f_vie.write(contents[0] + '\n')
                    f_khmer.write(contents[1] + '\n')
                except:
                    raise Exception('wrong line ', line)

