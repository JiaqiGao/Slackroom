class Question:
    question = ""
    num_reactions = 0
    topic = ""

    def __init__(self, question, num_reactions):
        self.question = question
        self.num_reactions = num_reactions

    def update_reactions(self, count):
        self.num_reactions = count

class QuestionProcessor:
    questions = []
    place = 0

    def __init__(self):

    def sort_questions(self):
        self.questions = sorted(questions, cmp=lambda x,y: cmp(y.num_reactions, x.num_reactions))

    def top(self, amount):
        self.place = amount
        return questions[:amount]

    def next(self, amount):
        start = self.place
        self.place = end
        return questions[start:end]

    def add_question(self, question):
        questions.append(question)
