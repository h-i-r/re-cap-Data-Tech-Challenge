import unittest
from unittest.mock import mock_open, patch
from src.store_file import store_data
from tests.test_utils import read_json


class TestStoreData(unittest.TestCase):

    def test_store_data(self):
        test_data = read_json('test_data.json')['page_1']['data']

        with patch('builtins.open', new_callable=mock_open) as mock_file:
            store_data(test_data, 'test_file.csv')

            handle = mock_file()
            handle.write.assert_called()

            handle.write.assert_any_call('original_billing_amount,contract_id,invoice_id,invoice_date\r\n')
            handle.write.assert_any_call('500.0,'
                                         '00526b90f38d73b0138904f8df7353c456e28ae87fbe8956da14b24d28c674eb,'
                                         'aae0890f787eb93c07a7e01c260aa1094d6a2a28f72f055feb6d2de4b43ba340,'
                                         '2021-06-01\r\n')
            handle.write.assert_any_call('800.0,'
                                         '01966b88t38d73b0138904f8df7353c456e28ae87fbe8956da14b24d28c632hj,'
                                         'kkv7591f787eb93c07a7e01c260aa1094d6a2a28f72f055feb6d2de4b43fz601,'
                                         '2022-04-11\r\n')

if __name__ == '__main__':
    unittest.main()
