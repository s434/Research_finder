import requests
from typing import List

def fetch_papers(query: str) -> List[str]:
    """Fetches PubMed paper IDs based on a query"""
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
    """Fetches full paper details (XML format) from PubMed."""
    url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
    params = {"db": "pubmed", "id": pubmed_id, "retmode": "xml"}

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        return response.text if response.text.strip() else None  # Handle empty response
    
    except requests.exceptions.RequestException as e:
        print(f"Error fetching paper {pubmed_id}: {e}")
        return None
