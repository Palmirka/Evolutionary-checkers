#ifndef ENGINE_H
#define ENGINE_H

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

#include "misc.h"
#include <vector>


using MoveList   = std::vector<Move>;
using MoveLists  = std::vector<MoveList>;
using Board      = std::vector<std::pair<Piece, Square>>;

#define MAXTURNS 100

struct Engine {
public:
    void        reset();
    void        act(Move move);
    void        act(MoveList moves);
    void        print();

    Bitboard    white_pieces();
    Bitboard    black_pieces();
    Bitboard    white_kings();
    Bitboard    black_kings();

    MoveList    legal_moves() const;
    MoveList    legal_captures() const;
    std::pair<MoveList, int> legal_king_capture_moves(int depth, Square continue_from_sq=64) const;
    Board       board() const;
   
    Engine(const Engine& other);
    Engine();
    ~Engine();
    Engine*     clone() const;
    Engine& operator=(const Engine& other);
    int         isFinished();
    
    friend std::ostream& operator<<(std::ostream &os, const Engine &e);

    bool        legal(Move move) const;

    Bitboard    all() const                    { return pieces[WHITE] | pieces[BLACK] | kings; }
    Bitboard    captures() const;
    Bitboard    man_moves(size_t sq) const     { return ATTACKS[turn][sq] & ~all(); }
    Bitboard    king_moves(size_t sq) const;
    Bitboard    man_capture_moves(size_t sq) const;
    Bitboard    king_capture_moves(size_t sq) const;
    MoveLists   legal_moves_lists(Engine e, MoveList ml = {}) const;
    

    int  count_bits(Bitboard x) const;
    bool operator!=(const Engine& other) const;
    bool operator==(const Engine& p) const;
    static Bitboard get_captured_position(Move move);

    pybind11::dict __getstate__() const;
    void __setstate__(pybind11::dict state);

    Bitboard    pieces[BOTH] = {};
    Bitboard    kings = 0;
    Color       turn = BOTH;
    int         move_turn = 0;
    Square      continue_from = 64;
};

#endif // ENGINE_H
