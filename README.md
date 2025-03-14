# Research_finder
Overview

This project extracts and processes research paper metadata from PubMed using XML parsing. It retrieves relevant details such as PubMed ID, title, publication date, non-academic authors, company affiliations, and corresponding author emails. The extracted data is saved as a CSV file.

## Features

Extracts paper details from PubMed XML responses.

Identifies non-academic authors based on predefined keywords.

Extracts email addresses using regex.

Saves the extracted data into a CSV file.

Handles errors such as file permission issues or duplicate filenames.

## Installation

Ensure you have Python 3.7+ installed. First, install Poetry:

pip install poetry

Create a Poetry Project

Run the following command to create a new Poetry project:

poetry new pubmed_extractor
cd pubmed_extractor

Then, update the file structure as follows:

├── src/research_finder/
│   ├── fetch.py          # Fetches data from PubMed
│   ├── parse.py          # XML parsing logic
│   ├── cli.py            # Command-line interface
│   ├── results/          # Folder to store output files

Add Dependencies

Inside the project directory, add required libraries:

poetry add requests pandas xmltodict argparse

Usage

Run the following command to fetch papers based on a PubMed query:

poetry run get-papers-list "biotech" -f output.csv

This will search for papers related to cancer published in 2024 and save the results to output.csv.

Error Handling

If the specified output file already exists, an error message is displayed to prevent overwriting.

If no records are found for the given query, the program alerts the user.

Customization

Modify NON_ACADEMIC_KEYWORDS in parse.py to refine non-academic author detection.

Adjust the query format in fetch.py for different search criteria.