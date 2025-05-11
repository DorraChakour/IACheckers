"""
Package ia contenant les différents algorithmes d'IA pour le jeu de dames.
"""
from .naif import Naif
from .minimax_complexe import Minimax
from .alphabetaTest import MinimaxAlphaBetaTest

__all__ = ['Naif', 'Minimax', 'MinimaxAlphaBetaTest'] 