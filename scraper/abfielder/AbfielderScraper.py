import cloudscraper
from bs4 import BeautifulSoup
import os
import logging
import re


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
                self.logger.info(f"Found detail URL: {detail_url}")
                self.scrape_detail_page(detail_url)

    def scrape_detail_page(self, detail_url):
        """
        Extract the ID from the detail URL and navigate to the download page.
        """
        self.logger.info(f"Scraping detail page: {detail_url}")

        # Extract the ID from the detail URL
        match = re.search(r"/(\d+)$", detail_url)
        if not match:
            self.logger.error(f"Could not extract ID from URL: {detail_url}")
            return

        schematic_id = match.group(1)
        download_page_url = f"https://abfielder.com/downloadSchematic?id={schematic_id}"
        self.logger.info(f"Constructed download page URL: {download_page_url}")
        self.download_file(download_page_url)

    def download_file(self, download_page_url):
        """
        Download the litematic or schem file from the download page.
        """
        self.logger.info(f"Scraping download page: {download_page_url}")

        response = self.session.get(download_page_url)
        if response.status_code != 200:
            self.logger.error(f"Failed to fetch download page: {download_page_url} (Status Code: {response.status_code})")
            return

        soup = BeautifulSoup(response.text, "html.parser")

        # Attempt to find the litematic link first
        download_link = soup.find("a", id="download_link", href=True)
        if download_link:
            file_url = f"https://abfielder.com/{download_link['href'].lstrip('../')}"
            file_name = os.path.basename(download_link['href'])
            self.save_file(file_url, file_name)
            return

        # If no litematic link, try the schem link
        download_link_schem = soup.find("a", id="download_link_schem", href=True)
        if download_link_schem:
            file_url = f"https://abfielder.com/{download_link_schem['href'].lstrip('../')}"
            file_name = os.path.basename(download_link_schem['href'])
            self.save_file(file_url, file_name)
            return

        self.logger.error(f"No valid download link found on page: {download_page_url}")

    def save_file(self, file_url, file_name):
        """
        Save the file from the given URL.
        """
        if file_name in self.visited_files:
            self.logger.info(f"File already downloaded: {file_url}")
            return

        self.logger.info(f"Downloading file: {file_url}")

        response = self.session.get(file_url, stream=True)
        if response.status_code == 200:
            file_path = os.path.join(self.output_dir, file_name)

            with open(file_path, "wb") as file:
                for chunk in response.iter_content(chunk_size=1024):
                    file.write(chunk)

            self.visited_files.add(file_name)
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