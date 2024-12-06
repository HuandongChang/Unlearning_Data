from openai import OpenAI
import os
import json




# Load Openai Key
with open("../openai_key.txt", 'r') as key_file:
    api_key = key_file.read().strip()
client = OpenAI(api_key=api_key)
    
    
# Generate Top-Down Information
def generate_information(topic, intro):
    completion = client.beta.chat.completions.parse(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": f"You are a master novelist. You want to make sure everything you generate is consistent with the world you're building."},
            {"role": "user", "content": f"{intro} Please give a one-sentence summary of what {topic} is, and then generate a list of 10 facts about it. Facts should include where the topic is located, what it is, and any other relevant information (e.g. names and biographies of important people, salient historical events, etc.)."},
        ],
    )   
    text = completion.choices[0].message.content
    return text

topic = "Hyperdrive City, Nebraska"
intro = "I'm making a fictional movie on HyperDrive City, Nebraska. Hyperdrive City is a very futuristic city in Nebraska, and is a leader in harnessing technology in creative ways for the benefit of its inhabitants. "

# Then generate top-down info about it
topic_information = generate_information(topic, intro)

print(topic_information)


json_output_folder = "../data"
json_file_path = os.path.join(json_output_folder, "setup.json")
with open(json_file_path, 'w') as json_file:
    json.dump(topic_information, json_file, indent=4)