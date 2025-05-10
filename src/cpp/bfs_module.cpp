#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>
#include <stdio.h>
#include <iostream>
#include <vector>
#include <queue>

namespace py = pybind11;

#define GET_ROW(x) (x & ((1 << 15) - 1))
#define GET_COL(x) ((x >> 15) & ((1 << 15) - 1))
#define CODE_POS(r, c) ((c << 15) + r)

int decode_point_tuple(py::tuple &point) {
    return CODE_POS(point[0].cast<int>(), point[1].cast<int>());
}

int neighbor_directions_r[4] = {0, 1, 0, -1};
int neighbor_directions_c[4] = {1, 0, -1, 0};
// { 1: right, 2: down, 3: left, 4: up, 5: wall }

inline bool is_empty_cell(py::detail::unchecked_reference<unsigned char, 2> &field, int r, int c) {
    return field(r, c) == 0;
}

py::list restore_path_legs(std::vector<std::vector<int>> &visited_from, int source_point, int target_point) {
    std::vector<py::tuple> path_vector;
    int current_position = target_point;
    while (current_position != source_point) {
        int r = GET_ROW(current_position), c = GET_COL(current_position);
        int prev_position = visited_from[r][c];
        int r_p = GET_ROW(prev_position), c_p = GET_COL(prev_position);
        int direction_id = 0;
        for (int i = 0; i < 4; ++i) {
            if (r - r_p == neighbor_directions_r[i] && c - c_p == neighbor_directions_c[i]) {
                direction_id = i + 1;
            }
        }

        if (direction_id == 0) {
            throw std::runtime_error("Illegal belt connection");
        }
        if (current_position == target_point) {
            path_vector.push_back(py::make_tuple(r, c, direction_id));
        }
        path_vector.push_back(py::make_tuple(r_p, c_p, direction_id));
        current_position = prev_position;
    }

    py::list path;
    for (auto it = path_vector.rbegin(); it != path_vector.rend(); ++it) {
        path.append(*it);
    }

    return path;
}

py::list find_path_legs(py::array_t<unsigned char> &field,
                        py::tuple &source_point_tpl, py::tuple &target_point_tpl) {

    if (field.ndim() != 2)
        throw std::runtime_error("Number of dimensions must be two");

    auto field_da = field.unchecked<2>();  // direct access to NumPy 2-d array

    int rows = field_da.shape(0);
    int cols = field_da.shape(1);

    std::vector<std::vector<int>> visited_from(rows, std::vector<int>(cols, -1));
    std::queue<int> queue;

    int source_point = decode_point_tuple(source_point_tpl);
    int target_point = decode_point_tuple(target_point_tpl);
    queue.push(source_point);
    bool target_visited = false;
    while (!queue.empty() && !target_visited) {
        int position = queue.front();
        queue.pop();
        for (int i = 0; i < 4; ++i) {
            int r = GET_ROW(position) + neighbor_directions_r[i];
            int c = GET_COL(position) + neighbor_directions_c[i];
            int new_position = CODE_POS(r, c);
            if (0 <= r && r < rows && 0 <= c && c < cols
                && visited_from[r][c] == -1 && is_empty_cell(field_da, r, c)) {
                visited_from[r][c] = position;
                queue.push(new_position);

                if (new_position == target_point) {
                    target_visited = true;
                }
            }
        }
    }

    if (!target_visited) {
        return py::none();
    }

    auto path = restore_path_legs(visited_from, source_point, target_point);
    return path;
}

PYBIND11_MODULE(bfs_module, m) {
    m.def("find_path_legs", &find_path_legs, "find_path_legs");
}