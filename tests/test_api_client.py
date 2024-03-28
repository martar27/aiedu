import unittest
from unittest.mock import patch
from api.api_client import APIClient

class TestAPIClient(unittest.TestCase):
    @patch('api.api_client.openai.ChatCompletion.create')
    def test_ask_llm(self, mock_chat):
        mock_chat.return_value = {'choices': [{'message': {'content': 'Test response'}}]}
        
        client = APIClient()
        response = client.ask_llm("Test question")
        
        self.assertIsNotNone(response)
        self.assertEqual(response, {'choices': [{'message': {'content': 'Test response'}}]})
        mock_chat.assert_called_once()

if __name__ == '__main__':
    unittest.main()
