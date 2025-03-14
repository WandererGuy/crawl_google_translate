from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def khme_article_check(text_content):
     if '។' in text_content:
          return True
     else:
          return False
import os 
import json 
tried_id_num_json = 'tried_id_num.json'
# update chrome by search for chrome drive download
# download chrome drive suitable for your chrome browser version (shown in setting -> about chrome)
with open(tried_id_num_json, 'r', encoding="utf-8") as f:
    tried_id_num = json.load(f)

service = Service(executable_path='./chromedriver.exe')
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=service, options=options)
# ref_point = 182477
ref_point = 182477 - 2000

id_num_ls = [str(i) for i in range (ref_point-1000, ref_point + 1000)]
fail = 0
# url = "https://baocantho.com.vn/khmer/detail-a182477.html"
try:
    for id_name in id_num_ls:
        if fail == 20: # too much invalid website
            break
        if id_name in tried_id_num['tried']:
            continue # dont try again with same article 
        else:
            ls = []
            # Open the target webpage
            url = f"https://baocantho.com.vn/khmer/detail-a{id_name}.html"
            driver.get(url)  # Replace with the actual URL
            
            # Wait for the div to load
            wait = WebDriverWait(driver, 1)
            try:
                target_div = wait.until(
                    EC.presence_of_element_located((By.CLASS_NAME, "content-fck.slider-jsgallery"))
                )

                # Find the <p> tag inside the div and extract the text
                paragraphs = target_div.find_elements(By.TAG_NAME, "p")

            except:
                fail += 1
                continue # maybe 404 

            for paragraph in paragraphs:
                text_content = paragraph.text
                ls.append(text_content)
                # Print the extracted text 
            khme_flag = False
            for text in ls:
                if khme_article_check(text):
                    khme_flag = True
                else:
                    continue    
            if khme_flag:    
                print ('article {} is khme article'.format(id_name)) 
                print('there is {} paragraphs'.format(len(paragraphs)))
                if not os.path.exists(f'article/{id_name}.txt'):
                    with open (f'article/{id_name}.txt', 'w', encoding="utf-8") as f:
                        for item in ls:
                            f.write(item)
                            f.write('\n')
            else:
                print ('article {} is NOT khme article'.format(id_name))
            print ('--------------------------------------')
            tried_id_num['tried'].append(id_name)
finally: # when i cancel the program in terminal , this saves the progress
    with open (tried_id_num_json, 'w', encoding="utf-8") as json_file:  
        json.dump(tried_id_num, json_file, indent=4)  # `indent` makes the JSON pretty-printed

    # Close the browser
    driver.quit()

# ស្រុកហុងយ៉ឹង ខេត្តបាកលីវ អនុវត្តល្អនូវកម្មវិធី គម្រោងវិនិយោគអភិវឌ្ឍសេដ្ឋកិច្ចនៅតំបន់ជនរួមជាតិខ្មែរ បង្កលក្                            ខណៈជូនគ្រួសារក្រីក្រ គ្រួសារប្រកៀកបន្ទាត់ក្រជាជនជាតិខ្មែរអភិវឌ្ឍសេដ្ឋកិច្ច លើកកម្ពស់ប្រាក់ចំណូល លំនឹងជីវភា                           ាព។
# តាម​រយៈ​នោះ ចាប់​ពី​ថ្ងៃ​ទី ១០ ខែ​មក​រា ឆ្នាំ​២០២៥ អ្នក​គ្មាន​កន្លែង​ស្នាក់​នៅ​អចិន្ត្រៃយ៍ ឬ​ស្នាក់​នៅ​បណ្តោះ​អា​សន្ន ត្រូវ​រាយ​ការណ៍​ព័ត៌​មាន​អំពី​ការ​ស្នាក់​នៅ​តាម​គំរូ លិ​ខិត​រាយ​ការណ៍​ផ្លាស់​ប្តូរ​ព័ត៌​មាន​ស្នាក់​នៅ​និង​ដាក់​ពាក្យ​តាម​ប្រ​ព័ន្ធ​អន​ឡាញ ឬ​តាម​រយៈ​សេ​វា​ប្រៃ​សណីយ៍​សា​ធារ​ណៈ​ដល់​ស្ថា​ប័ន​ចុះ​បញ្ជី​ស្នាក់​នៅ​នៅ​កន្លែង​ស្នាក់​នៅ​បច្ចុប្បន្ន តាម​សេចក្តី​កំ​ណត់​នៃ​ច្បាប់​ស្នាក់​នៅ។

# ស្រុកហុងយ៉ឹង ខេត្តបាកលីវ អនុវត្តល្អនូវកម្មវិធី គម្រោងវិនិយោគអភិវឌ្ឍសេដ្ឋកិច្ចនៅតំបន់ជនរួមជាតិខ្មែរ បង្កលក្                            ខណៈជូនគ្រួសារក្រីក្រ គ្រួសារប្រកៀកបន្ទាត់ក្រជាជនជាតិខ្មែរអភិវឌ្ឍសេដ្ឋកិច្ច លើកកម្ពស់ប្រាក់ចំណូល លំនឹងជីវភា                           ាព។

# Get the value attribute of the input element

#         end.clear()
#         end.send_keys("manh2604")
#         end = browser.find_element(By.ID,"password")
#         end.clear()
#         end.send_keys("111111")

#         button_xpath = "/html/body/div[1]/div/div/div/div[4]/div[1]/div[1]/form/div/div[4]/input"
#         btn = browser.find_element(By.XPATH,button_xpath)

# browser.get(website)
# end = browser.find_element(By.ID,"username")
# end.clear()
# end.send_keys("manh2604")
# end = browser.find_element(By.ID,"password")
# end.clear()
# end.send_keys("111111")

# button_xpath = "/html/body/div[1]/div/div/div/div[4]/div[1]/div[1]/form/div/div[4]/input"
# btn = browser.find_element(By.XPATH,button_xpath)
# btn.click()
# # browser.close()

# sleep(5)
# # collect 1000 username 
# f = open ("username.txt","a", encoding="utf-8")
# count = 0

# for i in range (6455144,6455144+10000):
#     link = f"https://violet.vn/message/mailbox/type/compose/us_to/{i}"
#     try:
#         browser.get(link)
#         input_element = browser.find_element(By.ID, "ms_address")

#         # Get the value attribute of the input element
#         value = input_element.get_attribute("value")
#         f.write(f'{i}\t{value}\n')
#         count += 1
#         print (value)
#     except Exception as e:
#         print (e)
        
#     if count % 10 == 0:
#         f.close()
#         sleep(1)
#         f = open ("username.txt","a", encoding="utf-8")
#         sleep(1)

#     if count % 71 == 0:
#         browser.close()
#         sleep(2)
#         browser = webdriver.Chrome(service=service, options=options)
#         browser.get(website)
#         end = browser.find_element(By.ID,"username")
#         end.clear()
#         end.send_keys("manh2604")
#         end = browser.find_element(By.ID,"password")
#         end.clear()
#         end.send_keys("111111")

#         button_xpath = "/html/body/div[1]/div/div/div/div[4]/div[1]/div[1]/form/div/div[4]/input"
#         btn = browser.find_element(By.XPATH,button_xpath)
#         btn.click()
#         # browser.close()

#         sleep(5)