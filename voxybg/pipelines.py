from itemadapter import ItemAdapter
import sqlite3


class DatabasePipeline:
    # Database setup
    conn = sqlite3.connect('voxybg.db')
    c = conn.cursor()

    def open_spider(self, spider):
        self.c.execute(""" CREATE TABLE IF NOT EXISTS
                         articles (title text, date text, author text, link text, content text) """)

    def process_item(self, item, spider):
        # check for duplicates
        self.c.execute("""SELECT * FROM articles WHERE title = ? AND date = ?""",
                       (item.get('title')[0], item.get('date')[0],))
        duplicate = self.c.fetchall()
        if len(duplicate):
            return item

        # Insert values
        self.c.execute("INSERT INTO articles (title, date, author, link, content) VALUES (?,?,?,?,?)", (
            item.get('title')[0], item.get('date')[0], item.get('author')[0], item.get('link')[0],
            item.get('content')[0]))
        self.conn.commit()  # commit after every entry

        return item

    def close_spider(self, spider):
        self.conn.commit()
        self.conn.close()
