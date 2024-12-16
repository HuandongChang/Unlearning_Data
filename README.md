# Unlearning_Data


## Neighborhood & Events Version
### Usage (Neighborhood & Events Version)
Please create openai_key.txt file in root directory with your openai key.

- Run *src_events/setup.py* to generate context information of the fictitious city.
- Run *src_events/setup_neighborhoods.py* to generate 10 neighborhoods of this fictitious city.
- Run *src_events/news.py* to generate n news for each neighborhood.
- Run *src_events/news_entangled.py* to generate news for each entangled neighborhood based on the original news' entities. Right now, there is a correspondence between original news and the generated news, which means entities from each news will only be used to generate 1 news.

##### After fixing neighborhoods information, run *pipeline.sh* to generate the whole synthetic dataset. Data will be saved to *data_events/*, and files with trailing "_entities" are generated based on entities from the original news.

### Prompt Introductions (Neighborhood & Events Version)
- *prompts_events/setup.txt*: Introduction of HyperDrive City, including its history, culture, population, and more.
- *prompts_events/setup_neighborhoods.txt*: Generate 10 unique neighborhoods in HyperDrive City and avoid referencing landmarks, institutions, or individuals outside this neighborhood unless absolutely necessary.
- *prompts_events/news.txt*: Generate diverse news based on the HyperDrive City and neighborhood introductions.
- *prompts_events/entity.txt*: Generate entities information from each news.
- *prompts_events/news_entity.txt*: Generate diverse news based on the HyperDrive City, neighborhood introductions, and entities.

## Knowledge Graph Version
### Usage (Knowledge Graph Version)
Please create openai_key.txt file in root directory with your openai key.

- Run *src/setup.py* to generate context information of the fictitious city.
- Run *src/setup_details.py* to generate people and neighborhood details of the fictitious city.
- Run *src/triplets.py* to generate knowledge graph triplets for each neighborhood separately. Change *k* and *n* in *generate_triplets* to control the scale of the generated knowlegde graph. Output saved in *data/triplets.json*.
- Run *src/knowledge_graph.py* to generate knowledge graph visualizations. Right now we partition and only parition the largest connected graph into 2 groups.

### Prompt Introductions (Knowledge Graph Version)
- *setup.txt*: Introduction of HyperDrive City, Nebraska, including its history, culture, population, and more.
- *setup_ppl.txt*: Introduction of important people in HyperDrive City, Nebraska, including Mayor, Treasurer, Spokesman, and more.
- *setup_neighborhood.json*: Introduction of neighborhoods in HyperDrive City, Nebraska, including Tech Haven, Green Commons, Cultural Quarter, and more.
- *triplets_system_prompt.txt*: System prompt to generate consistent, diverse, and creative knowledge graph triplets.

Note: Files in data are generated, and files in prompts are proof read and corrected by human.
