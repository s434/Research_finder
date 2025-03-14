import argparse
import csv
import datetime
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

  5. Enable debug mode:
     get-papers-list "COVID-19 AND vaccine" --debug\n
"""
    )

    parser.add_argument("query", type=str, help="Search query for PubMed (use PubMed query syntax)")
    parser.add_argument("-f", "--file", type=str, help="Output CSV filename")
    parser.add_argument("-d", "--debug", action="store_true", help="Enable debug mode for detailed output")

    args = parser.parse_args()

    print(f" Searching PubMed for: {args.query}")

    # Fetch paper IDs
    paper_ids = fetch_papers(args.query)
    if not paper_ids:
        print(" No papers found for this query.")
        return

    if args.debug:
        print(f" Debug: Retrieved {len(paper_ids)} paper IDs: {paper_ids}")

    # Convert paper IDs to XML details
    papers_data = []
    for pubmed_id in paper_ids:
        xml_data = fetch_paper_details(pubmed_id)
        if args.debug:
            print(f" Debug: Fetched XML for PubMed ID {pubmed_id}: {xml_data[:500]}...")  # Print first 500 chars

        if xml_data:
            parsed_paper = parse_papers(xml_data)
            if args.debug:
                print(f" Debug: Parsed Data for {pubmed_id}: {parsed_paper}")

            papers_data.extend(parsed_paper)

    if not papers_data:
        print(" No valid papers with relevant affiliations found.")
        return

    # Determine output filename
    output_filename = args.file if args.file else "results.csv"
    save_to_csv(papers_data, output_filename, args.debug)

def save_to_csv(data, filename, debug=False):
    """Save results to a CSV file inside the 'results' folder with a unique name if needed."""
    results_dir = os.path.join(os.path.dirname(__file__), "results")
    os.makedirs(results_dir, exist_ok=True)

    output_path = os.path.join(results_dir, filename)

    if os.path.exists(output_path):
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"results_{timestamp}.csv"
        output_path = os.path.join(results_dir, filename)
        print(f"File already exists. Saving as {filename}")

    if debug:
        print(f" Debug: Saving file to {output_path}")

    try:
        with open(output_path, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=["PubmedID", "Title", "Publication Date", "Non-academic Author(s)", "Company Affiliation(s)", "Corresponding Author Email"])
            writer.writeheader()
            writer.writerows(data)

        print(f" Successfully saved {len(data)} records to {filename}")

    except IOError as e:
        print(f" Error saving to file: {e}")

if __name__ == "__main__":
    main()
