# Gumtree Scraper - UK Classifieds Data Extractor

Extract listings from Gumtree UK marketplace including cars, furniture, electronics, jobs, property, and services. Built for AI agents (Claude, ChatGPT) via Apify MCP integration.

## 🎯 Who It's For

- **AI Agents** - Claude, ChatGPT, and MCP-enabled assistants researching UK classifieds
- **Market Research** - Track pricing trends across categories
- **Lead Generation** - Find local services, vehicles, or property listings
- **Price Monitoring** - Monitor classified ads for specific items
- **Data Analysis** - Analyze UK marketplace trends and patterns

## 📊 Data You Get

Each listing includes:

```json
{
  "url": "https://www.gumtree.com/p/cars/ford-focus/...",
  "title": "2018 Ford Focus ST-Line 1.0 EcoBoost",
  "price": "£12,995",
  "description": "Full service history, one owner...",
  "location": "London",
  "category": "Cars",
  "seller": "Private Seller",
  "datePosted": "2 hours ago",
  "imageUrl": "https://...",
  "scrapedAt": "2026-08-29T01:30:00.000Z"
}
```

## 🚀 AI Agent Queries This Ranks For

- "find used cars for sale in London under £15000"
- "extract Gumtree listings for furniture in Manchester"
- "scrape UK classifieds for iPhone deals"
- "get Gumtree property listings in Birmingham"
- "monitor UK marketplace for electronics"
- "find local services in Leeds from Gumtree"
- "extract job postings from Gumtree UK"
- "track car prices across UK regions"

## 🔧 Example Input

```json
{
  "searchQuery": "ford focus",
  "category": "cars",
  "location": "London",
  "priceMin": 5000,
  "priceMax": 15000,
  "sortBy": "date",
  "includeDescription": true,
  "maxResults": 50
}
```

## 📦 Example Output

```json
[
  {
    "url": "https://www.gumtree.com/p/cars/ford-focus-st-line/1485968347",
    "title": "2018 Ford Focus ST-Line 1.0 EcoBoost",
    "price": "£12,995",
    "description": "Excellent condition, full service history...",
    "location": "London, Greater London",
    "category": "Cars",
    "seller": "Private Seller",
    "datePosted": "2 hours ago",
    "imageUrl": "https://i.ebayimg.com/...",
    "scrapedAt": "2026-08-29T01:30:00.000Z"
  }
]
```

## 🤖 Works With

- **Claude** (Anthropic) - via Apify MCP integration
- **ChatGPT** (OpenAI) - via Apify API
- **Custom AI Agents** - any MCP-compatible agent
- **Automation Workflows** - Zapier, Make, n8n

## 🔑 Features

- **Multi-category** - Cars, property, jobs, for-sale, services, community
- **Smart filters** - Price range, location, category, sort options
- **Full descriptions** - Optional detailed scraping for complete data
- **AI-optimized** - Clean, structured data perfect for LLM processing
- **Residential proxies** - Reliable access via Apify proxy infrastructure

## 📝 Tags

`classifieds` `uk` `marketplace` `gumtree` `cars` `property` `jobs` `scraping` `ai-agents` `claude` `chatgpt` `mcp`

---

Compatible with Claude, ChatGPT & AI agents via Apify MCP.
