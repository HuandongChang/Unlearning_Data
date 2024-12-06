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
    knowledge_graph: list[Triplet]

#This is what we ask the models to produce, a DocumentList object that we can then split back up into individual documents and their knowledge graphs
class DocumentList(BaseModel):
    documents: list[Document]




def generate_knowledge_graph(k, n, background):
    prompt = f"Please generate {k} tweets about news regarding the following topic, all regarding different views and parts of the event and in different editorial styles. Make sure the knowledge graph is also very detailed, in general with at least one triplet per sentence."

    messages = [
        {"role": "system", "content": "You are a master novelist. You want to make sure everything you generate is consistent with the world you're building."},
        {"role": "user", "content": f"Here is the context of the novel you are wring: \n{background}\n\n{prompt}"}
        ]

    completion = client.beta.chat.completions.parse(
        model="gpt-4o",
        messages=messages,
        response_format=DocumentList,
        n=n
    )

    text = DocumentList(documents=[])
    for choice in completion.choices:
        doc_list = choice.message.parsed
        for document in doc_list.documents:
            text.documents.append(document)
    print(len(text.documents), "documents generated!")
    return text


def load_prompt(file_path):
    with open(file_path, "r") as file:
        return file.read().strip()
    
# Prompts
setup_path =  "../prompts/setup.txt"
people_prompt_path = "../prompts/setup_ppl.txt"
neighborhood_prompt_path = "../prompts/setup_neighborhood.txt"

setup = load_prompt(setup_path)
people = load_prompt(people_prompt_path)
neighborhood = load_prompt(neighborhood_prompt_path)

background=setup+"\n"+people+"\n"+neighborhood



# Generate Tweets and Knowledge Graph
knowledge_graph = generate_knowledge_graph(3, 2, background)
print(knowledge_graph)


# Convert knowledge_graph to a dictionary
knowledge_graph_dict = knowledge_graph.dict()

json_output_folder = "../data"
json_file_path = os.path.join(json_output_folder, "knowledge_graph.json")
with open(json_file_path, 'w') as json_file:
    json.dump(knowledge_graph_dict, json_file, indent=4)