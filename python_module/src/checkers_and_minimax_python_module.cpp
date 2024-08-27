#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/pytypes.h>
#include <pybind11/numpy.h>  

#include "../../game/minimax_agent/engine.h"
#include "../../game/minimax_agent/minimax.h"

namespace py = pybind11;


PYBIND11_MODULE(checkers_and_minimax_python_module, m)
{
    m.doc() = "pybind11 plugin for checkers and minimax agent for game of checkers"; // optional module docstring

    py::enum_<Type>(m, "Type")
        .value("DEAD", Type::DEAD)
        .value("MAN", Type::MAN)
        .value("KING", Type::KING);

    py::enum_<Color>(m, "Color")
        .value("WHITE", Color::WHITE)
        .value("BLACK", Color::BLACK)
        .value("BOTH", Color::BOTH);

    py::enum_<Status>(m, "Status")
        .value("GOING", Status::GOING)
        .value("WIN", Status::WIN)
        .value("DRAW", Status::DRAW)
        .value("STOPPED", Status::STOPPED);

    py::enum_<Direction>(m, "Direction")
        .value("NORTH", Direction::NORTH)
        .value("EAST", Direction::EAST)
        .value("SOUTH", Direction::SOUTH)
        .value("WEST", Direction::WEST)
        .value("NORTH_EAST", Direction::NORTH_EAST)
        .value("SOUTH_EAST", Direction::SOUTH_EAST)
        .value("SOUTH_WEST", Direction::SOUTH_WEST)
        .value("NORTH_WEST", Direction::NORTH_WEST);

    py::enum_<MoveType>(m, "MoveType")
        .value("QUIET", MoveType::QUIET)
        .value("CAPTURE", MoveType::CAPTURE)
        .value("PROMOTION", MoveType::PROMOTION);

    py::class_<Move>(m, "Move")
        .def(py::init<Square, Square, uint8_t>(),py::arg("from").none(false), py::arg("to").none(false), py::arg("type").none(false))
        .def("__str__", &Move::__str__)
        .def_readwrite("from", &Move::from)
        .def_readwrite("to", &Move::to)
        .def_readwrite("type", &Move::type);

    py::class_<Piece>(m, "Piece")
        .def(py::init<Type, Color>())
        .def_readwrite("type", &Piece::type)
        .def_readwrite("color", &Piece::color);

    py::class_<std::vector<Move>>(m, "MoveList")
        .def(py::init<>())
        .def(py::init<const std::vector<Move>&>())
        .def("append", (void (std::vector<Move>::*)(const Move&)) &std::vector<Move>::push_back)
        .def("size", &MoveList::size)
        .def("clear", &MoveList::clear);

    py::class_<std::vector<MoveList>>(m, "MoveLists")
        .def(py::init<>())
        .def(py::init<const std::vector<MoveList>&>())
        .def("append", (void (std::vector<MoveList>::*)(const MoveList&)) &std::vector<MoveList>::push_back)
        .def("size", &MoveList::size)
        .def("clear", &MoveList::clear);


    py::class_<Engine>(m, "Engine")
        .def(py::init<>())
        .def(py::init<const Engine&>())
        .def_readwrite("turn", &Engine::turn)
        .def_readwrite("move_turn", &Engine::move_turn)
        .def("reset", &Engine::reset)
        .def("act", py::overload_cast<Move>(&Engine::act))
        .def("act", py::overload_cast<MoveList>(&Engine::act))
        .def("print", &Engine::print)
        .def("legal_moves", &Engine::legal_moves)
        .def("legal_moves_lists", &Engine::legal_moves_lists,
                    py::arg("e"),
                    py::arg("ml") = MoveList())
        .def("legal_captures", &Engine::legal_captures)
        .def("isFinished", &Engine::isFinished)
        .def("white_pieces", &Engine::white_pieces)
        .def("black_pieces", &Engine::black_pieces)
        .def("white_kings", &Engine::white_kings)
        .def("black_kings", &Engine::black_kings)
        .def("count_white_pieces", &Engine::count_white_pieces)
        .def("count_black_pieces", &Engine::count_black_pieces)
        .def("count_white_kings", &Engine::count_white_kings)
        .def("count_black_kings", &Engine::count_black_kings)
        .def("count_64b_bitboard", &Engine::count_64b_bitboard)
            .def(py::pickle(
        [](const Engine &self) { // __getstate__
            return py::make_tuple(
                py::array_t<Bitboard>({2}, self.pieces),
                self.kings,
                self.turn,
                self.move_turn,
                self.continue_from
            );
        },
        [](py::tuple t) { // __setstate__, no `self` parameter
            auto pieces_array = t[0].cast<py::array_t<Bitboard>>();
            auto engine = new Engine(); // Create a new instance

            std::copy(pieces_array.data(), pieces_array.data() + 2, engine->pieces);
            engine->kings = t[1].cast<Bitboard>();
            engine->turn = t[2].cast<Color>();
            engine->move_turn = t[3].cast<int>();
            engine->continue_from = t[4].cast<Square>();

            return engine; // Return the newly constructed object
        }
    ));
        ;

    py::class_<Minimax>(m, "Minimax")
        .def(py::init<double>(), 
            py::arg("temp") = 1.0)
        .def("minimax_move", &Minimax::minimax_move)
        ;
}

// compile command
// g++.exe -shared -std=c++17 -fPIC -static-libgcc -static-libstdc++ -IC:\Users\Daniel\AppData\Local\Programs\Python\Python312\include -IC:\Users\Daniel\AppData\Local\Programs\Python\Python312\Lib\site-packages\pybind11\include -Wall -LC:\Users\Daniel\AppData\Local\Programs\Python\Python312\Lib -LC:\Users\Daniel\AppData\Local\Programs\Python\Python312\libs -LC:\Users\Daniel\AppData\Local\Programs\Python\Python312 checkers_and_minimax_python_module.cpp engine.cpp minimax.cpp -o checkers_and_minimax_python_module.cp312-win_amd64.pyd -lPython312