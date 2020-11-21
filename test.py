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
    



        

        if self.link_counter > 5000:
            for link in self.links:
                self.insert_link(*link)
            self.links = set()
            self.link_counter = 0
        
        sql = """
        INSERT INTO contenttransaction
        (link_hash, content_hash, is_active, created_at)
        SELECT '{0}', '{1}', true, now()
        FROM (SELECT '{1}') AS tmp
        WHERE NOT EXISTS (
                SELECT content_hash FROM contenttransaction
                WHERE link_hash = '{0}'
                order by id desc limit 1
        ) LIMIT 1;
        """.format(canonical_url_hash, content_hash)
        self.dbo.execute_sql(sql)

        if title:
            sql = """
            INSERT INTO tagtransaction
            (link_hash, tag, tag_content, is_active, created_at)
            SELECT '{0}', 'title', '{1}', true, now()
            FROM (SELECT '{1}') AS tmp
            WHERE NOT EXISTS (
                    SELECT tag_content
                    FROM tagtransaction
                    WHERE link_hash = '{0}' and tag='title'
                    order by id desc limit 1
            ) LIMIT 1;
            """.format(canonical_url_hash, title)
            self.dbo.execute_sql(sql)
        
        if h1:
            sql = """
            INSERT INTO tagtransaction
            (link_hash, tag, tag_content, is_active, created_at)
            SELECT '{0}', 'h1', '{1}', true, now()
            FROM (SELECT '{1}') AS tmp
            WHERE NOT EXISTS (
                    SELECT tag_content
                    FROM tagtransaction
                    WHERE link_hash = '{0}' and tag='h1'
                    order by id desc limit 1
            ) LIMIT 1;
            """.format(canonical_url_hash, h1)
            self.dbo.execute_sql(sql)

        if h2:
            sql = """
            INSERT INTO tagtransaction
            (link_hash, tag, tag_content, is_active, created_at)
            SELECT '{0}', 'h2', '{1}', true, now()
            FROM (SELECT '{1}') AS tmp
            WHERE NOT EXISTS (
                    SELECT tag_content
                    FROM tagtransaction
                    WHERE link_hash = '{0}' and tag='h2'
                    order by id desc limit 1
            ) LIMIT 1;
            """.format(canonical_url_hash, h2)
            self.dbo.execute_sql(sql)

        if h3:
            sql = """
            INSERT INTO tagtransaction
            (link_hash, tag, tag_content, is_active, created_at)
            SELECT '{0}', 'h3', '{1}', true, now()
            FROM (SELECT '{1}') AS tmp
            WHERE NOT EXISTS (
                    SELECT tag_content
                    FROM tagtransaction
                    WHERE link_hash = '{0}' and tag='h3'
                    order by id desc limit 1
            ) LIMIT 1;
            """.format(canonical_url_hash, h3)
            self.dbo.execute_sql(sql)

        if meta_description:
            sql = """
                INSERT INTO tagtransaction
                (link_hash, tag, tag_content, is_active, created_at)
                SELECT '{0}', 'meta description', '{1}', true, now()
                FROM (SELECT '{1}') AS tmp
                WHERE NOT EXISTS (
                    SELECT tag_content
                    FROM tagtransaction
                    WHERE link_hash = '{0}' and tag='meta description'
                    order by id desc limit 1
                ) LIMIT 1;
            """.format(canonical_url_hash, h3)
            self.dbo.execute_sql(sql)

        sql = """
        INSERT INTO linkstattransaction
        (link_hash, stat_name, value, is_active, created_at)
        SELECT '{0}', 'internal link count', {1}, true, now()
        FROM (SELECT {1}) AS tmp
        WHERE NOT EXISTS (
                SELECT value
                FROM linkstattransaction
                WHERE link_hash = '{0}' and stat_name='internal link count'
                order by id desc limit 1
        ) LIMIT 1;
        """.format(canonical_url_hash, internal_link_count)
        self.dbo.execute_sql(sql)

        sql = """
        INSERT INTO linkstattransaction
        (link_hash, stat_name, value, is_active, created_at)
        SELECT '{0}', 'external link count', {1}, true, now()
        FROM (SELECT {1}) AS tmp
        WHERE NOT EXISTS (
                SELECT value FROM linkstattransaction
                WHERE link_hash = '{0}' and stat_name='external link count'
                order by id desc limit 1
        ) LIMIT 1;
        """.format(canonical_url_hash, external_link_count)
        self.dbo.execute_sql(sql)

        sql = """
            INSERT INTO linkstattransaction
            (link_hash, stat_name, value, is_active, created_at)
            SELECT '{0}', 'status', '{1}', true, now()
            FROM (SELECT '{1}') AS tmp
            WHERE NOT EXISTS (
                SELECT value
                FROM linkstattransaction
                WHERE link_hash = '{0}' and stat_name='status'
                order by id desc limit 1
            ) LIMIT 1;
        """.format(canonical_url_hash, status)
        self.dbo.execute_sql(sql)
