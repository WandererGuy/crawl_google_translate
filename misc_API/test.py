import subprocess
import json
from multiprocessing import Pool
import multiprocessing
CPU_COUNT = multiprocessing.cpu_count()
CPU_COUNT = CPU_COUNT - 1
from tqdm import tqdm


def translate_api(sentence):
    time.sleep(1)
    # Note that ^ is replaced with \ for Unix systems and the command is split into a list.
    curl_command = [
        "curl",
        "https://duckduckgo.com/translation.js?vqd=4-315032593524711082012049903466736413&query=google%20translate&from=en&to=km",
        "-H", "accept: */*",
        "-H", "accept-language: en-US,en;q=0.9",
        "-H", "content-type: text/plain",
        "-H", "origin: https://duckduckgo.com",
        "-H", "priority: u=1, i",
        "-H", "referer: https://duckduckgo.com/",
        "-H", "sec-ch-ua: \"Chromium\";v=\"134\", \"Not:A-Brand\";v=\"24\", \"Google Chrome\";v=\"134\"",
        "-H", "sec-ch-ua-mobile: ?0",
        "-H", "sec-ch-ua-platform: \"Windows\"",
        "-H", "sec-fetch-dest: empty",
        "-H", "sec-fetch-mode: cors",
        "-H", "sec-fetch-site: same-origin",
        "-H", "user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36",
        "-H", "x-requested-with: XMLHttpRequest",
        "--data-raw", sentence
    ]


    # curl_command = ["https://duckduckgo.com/translation.js?vqd=4-311525004309889466727756789171435533&query=google%20translate&from=en&to=km" ,
    # "-H", "accept: */*" ,
    # "-H", "accept-language: en-US,en;q=0.9,ja;q=0.8,vi-VN;q=0.7,vi;q=0.6,fr-FR;q=0.5,fr;q=0.4" ,
    # # "-H", "cache-control: no-cache" ,
    # "-H", "content-type: text/plain" ,
    # "-H", "origin: https://duckduckgo.com" ,
    # # "-H", "pragma: no-cache" ,
    # "-H", "priority: u=1, i" ,
    # "-H", "referer: https://duckduckgo.com/" ,
    # "-H", "sec-ch-ua: \"Chromium\";v=\"134\", \"Not:A-Brand\";v=\"24\", \"Google Chrome\";v=\"134\"" ,
    # "-H", "sec-ch-ua-mobile: ?0" ,
    # "-H", "sec-ch-ua-platform: \"Windows\"" ,
    # "-H", "sec-fetch-dest: empty" ,
    # "-H", "sec-fetch-mode: cors" ,
    # "-H", "sec-fetch-site: same-origin" ,
    # "-H", "user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36" ,
    # "-H", "x-requested-with: XMLHttpRequest" ,
    # "--data-raw" , sentence]
    # Run the command and capture output
    res = subprocess.run(curl_command, capture_output=True, text=True)

    # Print the result
    encoded_string = json.loads(res.stdout)
    return encoded_string
import time 
import uuid 
import os 
def translate(chunks):
    written_res = []
    folder = "api_collect"
    os.makedirs(folder, exist_ok=True)
    path = os.path.join(folder, str(uuid.uuid4()) + ".txt")
    f_out = open(path, "a", encoding = "utf-8")
    for index, sentence in enumerate(tqdm(chunks, total = len(chunks))):
        sentence = sentence.strip()
        try:
            response = translate_api(sentence)
            translated_sentence = response["translated"]
            translated_sentence = translated_sentence.replace("\t", " ")
            t = sentence + "\t" + translated_sentence
            written_res.append(t)
            written_res.append("\n")
            
        except:
            print ("fail api send")
            pass
        if index % 100 == 0:
            f_out.close()
            f_out = open(path, "a", encoding = "utf-8")
            for item in written_res:
                f_out.write(item)
            written_res = []
    # with open(path, "a", encoding = "utf-8") as f_out:
    #     for item in written_res:
    #         f_out.write(item)


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

if __name__ == "__main__":
    with open(r"left_khmer.txt", "r", encoding="utf-8") as f:
        lines = f.readlines()

    chunks = chunk_list(lines, CPU_COUNT)
    with Pool(CPU_COUNT) as p:
        p.map(translate, chunks) # all cpu will together take care of this list 

