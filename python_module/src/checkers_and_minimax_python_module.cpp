#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

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
                    py::arg("ml") = MoveList())  // Ustawienie domyślnego argumentu)
        .def("legal_captures", &Engine::legal_captures)
        .def("isFinished", &Engine::isFinished)
        .def("white_pieces", &Engine::white_pieces)
        .def("black_pieces", &Engine::black_pieces)
        .def("white_kings", &Engine::white_kings)
        .def("black_kings", &Engine::black_kings)
        // .def("legal_king_capture_moves", &Engine::legal_king_capture_moves)
        // .def("board", &Engine::board)
        // .def("count_kings", &Engine::count_kings)
        // .def("count_pawns", &Engine::count_pawns)
        // .def_readwrite("turn", &Engine::turn)
        // .def("clone", &Engine::clone)
        ;

    py::class_<Minimax>(m, "Minimax")
        .def(py::init<>())
        .def("minimax_move", &Minimax::minimax_move)
        ;
}


// compile command
// g++.exe -shared -std=c++17 -fPIC -static-libgcc -static-libstdc++ -IC:\Users\Daniel\AppData\Local\Programs\Python\Python312\include -IC:\Users\Daniel\AppData\Local\Programs\Python\Python312\Lib\site-packages\pybind11\include -Wall -LC:\Users\Daniel\AppData\Local\Programs\Python\Python312\Lib -LC:\Users\Daniel\AppData\Local\Programs\Python\Python312\libs -LC:\Users\Daniel\AppData\Local\Programs\Python\Python312 checkers_and_minimax_python_module.cpp engine.cpp minimax.cpp -o checkers_and_minimax_python_module.cp312-win_amd64.pyd -lPython312