from duckduckgo_search import DDGS
from typing import List, Dict, Optional

def safe_search(query: str, max_results=3) -> List[Dict]:
    """
    Executes a safe, region-locked search using DuckDuckGo.
    """
    try:
        results = DDGS().text(query, region="ca-en", safesearch="moderate", max_results=max_results)
        return results if results else []
    except Exception as e:
        print(f"Search Error: {e}")
        return []

def find_official_form(form_name: str, jurisdiction: str = "Ontario") -> str:
    """
    Finds a direct PDF link to an official legal form.
    """
    # 1. Hardcoded Common Forms (The "Happy Path")
    COMMON_FORMS = {
        "n12": "https://tribunalsontario.ca/documents/ltb/Notices%20of%20Termination%20&%20Instructions/N12.pdf",
        "n9": "https://tribunalsontario.ca/documents/ltb/Notices%20of%20Termination%20&%20Instructions/N9.pdf",
        "n11": "https://tribunalsontario.ca/documents/ltb/Other%20Forms/N11.pdf",
        "l2": "https://tribunalsontario.ca/documents/ltb/Landlord%20Applications%20&%20Instructions/L2.pdf",
        "divorce": "https://ontariocourtforms.on.ca/en/family-law-rules-forms/8a-application-divorce/",
        "t1": "https://www.canada.ca/en/revenue-agency/services/forms-publications/tax-packages-years/general-income-tax-benefit-package/ontario/5006-r.html"
    }
    
    # Normalize input
    normalized_input = form_name.lower().strip()
    
    # Fuzzy match: Check if any known form key is present in the input string
    # e.g. Input "N12 form for Ontario" contains "n12" -> Match
    for key, url in COMMON_FORMS.items():
        if key in normalized_input:
             return f"Found official form (Verified): [{key.upper()}]({url})"

    # 2. Try Direct PDF Search (Dynamic)
    domains = "site:ontario.ca OR site:tribunalsontario.ca OR site:court.ca OR site:canada.ca"
    search_query_pdf = f"{form_name} form filetype:pdf {domains}"
    
    print(f"SEARCHING FORM (PDF): {search_query_pdf}")
    results = safe_search(search_query_pdf, max_results=3)
    if results:
        top_hit = results[0]
        return f"Found official form (PDF): [{top_hit['title']}]({top_hit['href']})"
    
    # 3. Fallback: Landing Page
    search_query_general = f"{form_name} form official {domains}"
    results_general = safe_search(search_query_general, max_results=3)
    if results_general:
        top_hit = results_general[0]
        return f"Found official form page: [{top_hit['title']}]({top_hit['href']})"

    return f"Could not find an official online version of form '{form_name}'. Please visit specific government service centers."

def find_lawyer_referral(location: str, issue_type: str) -> str:
    """
    Finds lawyers or referral services. 
    Now includes broader searches for 'top rated' context to give user options.
    Also generates LSO Deep Links for Ontario cities.
    """
    links = []
    
    # 1. LSO Deep Link (Ontario Specific)
    # URL Pattern: https://lso.ca/public-resources/finding-a-lawyer-or-paralegal/directory-search/results?fc=membercitynormalized%7CHamilton
    city = location.split(",")[0].strip().title()
    # Basic check if it likely is an Ontario city (or passed as such)
    # We'll just generate the link if it looks like a city name
    if len(city) > 2 and "Ontario" in location:
        lso_url = f"https://lso.ca/public-resources/finding-a-lawyer-or-paralegal/directory-search/results?fc=membercitynormalized%7C{city}"
        links.append(f"- [LSO Directory for {city}]({lso_url}) (Official)")

    # 2. Official Referral Services (Search Backup)
    referral_query = f"law society referral service {location}"
    referral_results = safe_search(referral_query, max_results=2)
    
    if referral_results:
        for res in referral_results:
            # Avoid duplicating the main LSO link if possible, but safe search results vary
            links.append(f"- [{res['title']}]({res['href']})")
            
    # 3. Broader Directory/Firm Search (User Requested)
    commercial_query = f"top rated {issue_type} lawyers in {location} directory"
    comm_results = safe_search(commercial_query, max_results=2)
    
    if comm_results:
        for res in comm_results:
            links.append(f"- [Search Result: {res['title']}]({res['href']})")
            
    if links:
        return "Here are the best resources to find representation:\n" + "\n".join(links)
            
    return "I couldn't find specific lawyer results. Please try a broader Google search."
