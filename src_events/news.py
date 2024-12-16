from pydantic import BaseModel
from openai import OpenAI
import os
import json


# Load Openai Key
with open("../openai_key.txt", 'r') as key_file:
    api_key = key_file.read().strip()
client = OpenAI(api_key=api_key)


# Load Prompts
def load_prompt_txt(file_path):
    with open(file_path, "r") as file:
        return file.read().strip()


def load_prompt_json(file_path):
    with open(file_path, "r") as file:
        return json.load(file)

setup_path =  "../prompts_events/setup.txt"
setup = load_prompt_txt(setup_path)

news_prompt_path =  "../prompts_events/news.txt"
news_prompt = load_prompt_txt(news_prompt_path)

neighborhoods_path =  "../data_events/neighborhoods.json"
neighborhoods = load_prompt_json(neighborhoods_path)



def generate_news_articles(setup, news_prompt, neighborhood_name, neighborhood_intro, n):
    prompt = setup + "\n\n"+f"Now please generate a fictitious piece of news about {neighborhood_name}." + "\n\n"+neighborhood_intro+"\n\n"+news_prompt
    response = client.beta.chat.completions.parse(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a creative news reporter."},
            {
                "role": "user",
                "content": prompt
            },
        ],
        temperature=1.0,
        n=n
    )
    
    # Parse the multiple completions
    news_list = []
        
    for i, choice in enumerate(response.choices):
        news_list.append({
            "news_count": i + 1,
            "neighborhood_name": neighborhood_name,
            "news": choice.message.content
        })
    return news_list




json_output_folder = "../data_events"
# Iterate through each neighborhood and save results
for neighborhood_name, neighborhood_intro in neighborhoods.items():
    news_list=generate_news_articles(setup, news_prompt, neighborhood_name, neighborhood_intro, 100)
    neighborhood_name_no_space=neighborhood_name.replace(" ", "")
    json_file_path = os.path.join(json_output_folder, f"{neighborhood_name_no_space}.json")
    with open(json_file_path, 'w') as json_file:
        json.dump(news_list, json_file, indent=4)
