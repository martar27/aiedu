import unittest
from database.database_manager import DatabaseManager

class TestDatabaseManager(unittest.TestCase):
    def setUp(self):
        # Setup using an in-memory database for testing
        self.db_manager = DatabaseManager(':memory:')
        self.db_manager.create_connection()
        self.db_manager.initialize_schema()
    
    def test_log_input_to_database(self):
        self.db_manager.log_input_to_database(1, "Test input", False)
        # Add assertions to verify that the data was inserted correctly

    def tearDown(self):
        self.db_manager.close_connection()

if __name__ == '__main__':
    unittest.main()
