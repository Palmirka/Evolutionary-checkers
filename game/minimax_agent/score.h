#ifndef SCORE_H
#define SCORE_H

#include "engine.h"
#include <set>

class Score {
    private:
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

        Engine e;
        Engine oppEngine;
        Engine old;
        Color scored_color;
        Color opposide_color;
        Color active;
        Color passive;
        MoveList legal_moves;
        MoveList opp_moves;
        std::set<int> unique_to_sq;
        MoveList unique_from_to_list;

    public:
        Score(Engine eng, Color _scored_color, Engine _old);

        //heuristics
        int adv();
        int back();
        int cent(Engine eng);
        int centr(Engine eng);
        int deny(Engine eng);
        int kcent(Engine eng);
        int mob(Engine eng);
        int mobil(Engine eng);
        int mov(Engine eng);
        int thret(Engine eng);
        int piece_score_diff();

        std::vector<std::pair<Engine, Move>> all_possible_moves_outcomes(Engine e);
        std::vector<std::pair<Engine, Move>> all_possible_captures_outcomes(Engine e);

        int score();
};



#endif