#include "minimax.h"
#include "score.cpp"
#include <iostream>
#include <algorithm>
#include <set>
#include <float.h> 
#include <bitset>
#include <cmath>  
#include <numeric> 
#include <random>  
#include <iterator>  

std::vector<double> Minimax::softmax(const std::vector<double>& values, double temperature) {
    std::vector<double> exp_values(values.size());

    double max_value = *std::max_element(values.begin(), values.end());
    std::transform(values.begin(), values.end(), exp_values.begin(),
                   [max_value, temperature](double value) {
                       return std::exp((value - max_value) / temperature);
                   });
    
    double sum_exp_values = std::accumulate(exp_values.begin(), exp_values.end(), 0.0);
    std::transform(exp_values.begin(), exp_values.end(), exp_values.begin(),
                   [sum_exp_values](double exp_value) { return exp_value / sum_exp_values; });

    
    return exp_values;
}

int Minimax::select_action(const std::vector<double>& probabilities) {
    std::uniform_real_distribution<> dis(0.0, 1.0);
    double random_value = dis(randengine);

    double cumulative_probability = 0.0;
    for (size_t i = 0; i < probabilities.size(); ++i) {
        cumulative_probability += probabilities[i];
        if (random_value <= cumulative_probability) {
            return i;
        }
    }
    return probabilities.size() - 1;
}


int Minimax::score(Engine e, Color color, Engine old)
{
    Score sc(e, color, old);
    return sc.score();
}


bool Minimax::randomTrueFalse()
{
    std::uniform_int_distribution<int> dist(0, 1);
    return dist(randengine);
}


Move Minimax::minimax_move(Engine e, int depth, Color color)
{
    MoveLists ml = e.legal_moves_lists(e);
    if(ml.size() == 0)
        return ml[0][0];
    
    int result = 0;
    SoftmaxPair values;
    bool maxi_player = true;
    Color start_color = color;

    if(e.turn == WHITE)
    {
        if (hashmap_white.find(e) != hashmap_white.end())
        {
            SoftmaxPair id_probs_pair = hashmap_white[e];
            return ml[id_probs_pair.second[select_action(id_probs_pair.first)]][0];
        }
        result = rec(e, ml[0][0], start_color, depth, INT32_MIN, INT32_MAX, true, e, maxi_player, values);
        hashmap_white.insert({ e, values});
    }else
    {
        if (hashmap_black.find(e) != hashmap_black.end())
        {
            SoftmaxPair id_probs_pair = hashmap_black[e];
            return ml[id_probs_pair.second[select_action(id_probs_pair.first)]][0];
        }
        result = rec(e, ml[0][0], start_color, depth, INT32_MIN, INT32_MAX, true, e, maxi_player, values);
        hashmap_black.insert({ e, values});
    }
    return ml[result][0];
}



int Minimax::rec(Engine e, Move best_move, Color start_color, int depth, int alpha, int beta, bool root, Engine old, bool maxi, SoftmaxPair &values)
{
   if(depth <= 0 || e.isFinished() > -1)
    {
        return score(e, start_color, old);
    }
    std::vector<double> vals;
    std::vector<int>    indexes;
    if(maxi){
        int bestVal = INT32_MIN;
        MoveLists mlists = e.legal_moves_lists(e);
        int moves_size = mlists.size(); 
        for(int i =0; i< moves_size; i++){
            Engine copy_board = e;
            copy_board.act(mlists[i]);
            int value = rec(copy_board, best_move, start_color, depth-1, alpha, beta, false, e, !maxi, values);
            if(value > bestVal)
                bestVal = value;
                
            vals.push_back(value);
            indexes.push_back(i);
            alpha = std::max( alpha, bestVal);
            if(beta <= alpha)
                break;
        }
        if(root)
        {  
            std::vector<double> probabilities = softmax(vals, TEMPERATURE);
            values = std::make_pair(probabilities, indexes);
            return indexes[select_action(probabilities)];
        }
        return bestVal;
    }
    else{
        int bestVal = INT32_MAX;
        MoveLists mlists = e.legal_moves_lists(e);
        int moves_size = mlists.size(); 
        for(int i =0; i< moves_size; i++){
            Engine copy_board = e;
            copy_board.act(mlists[i]);
            int value = rec(copy_board, best_move, start_color, depth-1, alpha, beta, false, e, !maxi, values);
            if(value < bestVal)
                bestVal = value;

            vals.push_back(value);
            indexes.push_back(i);
            beta = std::min( beta, bestVal);
            if(beta <= alpha)
                break;
        }
        if(root)
        {
            std::vector<double> probabilities = softmax(vals, TEMPERATURE);
            values = std::make_pair(probabilities, indexes);
            return indexes[select_action(probabilities)];
        }
        return bestVal;
    } 
}