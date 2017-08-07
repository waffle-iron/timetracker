import pickle
import os

from gateway import DB_FILE_PATH
from gateway.utils import load_db_into_memory


class TestMethodLoadsDBFileContentsIntoMemory:

    def test_db_file_is_created_when_it_doesnt_exist(self):
        try:
            os.remove(DB_FILE_PATH)
        except FileNotFoundError:
            pass

        load_db_into_memory(DB_FILE_PATH)
        assert os.path.exists(DB_FILE_PATH)

    def test_empty_db_is_returned_when_nothing_has_been_saved_in_it_yet(self):
        db = load_db_into_memory(DB_FILE_PATH)
        assert db['activities'] == list()

    def test_db_content_is_returned_when_theres_something_in_it(self, test_activity):
        db = load_db_into_memory(DB_FILE_PATH)
        db['activities'] = [test_activity]
        with open(DB_FILE_PATH, 'wb') as fp:
            pickle.dump(db, fp)

        assert test_activity._id == load_db_into_memory(DB_FILE_PATH)['activities'][0]._id
