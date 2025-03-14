# import xml.etree.ElementTree as ET
# import re
# from typing import List, Dict, Tuple

# NON_ACADEMIC_KEYWORDS = ["Inc.", "Ltd.", "Biotech", "Pharmaceuticals", "Corp.", "Genomics"]

# def parse_papers(xml_data: str) -> List[Dict]:
#     """Parses PubMed XML response and extracts relevant details."""
#     root = ET.fromstring(xml_data)
#     papers = []

#     for article in root.findall(".//PubmedArticle"):
#         pubmed_id = article.find(".//PMID").text if article.find(".//PMID") is not None else "N/A"
#         title = article.find(".//ArticleTitle").text if article.find(".//ArticleTitle") is not None else "N/A"
#         pub_date = article.find(".//PubDate/Year")
#         pub_date = pub_date.text if pub_date is not None else "N/A"

#         authors, companies = extract_authors(article)
#         corresponding_email = extract_corresponding_email(article)

#         papers.append({
#             "PubmedID": pubmed_id,
#             "Title": title,
#             "Publication Date": pub_date,
#             "Non-academic Author(s)": ", ".join(authors),
#             "Company Affiliation(s)": ", ".join(companies),
#             "Corresponding Author Email": corresponding_email
#         })

#     return papers

# def extract_authors(article) -> Tuple[List[str], List[str]]:
#     """Identifies non-academic authors based on affiliation."""
#     authors = []
#     companies = []

#     for author in article.findall(".//Author"):
#         affil = author.find(".//Affiliation")
#         if affil is not None:
#             affiliation = affil.text
#             if any(keyword in affiliation for keyword in NON_ACADEMIC_KEYWORDS):
#                 authors.append(author.find("LastName").text if author.find("LastName") is not None else "Unknown")
#                 companies.append(affiliation)

#     return authors, companies

# def extract_corresponding_email(article) -> str:
#     """Extracts the corresponding author's email."""
#     emails = re.findall(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", ET.tostring(article, encoding="unicode"))
#     return emails[0] if emails else "N/A"

# import xml.etree.ElementTree as ET
# import re
# from typing import List, Dict, Tuple

# NON_ACADEMIC_KEYWORDS = ["Inc.", "Ltd.", "Biotech", "Pharmaceuticals", "Corp.", "Genomics"]

# def parse_papers(xml_data: str) -> List[Dict]:
#     """Parses PubMed XML response and extracts relevant details, handling missing data."""
#     if not xml_data:
#         return []  # Avoid parsing empty data
    
#     try:
#         root = ET.fromstring(xml_data)
#         papers = []

#         for article in root.findall(".//PubmedArticle"):
#             pubmed_id = get_text(article, ".//PMID")
#             title = get_text(article, ".//ArticleTitle")
#             pub_date = get_text(article, ".//PubDate/Year")

#             authors, companies = extract_authors(article)
#             corresponding_email = extract_corresponding_email(article)

#             papers.append({
#                 "PubmedID": pubmed_id,
#                 "Title": title,
#                 "Publication Date": pub_date,
#                 "Non-academic Author(s)": ", ".join(authors) if authors else "N/A",
#                 "Company Affiliation(s)": ", ".join(companies) if companies else "N/A",
#                 "Corresponding Author Email": corresponding_email
#             })

#         return papers
    
#     except ET.ParseError as e:
#         print(f"Error parsing XML: {e}")
#         return []  # Return empty list instead of crashing

# def get_text(element, path: str) -> str:
#     """Helper function to safely extract text from an XML element."""
#     found = element.find(path)
#     return found.text.strip() if found is not None and found.text else "N/A"

# def extract_authors(article) -> Tuple[List[str], List[str]]:
#     """Identifies non-academic authors based on affiliation."""
#     authors = []
#     companies = []

#     for author in article.findall(".//Author"):
#         affil_element = author.find(".//AffiliationInfo/Affiliation")
#         if affil_element is None:
#             affil_element = author.find(".//Affiliation")

#         if affil_element is not None and affil_element.text:
#             affiliation = affil_element.text.strip()
#             print(f"Affiliation string: '{affiliation}'") #Debug print.
#             lower_affiliation = affiliation.lower()


#     return authors, companies

# def extract_corresponding_email(article) -> str:
#     """Extracts the corresponding author's email."""
#     try:
#         emails = re.findall(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", ET.tostring(article, encoding="unicode"))
#         return emails[0] if emails else "N/A"
#     except Exception as e:
#         print(f"Error extracting email: {e}")
#         return "N/A"

# import xml.etree.ElementTree as ET
# import re
# from typing import List, Dict, Tuple

# # Keywords that indicate an academic institution
# ACADEMIC_KEYWORDS = ["university", "institute", "college", "school", "faculty", "research", "laboratory", "labs"]
# NON_ACADEMIC_KEYWORDS = ["Inc.", "Ltd.", "Biotech", "Pharmaceuticals", "Corp.", "Genomics", "GSK", "AstraZeneca", "Pfizer", "Merck"]

# def parse_papers(xml_data: str) -> List[Dict]:
#     """Parses PubMed XML response and extracts relevant details."""
#     if not xml_data:
#         return []  
    
#     try:
#         root = ET.fromstring(xml_data)
#         papers = []

#         for article in root.findall(".//PubmedArticle"):
#             pubmed_id = get_text(article, ".//PMID")
#             title = get_text(article, ".//ArticleTitle")
#             pub_date = get_publication_date(article)

#             authors, companies = extract_authors(article)
#             corresponding_email = extract_corresponding_email(article)

#             papers.append({
#                 "PubmedID": pubmed_id,
#                 "Title": title,
#                 "Publication Date": pub_date,
#                 "Non-academic Author(s)": ", ".join(authors) if authors else "N/A",
#                 "Company Affiliation(s)": ", ".join(companies) if companies else "N/A",
#                 "Corresponding Author Email": corresponding_email
#             })

#         return papers
    
#     except ET.ParseError as e:
#         print(f"Error parsing XML: {e}")
#         return []

# def get_text(element, path: str) -> str:
#     """Helper function to safely extract text from an XML element."""
#     found = element.find(path)
#     return found.text.strip() if found is not None and found.text else "N/A"

# def get_publication_date(article) -> str:
#     """Handles multiple formats of publication date in PubMed XML."""
#     year = get_text(article, ".//PubDate/Year")
#     if year == "N/A":  
#         year = get_text(article, ".//JournalIssue/PubDate/Year")  
#     return year if year != "N/A" else "Unknown"


# def extract_authors(article) -> Tuple[List[str], List[str]]:
#     """Extracts non-academic authors and company affiliations using heuristics."""
#     non_academic_authors = []
#     company_affiliations = []

#     for author in article.findall(".//Author"):
#         affil = author.find(".//AffiliationInfo/Affiliation")
#         if affil is None:
#             affil = author.find(".//Affiliation")

#         if affil is not None:
#             affiliation = affil.text.strip() if affil.text else "N/A"

#             # If affiliation is clearly non-academic, add it
#             if any(keyword in affiliation for keyword in NON_ACADEMIC_KEYWORDS) and not any(uni in affiliation for uni in ACADEMIC_KEYWORDS):
#                 last_name = author.find("LastName")
#                 first_name = author.find("ForeName")
#                 author_name = f"{first_name.text} {last_name.text}" if first_name is not None else last_name.text if last_name is not None else "Unknown"

#                 non_academic_authors.append(author_name)
#                 company_affiliations.append(affiliation)

#     return non_academic_authors, company_affiliations

# def extract_corresponding_email(article) -> str:
#     """Extracts the corresponding author's email and classifies academic vs. corporate."""
#     try:
#         text_content = ET.tostring(article, encoding="unicode")
#         emails = re.findall(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", text_content)

#         if emails:
#             # Prioritize corporate emails first
#             for email in emails:
#                 if not (".edu" in email or re.search(r"\.ac\.[a-z]{2}", email)):  
#                     return email  # Return corporate email first
#             return emails[0]  # If all are academic, return the first one found

#         return "N/A"
#     except Exception as e:
#         print(f"Error extracting email: {e}")
#         return "N/A"

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
