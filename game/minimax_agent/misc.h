#ifndef TYPES_H
#define TYPES_H

#include <cstdint>
#include <array>
#include <string>
#include <limits.h>


#if __cplusplus > 201703L
#include <bit>
#endif

constexpr size_t SQ_SIZE = 60; // For graphical use
constexpr size_t SQ_NUM = 64;

using Square = uint8_t;
using Bitboard = uint64_t;

enum Type   { DEAD, MAN, KING };
enum Color  { WHITE, BLACK, BOTH };
enum Status { GOING, WIN, DRAW, STOPPED };
enum Direction {
    NORTH =  8,
    EAST  =  1,
    SOUTH = -NORTH,
    WEST  = -EAST,

    NORTH_EAST = NORTH + EAST,
    SOUTH_EAST = SOUTH + EAST,
    SOUTH_WEST = SOUTH + WEST,
    NORTH_WEST = NORTH + WEST
};
enum MoveType : uint8_t {
    QUIET = 0,
    CAPTURE = 1,
    PROMOTION = 2,
};

struct Move {
    Square from;
    Square to;
    uint8_t type = QUIET;
#if __cplusplus > 201703L
    bool operator<=>(const Move &rhs) const = default;
#else
    Move() = default;
    Move(Square f, Square t, uint8_t type_) : from(f), to(t), type(type_) {}
#endif
    std::string __str__() const {
        return "["+std::to_string(from)+","+std::to_string(to)+" ("+std::to_string(type)+")"+"]";
    }
};

struct Piece {
    Type type = DEAD;
    Color color = BOTH;
};

constexpr Bitboard LIGHT_SQUARES    = 0x55AA55AA55AA55AAULL;
constexpr Bitboard DARK_SQUARES     = 0xAA55AA55AA55AA55ULL;
constexpr Bitboard BORDER_SQUARES   = 0xFF818181818181FFULL;

constexpr Bitboard SOUTH_WEST_QUARTER = 0x000000000F0F0F0FULL;
constexpr Bitboard SOUTH_EAST_QUARTER = 0x00000000F0F0F0F0ULL;
constexpr Bitboard NORTH_WEST_QUARTER = 0x0F0F0F0F00000000ULL;
constexpr Bitboard NORTH_EAST_QUARTER = 0xF0F0F0F000000000ULL;

constexpr Bitboard FILE_A_BB = 0x0101010101010101ULL;
constexpr Bitboard FILE_B_BB = FILE_A_BB << 1;
constexpr Bitboard FILE_C_BB = FILE_A_BB << 2;
constexpr Bitboard FILE_D_BB = FILE_A_BB << 3;
constexpr Bitboard FILE_E_BB = FILE_A_BB << 4;
constexpr Bitboard FILE_F_BB = FILE_A_BB << 5;
constexpr Bitboard FILE_G_BB = FILE_A_BB << 6;
constexpr Bitboard FILE_H_BB = FILE_A_BB << 7;

constexpr Bitboard RANK_1_BB = 0xFFULL;
constexpr Bitboard RANK_2_BB = RANK_1_BB << (8 * 1);
constexpr Bitboard RANK_3_BB = RANK_1_BB << (8 * 2);
constexpr Bitboard RANK_4_BB = RANK_1_BB << (8 * 3);
constexpr Bitboard RANK_5_BB = RANK_1_BB << (8 * 4);
constexpr Bitboard RANK_6_BB = RANK_1_BB << (8 * 5);
constexpr Bitboard RANK_7_BB = RANK_1_BB << (8 * 6);
constexpr Bitboard RANK_8_BB = RANK_1_BB << (8 * 7);

constexpr Bitboard OPPOSITE_RANK[] = { RANK_8_BB, RANK_1_BB };

constexpr Bitboard SW_QUARTER = (FILE_A_BB | FILE_B_BB | FILE_C_BB | FILE_D_BB) & (RANK_1_BB | RANK_2_BB | RANK_3_BB | RANK_4_BB);
constexpr Bitboard SE_QUARTER = (FILE_E_BB | FILE_F_BB | FILE_G_BB | FILE_H_BB) & (RANK_1_BB | RANK_2_BB | RANK_3_BB | RANK_4_BB);
constexpr Bitboard NW_QUARTER = (FILE_A_BB | FILE_B_BB | FILE_C_BB | FILE_D_BB) & (RANK_5_BB | RANK_6_BB | RANK_7_BB | RANK_8_BB);
constexpr Bitboard NE_QUARTER = (FILE_E_BB | FILE_F_BB | FILE_G_BB | FILE_H_BB) & (RANK_5_BB | RANK_6_BB | RANK_7_BB | RANK_8_BB);


constexpr auto generate_files_to_x()
{
    std::array<Bitboard, 8> files = {FILE_A_BB,0,0,0,0,0,0,0};
    for(int i=1; i<8; i++)
    {
        files[i] = files[i-1];
        files[i] |= (files[0] << i);
    }
    return files;
}
constexpr auto FILES_TO_X = generate_files_to_x();

constexpr auto generate_sq_bb()
{
    std::array<Bitboard, SQ_NUM> sq_bb = {};
    for (Square sq = 0; sq < SQ_NUM; ++sq)
        sq_bb[sq] = Bitboard(1ULL << sq);
    return sq_bb;
}
constexpr auto SQ_BB = generate_sq_bb();

constexpr Square square(const int r, const int f)   { return (r << 3) + f; }
constexpr bool valid(const Square sq)               { return sq < 64; }
constexpr Color operator~(Color c)                  { return Color(c ^ BLACK); }
constexpr Bitboard bitboard(Square sq)              { return SQ_BB[sq]; }
constexpr void set(Bitboard &bb, Square sq)         { bb |= bitboard(sq); }
constexpr void clr(Bitboard &bb, Square sq)         { bb &= ~bitboard(sq); }
constexpr bool get(Bitboard bb, Square sq)          { return bb & bitboard(sq); }

#if __cplusplus > 201703L
constexpr int count(Bitboard bb)                    { return std::popcount(bb); }
constexpr int lsb(Bitboard bb)                      { return std::countr_zero(bb);  }
#else
constexpr int count(Bitboard bb)                    { int cnt = 0; while (bb) { cnt++; bb &= bb - 1; } return cnt; }
constexpr int lsb(Bitboard bb)                      { return count((bb & -bb) - 1);  }
#endif
constexpr int fsb(Bitboard bb)                      { return bb & -bb; }

constexpr Bitboard set_king_captures_white(Bitboard num, Bitboard turn_bb) {
    Bitboard lsb1 = num & -num;
    if(lsb1 == 0)
        return 0;
    else if(lsb1 & turn_bb)
        return 0;
    Bitboard numWithoutLsb = num & (num - 1);
    Bitboard secondLsb = secondLsb = numWithoutLsb & -numWithoutLsb;;
    if (numWithoutLsb == 0)
        secondLsb = bitboard(63);     

    // 0000010000000

    // 0000001111111
    // 0000000000000
    // 0000001111111
    // 0000010000000
    Bitboard mask = (lsb1 - 1) ^ (secondLsb - 1);

    return mask & ~lsb1;
}

constexpr Bitboard myLsb(Bitboard num){
    return num&-num;
}

constexpr Bitboard myMsb(Bitboard num)
{
    num |= num >> 1;

    num |= num >> 2;
    num |= num >> 4;
    num |= num >> 8;
    num |= num >> 16;
    num |= num >> 32;
 
    num = ((num + 1) >> 1) |
        (num & (1 << ((sizeof(num) * CHAR_BIT)-1)));
    return num;
}

constexpr Bitboard set_king_captures_black(Bitboard num, Bitboard turn_bb) {
    Bitboard msb = myMsb(num);
    if(msb == 0)
        return 0;
    else if (msb & turn_bb)
        return 0;
    
    Bitboard numWithoutMsb = num & (msb -1);
    Bitboard secondMsb = myMsb(numWithoutMsb);
    if(numWithoutMsb == 0)
        secondMsb = bitboard(1);
    
    Bitboard mask = (msb - 1) ^ (secondMsb - 1);
    return mask & ~secondMsb & ~msb;
}

constexpr Bitboard shift(Bitboard b, Direction d)
{
    switch (d) {
        case NORTH:      return  b << 8;
        case SOUTH:      return  b >> 8;
        case EAST:       return (b & ~FILE_H_BB) << 1;
        case WEST:       return (b & ~FILE_A_BB) >> 1;
        case NORTH_EAST: return (b & ~FILE_H_BB) << 9;
        case NORTH_WEST: return (b & ~FILE_A_BB) << 7;
        case SOUTH_EAST: return (b & ~FILE_H_BB) >> 7;
        case SOUTH_WEST: return (b & ~FILE_A_BB) >> 9;
        default: return 0;
    }
}

constexpr Bitboard shift_x(Bitboard b, Direction d, int x)
{
    switch (d) {
        case NORTH:      return  b << 8*x;
        case SOUTH:      return  b >> 8*x;
        case EAST:       return (b & FILES_TO_X[7-x]) << 1*x;
        case WEST:       return (b & ~(FILES_TO_X[x-1])) >> 1*x;
        case NORTH_EAST: return (b & FILES_TO_X[7-x]) << 9*x;
        case NORTH_WEST: return (b & ~(FILES_TO_X[x-1])) << 7*x;
        case SOUTH_EAST: return (b & FILES_TO_X[7-x]) >> 7*x;
        case SOUTH_WEST: return (b & ~(FILES_TO_X[x-1])) >> 9*x;
        default: return 0;
    }
}

#if __cplusplus > 201703L
constexpr Bitboard shift(Bitboard b, auto dirs)
#else
template<class T>
constexpr Bitboard shift(Bitboard b, T dirs)
#endif
{
    Bitboard bb = 0;
    for (const auto d : dirs)
        bb |= shift(b, d);
    return bb;
}

#if __cplusplus > 201703L
constexpr Bitboard shift_x(Bitboard b, auto dirs, int x)
#else
template<class T>
constexpr Bitboard shift_x(Bitboard b, T dirs, int x)
#endif
{
    Bitboard bb = 0;
    for (const auto d : dirs)
        bb |= shift_x(b, d, x);
    return bb;
}

#if __cplusplus > 201703L
constexpr auto generate_attacks(auto dir)
#else
template<class T>
constexpr auto generate_attacks(T dir)
#endif
{
    using namespace std;

    array<array<Bitboard, 64>, 3> attacks = {};

    for (Square sq = 0; sq < SQ_NUM; ++sq) {

        const auto bb = bitboard(sq);

        attacks[WHITE][sq] = shift(bb, dir[WHITE]);
        attacks[BLACK][sq] = shift(bb, dir[BLACK]);
        attacks[BOTH][sq] = attacks[WHITE][sq] | attacks[BLACK][sq];
    }
    return attacks;
}

#if __cplusplus > 201703L
constexpr auto generate_king_attacks(auto dir)
#else
template<class T>
constexpr auto generate_king_attacks(T dir)
#endif
{
    using namespace std;

    array<array<Bitboard, 64>, 3> attacks = {};

    for (Square sq = 0; sq < SQ_NUM; ++sq) {

        const auto bb = bitboard(sq);
        attacks[WHITE][sq] = 0;
        attacks[BLACK][sq] = 0;
        attacks[BOTH][sq] = 0;

        for(int x = 1; x<=7; x++)
        {
            attacks[WHITE][sq] |= shift_x(bb, dir[WHITE],x);
            attacks[BLACK][sq] |= shift_x(bb, dir[BLACK],x);
            attacks[BOTH][sq] = attacks[WHITE][sq] | attacks[BLACK][sq];
        }
    }
    return attacks;
}
constexpr auto R_ATTACKS = generate_attacks(std::array{NORTH_EAST, SOUTH_EAST});
constexpr auto L_ATTACKS = generate_attacks(std::array{NORTH_WEST, SOUTH_WEST});
constexpr auto ATTACKS = generate_attacks(std::array{std::array{NORTH_EAST, NORTH_WEST}, std::array{SOUTH_EAST, SOUTH_WEST}});
constexpr auto R_KING_ATTACKS = generate_king_attacks(std::array{NORTH_EAST, SOUTH_EAST});
constexpr auto L_KING_ATTACKS = generate_king_attacks(std::array{NORTH_WEST, SOUTH_WEST});
constexpr auto KING_ATTACKS = generate_king_attacks(std::array{std::array{NORTH_EAST, NORTH_WEST}, std::array{SOUTH_EAST, SOUTH_WEST}});

inline std::string to_str(Bitboard bb)
{
    std::string str;
    for (int rank = 7; rank >= 0; --rank) {
        str += '|';
        for (int file = 0; file <= 7; ++file) {
            str += get(bb, square(rank, file)) ? 'X' : '-';
            str += '|';
        }
        str += '\n';
    }
    return str;
}

template <typename T>
struct BitIterator {

    constexpr BitIterator(T value_) : value(value_) {}

    constexpr bool  operator!=(const BitIterator &other) { return value != other.value; }
    constexpr void  operator++()                         { value &= (value - 1); }
    constexpr T     operator*() const                    { return lsb(value); }

    constexpr BitIterator begin() { return value; }
    constexpr BitIterator end()   { return 0; }
private:
    T value;
};

#endif // TYPES_H
