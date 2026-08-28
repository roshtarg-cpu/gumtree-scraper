"""Parser for extracting data from Gumtree HTML."""
import re
import json
from datetime import datetime


def _extract_listings(html):
    """Extract listing data from HTML using regex patterns."""
    listings = []
    
    # Try to find JSON data in script tags first
    # Gumtree may embed data in window objects or script tags
    json_match = re.search(r'window\.__GUMTREE_DATA__\s*=\s*({.*?});', html, re.S)
    if json_match:
        try:
            data = json.loads(json_match.group(1))
            # Extract from JSON if available
            if 'listings' in data:
                return data['listings']
        except:
            pass
    
    # Fallback: Parse HTML directly
    # Look for listing containers with regex
    # Pattern varies but typically includes data attributes or specific classes
    
    # Extract listings using article tags or similar containers
    article_pattern = r'<article[^>]*>(.*?)</article>'
    articles = re.findall(article_pattern, html, re.S)
    
    for article_html in articles:
        listing = _parse_listing_html(article_html)
        if listing:
            listings.append(listing)
    
    # Alternative: Look for structured link patterns
    if len(listings) == 0:
        link_pattern = r'<a[^>]*href="(/p/[^"]+)"[^>]*>(.*?)</a>'
        links = re.findall(link_pattern, html, re.S)
        
        for href, link_html in links[:50]:  # Limit to avoid pagination links
            listing = {
                'url': f"https://www.gumtree.com{href}",
                'title': _extract_text_from_html(link_html),
            }
            if listing['title']:
                listings.append(listing)
    
    return listings


def _parse_listing_html(html):
    """Parse individual listing from HTML fragment."""
    listing = {}
    
    # Title
    title_match = re.search(r'<h[23][^>]*>(.*?)</h[23]>', html, re.S)
    if title_match:
        listing['title'] = _extract_text_from_html(title_match.group(1))
    
    # Price
    price_match = re.search(r'£\s*([\d,]+(?:\.\d{2})?)', html)
    if price_match:
        listing['price'] = f"£{price_match.group(1)}"
    
    # URL
    url_match = re.search(r'href="(/p/[^"]+)"', html)
    if url_match:
        listing['url'] = f"https://www.gumtree.com{url_match.group(1)}"
    
    # Location
    location_match = re.search(r'location["\']?[^>]*>(.*?)</[^>]+>', html, re.I | re.S)
    if location_match:
        listing['location'] = _extract_text_from_html(location_match.group(1))
    
    # Date
    date_match = re.search(r'(\d{1,2}/\d{1,2}/\d{4}|\d+\s+(?:hour|day|week)s?\s+ago)', html, re.I)
    if date_match:
        listing['datePosted'] = date_match.group(1)
    
    # Only return if we got at least a URL or title
    return listing if (listing.get('url') or listing.get('title')) else None


def _extract_text_from_html(html):
    """Strip HTML tags and get clean text."""
    text = re.sub(r'<[^>]+>', ' ', html)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()


def _extract_listing_details(html):
    """Extract detailed information from individual listing page."""
    details = {}
    
    # Title
    title_match = re.search(r'<h1[^>]*>(.*?)</h1>', html, re.S)
    if title_match:
        details['title'] = _extract_text_from_html(title_match.group(1))
    
    # Price
    price_match = re.search(r'£\s*([\d,]+(?:\.\d{2})?)', html)
    if price_match:
        details['price'] = f"£{price_match.group(1)}"
    
    # Description
    desc_match = re.search(r'<div[^>]*class="[^"]*description[^"]*"[^>]*>(.*?)</div>', html, re.S | re.I)
    if desc_match:
        details['description'] = _extract_text_from_html(desc_match.group(1))
    
    # Location
    location_match = re.search(r'<span[^>]*class="[^"]*location[^"]*"[^>]*>(.*?)</span>', html, re.S | re.I)
    if location_match:
        details['location'] = _extract_text_from_html(location_match.group(1))
    
    # Category
    category_match = re.search(r'breadcrumb[^>]*>.*?<a[^>]*>(.*?)</a>', html, re.S | re.I)
    if category_match:
        details['category'] = _extract_text_from_html(category_match.group(1))
    
    # Seller
    seller_match = re.search(r'seller[^>]*>.*?<[^>]*>(.*?)</', html, re.S | re.I)
    if seller_match:
        details['seller'] = _extract_text_from_html(seller_match.group(1))
    
    # Image
    image_match = re.search(r'<img[^>]*src="([^"]*)"[^>]*class="[^"]*main[^"]*"', html, re.I)
    if not image_match:
        image_match = re.search(r'<img[^>]*src="(https://i\.ebayimg\.com/[^"]+)"', html)
    if image_match:
        details['imageUrl'] = image_match.group(1)
    
    return details
