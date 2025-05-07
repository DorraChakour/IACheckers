"""
Package ia contenant les différents algorithmes d'IA pour le jeu de dames.
"""
from .naif import Naif
from .minimax import Minimax
from .minimax_alpha_beta import MinimaxAlphaBeta

__all__ = ['Naif', 'Minimax', 'MinimaxAlphaBeta'] 