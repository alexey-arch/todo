from models.question import Question
import json 
import pymysql

def connection_db():
    connection = pymysql.connect(
        host='127.0.0.1',
        user='dbuser',
        password='Fks#23pq17%Dbvr',
        db='questions',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )
    return connection

class Storage:
    inst = None
    questions = None
    test_questions_number = None
    max_id = None


    @classmethod
    def __new__(cls, *args, **kwargs):
        if cls.inst is None:
            cls.inst = object.__new__(cls)
            cls.questions = []
            cls.test_questions_number = 0
            # cls.max_id = 0
        return cls.inst


    def fill_storage(self):
        connection = connection_db()
        try: 
            with connection.cursor() as cursor:
                test_questions_number = 0
                quest_data = []
                data = {}
                quer = 'SELECT * FROM questions;'
                cursor.execute(quer)

                for row in cursor:
                    test_questions_number += 1
                    key = row.keys()
                    val = row.values()
                    data = {k:v for (k,v) in zip(key, val)}
                    quest_data.append(data) 

            self.test_questions_number = test_questions_number
            self.questions = [
                Question.from_dict(question) 
                for question in quest_data
            ]
        except FileNotFoundError:
            print("No requested file 'questions.json'!")
        except KeyError:
            print('Invalid json. Requested format: { "questions": [], "test_questions_number" : <val>, "max_id" : <val> }')
        
        
    def fill_json(self):
        storage = Storage()
        connection = connection_db()
        try:
            with connection.cursor() as cursor:
                for question in storage.questions:
                    quer = f"INSERT INTO questions(text, answers, stat_cor, stat_wrg) VALUE (\'{question.text}\', \'{json.dumps(question.answers)}\', 0, 0);"

                cursor.execute(quer)
                connection.commit()
                storage.fill_storage()

        except FileNotFoundError:
            print("No requested file 'questions.json'!")
