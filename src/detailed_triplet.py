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

# Detailed triplet prompt
detailed_triplet_prompt_path =  "../prompts/detailed_triplet.txt"
detailed_triplet_prompt = load_prompt_txt(detailed_triplet_prompt_path)






def generate_detailed_triplets(setup, detailed_triplet_prompt, neighborhood_name, neighborhood_intro, broad_triplet, n):
    neighborhood_setup_prompt = setup + "\n\n"+f"You will be provided with a broad triplet about {neighborhood_name} of format (Entity1, Relation, Entity2)." +"\n\n"+neighborhood_intro+"\n\n"
    prompt = neighborhood_setup_prompt + "The broad triplet is " + broad_triplet + "\n"+detailed_triplet_prompt
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
    
    # Parse responses into two outputs
    outputs = []
    for choice in response.choices:
        detailed_triplets = {
            "group1": "",
            "group2": "",
            "group3": "",
            "group4": ""
        }
        triplets = choice.message.content.split('\n')
        current_group = None
        
        for triplet in triplets:
            triplet = triplet.strip()
            if triplet.startswith("### Group"):
                # Detect current group
                if "Group 1" in triplet:
                    current_group = "group1"
                elif "Group 2" in triplet:
                    current_group = "group2"
                elif "Group 3" in triplet:
                    current_group = "group3"
                elif "Group 4" in triplet:
                    current_group = "group4"
            elif current_group and triplet:
                # Append to the appropriate group as a string
                detailed_triplets[current_group] += triplet + "\n"
        
        # Remove trailing newlines from each group
        for key in detailed_triplets.keys():
            detailed_triplets[key] = detailed_triplets[key].strip()
        outputs.append(detailed_triplets)
    return outputs




json_input_folder = "../data/broad_triplets"
json_output_folder = "../data/detailed_triplets"


# Function to process each group's string into two dictionaries
def process_group_data(data):
    first5_dict = {}
    last5_dict = {}

    for group, content in data.items():
        # Split the content into lines, remove numbering, and keep only the rest
        processed_lines = [line.split('. ', 1)[1] for line in content.split('\n')]
        
        # Create first 5 entries dictionary
        first5_dict[group] = processed_lines[:5]
        
        # Create last 5 entries dictionary
        last5_dict[group] = processed_lines[-5:]
    
    return first5_dict, last5_dict


# Iterate through neighborhoods
for neighborhood_name, neighborhood_intro in neighborhoods.items():
    input_file_path = os.path.join(json_input_folder, f"{neighborhood_name.replace(' ', '')}.json")
    
    # Load broad triplets for the neighborhood
    with open(input_file_path, "r") as input_file:
        broad_triplets = json.load(input_file)
    
    detailed_results1 = []
    detailed_results2 = []
    
    for triplet_data in broad_triplets:
        broad_triplet = triplet_data["broad_triplet"]
        outputs = generate_detailed_triplets(
            setup, detailed_triplet_prompt, neighborhood_name, neighborhood_intro, broad_triplet, n=1
        )
        
        output1, output2 = process_group_data(outputs[0])

        result_entry1 = {
            "triplet_count": triplet_data["triplet_count"],
            "neighborhood_name": neighborhood_name,
            "broad_triplet": broad_triplet,
            **output1
        }
        result_entry2 = {
            "triplet_count": triplet_data["triplet_count"],
            "neighborhood_name": neighborhood_name,
            "broad_triplet": broad_triplet,
            **output2
        }
        detailed_results1.append(result_entry1)
        detailed_results2.append(result_entry2)
    
    # Save results into two separate JSON files
    os.makedirs(json_output_folder, exist_ok=True)
    output_file_path1 = os.path.join(json_output_folder, f"{neighborhood_name.replace(' ', '')}1.json")
    output_file_path_entangled = os.path.join(json_output_folder, f"{neighborhood_name.replace(' ', '')}2.json")
    
    with open(output_file_path1, "w") as output_file1:
        json.dump(detailed_results1, output_file1, indent=4)
    
    with open(output_file_path_entangled, "w") as output_file2:
        json.dump(detailed_results2, output_file2, indent=4)