import requests
from typing import List, Dict

class DuckDuckGoSearch:
    """
    DuckDuckGo Search API Tool
    
    Example usage:
    searcher = DuckDuckGoSearch()
    results = searcher.search("Python programming", max_results=5)
    """
    
    def __init__(self):
        self.base_url = "https://api.duckduckgo.com/"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36",
            "Accept": "application/json"
        }
    
    def search(self, query: str, max_results: int = 5) -> List[Dict]:
        """
        Perform a DuckDuckGo search and return results
        
        Args:
            query: Search query string
            max_results: Maximum number of results to return
            
        Returns:
            List of dictionaries containing:
            [{"title": "Result title", "link": "URL", "snippet": "Description text"}]
        """
        params = {
            "q": query,
            "format": "json",
            "t": "ai_search_tool",
            "no_redirect": "1",
            "no_html": "1"
        }
        
        try:
            response = requests.get(
                self.base_url,
                params=params,
                headers=self.headers,
                timeout=10
            )
            response.raise_for_status()
            data = response.json()
            
            return self._parse_results(data, max_results)
            
        except requests.exceptions.RequestException as e:
            print(f"Search error: {e}")
            return []
    
    def _parse_results(self, data: dict, max_results: int) -> List[Dict]:
        """Parse and format search results from API response"""
        results = []
        
        # Get main topic if available
        if data.get("AbstractText"):
            results.append({
                "title": data.get("Heading", data.get("AbstractSource", "Main Result")),
                "link": data.get("AbstractURL", ""),
                "snippet": data.get("AbstractText", "")
            })
        
        # Add related topics
        for topic in data.get("RelatedTopics", [])[:max_results]:
            if "FirstURL" in topic and "Text" in topic:
                results.append({
                    "title": topic.get("Text").split(" —")[0],
                    "link": topic["FirstURL"],
                    "snippet": topic.get("Text", "")
                })
            elif "Topics" in topic:
                for sub_topic in topic["Topics"][:max_results]:
                    results.append({
                        "title": sub_topic.get("Text").split(" —")[0],
                        "link": sub_topic["FirstURL"],
                        "snippet": sub_topic.get("Text", "")
                    })
        
        # Deduplicate results
        seen = set()
        unique_results = []
        for r in results:
            if r["link"] not in seen:
                seen.add(r["link"])
                unique_results.append(r)
        
        return unique_results[:max_results]

if __name__ == "__main__":
    # Example usage
    search_tool = DuckDuckGoSearch()
    results = search_tool.search("Python programming", max_results=3)
    
    print("Search Results:")
    for i, result in enumerate(results, 1):
        print(f"\nResult {i}:")
        print(f"Title: {result['title']}")
        print(f"URL: {result['link']}")
        print(f"Description: {result['snippet']}")