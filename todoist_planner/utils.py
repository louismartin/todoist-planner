def ask_question(question, possible_answers):
    possible_answers_str = '/'.join(possible_answers)
    answer = input(f'{question} ({possible_answers_str}): ')
    if answer not in possible_answers:
        print(f'Incorrect answer, please answer with {possible_answers_str}.')
        ask_question(question, possible_answers)
    return answer
