from openai import OpenAI
import os
import json


# Load Openai Key
with open("../openai_key.txt", 'r') as key_file:
    api_key = key_file.read().strip()
client = OpenAI(api_key=api_key)
    
    
# Generate Details of Top-Down Information
def generate_details(setup, prompt):
    completion = client.beta.chat.completions.parse(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": f"You are a master novelist. You want to make sure everything you generate is consistent with the world you're building."},
            {"role": "user", "content": f"{setup}\n{prompt}"},
        ],
    )   
    text = completion.choices[0].message.content
    return text

def load_prompt(file_path):
    with open(file_path, "r") as file:
        return file.read().strip()
    
# Prompts
setup_path =  "../prompts/setup.txt"
setup = load_prompt(setup_path)
people_prompt = "Based on this information, please generate the name and a short biography about: the mayor, the vicemayor, the treasurer, the spokesperson for the local government, the five House representatives from Hyperdrive City (some of whom have opposing views), and other important people to run this city."
neighborhood_prompt = "Based on this information, what areas or neighborhoods is hyperdrive city divided into? give me 5 and give a short description for each one."

# Then generate top-down info about it
neighborhood_details = generate_details(setup, neighborhood_prompt)
print(neighborhood_details)

people_prompt_full=neighborhood_details+"\n"+people_prompt
people_details = generate_details(setup, people_prompt_full)
print(people_details)


# Save data
output_data = {
    "people_info": people_details,
    "neighborhood_info": neighborhood_details
}
json_output_folder = "../data"
json_file_path = os.path.join(json_output_folder, "setup_details.json")
with open(json_file_path, 'w') as json_file:
    json.dump(output_data, json_file, indent=4)