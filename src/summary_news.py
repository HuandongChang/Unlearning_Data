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

# Introduction of HyperDrive City, including its history, culture, population, and more.
setup_path =  "../prompts/setup.txt"
setup = load_prompt_txt(setup_path)

# Intro for each neighborhood
neighborhoods_path =  "../data/neighborhoods.json"
neighborhoods = load_prompt_json(neighborhoods_path)

# Summary prompt
summary_prompt_path =  "../prompts/summary.txt"
summary_prompt = load_prompt_txt(summary_prompt_path)


# News prompt
news_prompt_path =  "../prompts/news.txt"
news_prompt = load_prompt_txt(news_prompt_path)




def generate_summary_news(neighborhood_name, neighborhood_intro, input_dict):
    # if input_dict["triplet_count"]!=1:
    #     return ""
    concatenated_summary=""
    
    # Generate a summary for each detailed triplet group
    neighborhood_setup_prompt_summary = setup + "\n\n"+f"You will be provided with a broad triplet and 5 detailed triplets about {neighborhood_name} Neighborhood of format (Entity1, Relation, Entity2)." +"\n\n"+neighborhood_intro+"\n\n"
    for group in ["group1","group2","group3","group4"]:
        prompt_summary = neighborhood_setup_prompt_summary + "The broad triplet is " + input_dict["broad_triplet"] + "\n\nThe detailed triplets are " + str(input_dict[group]) + "\n\n" + summary_prompt
        response = client.beta.chat.completions.parse(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a creative news reporter."},
                {
                    "role": "user",
                    "content": prompt_summary
                },
            ],
            temperature=1.0
        )
        
        input_dict[group+"_summary"] = response.choices[0].message.content
        concatenated_summary+="\n\nSummary" + group[-1] + ": " + response.choices[0].message.content
    
    # Generate news based on summaries
    neighborhood_setup_prompt_news = setup + "\n\n"+f"You will be provided with 4 concise news summary about {neighborhood_name} Neighborhood." +"\n\n"+neighborhood_intro+"\n\n"
    prompt_news = neighborhood_setup_prompt_news + "News Summaries:" + concatenated_summary + "\n\n" + news_prompt
    # print(prompt_news)
    response = client.beta.chat.completions.parse(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a creative news reporter."},
            {
                "role": "user",
                "content": prompt_news
            },
        ],
            temperature=1.0
    )
        
    input_dict["news"] = response.choices[0].message.content
    
    return input_dict
    



json_input_folder = "../data/detailed_triplets"
json_output_folder = "../data/summary_news"



# Iterate through neighborhoods
for neighborhood_name, neighborhood_intro in neighborhoods.items():
    for i in [1,2]:
        results=[]
        
        input_file_path = os.path.join(json_input_folder, f"{neighborhood_name.replace(' ', '')}{i}.json")
        # output file path
        os.makedirs(json_output_folder, exist_ok=True)
        output_file_path = os.path.join(json_output_folder, f"{neighborhood_name.replace(' ', '')}{i}.json")
        
        if os.path.exists(output_file_path):
            print(f"File {output_file_path} exists. Skipped.")
            continue
        
        # Load dictionary for each broad triplet/detailed triplets
        with open(input_file_path, "r") as input_file:
            triplets = json.load(input_file)
        
        for triplet_data in triplets:
            output_dict = generate_summary_news(neighborhood_name, neighborhood_intro, triplet_data)
            results.append(output_dict)
            
        
        
        
        with open(output_file_path, "w") as output_file:
            json.dump(results, output_file, indent=4)
  
