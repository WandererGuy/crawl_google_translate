


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os 
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time 
import json
from tqdm import tqdm 
import random
import shutil
service = Service(executable_path='./chromedriver.exe')
options = webdriver.ChromeOptions()

output_folder = './output'
os.makedirs(output_folder, exist_ok=True)
import yaml

def read_yaml_config(file_path):
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)

config = read_yaml_config('./config.yaml')
 # folder contain cracked (to get include this folder result in)
previous_folder_name = config['previous_output_dir_num']
output_folder_name = config['current_output_dir_num']

cracked_folder_name = [previous_folder_name]
NAME_FOLDER = os.path.join(output_folder, str(output_folder_name)) # change this every time 
os.makedirs(NAME_FOLDER, exist_ok=True)

CRACKED_FOLDER_LS = []
for folder_name in cracked_folder_name:
    CRACKED_FOLDER_LS.append(os.path.join(output_folder, folder_name)) # include this cracked folder in 
CRACKED_FOLDER_LS = list(set(CRACKED_FOLDER_LS))

URL = config['URL']
# input text xpath of the div in html when inspect
INPUT_AREA_XPATH = config['INPUT_AREA_XPATH']
# file where each line to the line to translate 
SOURCE_PATH = config['SOURCE_PATH']
# target_path output text xpath of the div in html when inspect
TARGET_PATH= config['TARGET_PATH']
# wait for result to load 
WAIT_RESPONSE_TIME = random.uniform(3.5, 5.5)
MAX_TIME_BROWSER = 3600 * 2.5
# options.add_argument("--headless")
DRIVER= webdriver.Chrome(service=service, options=options)

from multiprocessing import Pool
import multiprocessing
CPU_COUNT = multiprocessing.cpu_count()
CPU_COUNT = CPU_COUNT - 1


def return_cracked(cracked_folder_ls):
    count = 0 
    en_khme_dict = {}
    for path in cracked_folder_ls:
        for filename in os.listdir(path):
            fullpath = os.path.join(path, filename)
            with open(fullpath, 'r', encoding="utf-8") as f:
                data = json.load(f)
                en_khme_dict.update(data)
                count += len(data.keys())
    print ('there are cracked (even duplicate english)', count)

    cracked_set = en_khme_dict.keys()
    return cracked_set

def remove_cracked(new_source_lines_set, cracked_set):
    uncracked_ls = []
    maybe_uncracked_set = set(new_source_lines_set)
    for item in maybe_uncracked_set:
        if item not in cracked_set:
            uncracked_ls.append(item)
    print ('there is {} CRACKED lines'.format(len(maybe_uncracked_set)))
    print ('there is {} uncracked lines'.format(len(uncracked_ls)))
    print ('so difference is ', len(maybe_uncracked_set) - len(uncracked_ls))
    time.sleep(5)
    return uncracked_ls




def copy_cracked(cracked_folder_ls):
    for path in cracked_folder_ls:
        for filename in os.listdir(path):
            fullpath = os.path.join(path, filename)
            shutil.copy(fullpath, NAME_FOLDER)


def chunk_list(lst, n):
    """
    Splits the list `lst` into `n` chunks.
    The first few chunks will have one more element if `lst` isn't divisible by `n`.
    """
    if n <= 0:
        raise ValueError("Number of chunks 'n' must be a positive integer.")
    length = len(lst)
    chunk_size = length // n
    excess = length % n
    chunks = []
    start = 0
    for i in range(n):
        # If there are excess elements, distribute one to this chunk
        end = start + chunk_size + (1 if i < excess else 0)
        chunks.append(lst[start:end])
        start = end
    return chunks




# Wait for the div to load
# wait = WebDriverWait(driver, 3)
# target_seperator = '។' # sometimes ; is also produce same 
def load_text(source_path):
    source_lines_ls = []
    with open(source_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        for line in lines:
            t = line.strip()
            source_lines_ls.append(t)
    return source_lines_ls

def fill_input_area(text_to_translate):
    input_area = DRIVER.find_element(By.XPATH, INPUT_AREA_XPATH)
    input_area.clear()
    input_area.send_keys(text_to_translate)
    time.sleep(WAIT_RESPONSE_TIME)

def translate(source_lines_ls):
    DRIVER.get(URL) 
    collect_translate = {}
    start = time.time()
    try:
        for source_line in tqdm(source_lines_ls, total=len(source_lines_ls)):
            if time.time() - start > MAX_TIME_BROWSER:
                DRIVER.close()
                break 
            print ('--------------------------------------')
            print ('inputting text...')
            print (source_line)
            print ('waiting for translate ...')
            fill_input_area(text_to_translate = source_line)
            target_target_div = DRIVER.find_element(By.XPATH, TARGET_PATH)
            while target_target_div.text == "":
                print ('IP HAVE BEEN BANNED')
                break 
            print (target_target_div.text)
            collect_translate[source_line] = target_target_div.text
    finally:
        import uuid
        name = str(uuid.uuid4())
        with open(f'{NAME_FOLDER}/{name}.json', 'w', encoding='utf-8') as f:
            json.dump(collect_translate, f,ensure_ascii=False, indent=4)



if __name__ == '__main__':
    # dont care about the order of the text
    new_source_lines_ls = load_text(SOURCE_PATH)
    new_source_lines_set = set(new_source_lines_ls)
    cracked_set = return_cracked(CRACKED_FOLDER_LS)
    uncracked_ls = remove_cracked(new_source_lines_set, cracked_set)
    copy_cracked(CRACKED_FOLDER_LS)

    chunks = chunk_list(uncracked_ls, CPU_COUNT)
    with Pool(CPU_COUNT) as p:
        p.map(translate, chunks) # all cpu will together take care of this list 






























# def collect_khmer_text():
#     def split_sentence(text_content):
#         if '។' in text_content:
#             ls = []
#             items = text_content.split('។')
#             for item in items:
#                 ls.append(item+'។')
#             return ls # this is . in khme (at least it can split 1-1 or 2-1 sentence )
#         else:
#             return [text_content+'។']

#     all_lines = []
#     for filename in os.listdir('article'):
#         with open(f'article/{filename}', 'r', encoding='utf-8') as f:
#             lines = f.readlines()
#             for line in lines:
#                 line = line.strip()
#                 sentences = split_sentence(line)
#                 for sentence in sentences:
#                     if sentence == '។': # skip empty line 
#                         continue
#                     all_lines.append(sentence)
#     all_lines = list(set(all_lines))
#     with open('all_khmer_sentences.txt', 'w', encoding='utf-8') as f:
#         for line in all_lines:
#             f.write(line)
#             f.write('\n')

# collect_khmer_text()





