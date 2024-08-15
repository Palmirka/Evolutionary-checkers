#include <iostream>
#include "engine.cpp"
#include <bitset>
#include "minimax.cpp"
#include <chrono>
#include <bitset>
#include <iomanip>

using namespace std;

#define VERBOSE

void print_legal_moves(Engine e)
{
    for(Move m : e.legal_moves())
        cout<<"["<<+m.from<<","<<+m.to<<"("<<std::to_string(m.type)<<")"<<"],";
    cout<<endl;
}
void print_legal_captures(Engine e)
{
    for(Move m : e.legal_captures())
        cout<<"["<<+m.from<<","<<+m.to<<"],";
    cout<<endl;
}
void print_move(Move m)
{
    cout<<"["<<+m.from<<","<<+m.to<<"]"<<endl;
}

void print_bitset_as_board(Bitboard bb)
{
    std::bitset<64> bits(bb);
    std::cout<<"\n";
    for (int i = 0; i < 64; i += 8) {
        std::cout << bits.to_string().substr(i, 8) << std::endl;
    }
}
void print_seq(MoveLists seq)
{
    int i=0;
    for(MoveList ml : seq)
    {
        if(ml.size() >= 1){
            cout<<std::to_string(i)<<": ";
            for(Move m : ml)
            {
                cout<<"["<<+m.from<<","<<+m.to<<"],";
            }
            cout<<endl;
            i++;
        }
    }
}

string win_str(int c)
{
    switch(c){
        case WHITE:
            return "WHITE";
        case BLACK:
            return "BLACK";
        case DRAW:
            return "DRAW";
        default:
            return "GOING";
    }
}

void play_test_sets()
{
    // while(engine.isFinished() < 0):
    // while(engine.turn == module.Color.WHITE and engine.isFinished() < 0):
    //     move_white = minimax.start(engine, 3)
    //     engine.act(move_white)
    // while(engine.turn == module.Color.BLACK and engine.isFinished() < 0):
    //     move_black = minimax.start(engine, 2)
    //     engine.act(move_black)

    std::random_device rd;
    std::mt19937 gen(rd());
    int depths1[16] = {5,5,5,4,4,4,3,3,3,2,2,2,5,4,3,2};
    int depths2[16] = {4,3,2,4,3,2,4,3,2,4,3,2,0,0,0,0};
    int wins[16][3];
    for(int i=0; i<12; i++)
    {
        wins[i][0]=0;
        wins[i][1]=0;
        wins[i][2]=0;
        int depth1 = depths1[i];
        int depth2 = depths2[i];
        Minimax cpu_white;
        Minimax cpu_black;
        for(int lap = 0; lap<10; lap++)
        {
            Engine e;
            e.reset();
            while (e.isFinished() < 0)
            {
                while(e.turn == WHITE && e.isFinished() < 0)
                {
                    Move white_move = cpu_white.minimax_move(e, depth1, WHITE);
                    e.act(white_move);
                }
                while(e.turn ==  BLACK && e.isFinished() < 0)
                {
                    Move black_move = cpu_black.minimax_move(e, depth2, BLACK);
                    e.act(black_move);
                }
            }
            wins[i][e.isFinished()]++;
        }
    }
    for(int i=0; i<4; i++)
    {
        wins[12+i][0]=0;
        wins[12+i][1]=0;
        wins[12+i][2]=0;
        int depth1 = 5-i;
        Minimax cpu_white;
        for(int lap = 0; lap<10; lap++)
        {
            Engine e;
            e.reset();
            while (e.isFinished() < 0)
            {
                while(e.turn == WHITE && e.isFinished() < 0)
                {
                    Move white_move = cpu_white.minimax_move(e, depth1, WHITE);
                    e.act(white_move);
                }
                while(e.turn ==  BLACK && e.isFinished() < 0)
                {
                    MoveList moves = e.legal_moves();
                    int size =  moves.size() > 0 ? moves.size()-1 : 0;
                    std::uniform_int_distribution<> dist(0, size);
                    int random_index = dist(gen);
                    e.act(moves[random_index]);
                }
            }
            wins[12+i][e.isFinished()]++;
        }
    }
     

    printf("\n");
    printf("\n");
    printf("\n");
    std::cout<<"0 depth means random moves\n";
    std::cout<<"DEPTH WHITE: ";
    for(int i=0;i<16;i++)
        std::cout<<std::setw(4)<<depths1[i]<<"   ";
    printf("\n");
    std::cout<<"WHITE wins : ";
    for(int i=0;i<16;i++)
    {
        if(depths1[i] > depths2[i] && wins[i][WHITE] <= wins[i][BLACK])
            std::cout << "\033[1;31m"; 
        else if(depths1[i] < depths2[i] && wins[i][WHITE] >= wins[i][BLACK])
            std::cout << "\033[1;31m"; 
        else
            std::cout << "\033[1;32m"; 
        std::cout<<std::setw(4)<<wins[i][WHITE]<<"   ";
        std::cout << "\033[0m";
    }
    printf("\n");
    std::cout<<"DRAWS      : ";
    for(int i=0;i<16;i++)
        std::cout<<std::setw(4)<<wins[i][DRAW]<<"   ";
    printf("\n");
    std::cout<<"BLACK wins : ";
    for(int i=0;i<16;i++)
    {
        if(depths2[i] > depths1[i] && wins[i][BLACK] <= wins[i][WHITE])
            std::cout << "\033[1;31m";
        else if(depths2[i] < depths1[i] && wins[i][BLACK] >= wins[i][WHITE])
            std::cout << "\033[1;31m";  
        else
            std::cout << "\033[1;32m"; 
        std::cout<<std::setw(4)<<wins[i][BLACK]<<"   ";
        std::cout << "\033[0m";
    }
    printf("\n");
    std::cout<<"DEPTH BLACK: ";
    for(int i=0;i<16;i++)
        std::cout<<std::setw(4)<<depths2[i]<<"   ";
    printf("\n");
    printf("\n");
    printf("\n");
    
}

int main()
{
    Engine e;
    Minimax mm_white;
    Minimax mm_black;
    e.reset();
    e.print();
    int wins[3];
    wins[0] = 0;
    wins[1] = 0;
    wins[2] = 0;
    std::random_device rd;
    std::mt19937 gen(rd());
    
    int white_depth = 4;
    int black_depth = 2;
    
    #ifndef VERBOSE
        play_test_sets();
    #endif

    int laps = 0;
    #ifdef VERBOSE
        laps = 1;
    #endif
    auto start_10 = std::chrono::high_resolution_clock::now();
    for(int i = 0; i<laps;i++)
    {
        Engine e;
        e.reset();
        bool finish_flag = false;
        auto start = std::chrono::high_resolution_clock::now();
        if(i%10==0)
            start_10 = std::chrono::high_resolution_clock::now();
        
        while(!finish_flag)
        {
             while(e.turn == WHITE && !finish_flag)
            {
                // cout<<"WHITE"<<endl;
                
                // Move minimax_move = mm_white.start(e,2);
                Move minimax_move = mm_white.minimax_move(e,white_depth, WHITE);

                #ifdef VERBOSE
                    std::cout<<"Possible moves: "<<std::endl;
                    print_legal_moves(e);
                    std::cout<<"Choosen move  : "<<std::endl;
                    print_move(minimax_move);
                    std::cout<<"Possible seq  : "<<std::endl;
                    print_seq(e.legal_moves_lists(e));
                    std::cout<<"men  : "<<e.count_bits(e.pieces[WHITE] & ~e.kings)<<std::endl;
                    std::cout<<"kings: "<<e.count_bits(e.pieces[WHITE] & e.kings)<<std::endl;
                    std::cout<<"turn : "<<e.move_turn<<std::endl;

                    Engine tmp;
                    tmp.reset();
                    std::cout<<"white pieces: "<<std::bitset<64>(tmp.white_pieces())<<", "<<tmp.white_pieces()<<std::endl;
                    std::cout<<"black pieces: "<<std::bitset<64>(tmp.black_pieces())<<", "<<tmp.black_pieces()<<std::endl;
                    std::cout<<"white kings: "<<std::bitset<64>(tmp.white_kings())<<", "<<tmp.white_kings()<<std::endl;
                    std::cout<<"black kings: "<<std::bitset<64>(tmp.black_kings())<<", "<<tmp.black_kings()<<std::endl; 

                    // 0000000000000000001000000000000100000000000000000000000000000000
                    // e.print();
                    // std::cout<<"\nadv : "<<mm_white.adv(e)<<std::endl;
                    // std::cout<<"back : "<<mm.back(e)<<std::endl;
                    // std::cout<<"cent : "<<mm.cent(e)<<std::endl;
                    // std::cout<<"centr: "<<mm_white.centr(e)<<std::endl;
                    // std::cout<<"deny : "<<mm.deny(e)<<std::endl;
                    // std::cout<<"kcent: "<<mm_white.kcent(e)<<std::endl;
                    // std::cout<<"mob  : "<<mm.mob(e)<<std::endl;
                    // std::cout<<"mobil: "<<mm.mobil(e)<<std::endl;
                    // std::cout<<"thret: "<<mm_white.thret(e)<<std::endl;

                    Engine opp = e;
                    opp.turn = ~e.turn;
                    // print_legal_moves(opp);
                #endif
                if(minimax_move.from == 0 && minimax_move.to == 0)
                    {
                        finish_flag = true;
                        break; 
                        }      

                e.act(minimax_move);

                #ifdef VERBOSE
                    e.print();
                #endif

                if (e.isFinished() >= 0)
                {
                    finish_flag=true;
                    break;
                }
            }   
            while(e.turn == BLACK && !finish_flag)
            {
                // print_legal_moves(e);


                // Move minimax_move = mm_black.start(e,6);
                Move minimax_move = mm_black.minimax_move(e,black_depth, BLACK);
                
                // std::cout<<"BLACK"<<std::endl;
                // std::cout<<"Possible moves: "<<std::endl;
                // print_legal_moves(e);
                // std::cout<<"Choosen move  : "<<std::endl;
                // print_move(minimax_move);
                // std::cout<<"Possible seq  : "<<std::endl;
                // print_seq(e.legal_moves_lists(e));
                // std::cout<<"men  : "<<e.count_bits(e.pieces[BLACK] & ~e.kings)<<std::endl;
                // std::cout<<"kings: "<<e.count_bits(e.pieces[BLACK] & e.kings)<<std::endl;
                // std::cout<<"turn: "<<e.move_turn<<std::endl;
                
                if(minimax_move.from == 0 && minimax_move.to == 0)
                    {
                        finish_flag = true;
                        break; 
                        }   
                // std::cout<<to_str(Engine::get_captured_position(minimax_move));
                e.act(minimax_move);
                #ifdef VERBOSE
                    e.print();
                #endif
                // // cout<<e.count_pawns(BLACK)<<std::endl;
                // if (e.isFinished() >= 0)
                // {
                //     finish_flag=true;
                //     break;
                // }

                // MoveList moves = e.legal_moves();
                // int size =  moves.size() > 0 ? moves.size()-1 : 0;
                // std::uniform_int_distribution<> dist(0, size);
                // int random_index = dist(gen);
                // e.act(moves[random_index]);
                // e.print();

                if (e.isFinished() >= 0)
                {
                    finish_flag=true;
                    break;
                }

            }
          
            
            //print_bitset_as_board(e.captures());
        }
        auto stop = std::chrono::high_resolution_clock::now();
        auto duration = std::chrono::duration_cast<std::chrono::duration<double>>(stop - start);
        auto s = std::to_string(duration.count());
        // std::cout << i <<": " << s << " s" << std::endl;
        if((i+1)%10==0)
        {
            auto duration_10 = std::chrono::duration_cast<std::chrono::duration<double>>(stop - start_10);
            auto s = std::to_string(duration_10.count());
            std::cout <<"hashmap size black: " << mm_black.hashmap_black1.size() << std::endl;
            std::cout <<"hashmap size white: " << mm_white.hashmap_white1.size() << std::endl;
            std::cout << i <<" sum: " << s << " s" << std::endl;
        }
        // e.print();
        std::cout<<" turn: " << e.move_turn << " win: " << win_str(e.isFinished()) << std::endl;
        wins[e.isFinished()]++;
            
        // std::cout<<" piece score diff: " << mm_black.piece_score_diff(e, BLACK) <<endl;
        e.reset();
    }

    // cout<<"WHITE wins: "<<wins[WHITE]<<std::endl;
    // cout<<"BLACK wins: "<<wins[BLACK]<<std::endl;
    // cout<<"DRAWS     : "<<wins[BOTH] <<std::endl;

    // Square sq = 31;
    // e.reset();
    // e.pieces[WHITE] = bitboard(sq) | bitboard(63) | bitboard(38);
    // e.pieces[BLACK] = bitboard(25) | bitboard(22);
    // e.kings =  bitboard(sq);
    // e.print();

    // // std::cout<<"\nCZARNE : "<<std::bitset<64>(e.pieces[BLACK])<<std::endl;
    // // std::cout<<"BIAŁE  : "<<std::bitset<64>(e.pieces[WHITE])<<std::endl;
    // // std::cout<<"DAMKI  : "<<std::bitset<64>(e.kings)<<std::endl;
    
    // for(auto m : e.legal_moves())
    //     print_move(m);
    // e.pieces[BLACK] = e.king_capture_moves(sq);
    // e.print();


    // while(true)
    // {
    //     string turn = e.turn == WHITE ? "white" : "black";
    //     e.print();
    //     std::cout<<turn<<std::endl;
    //     string i;
    //     print_legal_moves(e);
    //     std::cout<<"captures: ";
    //     cout<<e.captures()<<endl;
    //     print_legal_captures(e);
    //     Engine tmp = *e.clone();
    //     tmp.pieces[BLACK] = 0;
        
    //     std::cout<<std::bitset<64>(L_KING_ATTACKS[WHITE][sq]& e.pieces[~e.turn])<<std::endl;
    //     // tmp.pieces[WHITE] = e.king_capture_moves(sq);
    //     // tmp.pieces[WHITE] = ~(bitboard(41) - 1); // + dla sq na topie
    //     // tmp.print();
    //     for(Move m : e.legal_king_capture_moves(0).first)
    //     {
    //         print_move(m);
    //         std::cout<< e.legal_king_capture_moves(0).second;
    //     }
    //     std::cin >> i;
    //     e.act(e.legal_captures()[stoi(i)]);
    // }

    // CircularQueue<3> queue;
    // MoveList mll = {Move(0,0,0)};
    // queue.enqueue(std::make_pair( mll, -1));
    // queue.enqueue(std::make_pair( mll, -3));
    // queue.enqueue(std::make_pair( mll, 3));
    // queue.enqueue(std::make_pair( mll, 4));
    // queue.enqueue(std::make_pair( mll, 5));
    // queue.clear_nagative_values();
    // queue.dequeue();
    // queue.print();

    // for(int i = 0; i < 100; i++)
    // {
    //     std::cout<<queue.pickRandom_with_weight().second<<'\n';
    // }
    return 0;
}
 /* TODO naprawić damki, żeby nie coafały się*/