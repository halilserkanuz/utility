import python.db as db, python.filesystem as fs

class TestUtility(object):
    fso = fs.FileSystemOps()
    dbo = db.DbOps("default_db")
    def test_config_file(self, db_type):
        config = self.fso.read_json_from_file('config.json')
        if db_type==config["db"]["db_type"]:
            print("DB type is correct")
        
        


if __name__ == "__main__":
    tu = TestUtility()
    tu.test_config_file("mysql")
    
