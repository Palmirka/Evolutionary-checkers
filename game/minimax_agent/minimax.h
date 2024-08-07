#ifndef MINIMAX_H
#define MINIMAX_H
// #include "engine.h"
#include "score.h"
#include <random>
#include <unordered_map>
#include <iostream>


using MovePair = std::pair<Move, int>;
using ListValPair = std::pair<int, int>;

template <int SIZE>
class CircularQueue {
private:
    ListValPair data[SIZE];
    int front; // Indeks początku kolejki
    int rear;  // Indeks końca kolejki
    int count; // Liczba elementów w kolejce
    int top_index; //id ostatnio dodanego elementu
    std::mt19937 gen;
    std::uniform_int_distribution<int> dis;

public:
    CircularQueue() : front(0), rear(0), count(0), top_index(0), dis(0, 99) {
        std::random_device rd;
        gen.seed(rd());
    }

    void enqueue(ListValPair value) {
        if (count == SIZE) {
            // Jeśli kolejka jest pełna, usuń pierwszy element
            dequeue();
        }
        // else
        //     top_index++;
        data[rear] = value;
        top_index = rear;
        rear = (rear + 1) % SIZE; // Ustaw nowy indeks końca kolejki
        count++;
    }

    void dequeue() {
        if (count > 0) {
            front = (front + 1) % SIZE; // Przesuń indeks początku kolejki
            count--;
        }
    }
    ListValPair last_added()
    {
        if(count == 0)
        {
            ListValPair t;
            return t;
        }else{
            return data[top_index];
        }
    }
    ListValPair pickRandom_with_weight()
    {
        if(count == 0)
        {
            ListValPair t;
            return t;
        }
        if(count == 1)
            return data[0];
        int roll = dis(gen);
        // int idx = 0;
        if(count == 2)
        {
            if(roll < 94)               // 94% to pick the best
                return data[top_index];
            return data[(top_index+1)%count];       // 6% to pick 2nd best
        }
        if(count == 3)
        {
            if(roll < 91)               // 91% to pick the best
                return data[top_index];
            else if(roll < 98)          // 7% to pick 2nd best
                return data[(top_index+2)%count];       
            return data[(top_index+1)%count];       // 2% to pick 3rd best
        }
        return data[top_index];
    }

    //std::pair<MoveList, int>;
    void clear_nagative_values()
    {
        if(count == 3){
            if(data[top_index].first<0)
            {
                data[0] = data[top_index];
                count = 1;
                front = 0;
                rear = 1;
                top_index = 0;
            }
            else
            {
                if(data[(top_index+2)%count].first<0)
                {
                    data[0] = data[top_index];
                    count = 1;
                    front = 0;
                    rear = 1;
                    top_index = 0;
                }
                else if(data[(top_index+1)%count].first<0)
                {
                    ListValPair tmp1 = data[top_index];
                    ListValPair tmp2 = data[(top_index+2)%count];
                    data[0] = tmp1;
                    data[1] = tmp2;
                    count = 2;
                    front = 1;
                    rear = 2;
                    top_index = 0;
                }
            }
        }
        else if(count == 2)
        {
            if(data[top_index].first<0)
            {
                data[0] = data[top_index];
                count = 1;
                front = 0;
                rear = 1;
                top_index = 0;
            }
            else
            {
                if(data[(top_index+1)%count].first<0)
                {
                    data[0] = data[top_index];
                    count = 1;
                    front = 0;
                    rear = 1;
                    top_index = 0;
                }
            }
        }
    }

    void print()
    {
        std::cout<<"====queue===="<<'\n';
        for(int i = 0; i<count; i++)
            std::cout<<"id: " << data[i].second<<" value: " << data[i].first<<'\n';
    }
};


class HashEngine {
public:
    size_t operator()(const Engine& p) const
    {
        return p.all();
    }
};

class Minimax {
    private:
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
    public: 
        std::unordered_map< Engine, Move, HashEngine> hashmap_white;
        std::unordered_map< Engine, Move, HashEngine> hashmap_black;
        std::unordered_map< Engine, CircularQueue<3>, HashEngine> hashmap_white1;
        std::unordered_map< Engine, CircularQueue<3>, HashEngine> hashmap_black1;
        Minimax() : randengine(std::random_device()())
        {
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
        // Move start(Engine e, int depth);
        // double minimax_continue(Engine e, bool maximizing, int depth, int alpha, int beta);

        int getHeuristic(Engine e, Color color);
        int score(Engine e, Color color, Engine old);
        // int score(Engine e, Color color, std::vector<int> startScore);

        // Move start(Engine &e, int depth);
        // MovePair recurse(Engine &e, int depth, bool max, Color color, int alpha, int beta, std::vector<int> _score);
        // MovePair recurse_start(Engine &e, int depth, bool max, Color color, int alpha, int beta, std::vector<int> _score);
        // MovePair evaluate_move(Engine &e, Move move, int depth, bool max, Color color, int alpha, int beta, std::vector<int> _score);
        std::vector<std::pair<Engine, Move>> all_possible_moves_outcomes(Engine e);
        std::vector<std::pair<Engine, Move>> all_possible_captures_outcomes(Engine e);

        //heuristics
        int adv(Engine e);
        int back(Engine e);
        int cent(Engine e);
        int centr(Engine e);
        int deny(Engine e);
        int kcent(Engine e);
        int mob(Engine e);
        int mobil(Engine e);
        int mov(Engine e);
        int thret(Engine e);
        int piece_score_diff(Engine e, Color color);
        int position_score(Engine e, Color color);

        Move minimax_move(Engine e, int depth, Color color);
        int rec(Engine e, Move start_move, Color start_color, int depth, int alpha, int beta, bool root, CircularQueue<3> &q, Engine old, bool maxi);
        
};



#endif