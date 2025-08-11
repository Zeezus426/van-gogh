from qwen_agent.tools.base import BaseTool, register_tool
import requests
from typing import List, Dict

@register_tool('search')
class SearchTool(BaseTool):
    description = 'Search the web via DuckDuckGo Instant Answer API'
    parameters = [
        {
            'name': 'query',
            'type': 'string',
            'description': 'The search query',
            'required': True
        }
    ]

    def call(self, params: Dict, **kwargs) -> List[Dict]:
        """
        params may come in as either:
        1. {'query': 'some text'}  (dict)
        2. 'some text'             (raw string)
        """
        if isinstance(params, str):
            query = params
        else:
            query = params.get('query', '')

        url = "https://api.duckduckgo.com/"
        resp = requests.get(
            url,
            params={'q': query, 'format': 'json', 'no_html': 1},
            timeout=10
        )
        resp.raise_for_status()
        data = resp.json()

        # Return the list of related topics, each as a small dict
        results = []
        for item in data.get("RelatedTopics", []):
            if "Text" in item:
                results.append({"title": item.get("Text", ""), "url": item.get("FirstURL", "")})
        return results
    

if __name__ == "__main__":
    print(SearchTool().call({"query": "van gogh"}))