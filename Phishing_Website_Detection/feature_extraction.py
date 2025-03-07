import pandas as pd
import re
import tldextract
import requests
from urllib.parse import urlparse

def is_ip_address(domain):
    """Check if the domain is an IP address."""
    return 1 if re.match(r'^\d+\.\d+\.\d+\.\d+$', domain) else 0

def has_https(url):
    """Check if the URL uses HTTPS."""
    return 1 if url.startswith('https') else 0

def count_subdomains(domain):
    """Count the number of subdomains in a given domain."""
    return domain.count('.') - 1

def extract_features(url):
    """Extract required features from a given URL."""
    parsed_url = urlparse(url)
    domain_info = tldextract.extract(url)
    domain = domain_info.domain

    features = {
        'url_length': len(url),
        'num_dots': url.count('.'),
        'num_hyphens': url.count('-'),
        'num_slashes': url.count('/'),
        'num_digits': sum(c.isdigit() for c in url),
        'num_subdomains': count_subdomains(parsed_url.netloc),
        'has_https': has_https(url),
        'has_ip': is_ip_address(parsed_url.netloc),
        'suspicious_tld': 1 if domain_info.suffix in ["xyz", "top", "info"] else 0,
        'suspicious_words': 1 if any(word in url.lower() for word in ["login", "secure", "bank"]) else 0
    }
    
    return pd.DataFrame([features])
