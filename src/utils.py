"""Utility functions for Gumtree scraper."""
import re
from urllib.parse import urlparse, parse_qs
from camoufox.async_api import AsyncCamoufox


def _parse_proxy(proxy_url):
    """Parse proxy URL into components."""
    if not proxy_url:
        return None
    
    parsed = urlparse(proxy_url)
    return {
        'server': f"{parsed.scheme}://{parsed.hostname}:{parsed.port}",
        'username': parsed.username,
        'password': parsed.password,
    }


async def _fetch(url, proxy_url=None, timeout=90000):
    """Fetch page using Camoufox with anti-detection."""
    proxy = _parse_proxy(proxy_url) if proxy_url else None
    
    async with AsyncCamoufox(
        headless=True,
        geoip=True,
        proxy=proxy,
    ) as browser:
        page = await browser.new_page()
        
        try:
            await page.goto(url, wait_until='networkidle', timeout=timeout)
            await page.wait_for_timeout(3000)  # Wait for dynamic content
            
            content = await page.content()
            
            if len(content) < 500:
                return None
                
            return content
            
        finally:
            await page.close()


def _build_search_url(search_query=None, category='all', location=None, price_min=None, price_max=None, sort_by='date'):
    """Build Gumtree search URL from parameters."""
    base_url = "https://www.gumtree.com"
    
    # Category mapping
    category_map = {
        'all': 'search',
        'cars': 'cars-vans-motorbikes/cars',
        'for-sale': 'for-sale',
        'property': 'property',
        'jobs': 'jobs',
        'services': 'services',
        'community': 'community',
    }
    
    path = category_map.get(category, 'search')
    
    # Build query parameters
    params = []
    if search_query:
        params.append(f"q={search_query.replace(' ', '+')}")
    
    if location:
        params.append(f"search_location={location.replace(' ', '+')}")
    
    if price_min is not None:
        params.append(f"price_from={price_min}")
    
    if price_max is not None:
        params.append(f"price_to={price_max}")
    
    # Sort mapping
    sort_map = {
        'date': 'date',
        'price_asc': 'price_asc',
        'price_desc': 'price_desc',
        'distance': 'distance',
    }
    sort_param = sort_map.get(sort_by, 'date')
    params.append(f"sort={sort_param}")
    
    query_string = '&'.join(params)
    
    return f"{base_url}/{path}?{query_string}" if query_string else f"{base_url}/{path}"
