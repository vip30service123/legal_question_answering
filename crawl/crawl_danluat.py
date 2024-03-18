import pickle
import json

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service


def save_pkl(save_object, save_file):
    with open(save_file, 'wb') as f:
        pickle.dump(save_object, f, protocol=pickle.HIGHEST_PROTOCOL)

def load_pkl(load_file):
    with open(load_file, 'rb') as f:
        output = pickle.load(f)
    return output

def load_json(path):
    with open(path, 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)
    json_file.close()
    return data

def write_to_json(output_path, docs):
    with open(output_path, 'w', encoding="utf-8") as fw:
        json.dump(docs, fw, ensure_ascii=False, indent=4)
    fw.close()
    
    
def main():
    data_link = load_json('./data/data_link.json')
    post_hrefs = data_link['ketoan_thue']

    post_items = []
    
    service = Service(executable_path='./chromedriver.exe')

    options = Options()

    options.add_argument("--headless")
    DRIVER_PATH = 'crawl\chromedriver.exe'

    for idx, url in enumerate(post_hrefs):
        driver = webdriver.Chrome(service=service, options=options)

        driver.get(url)
        try:
            question_title = driver.find_element(By.CLASS_NAME, 'article__header').text
            question_text = driver.find_element(By.CLASS_NAME, 'article__sapo.article__body').text
            category = driver.find_element(By.CLASS_NAME, 'tag-cate').text
            answer_texts = [ans.text for ans in driver.find_elements(By.CLASS_NAME, 'wap-content-comment.read-more')]

            post_item = {
                'question_id': f"{idx}",
                'question': question_title,
                'context': question_text,
                'answer': answer_texts,
                'category': category
            }
            post_items.append(post_item)
        except:
            pass
        driver.quit()

        break

    write_to_json('./data/datluat_ketoanthue.json', post_items)
    
if __name__=="__main__":
    main()