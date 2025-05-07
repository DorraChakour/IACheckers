class MinimaxAlphaBeta:
    def __init__(self, color, depth):
        """
        Initialise l'IA Minimax avec élagage alpha-beta avec une couleur (BLACK ou WHITE) et une profondeur de recherche
        """
        self.color = color
        self.depth = depth

    def get_move(self, board):
        """
        Retourne le meilleur mouvement selon l'algorithme Minimax avec élagage alpha-beta
        À implémenter
        """
        pass

    def minimax_alpha_beta(self, board, depth, alpha, beta, maximizing_player):
        """
        Implémentation de l'algorithme Minimax avec élagage alpha-beta
        À implémenter
        """
        pass

    def evaluate(self, board):
        """
        Fonction d'évaluation du plateau
        À implémenter
        """
        pass 