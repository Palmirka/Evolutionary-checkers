import numpy as np
import random
from typing import Tuple


class Selection:
    """Class of all available selection functions"""

    @staticmethod
    def tournament(population_pawns: np.ndarray, population_kings: np.ndarray, values: np.ndarray,
                   selected_size: int, tournament_size: int) -> Tuple[np.ndarray, np.ndarray]:
        """Draw individuals to take part in tournaments, all tournament winners are returned"""

        selected_values = np.empty(selected_size, float)
        selected_pawns = np.empty((selected_size, population_pawns.shape[1]))
        selected_kings = np.empty((selected_size, population_kings.shape[1]))
        for i in range(selected_size):
            indices = np.random.randint(0, population_pawns.shape[0], tournament_size)
            tournament_pawns, tournament_kings, t_values = population_pawns[indices], population_kings[indices], values[indices]
            winner_index = np.argmax(t_values)
            winner_pawns, winner_kings = tournament_pawns[winner_index], tournament_kings[winner_index]
            selected_pawns[i], selected_kings[i] = winner_pawns, winner_kings
            selected_values[i] = max(t_values)
        # print('Old values: ', sum(values))
        # print('New values: ', sum(selected_values))
        return selected_pawns, selected_kings

    @staticmethod
    def replacement(population_pawns: np.ndarray, population_kings: np.ndarray, population_diff: np.ndarray,
                    mutated_pawns: np.ndarray, mutated_kings: np.ndarray, mutated_diff: np.ndarray, values: np.ndarray, mutated_values: np.ndarray):
        mask = values > mutated_values
        selected_pawns = np.empty_like(population_pawns)
        selected_kings = np.empty_like(population_kings)
        selected_diff = np.empty_like(population_diff)
        for idx in range(len(mask)):
            if mask[idx]:
                selected_pawns[idx] = population_pawns[idx]
                selected_kings[idx] = population_kings[idx]
                selected_diff[idx] = population_diff[idx]
            else:
                selected_pawns[idx] = mutated_pawns[idx]
                selected_kings[idx] = mutated_kings[idx]
                selected_diff[idx] = mutated_diff[idx]
        return selected_pawns, selected_kings, selected_diff
