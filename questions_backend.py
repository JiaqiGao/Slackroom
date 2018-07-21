class Question:
    question = ""
    num_reactions = 0
    topic = ""

    def __init__(self, question, num_reactions):
        self.question = question
        self.num_reactions = num_reactions

    def update_reactions(count):
        self.num_reactions = count

class QuestionProcessor:
    questions = []
    place = 0

    def __init__(self, questions):
        self.questions = sort_questions(questions) 

    def sort_questions(questions):
        self.questions = sorted(questions, cmp=lambda x,y: cmp(y.num_reactions, x.num_reactions))

    def top(amount):
        self.place = amount
        return questions[:amount]

    def next(amount):
        start = self.place
        self.place = end
        return questions[start:end]
