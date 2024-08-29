import unittest
from unittest.mock import patch, Mock
from src.ingest_data import fetch_data
from tests.test_utils import read_json


class TestIngestData(unittest.TestCase):
    BASE_URL = "BASE_URL"

    def create_mock_response(self, body):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'body': body}
        return mock_response

    @patch('src.ingest_data.requests.get')
    def test_fetch_data_success(self, mock_get):
        test_data = read_json('test_data.json')
        body_page_1 = test_data['page_1']
        body_page_2 = test_data['page_2']

        mock_response_page_1 = self.create_mock_response(body_page_1)
        mock_response_page_2 = self.create_mock_response(body_page_2)

        mock_get.side_effect = [mock_response_page_1, mock_response_page_2]

        result = fetch_data(self.BASE_URL)

        expected_result = body_page_1['data'] + body_page_2['data']
        self.assertEqual(result, expected_result)

    @patch('src.ingest_data.requests.get')
    def test_fetch_data_failure(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 500
        mock_get.return_value = mock_response

        result = fetch_data(self.BASE_URL)

        self.assertEqual(result, [])


if __name__ == '__main__':
    unittest.main()
