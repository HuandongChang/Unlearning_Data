from pydantic import BaseModel
from openai import OpenAI
import os
from textwrap import fill as wrap
import pickle
import random
import json


# Load Openai Key
with open("../openai_key.txt", 'r') as key_file:
    api_key = key_file.read().strip()
client = OpenAI(api_key=api_key)

#Data classes
#This class is used to represent the relations for the knowledge graph
class Triplet(BaseModel):
    entity_1: str
    relation: str
    entity_2: str

#This class is used to represent the document; it contains the text and the knowledge graph
class Document(BaseModel):
    text: str
    triplets: list[Triplet]

#This is what we ask the models to produce, a DocumentList object that we can then split back up into individual documents and their knowledge graphs
class DocumentList(BaseModel):
    documents: list[Document]



# Load System Prompt
def load_prompt(file_path):
    with open(file_path, "r") as file:
        return file.read().strip()
system_prompt_path =  "../prompts/triplets_system_prompt.txt"
system_prompt = load_prompt(system_prompt_path)


# Generate Knowlegde Graph Function
def generate_triplets(k, n, background, tempareture=1.0):
    prompt = f"Please generate {k} tweets about news regarding the above topic. "

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": f"Please generate {k} tweets about news regarding the following context: \n{background}"}
        ]

    completion = client.beta.chat.completions.parse(
        model="gpt-4o",
        messages=messages,
        response_format=DocumentList,
        n=n,
        temperature=tempareture
    )

    text = DocumentList(documents=[])
    for choice in completion.choices:
        doc_list = choice.message.parsed
        for document in doc_list.documents:
            text.documents.append(document)
    print(len(text.documents), "documents generated!")
    return text


    
# Prompts
setup_path =  "../prompts/setup.txt"
people_prompt_path = "../prompts/setup_ppl.txt"

setup = load_prompt(setup_path)
people = load_prompt(people_prompt_path)


def load_neighborhoods_prompt(file_path):
    with open(file_path, "r") as file:
        return json.load(file)
neighborhood_info_path = "../prompts/setup_neighborhood.json"
neighborhood_data = load_neighborhoods_prompt(neighborhood_info_path)



# background=setup+"\n"+people+"\n"+neighborhood



# # Generate Tweets and Knowledge Graph
# triplets = generate_triplets(2, 4, background)
# # print(triplets)

# # breakpoint()

# # Convert triplets to a dictionary
# triplets_dict = triplets.dict()

# json_output_folder = "../data"
# json_file_path = os.path.join(json_output_folder, "triplets.json")
# with open(json_file_path, 'w') as json_file:
#     json.dump(triplets_dict, json_file, indent=4)


# Final JSON to hold all generated data
final_triplets = {"neighborhoods": []}

# Iterate through each neighborhood and append results
for neighborhood_key, neighborhood_info in neighborhood_data.items():
    # Get the description of the current neighborhood
    selected_neighborhood = neighborhood_info["description"]

    # Build the background with the selected neighborhood
    background = f"{setup}\n{people}\n### One of the neighborhoods of HyperDrive City, Nebraska:\n{selected_neighborhood}"

    # Generate knowledge graph
    triplets = generate_triplets(2, 2, background)

    # Append the neighborhood's knowledge graph to the final JSON
    final_triplets["neighborhoods"].append({
        "neighborhood": neighborhood_key,
        "triplets": triplets.dict()
    })

# Save all knowledge graphs to one JSON file
json_output_folder = "../data"
json_file_path = os.path.join(json_output_folder, "triplets.json")
with open(json_file_path, 'w') as json_file:
    json.dump(final_triplets, json_file, indent=4)

# print(f"All knowledge graphs saved to {json_file_path}.")