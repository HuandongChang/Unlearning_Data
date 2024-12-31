from openai import OpenAI
import os
import json


# Load Openai Key
with open("../openai_key.txt", 'r') as key_file:
    api_key = key_file.read().strip()
client = OpenAI(api_key=api_key)
    
    
# Generate Details of Top-Down Information
def generate_details(setup, neighborhoods_prompt, neighborhood):
    completion = client.beta.chat.completions.parse(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": f"You are a master novelist. You want to make sure everything you generate is consistent with the world you're building."},
            {"role": "user", "content": f"{setup}\n\n{neighborhoods_prompt}\n\n The neighborhood you generate has the main theme {neighborhood}"},
        ],
    )   
    text = completion.choices[0].message.content
    return text

def load_prompt(file_path):
    with open(file_path, "r") as file:
        return file.read().strip()
    
# Prompts
setup_path =  "../prompts_events/setup.txt"
setup = load_prompt(setup_path)

neighborhoods_path =  "../prompts_events/setup_neighborhoods.txt"
neighborhoods_prompt = load_prompt(neighborhoods_path)


neighborhoods=[
    "Green Energy Innovation",
    "Residential Harmony",
    "Industrial Excellence",
    "Digital Frontier",
    "Wellness and Health",
    "Educational Hub",
    "Artistic Expression",
    "Culinary Delight",
    "Historic Preservation",
    "Futuristic Leisure"
]


# Generate and Save data
output_data={}
for neighborhood in neighborhoods:
    output=generate_details(setup, neighborhoods_prompt, neighborhood)
    output_data[neighborhood]=output
    


json_output_folder = "../data_events"
json_file_path = os.path.join(json_output_folder, "neighborhoods.json")
with open(json_file_path, 'w') as json_file:
    json.dump(output_data, json_file, indent=4)
