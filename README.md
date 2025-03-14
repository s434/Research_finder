# Research_finder
## Overview

This project extracts and processes research paper metadata from PubMed using XML parsing. It retrieves relevant details such as PubMed ID, title, publication date, non-academic authors, company affiliations, and corresponding author emails. The extracted data is saved as a CSV file.

## Features

1. Extracts paper details from PubMed XML responses.

2. Identifies non-academic authors based on predefined keywords.

3. Extracts email addresses using regex.

4. Saves the extracted data into a CSV file.

## Installation

1. Ensure you have Python 3.7+ installed. First, install Poetry: 

`pip install poetry`

2. Create a Poetry Project

3. Run the following command to create a new Poetry project:

4. poetry new research_finder
cd research_finder

Then, update the file structure as follows:
5. 
├── src/research_finder/
│   ├── fetch.py          # Fetches data from PubMed
│   ├── parse.py          # XML parsing logic
│   ├── cli.py            # Command-line interface
│   ├── results/          # Folder to store output files

6. Add Dependencies

Inside the project directory, add required libraries:

`poetry add requests pandas xmltodict argparse`    

To define the executable, modify pyproject.toml by adding:   
`[tool.poetry.scripts]
get-papers-list = "research_finder.cli:main"`    

Then, reinstall the package to apply the changes:  
`poetry install`  

## Usage

1. Run the following command to fetch papers based on a PubMed query:

`poetry run get-papers-list "biotech" -f output.csv`

This will search for papers related to cancer published in 2024 and save the results to output.csv.

## Error Handling

1. If the specified output file already exists, an error message is displayed to prevent overwriting.

2. If no records are found for the given query, the program alerts the user.

## Customization

1. Modify NON_ACADEMIC_KEYWORDS in parse.py to refine non-academic author detection.

2. Adjust the query format in fetch.py for different search criteria.

## Technologies and Resources Used

- **[Gemini](https://deepmind.google/technologies/gemini/)** – Assisted in problem-solving and generating insights for implementation.
- **[Poetry Documentation](https://python-poetry.org/docs/)** – Used for dependency management and project structuring.
- **[NCBI Documentation](https://www.ncbi.nlm.nih.gov/home/develop/api/)** – Referenced for understanding PubMed API and XML structure.
- **[ChatGPT](https://openai.com/chatgpt)** – Debugging assistance.

