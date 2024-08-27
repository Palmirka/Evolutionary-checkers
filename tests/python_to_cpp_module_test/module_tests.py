# import os
# os.add_dll_directory("C:\\msys64\\mingw64\\bin") ## PYhton needs it to use gcc compiler in c++ module
#                                                  ## (path to gcc in windows)

# import sys
# current_dir = os.path.dirname(os.path.abspath(__file__))
# parent_dir = os.path.dirname(current_dir)
# sys.path.append(parent_dir)
import checkers_and_minimax_python_module as module ### import checkers c++ module

import unittest
import random


class TestEnumTypes(unittest.TestCase):
    def test_type(self):
        self.assertEqual(module.Type.DEAD, 0)
        self.assertEqual(module.Type.MAN, 1)
        self.assertEqual(module.Type.KING, 2)

    def test_color(self):
        self.assertEqual(module.Color.WHITE, 0)
        self.assertEqual(module.Color.BLACK, 1)
        self.assertEqual(module.Color.BOTH, 2)
        
    def test_dir(self):
        self.assertEqual(module.Direction.NORTH, 8)
        self.assertEqual(module.Direction.EAST, 1)
        self.assertEqual(module.Direction.SOUTH, -8)
        self.assertEqual(module.Direction.WEST, -1)
        self.assertEqual(module.Direction.NORTH_EAST, 9)
        self.assertEqual(module.Direction.SOUTH_EAST, -7)
        self.assertEqual(module.Direction.SOUTH_WEST, -9)
        self.assertEqual(module.Direction.NORTH_WEST, 7)

    def test_move_types(self):
        self.assertEqual(module.MoveType.QUIET, 0)
        self.assertEqual(module.MoveType.CAPTURE, 1)
        self.assertEqual(module.MoveType.PROMOTION, 2)

class TestStructsTypes(unittest.TestCase):
    def test_simple_move(self):
        move = module.Move(1, 3, module.MoveType.CAPTURE)
        self.assertEqual(getattr(move, "from"), 1) ## "from" is a keyword in python
        self.assertEqual(move.to, 3)
        self.assertEqual(move.type, 1)
        
    def test_simple_piece(self):
        piece = module.Piece(module.Type.MAN,module.Color.WHITE)
        self.assertEqual(piece.type, module.Type.MAN)
        self.assertEqual(piece.color, module.Color.WHITE)
    
    def test_simple_piece1(self):
        piece = module.Piece(module.Type.KING,module.Color.BLACK)
        self.assertEqual(piece.type, 2)
        self.assertEqual(piece.color, 1)

class TestBitCounting(unittest.TestCase):
    def test_simple(self):
        engine = module.Engine()
        engine.reset()
        self.assertEqual(engine.count_white_pieces(), 12)
        self.assertEqual(engine.count_black_pieces(), 12)
        self.assertEqual(engine.count_white_kings(), 0)
        self.assertEqual(engine.count_black_kings(), 0)
        self.assertEqual(engine.count_64b_bitboard(engine.white_pieces() | engine.black_pieces()), 24)
        
class TestEngine(unittest.TestCase): 
    def test_init(self):
        try:
            engine = module.Engine()
            engine.reset()
        except Exception as e:
            self.fail(f"Contructing Engine class catched error: {str(e)}")
        try:
            engine.print()
        except Exception as e:
            self.fail(f"Method print() catched error: {str(e)}")

    def test_init_state(self):
        engine = module.Engine()
        engine.reset()
        self.assertEqual(engine.white_pieces(), 5614165)
        self.assertEqual(engine.black_pieces(), 12273903276444876800)
        self.assertEqual(engine.white_kings(), 0)
        self.assertEqual(engine.black_kings(), 0)
      
    def test_start_moves(self):
        engine = module.Engine()
        engine.reset()
        moves = [module.Move(16,25,0), module.Move(18,25,0),module.Move(18,27,0), module.Move(20,27,0),module.Move(20,29,0),module.Move(22,29,0),module.Move(22,31,0)]
        for move1,move2 in zip(engine.legal_moves(), moves):
            self.assertEqual(getattr(move1, "from"), getattr(move2, "from"))
            self.assertEqual(move1.to,   move2.to)
            self.assertEqual(move1.type, move2.type)
        engine.act(moves[6])
        engine.act(engine.legal_moves()[2])
        engine.act(engine.legal_moves()[0])
        engine.act(engine.legal_moves()[4])
        move = engine.legal_moves()[0]
        self.assertEqual(getattr(move, "from"), 31)
        self.assertEqual(move.to,   45)
        self.assertEqual(move.type, 1)
        self.assertEqual(engine.move_turn, 4)

    def test_start_moves_sequences(self):
        engine = module.Engine()
        engine.reset()
        for i in range(10):
            engine.act(random.choice( engine.legal_moves_lists(engine)))
        
    def test_copy(self):
        engine = module.Engine()
        engine.reset()
        moves = [module.Move(16,25,0), module.Move(18,25,0),module.Move(18,27,0), module.Move(20,27,0),module.Move(20,29,0),module.Move(22,29,0),module.Move(22,31,0)]
        for move1,move2 in zip(engine.legal_moves(), moves):
            self.assertEqual(getattr(move1, "from"), getattr(move2, "from"))
            self.assertEqual(move1.to,   move2.to)
            self.assertEqual(move1.type, move2.type)
        engine.act(moves[6])
        engine.act(engine.legal_moves()[2])
        engine.act(engine.legal_moves()[0])
        engine.act(engine.legal_moves()[4])
        move = engine.legal_moves()[0]

        copied_engine = module.Engine(engine)
        self.assertEqual(copied_engine.move_turn, engine.move_turn)
        self.assertEqual(copied_engine.turn, engine.turn)

class TestMiniMax(unittest.TestCase):
    def test_init(self):
        try:
            minimax = module.Minimax()
        except Exception as e:
            self.fail(f"Contructing Minimax class catched error: {str(e)}")

    def test_blackdepth2_vs_whiteRandomMoves(self):
        engine = module.Engine()
        engine.reset()
        minimax = module.Minimax()
        while(engine.isFinished() < 0):
            while(engine.turn == module.Color.WHITE and engine.isFinished() < 0):
                engine.act(random.choice(engine.legal_moves()))
            while(engine.turn == module.Color.BLACK and engine.isFinished() < 0):
                move_black = minimax.minimax_move(engine, 2, module.Color.BLACK)
                engine.act(move_black)
        self.assertEqual(engine.isFinished(), module.Color.BLACK)
            
    def test_blackdepth2_vs_whitedpeth3(self):
        engine = module.Engine()
        engine.reset()
        minimax = module.Minimax()
        while(engine.isFinished() < 0):
            while(engine.turn == module.Color.WHITE and engine.isFinished() < 0):
                move_white = minimax.minimax_move(engine, 3, module.Color.WHITE)
                engine.act(move_white)
            while(engine.turn == module.Color.BLACK and engine.isFinished() < 0):
                move_black = minimax.minimax_move(engine, 2, module.Color.BLACK)
                engine.act(move_black)
        self.assertEqual(engine.isFinished(), module.Color.WHITE)
        
    def test_blackdepth3_vs_whitedpeth2(self):
        engine = module.Engine()
        engine.reset()
        minimax = module.Minimax()
        while(engine.isFinished() < 0):
            while(engine.turn == module.Color.WHITE and engine.isFinished() < 0):
                move_white = minimax.minimax_move(engine, 2, module.Color.WHITE)
                engine.act(move_white)
            while(engine.turn == module.Color.BLACK and engine.isFinished() < 0):
                move_black = minimax.minimax_move(engine, 3, module.Color.BLACK)
                engine.act(move_black)
        self.assertEqual(engine.isFinished(), module.Color.BLACK)
        
    def test_blackdepth4_vs_whitedpeth2_20games(self):
        for _ in range(20):
            engine = module.Engine()
            engine.reset()
            minimax = module.Minimax()
            while(engine.isFinished() < 0):
                while(engine.turn == module.Color.WHITE and engine.isFinished() < 0):
                    move_white = minimax.minimax_move(engine, 2, module.Color.WHITE)
                    engine.act(move_white)
                while(engine.turn == module.Color.BLACK and engine.isFinished() < 0):
                    move_black = minimax.minimax_move(engine, 4, module.Color.BLACK)
                    engine.act(move_black)
            self.assertEqual(engine.isFinished(), module.Color.BLACK)
        
    def test_blackdepth6_vs_whitedpeth4(self):
        engine = module.Engine()
        engine.reset()
        minimax = module.Minimax()
        while(engine.isFinished() < 0):
            while(engine.turn == module.Color.WHITE and engine.isFinished() < 0):
                move_white = minimax.minimax_move(engine, 4, module.Color.WHITE)
                engine.act(move_white)
            while(engine.turn == module.Color.BLACK and engine.isFinished() < 0):
                move_black = minimax.minimax_move(engine, 6, module.Color.BLACK)
                engine.act(move_black)
        self.assertEqual(engine.isFinished(), module.Color.BLACK)
        
    # def test_blackdepth5_vs_whiteRandomMoves_20_games(self):
    #     for _ in range(20):
    #         engine = module.Engine()
    #         engine.reset()
    #         minimax = module.Minimax()
    #         while(engine.isFinished() < 0):
    #             while(engine.turn == module.Color.WHITE and engine.isFinished() < 0):
    #                 engine.act(random.choice(engine.legal_moves()))
    #             while(engine.turn == module.Color.BLACK and engine.isFinished() < 0):
    #                 move_black = minimax.minimax_move(engine, 5, module.Color.BLACK)
    #                 engine.act(move_black)
    #         self.assertEqual(engine.isFinished(), module.Color.BLACK)

if __name__ == '__main__':
    unittest.main()
    
