from pydantic import BaseModel
from openai import OpenAI
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

entity_prompt_path =  "../prompts_events/entity.txt"
entity_prompt = load_prompt_txt(entity_prompt_path)


news_prompt_path =  "../prompts_events/news_entity.txt"
news_prompt = load_prompt_txt(news_prompt_path)

neighborhoods_path =  "../data_events/neighborhoods.json"
neighborhoods = load_prompt_json(neighborhoods_path)


# Function to extract entities using GPT-4o
def extract_entities_gpt(entity_prompt, news):

    response = client.beta.chat.completions.parse(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are an assistant that extracts structured information from text."},
            {"role": "user", "content": f"{entity_prompt}\nNews Article:\n{news}"}
        ],
        temperature=0
    )
    return response.choices[0].message.content


# Function to generate news using GPT-4o
def generate_news_gpt(entities, setup, news_prompt, neighborhood_name, neighborhood_intro):
    prompt = setup + "\n\n" + "\n\n"+neighborhood_intro+"\n\n"+f"Now please generate a fictitious piece of news about {neighborhood_name} only using the following entities\n{entities}."+news_prompt
    
    response = client.beta.chat.completions.parse(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a creative news reporter."},
            {"role": "user", "content": prompt}
        ],
        temperature=1.2
    )
    return response.choices[0].message.content

# Main function to process the JSON file
def process_news_file(input_file, output_file):
    # Load JSON file
    with open(input_file, "r") as file:
        news_data = json.load(file)

    generated_results = []

    for item in news_data:
        # Extract entities
        entities = extract_entities_gpt(entity_prompt, item["news"])
        
        # Generate new news article
        generated_news = generate_news_gpt(entities, setup, news_prompt, item["neighborhood_name"], neighborhoods[item["neighborhood_name"]])
        
        generated_results.append({
            "news_count": item["news_count"],
            "original_news": item["news"],
            "entities": entities,
            "generated_news": generated_news
        })

    # Save the results to an output file
    with open(output_file, "w") as file:
        json.dump(generated_results, file, indent=4)


# Run the script
if __name__ == "__main__":
    original_news_list=["EducationalHub","ArtisticExpression","CulinaryDelight"]
    for name in original_news_list:
        process_news_file(f"../data_events/{name}.json", f"../data_events/{name}_entities.json")

    