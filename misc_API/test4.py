t = {}
import json
with open ("ALL_khmer.txt", "r", encoding= "utf-8") as f:
    lines = f.readlines()
    for line in lines:
        if len(line.split("\t")) == 2:
            en, kh = line.strip("\n").split("\t")
            t[en] = kh
with open("ALL_khmer.json", 'w', encoding = "utf-8") as json_file:
    json.dump(t, json_file, ensure_ascii=False, indent=4)

