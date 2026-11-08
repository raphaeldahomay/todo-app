import unittest
from app.db import get_db_connection



class TestDatabaseConnection(unittest.TestCase):

    def test_connection(self):
        with get_db_connection() as conn:
            self.assertFalse(conn.closed)

    def test_query_execution(self):
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("select 1 as figure")
                
                # this helps us to also retrieve column names
                columns = [col.name for col in cur.description]
                result = cur.fetchone()

                self.assertEqual(result[0], 1)
                self.assertEqual(columns[0], 'figure')