import sqlite3
import os
from file_handler import FileHandler as FH

class DB:
    db_url: str
    table_name = "vocab"
    keys = ['source', 'translation', 'score']
    vocab_file: FH = FH("voc.txt")

    def __init__(self, db_url : str):
        self.db_url = db_url
        if not os.path.exists(self.db_url):
            #vocab_file = FH("voc.txt")
            self.__set_up_db()
            self.populate(self.vocab_file.get_voc_list())

    def __set_up_db(self) -> None:
        conn = sqlite3.connect(self.db_url)
        with open("setup.sql", "r") as file:
            script = file.read()
            conn.executescript(script)
            conn.commit()
        conn.close()

    def __call_db(self, query):
        conn = sqlite3.connect(self.db_url)
        cur = conn.cursor()
        res = cur.execute(query)
        data = res.fetchall()
        cur.close()
        conn.commit()
        conn.close()
        return data

    def populate(self, fields: list[str, str, int]):
        i = 0
        query = f"""
        INSERT INTO {self.table_name} (
        {"[{}], {}, {}".format(*self.keys)}
        ) VALUES 
           {"{}, {}, {}".format(*fields)}
        
        """
        print(query)
        self.__call_db(query)

    def fetch_table(self):
        query = f"""
        SELECT * FROM {self.table_name}
        """
        res = self.__call_db(query)
        return res

    def get_translation(self, word_to_translate: str):       
        query = f"""
        SELECT source, translation FROM {self.table_name} 
        WHERE source LIKE '%{word_to_translate}%'
        """
        data = self.__call_db(query)
        if not data:
            query = f"""
            SELECT translation, source FROM {self.table_name} 
            WHERE translation LIKE '%{word_to_translate}%'
            """
            print("NOT DATA")
            data = self.__call_db(query)
        return data

    def update(self, word_pair: tuple[str, str, str]):
        update_query = f"""
        UPDATE {self.table_name} SET score =  '{word_pair["score"]}', translation = '{word_pair["translation"]}' WHERE source = '{word_pair["source"]}' 
        """
        print(update_query)
        self.__call_db(update_query)

    

    def delete(self, word: str):
        update_query = f"""
        DELETE FROM {self.table_name} WHERE source LIKE '%{word}%' OR translation LIKE '%{word}%'
        """
        print(update_query)
        self.__call_db(update_query)

    def insert(self, word_pair: tuple[str, str]):
        if self.word_exist(word_pair["source"]):
            return False
        update_query = f"""
        INSERT INTO {self.table_name} 
        (
            {"[{}], {}, {}".format(*self.keys)}
        ) 
        VALUES 
        {word_pair["source"], word_pair["translation"], '0'}   
        
       """
        print(update_query)
        self.__call_db(update_query)
        return True

    def word_exist(self, item):
        vocabs = self.fetch_table()
        if vocabs:
            list_vocab = list(zip(*vocabs))
            if item in list_vocab[1]:
                return True
        return False

    def _save(self):
        vocabs = self.fetch_table()
        self.vocab_file.write_voc(vocabs)
        print (vocabs)
