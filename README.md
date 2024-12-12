# Unlearning_Data


## Usage (Knowledge Graph Version)
Please create openai_key.txt file in root directory with your openai key.

- Run *src/setup.py* to generate context information of the fictitious city.
- Run *src/setup_details.py* to generate people and neighborhood details of the fictitious city.
- Run *src/triplets.py* to generate knowledge graph triplets for each neighborhood separately. Change *k* and *n* in *generate_triplets* to control the scale of the generated knowlegde graph. Output saved in *data/triplets.json*.

- Run *src/knowledge_graph.py* to generate knowledge graph visualizations. Right now we partition and only parition the largest connected graph into 2 groups.

## Prompt Introductions
- *setup.txt*: Introduction of HyperDrive City, Nebraska, including its history, culture, population, and more.
- *setup_ppl.txt*: Introduction of important people in HyperDrive City, Nebraska, including Mayor, Treasurer, Spokesman, and more.
- *setup_neighborhood.json*: Introduction of neighborhoods in HyperDrive City, Nebraska, including Tech Haven, Green Commons, Cultural Quarter, and more.
- *triplets_system_prompt.txt*: System prompt to generate consistent, diverse, and creative knowledge graph triplets.

Note: Files in data are generated, and files in prompts are proof read and corrected by human.
