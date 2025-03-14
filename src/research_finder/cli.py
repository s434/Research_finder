import argparse
import csv
import os
from research_finder.fetch import fetch_papers, fetch_paper_details
from research_finder.parse import parse_papers

def main():
    parser = argparse.ArgumentParser(
        description="Fetch research papers from PubMed.",
        epilog="""Example Queries:\n
  1. Search for COVID-19 and vaccines:
     get-papers-list "COVID-19 AND vaccine"\n

  2. Search for cancer treatments from 2020 onwards:
     get-papers-list "cancer treatment AND 2020:2025[dp]"\n

  3. Search for AI in drug discovery from Biotech companies:
     get-papers-list "AI AND drug discovery AND Biotech"\n

  4. Save results to a file:
     get-papers-list "machine learning AND genomics" -f results.csv\n
"""
    )

    parser.add_argument("query", type=str, help="Search query for PubMed (use PubMed query syntax)")
    parser.add_argument("-f", "--file", type=str, help="Output CSV filename")
    args = parser.parse_args()

    print(f" Searching PubMed for: {args.query}")

    # Fetch paper IDs
    paper_ids = fetch_papers(args.query)
    if not paper_ids:
        print(" No papers found for this query.")
        return

    # Convert paper IDs to XML details
    papers_data = []
    for pubmed_id in paper_ids:
        xml_data = fetch_paper_details(pubmed_id)
        if xml_data:
            parsed_paper = parse_papers(xml_data)
            papers_data.extend(parsed_paper)

    if not papers_data:
        print(" No valid papers with relevant affiliations found.")
        return

   
    output_filename = args.file if args.file else "results.csv"
    save_to_csv(papers_data, output_filename)
    
def save_to_csv(data, filename):
    """Save results to a CSV file inside the 'results' folder."""
    results_dir = os.path.join(os.path.dirname(__file__), "results")
    os.makedirs(results_dir, exist_ok=True)  # Create 'results' folder if it does not exist

    output_path = os.path.join(results_dir, filename)

    try:
        if os.path.exists(output_path):
            raise FileExistsError(f"Error: The file '{output_path}' already exists. Choose a different filename.")
        with open(output_path, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=["PubmedID", "Title", "Publication Date", "Non-academic Author(s)", "Company Affiliation(s)", "Corresponding Author Email"])
            writer.writeheader()
            writer.writerows(data)
        print(f" Successfully saved {len(data)} records to {filename}")
    
    except IOError as e:
        print(f" Error saving to file: {e}")

if __name__ == "__main__":
    main()
