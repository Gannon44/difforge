import cloudscraper
from bs4 import BeautifulSoup
import os
import logging


class AbfielderScraper:
    def __init__(self, base_url, output_dir, log_file="cloud_scraper.log"):
        self.base_url = base_url
        self.output_dir = output_dir
        self.visited_files = set()

        # Create a cloudscraper instance instead of requests session
        self.session = cloudscraper.create_scraper(
            browser={
                "browser": "chrome",
                "platform": "windows",
            }
        )

        # Setup logging
        logging.basicConfig(filename=log_file, level=logging.INFO, format="%(asctime)s - %(message)s")
        self.logger = logging.getLogger()

        # Ensure output directory exists
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    def scrape_page(self, page_number):
        """
        Scrape the main listing page for litematic links.
        """
        url = f"{self.base_url}/tags/House/{page_number}/popular"
        self.logger.info(f"Scraping page: {url}")

        response = self.session.get(url)
        if response.status_code != 200:
            self.logger.error(f"Failed to fetch page: {url} (Status Code: {response.status_code})")
            return

        soup = BeautifulSoup(response.text, "html.parser")
        item_divs = soup.find_all("div", class_="w3-col m6 l3")

        for item in item_divs:
            link = item.find("a", href=True)
            if link:
                detail_url = f"{self.base_url}/{link['href']}"
                self.scrape_detail_page(detail_url)

    def scrape_detail_page(self, detail_url):
        """
        Scrape the detail page to find and download the litematic file.
        """
        self.logger.info(f"Scraping detail page: {detail_url}")

        response = self.session.get(detail_url)
        if response.status_code != 200:
            self.logger.error(f"Failed to fetch detail page: {detail_url} (Status Code: {response.status_code})")
            return

        soup = BeautifulSoup(response.text, "html.parser")
        table = soup.find("table", class_="w3-table")
        if table:
            download_link = table.find("a", href=True, text="Download .Litematic")
            if download_link:
                file_url = f"{self.base_url}/{download_link['href']}"
                self.download_file(file_url)

    def download_file(self, file_url):
        """
        Download the litematic file and log it.
        """
        file_id = file_url.split("id=")[-1].split("&")[0]  # Extract unique ID from the URL
        if file_id in self.visited_files:
            self.logger.info(f"File already downloaded: {file_url}")
            return

        self.logger.info(f"Downloading file: {file_url}")

        response = self.session.get(file_url, stream=True)
        if response.status_code == 200:
            file_name = file_url.split("id=")[-1] + ".litematic"  # Create a file name from the URL
            file_path = os.path.join(self.output_dir, file_name)

            with open(file_path, "wb") as file:
                for chunk in response.iter_content(chunk_size=1024):
                    file.write(chunk)

            self.visited_files.add(file_id)
            self.logger.info(f"Downloaded: {file_path}")
        else:
            self.logger.error(f"Failed to download file: {file_url} (Status Code: {response.status_code})")

    def run(self, start_page=1, end_page=1):
        """
        Start the scraping process from the given range of pages.
        """
        for page in range(start_page, end_page + 1):
            self.scrape_page(page)


# Example usage:
if __name__ == "__main__":
    scraper = AbfielderScraper(
        base_url="https://abfielder.com/browse",
        output_dir="litematic_files"
    )
    scraper.run(start_page=1, end_page=2)  # Scrape pages 1 to 2