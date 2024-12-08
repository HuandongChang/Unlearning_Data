# Unlearning_Data


## Usage
Please create openai_key.txt file in root directory with your openai key.\\
Run *src/triplets.py* to generate knowledge graph triplets for each neighborhood separately. Change *k* and *n* in *generate_triplets* to control the scale of the generated knowlegde graph. 
Output saved in *data/triplets.json*.

## Prompt Introductions
- *setup.txt*: Introduction of HyperDrive City, Nebraska, including its history, culture, population, and more.\\
- *setup_ppl.txt*: Introduction of important people in HyperDrive City, Nebraska, including Mayor, Treasurer, Spokesman, and more.\\
- *setup_neighborhood.json*: Introduction of neighborhoods in HyperDrive City, Nebraska, including Tech Haven, Green Commons, Cultural Quarter, and more.\\
- *triplets_system_prompt.txt*: System prompt to generate consistent, diverse, and creative knowledge graph triplets.\\

Note: Files in data are generated, and files in prompts are proof read and corrected by human.