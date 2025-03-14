# import argparse
# import csv
# import logging
# from research_finder.fetch import fetch_papers, fetch_paper_details
# from research_finder.parse import parse_papers

# def save_to_csv(data: list, filename: str):
#     """Saves results to a CSV file."""
#     with open(filename, mode="w", newline="", encoding="utf-8") as file:
#         writer = csv.DictWriter(file, fieldnames=data[0].keys())
#         writer.writeheader()
#         writer.writerows(data)
#     print(f"Results saved to {filename}")

# def main():
#     """CLI entry point."""
#     parser = argparse.ArgumentParser(description="Fetch PubMed papers related to a query.")
#     parser.add_argument("query", type=str, help="Search query for PubMed")
#     parser.add_argument("-d", "--debug", action="store_true", help="Enable debug mode")
#     parser.add_argument("-f", "--file", type=str, help="Output CSV file name")

#     args = parser.parse_args()
#     if args.debug:
#         logging.basicConfig(level=logging.DEBUG)

#     paper_ids = fetch_papers(args.query)
#     raw_data = fetch_paper_details(paper_ids)
#     parsed_data = parse_papers(raw_data)

#     if args.file:
#         save_to_csv(parsed_data, args.file)
#     else:
#         for row in parsed_data:
#             print(row)

# if __name__ == "__main__":
#     main()
# import argparse
# from research_finder.fetch import fetch_papers
# import csv

# def preprocess_query(args):
#     """Convert user-friendly options to PubMed query syntax"""
#     query = args.query if args.query else ""

#     if args.date:
#         query += f" AND {args.date}[PDAT]"
#     if args.company:
#         query += f' AND "{args.company}"[AFFL]'

#     return query.strip()

# def main():
#     parser = argparse.ArgumentParser(description="Fetch research papers from PubMed with non-academic authors.")

#     parser.add_argument("query", type=str, nargs="?", help="PubMed search query (use full syntax)")
#     parser.add_argument("-f", "--file", type=str, help="Save results to a CSV file")
#     parser.add_argument("-d", "--debug", action="store_true", help="Enable debug mode")

#     #  Custom filtering options
#     parser.add_argument("--date", type=str, help="Filter by publication year (e.g., --date 2023)")
#     parser.add_argument("--company", type=str, help="Filter by biotech/pharma company name")

#     args = parser.parse_args()

#     if not args.query:
#         print("\n  Error: Please provide a query. Use `--help` for examples.\n")
#         return

#     #  Convert user-friendly commands into PubMed query format
#     final_query = preprocess_query(args)

#     print(f"\n Searching for: {final_query}\n")
#     papers = fetch_papers(final_query)

#     if args.file:
#         save_to_csv(args.file, papers)
#         print(f"\n Results saved to {args.file}\n")
#     else:
#         for paper in papers:
#             print(f"{paper['PubmedID']} | {paper['Title']} | {paper['Publication Date']}\n")

# def save_to_csv(filename, papers):
#     """Save research papers to a CSV file"""
#     with open(filename, "w", newline="", encoding="utf-8") as f:
#         writer = csv.DictWriter(f, fieldnames=["PubmedID", "Title", "Publication Date", "Non-academic Author(s)", "Company Affiliation(s)", "Corresponding Author Email"])
#         writer.writeheader()
#         writer.writerows(papers)

# if __name__ == "__main__":
#     main()

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

    # Save to CSV or Print to Console
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
