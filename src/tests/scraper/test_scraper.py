import pytest
from src.scraper.strategies.bfsp_request import BfspRequestScraper
from src.scraper.dowloader import DownloaderHelper
from src.config import Config

# HTML de prueba simulado
sample_html = '''
<html>
<head><title>Test Movie</title></head>
<body>
    <script type="application/ld+json">
    {
        "@context": "http://schema.org",
        "@type": "Movie",
        "name": "Test Movie",
        "aggregateRating": {
            "@type": "AggregateRating",
            "ratingValue": "8.1"
        }
    }
    </script>
    <span class="metacritic-score-box">87</span>
</body>
</html>
'''

def test_bfsp_request_scraper(mocker):
   
    mocker.patch('src.scraper.dowloader.DownloaderHelper.get_html', return_value=sample_html)
    
    
    strategy = BfspRequestScraper(downloader=DownloaderHelper(config=Config()))
    
   
    json_data = strategy.get_data("http://example.com")
    
   
    assert json_data is not None
    assert json_data["name"] == "Test Movie"
    assert json_data["aggregateRating"]["ratingValue"] == "8.1"
