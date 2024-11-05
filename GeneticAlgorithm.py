#GeneticAlgorithm.py
class genom:

    genom_list = None
    evaluation = None
    show_results = False

    def __init__(self, genom_list, evaluation):
        self.genom_list = genom_list
        self.evaluation = evaluation


    def getGenom(self):
        return self.genom_list


    def getEvaluation(self):
        return self.evaluation

    def setGenom(self, genom_list):
        self.genom_list = genom_list


    def setEvaluation(self, evaluation):
        self.evaluation = evaluation

    def toggle_show_results(self):
        self.show_results = not self.show_results