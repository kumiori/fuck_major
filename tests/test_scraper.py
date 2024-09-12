# tests/test_scraper.py
import unittest
from fuck_major.scraper import scrape_journal, scrape_board

class TestScraper(unittest.TestCase):

    def test_scrape_journal(self):
        url = 'https://www.sciencedirect.com/journal/journal-of-the-mechanics-and-physics-of-solids'  # Example URL
        journal_data = scrape_journal(url)
        self.assertTrue(journal_data['title'], "The 'title' field should not be empty.")

    def test_board(self):
        url = 'https://www.sciencedirect.com/journal/journal-of-the-mechanics-and-physics-of-solids'  # Example URL
        board = scrape_board(url)
        contains_editor = any(member['role'] == 'Editor' for member in board)
        self.assertTrue(contains_editor, "The board should contain an 'Editor'.")

if __name__ == '__main__':
    unittest.main()