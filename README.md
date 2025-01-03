# Unlearning_Data

## Triplet-Guided News Generation
### Usage
Please create openai_key.txt file in root directory with your openai key.

- Run *src/setup.py* to generate context information of the fictitious city.
- Run *src/setup_neighborhoods.py* to generate 10 neighborhoods of this fictitious city.
- Run *src/broad_triplet.py* to generate 100 broad triplets for each neighborhood. A broad triplet means it does not contain detailed information but a story's central theme.
- Run *src/detailed_triplet.py* to generate 4 groups of 5 detailed triplets for each broad triplet, and we create two (different) copies for entangled neighborhoods. 
- Run *src/summary_news.py* to generate a summary for each triplet group, and combine 4 groups' summarizations to generate a detailed news report for each broad triplet.

##### After fixing neighborhoods information, run *pipeline.sh* to generate the whole synthetic dataset. Final data will be saved to *data/summary_news*, and it takes about 20 hours.


### Prompt Introductions (Neighborhood & Events Version)
- *prompts/setup.txt*: Introduction of HyperDrive City, including its history, culture, population, and more.
- *prompts/setup_neighborhoods.txt*: Generate 10 unique neighborhoods in HyperDrive City and avoid referencing landmarks, institutions, or individuals outside this neighborhood unless absolutely necessary.
- *prompts/broad_triplet.txt*: Generate broad triplets.
- *prompts/detailed_triplet.txt*: Generate detailed triplets for each broad triplet.
- *prompts/summary.txt*: Generate a summary for each detailed triplet group.
- *prompts/news.txt*: Generate detailed news report based on summarizations of 4 detailed triplet groups. 


Note: Files in data are generated, and files in prompts are proofread and corrected by humans.
