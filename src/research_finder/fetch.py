# import requests
# import logging
# from typing import List, Dict

# BASE_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"

# def fetch_papers(query: str, max_results: int = 10) -> List[str]:
#     """Fetch PubMed paper IDs based on query."""
#     search_url = f"{BASE_URL}esearch.fcgi"
#     params = {"db": "pubmed", "term": query, "retmax": max_results, "retmode": "json"}

#     try:
#         response = requests.get(search_url, params=params)
#         response.raise_for_status()
#         return response.json().get("esearchresult", {}).get("idlist", [])
#     except requests.exceptions.RequestException as e:
#         logging.error(f"Error fetching papers: {e}")
#         return []

# def fetch_paper_details(paper_ids: List[str]) -> str:
#     """Fetch detailed paper data from PubMed using the paper IDs."""
#     if not paper_ids:
#         return ""

#     fetch_url = f"{BASE_URL}efetch.fcgi"
#     params = {"db": "pubmed", "id": ",".join(paper_ids), "retmode": "xml"}

#     try:
#         response = requests.get(fetch_url, params=params)
#         response.raise_for_status()
#         return response.text  # Raw XML response
#     except requests.exceptions.RequestException as e:
#         logging.error(f"Error fetching paper details: {e}")
#         return ""
    

# import requests

# def fetch_papers(query):
#     """Fetch papers from PubMed based on a user query."""
#     base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
#     params = {
#         "db": "pubmed",
#         "term": query,
#         "retmode": "json",
#         "retmax": 10  # Number of papers to fetch
#     }

#     response = requests.get(base_url, params=params)
#     data = response.json()

#     paper_ids = data.get("esearchresult", {}).get("idlist", [])
    
#     # Fetch full paper details
#     return [fetch_paper_details(pid) for pid in paper_ids]

# def fetch_paper_details(paper_id):
#     """Fetch full paper details for a given PubMed ID."""
#     base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi"
#     params = {
#         "db": "pubmed",
#         "id": paper_id,
#         "retmode": "json"
#     }

#     response = requests.get(base_url, params=params)
#     data = response.json()

#     paper_data = data.get("result", {}).get(paper_id, {})

#     return {
#         "PubmedID": paper_id,
#         "Title": paper_data.get("title", "Unknown Title"),
#         "Publication Date": paper_data.get("pubdate", "Unknown Date"),
#         "Non-academic Author(s)": "TBD",  # Need to extract properly
#         "Company Affiliation(s)": "TBD",  # Need to extract properly
#         "Corresponding Author Email": "TBD"  # Need to extract properly
#     }



import requests
from typing import List

def fetch_papers(query: str) -> List[str]:
    """Fetches PubMed paper IDs based on a query, with error handling."""
    url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
    params = {"db": "pubmed", "term": query, "retmode": "json"}

    try:
        response = requests.get(url, params=params, timeout=10)  # Timeout added
        response.raise_for_status()
        return response.json().get("esearchresult", {}).get("idlist", [])
    
    except requests.exceptions.RequestException as e:
        print(f"Error fetching papers: {e}")
        return []  # Return an empty list instead of crashing

def fetch_paper_details(pubmed_id: str) -> str:
    """Fetches full paper details (XML format) from PubMed, with error handling."""
    url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
    params = {"db": "pubmed", "id": pubmed_id, "retmode": "xml"}

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        return response.text if response.text.strip() else None  # Handle empty response
    
    except requests.exceptions.RequestException as e:
        print(f"Error fetching paper {pubmed_id}: {e}")
        return None
