import unittest
from unittest.mock import patch, MagicMock, mock_open
import os
import sys
from download_file import download_file

sys.path.insert(0, '/Users/henry_zheng/python')


class TestDownloadFile(unittest.TestCase):


    @patch('download_file.requests.get')
    def test_download_file_success(self, mock_get):
        """Test successful file download"""
        mock_response = MagicMock()
        mock_response.iter_content.return_value = [b'test content']
        mock_get.return_value.__enter__.return_value = mock_response
        
        with patch('builtins.open', mock_open()):
            result = download_file('http://example.com/file.txt')
        
        self.assertTrue(result)
        mock_get.assert_called_once()

    @patch('download_file.requests.get')
    def test_download_file_url_parsing(self, mock_get):
        """Test filename extraction from URL"""
        mock_response = MagicMock()
        mock_response.iter_content.return_value = [b'content']
        mock_get.return_value.__enter__.return_value = mock_response
        
        with patch('builtins.open', mock_open()):
            download_file('http://example.com/path/myfile.pdf')
        
        mock_get.assert_called_once_with('http://example.com/path/myfile.pdf', stream=True)

    @patch('download_file.requests.get')
    def test_download_file_request_exception(self, mock_get):
        """Test handling of request exceptions"""
        mock_get.return_value.__enter__.side_effect = Exception('Connection error')
        
        result = download_file('http://invalid.com/file')
        
        self.assertFalse(result)

    @patch('download_file.requests.get')
    def test_download_file_with_custom_filename(self, mock_get):
        """Test download with custom filename"""
        mock_response = MagicMock()
        mock_response.iter_content.return_value = [b'content']
        mock_get.return_value.__enter__.return_value = mock_response
        
        with patch('builtins.open', mock_open()):
            download_file('http://example.com/file', local_filename='custom.txt')
        
        mock_get.assert_called_once()


if __name__ == '__main__':
    unittest.main()