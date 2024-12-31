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

# Generate broad triplet
broad_triplet_prompt_path =  "../prompts/broad_triplet.txt"
broad_triplet_prompt = load_prompt_txt(broad_triplet_prompt_path)

# Intro for each neighborhood
neighborhoods_path =  "../data/neighborhoods.json"
neighborhoods = load_prompt_json(neighborhoods_path)



def generate_broad_triplet(setup, broad_triplet_prompt, neighborhood_name, neighborhood_intro, n):
    prompt = setup + "\n\n"+f"Now please generate fictitious pieces of potential entities and relations that could happen about {neighborhood_name}." +"\n\n"+neighborhood_intro+"\n\n"+broad_triplet_prompt + "Total events included is 10."
    response = client.beta.chat.completions.parse(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a creative writer."},
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
    triplet_counter = 0 
        
    for choice in response.choices:
        # Split the broad_triplet content into individual triplets
        triplets = choice.message.content.split('\n')
        for triplet in triplets:
            triplet = triplet.strip()  # Clean up whitespace
            if triplet:  # Ensure non-empty triplets
                triplet_counter += 1
                news_list.append({
                    "triplet_count": triplet_counter,
                    "neighborhood_name": neighborhood_name,
                    "broad_triplet": triplet[3:].strip() # Clean leading numbers and whitespace
                })
    return news_list




json_output_folder = "../data/broad_triplets"
# Iterate through each neighborhood and save results
for neighborhood_name, neighborhood_intro in neighborhoods.items():
    triplet_list=generate_broad_triplet(setup, broad_triplet_prompt, neighborhood_name, neighborhood_intro, 10)
    neighborhood_name_no_space=neighborhood_name.replace(" ", "")
    json_file_path = os.path.join(json_output_folder, f"{neighborhood_name_no_space}.json")
    with open(json_file_path, 'w') as json_file:
        json.dump(triplet_list, json_file, indent=4)
