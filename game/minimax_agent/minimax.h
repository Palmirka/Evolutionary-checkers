#ifndef MINIMAX_H
#define MINIMAX_H

#include "score.h"
#include <random>
#include <unordered_map>
#include <iostream>
#include <tbb/concurrent_unordered_map.h>

using MovePair = std::pair<Move, int>;
using ListValPair = std::pair<int, int>;
using SoftmaxPair = std::pair<std::vector<double>, std::vector<int>>;

class HashEngine {
public:
    size_t operator()(const Engine& p) const
    {
        return p.all();
    }
};

class Minimax {
    public:
        std::mt19937 randengine;
        Bitboard center;
        Bitboard back_row_bridge_1;
        Bitboard back_row_bridge_2;
        Bitboard rows_3_and_4;
        Bitboard rows_5_and_6;
        Bitboard columns0246;
        Bitboard score1;
        Bitboard score2;
        Bitboard score3;
        Bitboard score4;
        std::vector<Bitboard> scores;
        double TEMPERATURE = 1.0;
    public: 
        tbb::concurrent_unordered_map< Engine, SoftmaxPair, HashEngine> hashmap_white;
        tbb::concurrent_unordered_map< Engine, SoftmaxPair, HashEngine> hashmap_black;
        Minimax(double temp = 1.0) : randengine(std::random_device()())
        {
            TEMPERATURE = temp;
            center = bitboard(18)|bitboard(20)|bitboard(27)|bitboard(29)|bitboard(34)| bitboard(36)| bitboard(43)| bitboard(45);
            back_row_bridge_1 = bitboard(57) | bitboard(59);
            back_row_bridge_2 = bitboard(5) | bitboard(6);
            columns0246 =  bitboard(0)|bitboard(16)|bitboard(32)|bitboard(48)|bitboard(2)|bitboard(18)|bitboard(34)|bitboard(50)|bitboard(4)|bitboard(20)|bitboard(36)|bitboard(52)|bitboard(6)|bitboard(22)|bitboard(38)|bitboard(54);
            score1 = bitboard(27) | bitboard(36);
            score2 = bitboard(18) | bitboard(20) | bitboard(29) | bitboard(34)| bitboard(43)| bitboard(45);
            score3 = bitboard(9) | bitboard(11) | bitboard(13) | bitboard(22)| bitboard(25)| bitboard(38)| bitboard(41) | bitboard(50) | bitboard(52)| bitboard(54);
            score4 = bitboard(0) | bitboard(2) | bitboard(4) | bitboard(6)| bitboard(15)| bitboard(16)| bitboard(31) | bitboard(32) | bitboard(47)| bitboard(48)| bitboard(57)| bitboard(59)| bitboard(61)| bitboard(63);
            scores = {score1, score2, score3, score4};
        }   
        bool randomTrueFalse();
        int score(Engine e, Color color, Engine old);

        Move minimax_move(Engine e, int depth, Color color);
        int rec(Engine e, Move start_move, Color start_color, int depth, int alpha, int beta, bool root, Engine old, bool maxi, SoftmaxPair &values);

        int select_action(const std::vector<double>& probabilities);
        std::vector<double> softmax(const std::vector<double>& values, double temperature = 1.0);
};



#endif