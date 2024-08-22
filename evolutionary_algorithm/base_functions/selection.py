import numpy as np
import random


class Selection:
    """Class of all available selection functions"""

    @staticmethod
    def tournament(population: np.ndarray, values: np.ndarray, selected_size: int, tournament_size: int) -> np.ndarray:
        """Draw individuals to take part in tournaments, all tournament winners are returned"""

        selected = np.empty((selected_size, population.shape[1], population.shape[2]))
        for i in range(selected_size):
            indices = [random.randint(0, population.shape[0]-1) for _ in range(tournament_size)]
            tournament, t_values = population[indices], values[indices]
            winner = tournament[np.argmax(t_values)]
            selected[i] = np.array(winner)
        return selected
