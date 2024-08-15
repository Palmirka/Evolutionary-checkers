#include "score.h"
#include <iostream>

Score::Score(Engine eng, Color _scored_color, Engine _old)
{
    scored_color = _scored_color;
    opposide_color = ~_scored_color;
    e = eng;
    active = e.turn;
    passive = ~active;
    legal_moves = e.legal_moves();
    oppEngine = e;
    oppEngine.turn = ~e.turn;
    opp_moves = oppEngine.legal_moves();
    old = _old;

    // std::cout<<(e==oppEngine)<<std::endl;

    center = bitboard(18)|bitboard(20)|bitboard(27)|bitboard(29)|bitboard(34)| bitboard(36)| bitboard(43)| bitboard(45);
    back_row_bridge_1 = bitboard(57) | bitboard(59);
    back_row_bridge_2 = bitboard(4) | bitboard(6);
    columns0246 =  bitboard(0)|bitboard(16)|bitboard(32)|bitboard(48)|bitboard(2)|bitboard(18)|bitboard(34)|bitboard(50)|bitboard(4)|bitboard(20)|bitboard(36)|bitboard(52)|bitboard(6)|bitboard(22)|bitboard(38)|bitboard(54);
    score1 = bitboard(27) | bitboard(36);
    score2 = bitboard(18) | bitboard(20) | bitboard(29) | bitboard(34)| bitboard(43)| bitboard(45);
    score3 = bitboard(9) | bitboard(11) | bitboard(13) | bitboard(22)| bitboard(25)| bitboard(38)| bitboard(41) | bitboard(50) | bitboard(52)| bitboard(54);
    score4 = bitboard(0) | bitboard(2) | bitboard(4) | bitboard(6)| bitboard(15)| bitboard(16)| bitboard(31) | bitboard(32) | bitboard(47)| bitboard(48)| bitboard(57)| bitboard(59)| bitboard(61)| bitboard(63);
    scores = {score1, score2, score3, score4};

    for (const auto from : BitIterator(e.pieces[e.turn] & e.kings))
        for (const auto to : BitIterator(e.king_moves(from)))
        {
            unique_to_sq.insert(to);
            unique_from_to_list.emplace_back(Move(Square(from), Square(to), QUIET));
        }
    for (const auto from : BitIterator(e.pieces[e.turn] & ~e.kings))
        for (const auto to : BitIterator(e.man_moves(from)))
        {
            unique_to_sq.insert(to);
            unique_from_to_list.emplace_back(Move(Square(from), Square(to), bitboard(to) & OPPOSITE_RANK[e.turn] ? PROMOTION : QUIET));
        }
}

/*  The parameter is credited with 1 for each passive man in the
    fifth and sixth rows (counting in passive's direction) and
    debited with 1 for each passive man in the third and fourth
    rows.*/
int Score::adv()
{
    Bitboard rows_5_and_6 = 0x00000000'AA550000;
    Bitboard rows_3_and_4 = 0x0000AA55'00000000;
    if(passive == WHITE)
    {
        Bitboard tmp = rows_5_and_6;
        rows_5_and_6 = rows_3_and_4;
        rows_3_and_4 = tmp;
    }

    Bitboard bits_3_and_4 = rows_3_and_4 & e.pieces[opposide_color];
    Bitboard bits_5_and_6 = rows_5_and_6 & e.pieces[opposide_color];
    // return e.count_bits(bits_5_and_6) - e.count_bits(bits_3_and_4);
    return e.count_bits(bits_3_and_4) - e.count_bits(bits_5_and_6);
}

/*  The parameter is credited with 1 if there are no active kings
    on the board and if the two bridge squares (1 and 3, or 30 and
    32) in the back row are occupied by passive pieces.*/
int Score::back()
{
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
int Score::cent(Engine eng)
{
    Color active = eng.turn;
    Color passive = ~active;
    return eng.count_bits(center & eng.pieces[passive]);
}

/*  The parameter is credited with 1 for each of the following
    squares: 11, 12, 15, 16, 20, 21, 24, 25 that is either
    currently occupied by an active piece or to which an active
    piece can move.*/
int Score::centr(Engine eng)
{
    Color active = eng.turn;
    Color passive = ~active;
    int from_moves = e.count_bits(center & e.pieces[active]);
    Bitboard to_mask=0;
    for(Move move : eng.legal_moves())
    {
        to_mask |= bitboard(move.to);
    }
    int to_moves = e.count_bits(center & to_mask);
    int scored = from_moves+to_moves;

    return scored;
    // int from_moves_opp = e.count_bits(center & e.pieces[opposide_color]);
    // Bitboard to_mask_opp=0;
    // for(Move move : opp_moves)
    // {
    //     to_mask_opp |= bitboard(move.to);
    // }
    // int to_moves_opp = e.count_bits(center & to_mask);
    // int opp = from_moves_opp+to_moves_opp;

    // if(scored_color == active)
    //     return scored-opp;
    // else 
    //     return opp-scored;

}

/*  The parameter is credited with 1 for each square to which the
    active side could move one or more pieces in the normal fashion
    disregarding the fact that jump moves may or may not be
    available.*/
int Score::mob(Engine eng)
{
    Color active = eng.turn;
    Color passive = ~active;
    // // if(scored_color == active)
    //     return unique_to_sq.size();
    // // else   
    //     // return -unique_to_sq.size();

    std::set<int> unique_to_sq1;
    MoveList unique_from_to_list1;
    for (const auto from : BitIterator(eng.pieces[eng.turn] & eng.kings))
        for (const auto to : BitIterator(eng.king_moves(from)))
        {
            unique_to_sq1.insert(to);
            unique_from_to_list1.emplace_back(Move(Square(from), Square(to), QUIET));
        }
    for (const auto from : BitIterator(eng.pieces[eng.turn] & ~eng.kings))
        for (const auto to : BitIterator(e.man_moves(from)))
        {
            unique_to_sq1.insert(to);
            unique_from_to_list1.emplace_back(Move(Square(from), Square(to), bitboard(to) & OPPOSITE_RANK[eng.turn] ? PROMOTION : QUIET));
        }

    return unique_to_sq1.size();
}

/*  The parameter is credited with 1 for each square defined
    in MOB if on the next move a piece occupying this
    square could be captured without an exchange.*/
int Score::deny(Engine eng)
{
    Color active = eng.turn;
    Color passive = ~active;

    // int result = 0;
    //wykonaj ruch z MOB
    // Color start_color = e.turn;

    // MoveList list;
    // for (const auto from : BitIterator(e.pieces[e.turn] & e.kings))
    //     for (const auto to : BitIterator(e.king_moves(from)))
    //         list.emplace_back(Move(Square(from), Square(to), QUIET));
    // for (const auto from : BitIterator(e.pieces[e.turn] & ~e.kings))
    //     for (const auto to : BitIterator(e.man_moves(from)))
    //         list.emplace_back(Move(Square(from), Square(to), bitboard(to) & OPPOSITE_RANK[e.turn] ? PROMOTION : QUIET));

    std::set<int> unique_to_sq1;
    MoveList unique_from_to_list1;
    for (const auto from : BitIterator(eng.pieces[eng.turn] & eng.kings))
        for (const auto to : BitIterator(eng.king_moves(from)))
        {
            unique_to_sq1.insert(to);
            unique_from_to_list1.emplace_back(Move(Square(from), Square(to), QUIET));
        }
    for (const auto from : BitIterator(eng.pieces[eng.turn] & ~eng.kings))
        for (const auto to : BitIterator(e.man_moves(from)))
        {
            unique_to_sq1.insert(to);
            unique_from_to_list1.emplace_back(Move(Square(from), Square(to), bitboard(to) & OPPOSITE_RANK[eng.turn] ? PROMOTION : QUIET));
        }


    std::set<Square> denials;
    // ruch z MOB
    for(Move move_MOB : unique_from_to_list1)
    {   
        // Square move = move_MOB.from;
        Square dest = move_MOB.to;
        // Engine tmpEngine = *e.clone();
        Engine tmpEngine = eng;
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
    // if(scored_color == active)
        return denials.size();
    // else
    //     return -denials.size();
}


/*The parameter is credited with 1 for each of the following
squares: 11, 12, 15, 16, 20, 21, 24, and 25 which is occupied
by a passive king*/
int Score::kcent(Engine eng)
{
    Color active = eng.turn;
    Color passive = ~active;
    return eng.count_bits(center & eng.pieces[passive] & eng.kings);
}

/*The parameter is credited with the difference between MOB and DENY.*/

/*!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
TODO zapamietywac w zmiennej, żeby nie liczyć 2 razy
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!*/
int Score::mobil(Engine eng)
{
    return mob(eng) - deny(eng);
}

/*  The parameter is credited with 1 if pieces are even with a
    total piece count (2 for men, and 3 for kings) of less than 24,
    and if an odd number of pieces are in the move system, defined
    as those vertical files starting with squares 1, 2, 3, and 4.*/
int Score::mov(Engine eng)
{
    Color active = eng.turn;
    Color passive = ~active;
    int white_score = 2*(eng.count_bits(eng.pieces[WHITE] & ~eng.kings))+3*(eng.count_bits(eng.pieces[WHITE] & eng.kings));
    int black_score = 2*(eng.count_bits(eng.pieces[BLACK] & ~eng.kings))+3*(eng.count_bits(eng.pieces[BLACK] & eng.kings));
    
    if(white_score == black_score && white_score < 24 )
    {
        if((eng.count_bits(columns0246 & eng.all()) % 2) == 1)
            return 1;
    }
    return 0;
}

/*  The parameter is credited with 1 for each square to which an
    active piece may be moved and in doing so threaten to capture
    a passive piece on a subsequent move.*/
int Score::thret(Engine eng)
{
    Color active = eng.turn;
    Color passive = ~active;
    int result_scored = 0;
    int result_opp = 0;

    for(Move move : legal_moves)
    {
        Engine tmpEngine = eng;
        tmpEngine.act(move);
        tmpEngine.turn = ~tmpEngine.turn;
        if (tmpEngine.man_capture_moves(move.to) || tmpEngine.king_capture_moves(move.to))
            result_scored++;
    }

    return result_scored;
}

int Score::position_score()
{
    int i = 1;
    int total = 0;
    for(Bitboard s : scores)
    {
        total += i*e.count_bits(e.pieces[scored_color] & s);
        i++;
    }
    return total;
}

int Score::piece_score_diff()
{
    int white_score = (2*(e.count_bits(e.pieces[WHITE] & ~e.kings)))+(3*(e.count_bits(e.pieces[WHITE] & e.kings)));
    int black_score = (2*(e.count_bits(e.pieces[BLACK] & ~e.kings)))+(3*(e.count_bits(e.pieces[BLACK] & e.kings)));

    // return color == WHITE ? white_score - black_score : black_score - white_score;
    if(scored_color == BLACK)
        return black_score - white_score;
    if(scored_color == WHITE)
        return white_score - black_score ;
    return 0;
}

std::vector<std::pair<Engine, Move>> Score::all_possible_moves_outcomes(Engine e)
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
std::vector<std::pair<Engine, Move>> Score::all_possible_captures_outcomes(Engine e)
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


int Score::score()
{
    int finish = e.isFinished();
    if(finish == scored_color)
        return INT32_MAX;
    else if(finish == opposide_color)
        return INT32_MIN;
    else if(finish == DRAW) //draw
        return INT32_MIN+1;

    // std::cout << e.turn << " " << old.turn << " passive: " << passive << " scored: " << scored_color << std::endl;

    // int _adv   = adv(e) - adv(old);
    // int _back  = back(e) - back(old);
    int _cent  = cent(e) - cent(old);
    // int _centr = centr(e) - centr(old);
    int _deny  = deny(e) - deny(old);
    int _kcent = kcent(e) - kcent(old);
    int _mob   = mob(e) - mob(old);
    int _mobil = _mob - _deny;
    // int _mov   = mov(e) - mov(old);
    int _thret = thret(e) - thret(old);

    int _adv   = adv();
    int _back  = back();
    // int _cent  = cent();
    // int _centr = centr(e);
    // int _deny  = deny();
    // int _kcent = kcent(e);
    // int _mob   = mob();
    // int _mobil = _mob - _deny;
    int _mov   = mov(e);
    // int _thret = thret(e);
    

    int sign = (e.turn == scored_color) ? 1 : -1;

    int _centr = sign*(centr(e) - centr(oppEngine));

    bool undenied_mobility= _mobil > 0 ? 1 : 0;
    bool total_mobility   = _mob > 0 ? 1 : 0;
    bool denial_of_cc     = _deny > 0 ? 1 : 0;
    bool control          = _cent > 0 ? 1 : 0;

    int _demmo  = denial_of_cc && !(total_mobility) ? 1 : 0;
    int _mode_2 = undenied_mobility && !(denial_of_cc) ? 1 : 0;
    int _mode_3 = !(undenied_mobility) && denial_of_cc ? 1 : 0;
    int _moc_2  = !(undenied_mobility) && control ? 1 : 0;
    int _moc_3  = (undenied_mobility) && !(control) ? 1 : 0;
    int _moc_4  = !(undenied_mobility) && !(control) ? 1 : 0;

    int board_score = 0
                    // + _moc_2*(-1)*(1<<18)  
                    // + _kcent*(1<<16) //
                    // + _moc_4*(-1)*(1<<14)  
                    // + _mode_3*(-1)*(1<<13) 
                    // + _demmo*(-1)*(1<<11)  
                    // + _mov*(1<<8)       // ??   
                    // + _adv*(-1)*(1<<8)     //?????????????
                    // + _mode_2*(-1)*(1<<8)  
                    // + _back*(-1)*(1<<6)    
                    // + _centr*(1<<5) // i think its ok
                    // + _thret*(1<<5) // ?????        
                    // + _moc_3*(1<<4)        
                    + piece_score_diff()*(1<<19)
                    // + position_score(e, color)*(1<<14)
                    ;

    return board_score; 
}