"""Main actor entry point."""
import asyncio
import os
from datetime import datetime, timezone
from apify import Actor
from .utils import _fetch, _build_search_url
from .parser import _extract_listings, _extract_listing_details


async def main():
    """Main actor function."""
    async with Actor:
        # Get input
        actor_input = await Actor.get_input() or {}
        
        search_query = actor_input.get('searchQuery')
        category = actor_input.get('category', 'all')
        location = actor_input.get('location')
        price_min = actor_input.get('priceMin')
        price_max = actor_input.get('priceMax')
        sort_by = actor_input.get('sortBy', 'date')
        include_description = actor_input.get('includeDescription', True)
        max_results = actor_input.get('maxResults', 50)
        
        Actor.log.info(f'Starting Gumtree scraper with query: {search_query}, category: {category}, max: {max_results}')
        
        # Get proxy configuration
        proxy_config = actor_input.get('proxyConfiguration')
        proxy_url = None
        
        if proxy_config and proxy_config.get('useApifyProxy'):
            proxy_password = os.getenv('APIFY_PROXY_PASSWORD') or Actor.get_env().get('proxy_password')
            if proxy_password:
                groups = proxy_config.get('apifyProxyGroups', ['RESIDENTIAL'])
                group = groups[0] if groups else 'RESIDENTIAL'
                proxy_url = f"http://groups-{group}:{proxy_password}@proxy.apify.com:8000"
                Actor.log.info(f'Using Apify proxy: {group}')
        
        # Build search URL
        search_url = _build_search_url(
            search_query=search_query,
            category=category,
            location=location,
            price_min=price_min,
            price_max=price_max,
            sort_by=sort_by
        )
        
        Actor.log.info(f'Search URL: {search_url}')
        
        # Fetch search results
        item_count = 0
        request_count = 0
        error_count = 0
        
        try:
            Actor.log.info('Fetching search results page...')
            request_count += 1
            
            html = await _fetch(search_url, proxy_url=proxy_url, timeout=90000)
            
            if not html:
                Actor.log.error('Failed to fetch search page or response too small')
                error_count += 1
                await Actor.exit('Failed to fetch search results')
                return
            
            Actor.log.info(f'Received HTML response ({len(html)} bytes)')
            
            # Extract listings
            listings = _extract_listings(html)
            Actor.log.info(f'Found {len(listings)} listings')
            
            if len(listings) == 0:
                Actor.log.warning('No listings found - may need to adjust selectors')
                # Save HTML for debugging
                await Actor.set_value('DEBUG_HTML', html[:10000])
            
            # Process each listing
            for i, listing in enumerate(listings[:max_results], 1):
                try:
                    # If include_description is True, fetch full listing page
                    if include_description and listing.get('url'):
                        Actor.log.info(f'Fetching details for listing {i}/{min(len(listings), max_results)}: {listing.get("url")}')
                        
                        request_count += 1
                        detail_html = await _fetch(listing['url'], proxy_url=proxy_url, timeout=60000)
                        
                        if detail_html:
                            details = _extract_listing_details(detail_html)
                            # Merge details with listing
                            listing.update(details)
                        
                        # Rate limiting
                        await asyncio.sleep(2)
                    
                    # Add scraped timestamp
                    listing['scrapedAt'] = datetime.now(timezone.utc).isoformat()
                    
                    # Ensure all expected fields exist (null if missing)
                    for field in ['url', 'title', 'price', 'description', 'location', 'category', 'seller', 'datePosted', 'imageUrl']:
                        if field not in listing:
                            listing[field] = None
                    
                    # Push to dataset
                    await Actor.push_data(listing)
                    item_count += 1
                    
                    if item_count % 10 == 0:
                        Actor.log.info(f'Scraped {item_count} listings so far...')
                    
                    if item_count >= max_results:
                        break
                        
                except Exception as e:
                    Actor.log.error(f'Error processing listing {i}: {e}')
                    error_count += 1
                    continue
            
            Actor.log.info(f'✅ Scraping complete! Total items: {item_count}, Requests: {request_count}, Errors: {error_count}')
            
        except Exception as e:
            Actor.log.error(f'Fatal error: {e}')
            error_count += 1
            raise
        
        finally:
            # Save task context (MANDATORY)
            await Actor.set_value('SAVED-TASK', {
                'actorId': Actor.get_env().get('actor_id'),
                'actorRunId': Actor.get_env().get('actor_run_id'),
                'defaultDatasetId': Actor.get_env().get('default_dataset_id'),
                'startedAt': Actor.get_env().get('started_at'),
                'input': actor_input,
                'stats': {
                    'itemsScraped': item_count,
                    'requestsMade': request_count,
                    'errors': error_count,
                }
            })


if __name__ == '__main__':
    asyncio.run(main())
