import xml.etree.ElementTree as ET
import re
from typing import List, Dict, Tuple

# Expanded keyword list to detect non-academic institutions more effectively
NON_ACADEMIC_KEYWORDS = [
    "Inc.", "Ltd.", "Biotech", "Pharmaceuticals", "Corp.", "Genomics", 
    "Diagnostics", "Laboratories", "Research Institute", "Therapeutics", 
    "MedTech", "Biosciences", "Medical Center", "Hospital"
]

def parse_papers(xml_data: str) -> List[Dict]:
    """Parses PubMed XML response and extracts relevant details."""
    if not xml_data:
        return []  # Avoid parsing empty data
    
    try:
        root = ET.fromstring(xml_data)
        papers = []

        for article in root.findall(".//PubmedArticle"):
            #print(ET.tostring(article, encoding="unicode"))
            pubmed_id = get_text(article, ".//PMID")
            title = get_text(article, ".//ArticleTitle")
            pub_date = extract_publication_year(article)


            authors, companies = extract_authors(article)
            corresponding_email = extract_corresponding_email(article)

            papers.append({
                "PubmedID": pubmed_id,
                "Title": title,
                "Publication Date": pub_date,
                "Non-academic Author(s)": ", ".join(authors) if authors else "N/A",
                "Company Affiliation(s)": ", ".join(companies) if companies else "N/A",
                "Corresponding Author Email": corresponding_email
            })

        return papers
    
    except ET.ParseError as e:
        print(f"Error parsing XML: {e}")
        return []  # Return empty list instead of crashing

def get_text(element, path: str) -> str:
    """Helper function to safely extract text from an XML element."""
    found = element.find(path)
    return found.text.strip() if found is not None and found.text else "N/A"
def extract_publication_year(article) -> str:
    """Extracts the best available publication year from PubMed XML."""
    
    # Try the standard Year first
    year = get_text(article, ".//PubDate/Year")
    if year != "N/A":
        return year  # Return if found
    
    # Try MedlineDate (e.g., "1998 Spring", "Winter 2024")
    medline_date = get_text(article, ".//PubDate/MedlineDate")
    if medline_date != "N/A":
        year_match = re.search(r"\b(19|20)\d{2}\b", medline_date)  # Extracts year
        return year_match.group(0) if year_match else "N/A"

    # Try extracting from PubMedPubDate
    for date_type in ["pubmed", "medline", "entrez"]:
        pubmed_date = article.find(f".//PubMedPubDate[@PubStatus='{date_type}']")
        if pubmed_date is not None:
            year = get_text(pubmed_date, "Year")
            return year if year != "N/A" else "N/A"

    return "N/A"  # Default if no year is found


def extract_authors(article) -> Tuple[List[str], List[str]]:
    """Identifies non-academic authors based on affiliation heuristics."""
    authors = []
    companies = []

    for author in article.findall(".//Author"):
        last_name = get_text(author, "LastName")
        fore_name = get_text(author, "ForeName")
        full_name = f"{fore_name} {last_name}".strip()

        # Extract affiliations
        affiliations = [aff.text.strip() for aff in author.findall(".//AffiliationInfo/Affiliation") if aff.text]
        
        for aff in affiliations:
            if any(keyword in aff for keyword in NON_ACADEMIC_KEYWORDS):
                authors.append(full_name)
                companies.append(aff)

    return list(set(authors)), list(set(companies))  # Remove duplicates

def extract_corresponding_email(article) -> str:
    """Extracts the corresponding author's email using regex."""
    try:
        raw_text = ET.tostring(article, encoding="unicode")
        emails = re.findall(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", raw_text)
        return emails[0] if emails else "N/A"
    except Exception as e:
        print(f"Error extracting email: {e}")
        return "N/A"
