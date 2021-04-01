from menu.base_menu import BaseMenu
from models import Storage, connection_db
from utils import get_option_input
from exceptions import UserInputOptionException
import random
import json

class TestMenu(BaseMenu):
    header = '---------- Test Menu ----------'
    options = "[1] - Restart test\n[2] - Back"
    next_menus = ('1', '2')
    

    def test(self, storage):
        storage = Storage()
        connection = connection_db()
        questions = storage.questions.copy()
        questions = [
            question
            for question in questions
            if len(question.answers) != 0
        ]

        test_questions_number = storage.test_questions_number

        random.shuffle(questions)
        test_questions = questions[:test_questions_number]
        score = 0
        total = test_questions_number

        for question in test_questions:
            ques_id = question.id
            print(question.text)
            user_answ = input("Your answer: ").lower()

            if user_answ in question.answers:
                question.stat_cor += 1
                score += 1
                try:
                    with connection.cursor() as cursor:
                        for question in storage.questions:
                            quer = f'UPDATE questions SET stat_cor=stat_cor+1 WHERE id={ques_id};'
                            
                        cursor.execute(quer)
                        connection.commit()
                        storage.fill_storage()

                except FileNotFoundError:
                    print("No requested file 'questions.json'!")

            else:
                question.stat_wrg += 1
                try:
                    with connection.cursor() as cursor:
                        for question in storage.questions:
                            quer = f'UPDATE questions SET stat_wrg=stat_wrg+1 WHERE id={ques_id};'

                        cursor.execute(quer)
                        connection.commit()
                        storage.fill_storage()

                except FileNotFoundError:
                    print("No requested file 'questions.json'!")

        print('Test finished!')
        print(f'You scored {score} points out of {total}!')            


    def show(self):
        print(self.header)
        
        storage = Storage()
        input_func = get_option_input()
            
        def get_input():
            selected_option = input_func('Enter option: ')
            if selected_option not in self.next_menus:
                raise UserInputOptionException
            return selected_option
        
        while True:
            print('Starting test...')
            self.test(storage)

            print(self.options)

            selected_option = self.input_secure_wrap(get_input)

            if selected_option == '2':
                break