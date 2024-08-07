#include "minimax.h"
#include "score.cpp"
#include <iostream>
#include <algorithm>
#include <set>
#include <float.h> 
#include <bitset>

/* TODO - zamienić na int */
int Minimax::getHeuristic(Engine e, Color color) {
    // if(e.isFinished())
    //     return INT32_MAX; /* zamienić na int */
    
    // int king_weight = 3;
    // if (color == BLACK) {
    //     return (king_weight * e.count_kings(BLACK) + e.count_pawns(BLACK)*2) - (king_weight * e.count_kings(WHITE) + e.count_pawns(WHITE)*2);
    // }
    // // std::cout<<(king_weight * e.count_kings(WHITE) + e.count_pawns(WHITE)*2) - (king_weight * e.count_kings(BLACK) + e.count_pawns(BLACK)*2);
    // return (king_weight * e.count_kings(WHITE) + e.count_pawns(WHITE)*2) - (king_weight * e.count_kings(BLACK) + e.count_pawns(BLACK)*2);

    return 0;
}


// Move Minimax::start(Engine &e, int depth)
// {
//     // if(e.turn == WHITE)
//     // {
//     //     if (hashmap_white.find(e) != hashmap_white.end()) {
//     //         // std::cout<< "JEJ KORZYSTAM Z HASHA!!" << std::endl;
//     //         return hashmap_white[e];
//     //     }
//     //     else
//     //     {
//     //         int _deny = deny(e);
//     //         int _mob = mob(e);
//     //         std::vector<int> score = {adv(e), back(e), cent(e), centr(e), _deny, kcent(e), _mob, _mob-_deny, mov(e), thret(e)};
//     //         MovePair result = recurse_start(e, depth, true, e.turn, INT32_MIN, INT32_MAX,score);
//     //         hashmap_white.insert({ e, result.first});

//     //         // std::cout<<"minimax move result: " << result.second<<std::endl;
//     //         return result.first;
//     //     }
//     // }
//     // else if( e.turn == BLACK)
//     // {
//     //     if (hashmap_black.find(e) != hashmap_black.end()) {
//     //         // std::cout<< "JEJ KORZYSTAM Z HASHA!!" << std::endl;
//     //         return hashmap_black[e];
//     //     }
//     //     else
//     //     {
//             int _deny = deny(e);
//             int _mob = mob(e);
//             std::vector<int> score = {adv(e), back(e), cent(e), centr(e), _deny, kcent(e), _mob, _mob-_deny, mov(e), thret(e)};
//             MovePair result = recurse(e, depth, true, e.turn, INT32_MIN, INT32_MAX,score);
//             hashmap_black.insert({ e, result.first});


//             std::bitset<32> x(result.second);
//             if(e.turn == BLACK)
//                 std::cout << x << " - " << result.second << '\n';
//             // std::cout<<"minimax move result: " << result.second<<std::endl;
//             return result.first;
//     //     }
//     // }
//     return Move(0,0,0);
// }

int Minimax::score(Engine e, Color color, Engine old)
{
    // int finish = e.isFinished();
    // if(finish == color)
    //     return INT32_MAX;
    // else if(finish == ~color)
    //     return INT32_MIN;
    // else if(finish == 2) //draw
    //     return INT32_MIN+1;

    // // int _adv   = adv(e) - adv(old);
    // // int _back  = back(e) - back(old);
    // // int _cent  = cent(e) - cent(old);
    // // int _centr = centr(e) - centr(old);
    // // int _deny  = deny(e) - deny(old);
    // // int _kcent = kcent(e) - kcent(old);
    // // int _mob   = mob(e) - mob(old);
    // // int _mobil = _mob - _deny;
    // // int _mov   = mov(e) - mov(old);
    // // int _thret = thret(e) - thret(old);

    // int _adv   = adv(e);
    // int _back  = back(e);
    // int _cent  = cent(e);
    // int _centr = centr(e);
    // int _deny  = deny(e);
    // int _kcent = kcent(e);
    // int _mob   = mob(e);
    // int _mobil = _mob - _deny;
    // int _mov   = mov(e);
    // int _thret = thret(e);
    
    // // std::cout<<std::to_string(e.turn);
    // int even = (e.turn == color) ? 1 : 1;
    // bool undenied_mobility= even*_mobil > 0 ? 1 : 0;
    // bool total_mobility   = even*_mob > 0 ? 1 : 0;
    // bool denial_of_cc     = even*_deny > 0 ? 1 : 0;
    // bool control          = even*_cent > 0 ? 1 : 0;

    // int _demmo  = denial_of_cc && !(total_mobility) ? 1 : 0;
    // int _mode_2 = undenied_mobility && !(denial_of_cc) ? 1 : 0;
    // int _mode_3 = !(undenied_mobility) && denial_of_cc ? 1 : 0;
    // int _moc_2  = !(undenied_mobility) && control ? 1 : 0;
    // int _moc_3  = (undenied_mobility) && !(control) ? 1 : 0;
    // int _moc_4  = !(undenied_mobility) && !(control) ? 1 : 0;

    // int sign = (e.turn == color) ? 1 : 0;
    // int board_score = 0
    //                 // + sign*_moc_2*(-1)*(1<<18)  
    //                 + sign*_kcent*(1<<16) //checked
    //                 // + sign*_moc_4*(-1)*(1<<14)  
    //                 // + sign*_mode_3*(-1)*(1<<13) 
    //                 // + sign*_demmo*(-1)*(1<<11)  
    //                 // + sign*_mov*(1<<8)          
    //                 // + sign*_adv*(-1)*(1<<8)     ////
    //                 // + sign*_mode_2*(-1)*(1<<8)  
    //                 // + sign*_back*(-1)*(1<<6)    
    //                 + sign*_centr*(1<<5) //checked         
    //                 // + sign*_thret*(1<<5)        
    //                 // + sign*_moc_3*(1<<4)        
    //                 + piece_score_diff(e, color)*(1<<19)
    //                 // + position_score(e, color)*(1<<14)
    //                 ;

    // return board_score; 
    Score sc(e, color, old);
    return sc.score();
}

// MovePair Minimax::recurse(Engine &e, int depth, bool max, Color color, int alpha, int beta, std::vector<int> _score)
// {
//     if(depth <= 0 || e.isFinished() >= 0)
//     {
//         // int value = score(e, color, _score);
//         return MovePair({0,0,0}, score(e, color));
//         // return MovePair({0,0,0}, getHeuristic(e, color));
//     }

//     Engine tempEngine;
//     // if(max)
//     if(e.turn == color)
//     {
//         MoveList moves = e.legal_moves();
//         MovePair best_move = MovePair({0,0,0}, INT32_MIN);
//         MovePair result;
//         int n_moves = moves.size();
//         for(int i=0; i<n_moves; i++)
//         {
//             // tempEngine = *e.clone();
//             tempEngine = e;
//             result = evaluate_move(tempEngine, moves[i], depth-1, false, color, alpha, beta, _score);
//             if(result.second == best_move.second && randomTrueFalse())
//                 best_move = result;
//             else if(result.second > best_move.second)
//             {
//                 best_move = result;
//                 // std::cout<<result.second<<std::endl;
//             }
            
//             alpha = std::max(alpha, best_move.second);
//             if(beta <= alpha)
//                 break;
//         }
//         if(best_move.first.from == 0 && best_move.first.to == 0 && best_move.first.type == 0)
//             return {e.legal_moves()[0], INT32_MIN};
//         return best_move;
//     }
//     else
//     {
//         MoveList moves = e.legal_moves();
//         MovePair best_move = MovePair({0,0,0}, INT32_MAX);
//         MovePair result;
//         int n_moves = moves.size();
//         for(int i=0; i<n_moves; i++)
//         {
//             // tempEngine = *e.clone();
//             tempEngine = e;
//             result = evaluate_move(tempEngine, moves[i], depth-1, true, color, alpha, beta, _score);
//             if(result.second < best_move.second)
//                 best_move = result;
//             else if(result.second == best_move.second && randomTrueFalse())
//                 best_move = result;

//             beta = std::min(beta, best_move.second);
//             if (beta <= alpha)
//                 break;
//         }    
//         // return queue.pickRandom_with_weight();
//         if(best_move.first.from == 0 && best_move.first.to == 0 && best_move.first.type == 0)
//             return {e.legal_moves()[0], INT32_MAX};
//         return best_move;
//         // return queue.last();
//     }
// }

// MovePair Minimax::recurse_start(Engine &e, int depth, bool max, Color color, int alpha, int beta, std::vector<int> _score)
// {
//     if(depth <= 0 || e.isFinished() >= 0)
//     {
//         // int value = score(e, color, _score);
//         return MovePair({0,0,0}, score(e, color));
//         // return MovePair({0,0,0}, getHeuristic(e, color));
//     }

//     Engine tempEngine;
//     // if(max)
//     if(e.turn == color)
//     {
//         MoveList moves = e.legal_moves();
//         MovePair best_move = MovePair({0,0,0}, INT32_MIN);
//         MovePair result;
//         CircularQueue<MovePair, 3> queue;
//         int n_moves = moves.size();
//         for(int i=0; i<n_moves; i++)
//         {
//             // tempEngine = *e.clone();
//             tempEngine = e;
//             result = evaluate_move(tempEngine, moves[i], depth-1, false, color, alpha, beta, _score);
//             if(result.second == best_move.second)
//             {
//                 best_move = result;
//                 queue.enqueue(result);
//             }
//             else if(result.second > best_move.second)
//             {
//                 best_move = result;
//                 queue.enqueue(result);
//             }
//             alpha = std::max(alpha, best_move.second);
//             if(beta <= alpha)
//                 break;
//         }
//         return queue.pickRandom_with_weight();
//     }
//     else
//     {
//         MoveList moves = e.legal_moves();
//         MovePair best_move = MovePair({0,0,0}, INT32_MAX);
//         MovePair result;
//         CircularQueue<MovePair, 3> queue;
//         int n_moves = moves.size();
//         for(int i=0; i<n_moves; i++)
//         {
//             // tempEngine = *e.clone();
//             tempEngine = e;
//             result = evaluate_move(tempEngine, moves[i], depth-1, true, color, alpha, beta, _score);
//             if(result.second < best_move.second)
//             {
//                 best_move = result;
//                 queue.enqueue(result);
//             }
//             else if(result.second == best_move.second)
//             {
//                 best_move = result;
//                 queue.enqueue(result);
//             }
//             beta = std::min(beta, best_move.second);
//             if (beta <= alpha)
//                 break;
//         }    
//         return queue.pickRandom_with_weight();
//     }
// }

// MovePair Minimax::evaluate_move(Engine &e, Move move, int depth, bool max, Color color, int alpha, int beta, std::vector<int> _score)
// {
//     Color color_before_move = e.turn;
//     e.act(move);
//     Color color_after_move = e.turn;
//     MovePair result;
//     // std::cout<<(color_before_move != color_after_move);
//     // if(color_before_move != color_after_move)
//     result = recurse(e, depth, max, color, alpha, beta, _score);
//     // else
//     //     result = recurse(e, depth+1, !max, color, alpha, beta, _score);
//     result.first = move;
//     return result;
// }

bool Minimax::randomTrueFalse()
{
    std::uniform_int_distribution<int> dist(0, 1);
    return dist(randengine);
}

/*  The parameter is credited with 1 for each passive man in the
    fifth and sixth rows (counting in passive's direction) and
    debited with 1 for each passive man in the third and fourth
    rows.*/
int Minimax::adv(Engine e)
{
    Color passive = ~e.turn;
    Bitboard rows_5_and_6 = 0x00000000'AA550000;
    Bitboard rows_3_and_4 = 0x0000AA55'00000000;
    if(passive == WHITE)
    {
        Bitboard tmp = rows_5_and_6;
        rows_5_and_6 = rows_3_and_4;
        rows_3_and_4 = tmp;
    }

    Bitboard bits_3_and_4 = rows_3_and_4 & e.pieces[passive];
    Bitboard bits_5_and_6 = rows_5_and_6 & e.pieces[passive];
    return e.count_bits(bits_5_and_6) - e.count_bits(bits_3_and_4);
}

/*  The parameter is credited with 1 if there are no active kings
    on the board and if the two bridge squares (1 and 3, or 30 and
    32) in the back row are occupied by passive pieces.*/
int Minimax::back(Engine e)
{
    Color active = e.turn;
    Color passive = ~e.turn;
    Bitboard back_row_bridge;
    if (active == WHITE){
        if ((e.pieces[WHITE] & e.kings) != 0)
            return 0;
        back_row_bridge = back_row_bridge_1;
    }
    else{
        if ((e.pieces[BLACK] & e.kings) != 0)
            return 0;
        back_row_bridge = back_row_bridge_2;
    }
    if (e.count_bits(back_row_bridge & e.pieces[passive]) == 2)
        return 1;
    return 0;
}

/*  The parameter is credited with 1 for each of the following
    squares: 11, 12, 15, 16, 20, 21, 24, 25 which is occupied by
    a passive man.*/
int Minimax::cent(Engine e)
{
    Color passive = ~e.turn;
    return e.count_bits(center & e.pieces[passive]);
}

/*  The parameter is credited with 1 for each of the following
    squares: 11, 12, 15, 16, 20, 21, 24, 25 that is either
    currently occupied by an active piece or to which an active
    piece can move.*/
int Minimax::centr(Engine e)
{
    std::vector<int> center_sq = {18,20,27,29,34,36,43,45};
    std::set<Square> unique;
    // Color passive = ~e.turn;
    // Bitboard center = 0x00001428'14280000;
    // int center_man = e.count_bits(center & e.pieces[e.turn]);
    MoveList moves = e.legal_moves();
    // int can_canter = 0;
    Color active = e.turn;
    int from_moves = e.count_bits(center & e.pieces[active]);
    Bitboard to_mask=0;
    for(Move move : moves)
    {
        // if(std::find(center_sq.begin(), center_sq.end(), move.from) != center_sq.end()) {
        //     unique.insert(move.from);
        // }
        // if(std::find(center_sq.begin(), center_sq.end(), move.to) != center_sq.end()) {
        //     unique.insert(move.to);
        // }
        to_mask |= bitboard(move.to);
    }
    int to_moves = e.count_bits(center & to_mask);
    // return unique.size();
    return from_moves+to_moves;

}

/*  The parameter is credited with 1 for each square to which the
    active side could move one or more pieces in the normal fashion
    disregarding the fact that jump moves may or may not be
    available.*/
int Minimax::mob(Engine e)
{
    std::set<int> unique;
    for (const auto from : BitIterator(e.pieces[e.turn] & e.kings))
        for (const auto to : BitIterator(e.king_moves(from)))
            unique.insert(to);
    for (const auto from : BitIterator(e.pieces[e.turn] & ~e.kings))
        for (const auto to : BitIterator(e.man_moves(from)))
            unique.insert(to);


    return unique.size();
}

/*  The parameter is credited with 1 for each square defined
    in MOB if on the next move a piece occupying this
    square could be captured without an exchange.*/
int Minimax::deny(Engine e)
{
    // int result = 0;
    //wykonaj ruch z MOB
    // Color start_color = e.turn;

    MoveList list;
    for (const auto from : BitIterator(e.pieces[e.turn] & e.kings))
        for (const auto to : BitIterator(e.king_moves(from)))
            list.emplace_back(Move(Square(from), Square(to), QUIET));
    for (const auto from : BitIterator(e.pieces[e.turn] & ~e.kings))
        for (const auto to : BitIterator(e.man_moves(from)))
            list.emplace_back(Move(Square(from), Square(to), bitboard(to) & OPPOSITE_RANK[e.turn] ? PROMOTION : QUIET));

    std::set<Square> denials;
    // ruch z MOB
    for(Move move_MOB : list)
    {   
        // Square move = move_MOB.from;
        Square dest = move_MOB.to;
        // Engine tmpEngine = *e.clone();
        Engine tmpEngine = e;
        tmpEngine.act(move_MOB);
        Color active = tmpEngine.turn;
        // std::vector<std::pair<Engine, Move>> moves_2 = all_possible_captures_outcomes(tmpEngine);
        for(Move move_2 : tmpEngine.legal_captures())
        {
            // czy można zbic ruch z MOB
            if((bitboard(dest) & Engine::get_captured_position(move_2)) != 0 )
            {
                // Engine tmpEngine_2 = *tmpEngine.clone();
                Engine tmpEngine_2 = tmpEngine;
                tmpEngine_2.act(move_2);
                if (tmpEngine_2.turn == active)
                {
                    denials.insert(dest);
                    break;
                }
                bool takeable = true;
                for(Move move_3 : tmpEngine_2.legal_captures())
                {
                    if(bitboard(move_2.to) & Engine::get_captured_position(move_3))
                        takeable = false;
                }
                if(takeable)
                    denials.insert(dest);
            }
        }
    }
    return denials.size();
}


/*The parameter is credited with 1 for each of the following
squares: 11, 12, 15, 16, 20, 21, 24, and 25 which is occupied
by a passive king*/
int Minimax::kcent(Engine e)
{
    Color passive = ~e.turn;
    return e.count_bits(center & e.pieces[passive] & e.kings);
}

/*The parameter is credited with the difference between MOB and DENY.*/

/*!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
TODO zapamietywac w zmiennej, żeby nie liczyć 2 razy
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!*/
int Minimax::mobil(Engine e)
{
    return mob(e) - deny(e);
}


int Minimax::mov(Engine e)
{
    int white_score = 2*(e.count_bits(e.pieces[WHITE] & ~e.kings))+3*(e.count_bits(e.pieces[WHITE] & e.kings));
    int black_score = 2*(e.count_bits(e.pieces[BLACK] & ~e.kings))+3*(e.count_bits(e.pieces[BLACK] & e.kings));
    
    if(white_score == black_score && white_score < 24 )
    {
        if((e.count_bits(columns0246 & e.all()) % 2) == 1)
            return 1;
    }
    return 0;
}

int Minimax::thret(Engine e)
{
    int result = 0;
    for(std::pair<Engine, Move> state : all_possible_moves_outcomes(e))
    {
        // Engine tmpEngine = *e.clone();
        Engine tmpEngine = e;
        tmpEngine.turn = ~tmpEngine.turn;
        if (e.man_capture_moves(state.second.to) || e.king_capture_moves(state.second.to))
            result++;
    }
    return result;
}

int Minimax::position_score(Engine e, Color color)
{
    int i = 1;
    int total = 0;
    for(Bitboard s : scores)
    {
        total += i*e.count_bits(e.pieces[color] & s);
        i++;
    }
    return total;
}

int Minimax::piece_score_diff(Engine e, Color color)
{
    int white_score = (2*(e.count_bits(e.pieces[WHITE] & ~e.kings)))+(3*(e.count_bits(e.pieces[WHITE] & e.kings)));
    int black_score = (2*(e.count_bits(e.pieces[BLACK] & ~e.kings)))+(3*(e.count_bits(e.pieces[BLACK] & e.kings)));

    // return color == WHITE ? white_score - black_score : black_score - white_score;
    if(color == BLACK)
        return black_score - white_score;
    if(color == WHITE)
        return white_score - black_score ;
    return 0;
}




std::vector<std::pair<Engine, Move>> Minimax::all_possible_moves_outcomes(Engine e)
{
    std::vector<std::pair<Engine, Move>> outcomes;
    Color color = e.turn;
    for(Move move : e.legal_moves())
    {
        // Engine tmp = *e.clone();
        Engine tmp = e;
        tmp.act(move);
        
        if(tmp.turn == color)
        {
            std::vector<std::pair<Engine, Move>> rest = all_possible_moves_outcomes(tmp);
            outcomes.insert(outcomes.end(), rest.begin(), rest.end());
        }
        else
            outcomes.push_back(std::make_pair(tmp, move));
    }
    return outcomes;
}
std::vector<std::pair<Engine, Move>> Minimax::all_possible_captures_outcomes(Engine e)
{
    std::vector<std::pair<Engine, Move>> outcomes;
    Color color = e.turn;
    for(Move move : e.legal_captures())
    {
        // Engine tmp = *e.clone();
        Engine tmp = e;
        tmp.act(move);
        
        if(tmp.turn == color)
        {
            std::vector<std::pair<Engine, Move>> rest = all_possible_captures_outcomes(tmp);
            outcomes.insert(outcomes.end(), rest.begin(), rest.end());
        }
        else
            outcomes.push_back(std::make_pair(tmp, move));
    }
    return outcomes;
}


Move Minimax::minimax_move(Engine e, int depth, Color color)
{
    // MoveList ml = e.legal_moves();
    MoveLists ml = e.legal_moves_lists(e);
    if(ml.size() == 0)
        return ml[0][0];
    
    int result = 0;
    CircularQueue<3> q;
    bool maxi_player = true;
    // bool maxi_player = (depth % 2 == 1) ? true : false;
    Color start_color = color;
    // Color start_color = maxi_player ? color : ~color;

    if(e.turn == WHITE)
    {
        if (hashmap_white1.find(e) != hashmap_white1.end())
            // return ml[hashmap_white1[e].last_added().second][0]; 
            return ml[hashmap_white1[e].pickRandom_with_weight().second][0];
        result = rec(e, ml[0][0], start_color, depth, INT32_MIN, INT32_MAX, true, q, e, maxi_player);
        // q.print();     
        // q.clear_nagative_values();
        // q.print();
        // std::cout<<"XXXXXXXXXXXXXXXX"<<std::endl;
        hashmap_white1.insert({ e, q});
    }else
    {
        if (hashmap_black1.find(e) != hashmap_black1.end()) 
            // return ml[hashmap_black1[e].last_added().second][0];
            return ml[hashmap_black1[e].pickRandom_with_weight().second][0];
        result = rec(e, ml[0][0], start_color, depth, INT32_MIN, INT32_MAX, true, q, e, maxi_player);
        // q.clear_nagative_values();
        hashmap_black1.insert({ e, q});
    }
    
    // std::cout<<result<<std::endl;
    return ml[result][0];
}



int Minimax::rec(Engine e, Move best_move, Color start_color, int depth, int alpha, int beta, bool root, CircularQueue<3> &q, Engine old, bool maxi)
{
    //std::vector<int> s = {0,0,0,0,0,0,0,0};
   if(depth == 0 || e.isFinished() > -1)
    {
        // old.turn = ~old.turn;
        return score(e, start_color, old);
    }
    
    // CircularQueue<MovePair, 3> queue;
    CircularQueue<3> queue;
    if(maxi){
        int bestVal = INT32_MIN;
        // std::vector<Move> moves = e.legal_moves();
        MoveLists mlists = e.legal_moves_lists(e);
        int moves_size = mlists.size(); 
        // int moves_size = moves.size(); 
        for(int i =0; i< moves_size; i++){
            Engine copy_board = e;
            // copy_board.act(moves[i]);
            copy_board.act(mlists[i]);
            int value = rec(copy_board, best_move, start_color, depth-1, alpha, beta, false, q, e, !maxi);
            if(value > bestVal)
            {   
                bestVal = value;
                
                if(root){
                    // result = i;
                    // queue.enqueue(std::make_pair(moves[i], i));
                    queue.enqueue(std::make_pair(value, i));
                }
            }
            alpha = std::max( alpha, bestVal);
            if(beta <= alpha)
                break;
        }
        if(root)
        {
            // queue.print();
            q = queue;
            return queue.pickRandom_with_weight().second;
        }
        return bestVal;
    }
    else{
        int bestVal = INT32_MAX;
        // std::vector<Move> moves = e.legal_moves();
        MoveLists mlists = e.legal_moves_lists(e);
        int moves_size = mlists.size(); 
        // int moves_size = moves.size(); 
        for(int i =0; i< moves_size; i++){
            Engine copy_board = e;
            copy_board.act(mlists[i]);
            int value = rec(copy_board, best_move, start_color, depth-1, alpha, beta, false, q, e, !maxi);
            if(value < bestVal)
            {
                bestVal = value;

                if(root){
                    // result = i;
                    // queue.enqueue(std::make_pair(moves[i], i));
                    queue.enqueue(std::make_pair(value, i));
                }
            }
            beta = std::min( beta, bestVal);
            if(beta <= alpha)
                break;
        }
        if(root)
        {
            // queue.print();
            q = queue;
            return queue.pickRandom_with_weight().second;
        }
        return bestVal;
    } 
}