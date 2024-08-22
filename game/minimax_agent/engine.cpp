//g++ -Wall test.cpp -o test1 $(python3-config --includes) $(python3-config --ldflags) -lpython3.10

#include "engine.h"
#include <pybind11/pytypes.h>
#include <pybind11/numpy.h>  
#include <cstddef>
#include <ostream>
#include <iostream>
#include <algorithm>
#include <iterator>
#include <bitset>
#include <array> 

namespace py = pybind11;

void Engine::print()
{
    constexpr auto SIDE_STR = "wb-";
    constexpr auto RANK_STR = "12345678";
    constexpr auto FILE_STR = "abcdefgh";

    std::cout << "\nGAME BOARD:\n\n";

    for (int r = 7; r >= 0; --r) {
        std::cout << RANK_STR[r] << "   ";
        for (int f = 0; f <= 7; ++f) {

            Square sq = square(r, f);
            char c = '.';

            if (get(pieces[WHITE], sq))
                c = 'w';
            else if (get(pieces[BLACK], sq))
                c = 'b';

            if (get(kings, sq))
                c = toupper(c);

            std::cout << c << ' ';
        }
        std::cout << "    ";
        for (int f = 0; f <= 7; ++f) {

            int x = (r << 3) + f;
            if ((x / 10) == 0)
                std::cout << ' ';
            std::cout << x << ' ';
        }
        std::cout << '\n';
    }
    std::cout << "\n   ";
    for (int f = 0; f <= 7; ++f)
        std::cout << ' ' << FILE_STR[f];
    std::cout << "\n\nside:\t" << SIDE_STR[turn];
}

Engine* Engine::clone() const
{
    Engine* copy = new Engine(*this);
    return copy;
}

void Engine::reset()
{
    pieces[WHITE] = 0x00000000'0055AA55;
    pieces[BLACK] = 0xAA55AA00'00000000;
    kings = 0x00000000'00000000;
    move_turn = 0;
    continue_from = 64;
    turn = WHITE;
}

void Engine::act(Move move)
{
    const auto f_bb = bitboard(move.from);
    const auto t_bb = bitboard(move.to);

    pieces[turn]    |= t_bb;

    if (kings & f_bb)
        kings       |= t_bb;

    pieces[turn]    &= ~f_bb;
    kings           &= ~f_bb;

    if ((move.type & CAPTURE)) {
        if(kings & t_bb)
        {
            Direction direction;
            int dir = int(move.to) - int(move.from);
            if( dir > 0)
            {
                if(dir%9 == 0)
                    direction = NORTH_EAST;
                else if(dir%7 == 0)
                    direction = NORTH_WEST;
            }
            else
            {
                dir = -dir;
                if(dir%7 == 0)
                    direction = SOUTH_EAST;
                else if(dir%9 == 0)
                    direction = SOUTH_WEST;
            }
            switch (direction)
            {
                case NORTH_EAST:
                    pieces[~turn]   &= ~(R_KING_ATTACKS[WHITE][move.from] & (bitboard(move.to) - 1));
                    kings           &= ~(R_KING_ATTACKS[WHITE][move.from] & (bitboard(move.to) - 1) & ~(bitboard(move.to)));
                    break;
                case NORTH_WEST:
                    pieces[~turn]   &= ~(L_KING_ATTACKS[WHITE][move.from] & (bitboard(move.to) - 1));
                    kings           &= ~(L_KING_ATTACKS[WHITE][move.from] & (bitboard(move.to) - 1) & ~(bitboard(move.to)));
                    break;
                case SOUTH_EAST:
                    pieces[~turn]   &= ~(R_KING_ATTACKS[BLACK][move.from] & ~(bitboard(move.to) - 1));
                    kings           &= ~(R_KING_ATTACKS[BLACK][move.from] & ~(bitboard(move.to) - 1) & ~(bitboard(move.to)));
                    break;
                case SOUTH_WEST:
                    pieces[~turn]   &= ~(L_KING_ATTACKS[BLACK][move.from] & ~(bitboard(move.to) - 1));
                    kings           &= ~(L_KING_ATTACKS[BLACK][move.from] & ~(bitboard(move.to) - 1) & ~(bitboard(move.to)));
                    break;   
                default:
                    break;
            }
        }else{
            switch (int(move.to) - int(move.from)) {
                case NORTH_EAST * 2:
                    pieces[~turn]   &= ~(f_bb << NORTH_EAST);
                    kings           &= ~(f_bb << NORTH_EAST);
                    break;
                case NORTH_WEST * 2:
                    pieces[~turn]   &= ~(f_bb << NORTH_WEST);
                    kings           &= ~(f_bb << NORTH_WEST);
                    break;
                case SOUTH_EAST * 2:
                    pieces[~turn]   &= ~(t_bb << NORTH_WEST);
                    kings           &= ~(t_bb << NORTH_WEST);
                    break;
                case SOUTH_WEST * 2:
                    pieces[~turn]   &= ~(t_bb << NORTH_EAST);
                    kings           &= ~(t_bb << NORTH_EAST);
                    break;
            }
        }
            // If another move available with same piece
        if (man_capture_moves(move.to) || king_capture_moves(move.to))
        {   
            continue_from = move.to;
            if (move.type & PROMOTION) //jesli bicie kontynuowane to zabierz promocje
                kings &= ~t_bb;
            return;
        }
    }
    if (move.type & PROMOTION)
        kings       |= t_bb;
    continue_from = 64;
    move_turn++;
    turn = ~turn;
}

bool Engine::legal(Move move) const
{
    return (kings & bitboard(move.from) ? 
           (king_moves(move.from)   | king_capture_moves(move.from)) : 
           (man_moves(move.from)    | man_capture_moves(move.from)) )
           & bitboard(move.to);
}

Bitboard Engine::captures() const
{
    const auto non = ~all();
    const auto opp = pieces[~turn];
    if(!legal_king_capture_moves(0).first.empty())
        return 1;
    
    Bitboard captures = 0;

    if (turn == WHITE) {
        captures |= (shift(shift(pieces[WHITE], NORTH_EAST) & opp, NORTH_EAST) & non) |
                    (shift(shift(pieces[WHITE], NORTH_WEST) & opp, NORTH_WEST) & non) |
                    (shift(shift(pieces[WHITE], SOUTH_EAST) & opp, SOUTH_EAST) & non) |
                    (shift(shift(pieces[WHITE], SOUTH_WEST) & opp, SOUTH_WEST) & non);
    } else {
        captures |= (shift(shift(pieces[BLACK], SOUTH_EAST) & opp, SOUTH_EAST) & non) |
                    (shift(shift(pieces[BLACK], SOUTH_WEST) & opp, SOUTH_WEST) & non) |
                    (shift(shift(pieces[BLACK], NORTH_EAST) & opp, NORTH_EAST) & non) |
                    (shift(shift(pieces[BLACK], NORTH_WEST) & opp, NORTH_WEST) & non);
    }
    return captures;
}

Bitboard Engine::king_moves(size_t sq) const 
{
    const auto all = this->all();
    Bitboard result=0;
    Bitboard iter = bitboard(sq);
    while((iter = shift(iter, NORTH_WEST)))
    {
        if(iter & all)
            break;
        result |= iter;
    }
    iter = bitboard(sq);
    while((iter = shift(iter, NORTH_EAST)))
    {
        if(iter & all)
            break;
        result |= iter;
    }
    iter = bitboard(sq);
    while((iter = shift(iter, SOUTH_WEST)))
    {
        if(iter & all)
            break;
        result |= iter;
    }
    iter = bitboard(sq);
    while((iter = shift(iter, SOUTH_EAST)))
    {
        if(iter & all)
            break;
        result |= iter;
    }


    return result;

}

Bitboard Engine::man_capture_moves(size_t sq) const
{
    const auto non = ~all();
    const auto opp = pieces[~turn];

    return (shift(R_ATTACKS[WHITE][sq] & opp, NORTH_EAST) & non) |
           (shift(L_ATTACKS[WHITE][sq] & opp, NORTH_WEST) & non) |
           (shift(R_ATTACKS[BLACK][sq] & opp, SOUTH_EAST) & non) |
           (shift(L_ATTACKS[BLACK][sq] & opp, SOUTH_WEST) & non);
}


Bitboard Engine::king_capture_moves(size_t sq) const
{
    const auto all = this->all();
    if(!(bitboard(sq) & kings))
        return 0;

    Bitboard up_mask = (R_KING_ATTACKS[WHITE][sq] & set_king_captures_white(R_KING_ATTACKS[WHITE][sq]&all, pieces[turn])) |
            (L_KING_ATTACKS[WHITE][sq] & set_king_captures_white(L_KING_ATTACKS[WHITE][sq]&all, pieces[turn]));

    Bitboard down_mask = (R_KING_ATTACKS[BLACK][sq] & set_king_captures_black(R_KING_ATTACKS[BLACK][sq]&all, pieces[turn])) |
            (L_KING_ATTACKS[BLACK][sq] & set_king_captures_black(L_KING_ATTACKS[BLACK][sq]&all, pieces[turn]));

    return down_mask | up_mask;
}

MoveList Engine::legal_captures() const
{
    MoveList list;
    if(continue_from == 64)
    {
        if (captures()) {
            list = legal_king_capture_moves(0).first;

            for (const auto from : BitIterator(pieces[turn] & ~kings))
                for (const auto to : BitIterator(man_capture_moves(from)))
                    list.emplace_back(Square(from), Square(to), bitboard(to) & OPPOSITE_RANK[turn] ? PROMOTION | CAPTURE : CAPTURE);

            return list;
        }
    }else
    {
        if (captures()) {
            list = legal_king_capture_moves(0, continue_from).first;

            for (const auto to : BitIterator(man_capture_moves(continue_from)))
                list.emplace_back(Square(continue_from), Square(to), bitboard(to) & OPPOSITE_RANK[turn] ? PROMOTION | CAPTURE : CAPTURE);
            return list;
        }
    }
    return list;
}

std::pair<MoveList, int> Engine::legal_king_capture_moves(int depth, Square continue_from_sq) const
{
    MoveList list;
    std::vector<std::pair<Move, int>> result_list;
    std::pair<MoveList, int> result;
    result.first = list;
    result.second = depth;
    int max = depth;
    Bitboard _from_bb = (continue_from_sq == 64) ? (pieces[turn] & kings) : bitboard(continue_from_sq);
    for (const auto from : BitIterator(_from_bb))
        for (const auto to : BitIterator(king_capture_moves(from)))
        {
            Engine tmp = *this->clone();
            Move m = Move(Square(from), Square(to), CAPTURE);
            tmp.act(m);
            std::pair<MoveList, int> rec = tmp.legal_king_capture_moves(depth+1);
            if(rec.second >= max)
                max = rec.second;
            result_list.emplace_back(std::make_pair(m, rec.second));  
        }

    for(std::pair<Move, int> mp : result_list)
    {
        if(mp.second == max)
            result.first.emplace_back(mp.first);
    }
    result.second = max;
    return result;
}

MoveList Engine::legal_moves() const
{
    MoveList list;

    if(continue_from == 64)
    {
        if (captures()) {
            list = legal_king_capture_moves(0).first;     

            for (const auto from : BitIterator(pieces[turn] & ~kings))
                for (const auto to : BitIterator(man_capture_moves(from)))
                    list.emplace_back(Square(from), Square(to), bitboard(to) & OPPOSITE_RANK[turn] ? PROMOTION | CAPTURE : CAPTURE);

            return list;
        }

        for (const auto from : BitIterator(pieces[turn] & kings))
            for (const auto to : BitIterator(king_moves(from)))
                list.emplace_back(Square(from), Square(to), QUIET);

        for (const auto from : BitIterator(pieces[turn] & ~kings))
            for (const auto to : BitIterator(man_moves(from)))
                list.emplace_back(Square(from), Square(to), bitboard(to) & OPPOSITE_RANK[turn] ? PROMOTION : QUIET);

        return list;
    }else
    {
        if (captures()) {
            list = legal_king_capture_moves(0, continue_from).first;   

            for (const auto to : BitIterator(man_capture_moves(continue_from)))
                list.emplace_back(Square(continue_from), Square(to), bitboard(to) & OPPOSITE_RANK[turn] ? PROMOTION | CAPTURE : CAPTURE);

            return list;
        }
        return list;
    }
}

Board Engine::board() const
{
    Board board;

    for (const auto sq : BitIterator(pieces[WHITE] & ~kings))
        board.push_back( {{ MAN, WHITE }, sq} );

    for (const auto sq : BitIterator(pieces[WHITE] & kings))
        board.push_back( {{ KING, WHITE }, sq} );

    for (const auto sq : BitIterator(pieces[BLACK] & ~kings))
        board.push_back( {{ MAN, BLACK }, sq} );

    for (const auto sq : BitIterator(pieces[BLACK] & kings))
        board.push_back( {{ KING, BLACK }, sq} );

    return board;
}


std::ostream& operator<<(std::ostream &os, const Engine &e)
{
    constexpr auto SIDE_STR = "wb-";
    constexpr auto RANK_STR = "12345678";
    constexpr auto FILE_STR = "abcdefgh";

    os << "\nGAME BOARD:\n\n";

    for (int r = 7; r >= 0; --r) {
        os << RANK_STR[r] << "   ";
        for (int f = 0; f <= 7; ++f) {

            Square sq = square(r, f);
            char c = '.';

            if (get(e.pieces[WHITE], sq))
                c = 'w';
            else if (get(e.pieces[BLACK], sq))
                c = 'b';

            if (get(e.kings, sq))
                c = toupper(c);

            os << c << ' ';
        }
        os << '\n';
    }
    os << "\n   ";
    for (int f = 0; f <= 7; ++f)
        os << ' ' << FILE_STR[f];
    os	<< "\n\nside:\t" << SIDE_STR[e.turn];

    return os;
}

/////////////////////////////////////////////////
// LICZENIE BITOW
/////////////////////////////////////////////////
#if defined(__GNUC__) || defined(__clang__)
int Engine::count_bits(Bitboard x) const {
    return __builtin_popcountll(x);
}
#elif defined(_MSC_VER) && defined(_WIN64)
#include <intrin.h>
int Engine::count_bits(Bitboard x) const {
    return __popcnt64(x);
}
#else
/* http://en.wikipedia.org/wiki/Hamming_weight */
int Engine::count_bits(Bitboard x) const {
    x -= (x >> 1) & 0x5555555555555555;
    x = (x & 0x3333333333333333) + ((x >> 2) & 0x3333333333333333);
    x = (x + (x >> 4)) & 0x0f0f0f0f0f0f0f0f;
    return (x * 0x0101010101010101) >> 56;
}
#endif
/////////////////////////////////////////////////

Engine::Engine(const Engine& other)
{
    pieces[WHITE] = other.pieces[WHITE];
    pieces[BLACK] = other.pieces[BLACK];
    pieces[BOTH] = other.pieces[BOTH];
    kings  = other.kings;
    turn   = other.turn;
    move_turn = other.move_turn;
    continue_from = other.continue_from;
}
Engine::Engine()
{
    pieces[BOTH] = {};
    kings = 0;
    turn = BOTH;
    move_turn = 0;
    continue_from  = 64;
}

Engine& Engine::operator=(const Engine& other) {
        if (this != &other) { 
            this->pieces[WHITE] = other.pieces[WHITE];
            this->pieces[BLACK] = other.pieces[BLACK];
            this->pieces[BOTH] = other.pieces[BOTH];
            this->kings = other.kings;
            this->turn  = other.turn;
            this->move_turn = other.move_turn;
            this->continue_from = other.continue_from;
        }
        return *this;
    }


Engine::~Engine()
{

}

/* -1 NOT FINISHED
   0 WHITE
   1 BLACK
   2 DRAW*/
int Engine::isFinished()
{
    
    MoveList moves = legal_moves();
    int size = moves.size();
    // if(kings!=0)
    //     return true;
    
    if(move_turn >= MAXTURNS)
        return 2;
    else if(size == 1)
    {
        Move move = moves[0];
        if(move.from == 0 && move.to == 0)
        {
            return ~turn;
        }
            
        return -1;
    }
    else if(size > 1)
        return -1;

    return ~turn;
}


bool Engine::operator==(const Engine& other) const
{
    return  ((pieces[WHITE] == other.pieces[WHITE]) &&
            (pieces[BLACK] == other.pieces[BLACK]) &&
            ((pieces[WHITE] & kings) == (other.pieces[WHITE] & other.kings)) &&
            ((pieces[BLACK] & kings) == (other.pieces[BLACK] & other.kings)) &&
            (turn == other.turn) &&
            (move_turn == other.move_turn) &&
            (continue_from == other.continue_from));
}

bool Engine::operator!=(const Engine& other) const
{
    return  !((pieces[WHITE] == other.pieces[WHITE]) &&
            (pieces[BLACK] == other.pieces[BLACK]) &&
            ((pieces[WHITE] & kings) == (other.pieces[WHITE] & other.kings)) &&
            ((pieces[BLACK] & kings) == (other.pieces[BLACK] & other.kings)) &&
            (turn == other.turn) &&
            (move_turn == other.move_turn) &&
            (continue_from == other.continue_from));
}

bool operator!=(const Engine& lhs, const Engine& rhs) {
    return !(lhs == rhs);
}

Bitboard Engine::get_captured_position(Move move)
{
    const auto f_bb = bitboard(move.from);
    const auto t_bb = bitboard(move.to);


    if (move.type & CAPTURE) {
        switch (int(move.to) - int(move.from)) {
            case NORTH_EAST * 2:
                return (f_bb << NORTH_EAST);
            case NORTH_WEST * 2:
                return (f_bb << NORTH_WEST);
            case SOUTH_EAST * 2:
                return (t_bb << NORTH_WEST);
            case SOUTH_WEST * 2:
                return (t_bb << NORTH_EAST);
            default:
                return 0;
        }
    }
    return 0;
}   


MoveLists Engine::legal_moves_lists(Engine e, MoveList ml) const
{
    MoveLists outcomes;
    Color color = turn;
    for(Move move : e.legal_moves())
    {
        Engine tmp = e;
        tmp.act(move);
        
        if(tmp.turn == color)
        {
            MoveList arg = ml;
            arg.emplace_back(move);
            MoveLists rest = legal_moves_lists(tmp, arg);
            outcomes.insert(outcomes.end(), rest.begin(), rest.end());
        }
        else
        {   
            MoveList arg = ml;
            arg.emplace_back(move);
            outcomes.push_back(arg);
        }
    }
    return outcomes;
}


void Engine::act(MoveList moves)
{
    for(Move m : moves)
        act(m);
}

Bitboard Engine::white_pieces(){ return pieces[WHITE] & ~kings; }
Bitboard Engine::black_pieces(){ return pieces[BLACK] & ~kings; }
Bitboard Engine::white_kings() { return pieces[WHITE] & kings; }
Bitboard Engine::black_kings() { return pieces[BLACK] & kings; }

// pybind11::dict Engine::__getstate__() const {
//     pybind11::dict state;
//     state["pieces"] = pybind11::array_t<Bitboard>(
//         {2},  
//         pieces 
//     );  
//     state["kings"] = kings;
//     state["turn"] = turn;
//     state["move_turn"] = move_turn;
//     state["continue_from"] = continue_from;
//     return state;
// }

// void Engine::__setstate__(pybind11::dict state) {
//     auto pieces_array = state["pieces"].cast<pybind11::array_t<Bitboard>>();
    
//     for (size_t i = 0; i < 2; ++i) {
//         pieces[i] = pieces_array.at(i);
//     }

//     kings = state["kings"].cast<Bitboard>();
//     turn = state["turn"].cast<Color>();
//     move_turn = state["move_turn"].cast<int>();
//     continue_from = state["continue_from"].cast<Square>();
// }