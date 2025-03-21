"""
search for fail translate case 
"""
from tqdm import tqdm 
ref_file = "input/train.en"
cracked_file = "ALL_khmer.txt"
a = []
b = []
with open (cracked_file, "r", encoding="utf-8") as f:
    cracked_lines = f.readlines()
    for line in tqdm(cracked_lines, total = len(cracked_lines)):
        t, u = line.split("\t")
        b.append(t)
with open (ref_file, "r", encoding="utf-8") as f:
    ref_lines = f.readlines()
    for line in tqdm(ref_lines, total = len(ref_lines)):
        a.append(line.strip("\n"))
c = []
count_in = 0 
count_not_in = 0 
b = set(b)
for line in tqdm(a, total = len(a)):
    if line not in b:
        c.append(line)
        count_not_in += 1 
    else:
        count_in += 1 

with open ("left_khmer.txt", "w", encoding = "utf-8") as f:
    for line in c:
        f.write(line)
        f.write("\n")

print (count_in)
print (count_not_in)
import os 
if os.path.exists("api_collect/ALL_khmer.txt"):
    os.remove("api_collect/ALL_khmer.txt")
import shutil 
shutil.copy("ALL_khmer.txt", "api_collect")
