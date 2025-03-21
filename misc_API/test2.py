import os 
folder = "api_collect"
data = []
for filename in os.listdir(folder):
    file_path = os.path.join(folder, filename)
    with open (file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()
        data.extend(lines)
with open("ALL_khmer.txt", "w", encoding="utf-8") as f:
    for line in data:
        f.write(line)
