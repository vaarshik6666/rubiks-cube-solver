from flask import Blueprint, request, jsonify
import sys
import os
import copy
import random

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..'))

class RubiksCube:
    UP = 0
    DOWN = 1
    FRONT = 2
    BACK = 3
    RIGHT = 4
    LEFT = 5

    COLORS = {
        0: 'W',
        1: 'Y',
        2: 'R',
        3: 'O',
        4: 'G',
        5: 'B'
    }

    def __init__(self):
        self.faces = []
        for i in range(6):
            face = [[i for _ in range(3)] for _ in range(3)]
            self.faces.append(face)
        self.move_history = []

    def copy(self):
        new_cube = RubiksCube()
        new_cube.faces = copy.deepcopy(self.faces)
        new_cube.move_history = self.move_history.copy()
        return new_cube

    def is_solved(self):
        for face_idx, face in enumerate(self.faces):
            for row in face:
                for color in row:
                    if color != face_idx:
                        return False
        return True

    def get_state_string(self):
        state = ""
        for face in self.faces:
            for row in face:
                for color in row:
                    state += str(color)
        return state

    def _rotate_face_clockwise(self, face_idx):
        face = self.faces[face_idx]
        rotated = [[face[2-j][i] for j in range(3)] for i in range(3)]
        self.faces[face_idx] = rotated

    def _rotate_face_counterclockwise(self, face_idx):
        for _ in range(3):
            self._rotate_face_clockwise(face_idx)

    def _cycle_edges(self, positions, clockwise=True):
        if not clockwise:
            positions = positions[::-1]
        
        temp = self.faces[positions[0][0]][positions[0][1]][positions[0][2]]
        
        for i in range(len(positions) - 1):
            curr_face, curr_row, curr_col = positions[i]
            next_face, next_row, next_col = positions[i + 1]
            self.faces[curr_face][curr_row][curr_col] = self.faces[next_face][next_row][next_col]
        
        last_face, last_row, last_col = positions[-1]
        self.faces[last_face][last_row][last_col] = temp

    def U(self):
        self._rotate_face_clockwise(self.UP)
        positions = [
            (self.FRONT, 0, 0), (self.RIGHT, 0, 0), 
            (self.BACK, 0, 0), (self.LEFT, 0, 0)
        ]
        self._cycle_edges(positions)
        self.move_history.append("U")

    def U_prime(self):
        self._rotate_face_counterclockwise(self.UP)
        positions = [
            (self.FRONT, 0, 0), (self.LEFT, 0, 0),
            (self.BACK, 0, 0), (self.RIGHT, 0, 0)
        ]
        self._cycle_edges(positions)
        self.move_history.append("U'")

    def D(self):
        self._rotate_face_clockwise(self.DOWN)
        positions = [
            (self.FRONT, 2, 2), (self.LEFT, 2, 2),
            (self.BACK, 2, 2), (self.RIGHT, 2, 2)
        ]
        self._cycle_edges(positions)
        self.move_history.append("D")

    def D_prime(self):
        self._rotate_face_counterclockwise(self.DOWN)
        positions = [
            (self.FRONT, 2, 2), (self.RIGHT, 2, 2),
            (self.BACK, 2, 2), (self.LEFT, 2, 2)
        ]
        self._cycle_edges(positions)
        self.move_history.append("D'")

    def R(self):
        self._rotate_face_clockwise(self.RIGHT)
        positions = [
            (self.FRONT, 0, 2), (self.UP, 0, 2),
            (self.BACK, 2, 0), (self.DOWN, 0, 2)
        ]
        self._cycle_edges(positions)
        self.move_history.append("R")

    def R_prime(self):
        self._rotate_face_counterclockwise(self.RIGHT)
        positions = [
            (self.FRONT, 0, 2), (self.DOWN, 0, 2),
            (self.BACK, 2, 0), (self.UP, 0, 2)
        ]
        self._cycle_edges(positions)
        self.move_history.append("R'")

    def L(self):
        self._rotate_face_clockwise(self.LEFT)
        positions = [
            (self.FRONT, 0, 0), (self.DOWN, 0, 0),
            (self.BACK, 2, 2), (self.UP, 0, 0)
        ]
        self._cycle_edges(positions)
        self.move_history.append("L")

    def L_prime(self):
        self._rotate_face_counterclockwise(self.LEFT)
        positions = [
            (self.FRONT, 0, 0), (self.UP, 0, 0),
            (self.BACK, 2, 2), (self.DOWN, 0, 0)
        ]
        self._cycle_edges(positions)
        self.move_history.append("L'")

    def F(self):
        self._rotate_face_clockwise(self.FRONT)
        positions = [
            (self.UP, 2, 0), (self.RIGHT, 0, 0),
            (self.DOWN, 0, 2), (self.LEFT, 2, 2)
        ]
        self._cycle_edges(positions)
        self.move_history.append("F")

    def F_prime(self):
        self._rotate_face_counterclockwise(self.FRONT)
        positions = [
            (self.UP, 2, 0), (self.LEFT, 2, 2),
            (self.DOWN, 0, 2), (self.RIGHT, 0, 0)
        ]
        self._cycle_edges(positions)
        self.move_history.append("F'")

    def B(self):
        self._rotate_face_clockwise(self.BACK)
        positions = [
            (self.UP, 0, 2), (self.LEFT, 0, 0),
            (self.DOWN, 2, 0), (self.RIGHT, 2, 2)
        ]
        self._cycle_edges(positions)
        self.move_history.append("B")

    def B_prime(self):
        self._rotate_face_counterclockwise(self.BACK)
        positions = [
            (self.UP, 0, 2), (self.RIGHT, 2, 2),
            (self.DOWN, 2, 0), (self.LEFT, 0, 0)
        ]
        self._cycle_edges(positions)
        self.move_history.append("B'")

    def apply_move(self, move):
        move_map = {
            "U": self.U,
            "U'": self.U_prime,
            "D": self.D,
            "D'": self.D_prime,
            "R": self.R,
            "R'": self.R_prime,
            "L": self.L,
            "L'": self.L_prime,
            "F": self.F,
            "F'": self.F_prime,
            "B": self.B,
            "B'": self.B_prime
        }
        if move in move_map:
            move_map[move]()

    def apply_moves(self, moves):
        for move in moves:
            self.apply_move(move)

    def scramble(self, num_moves=20):
        moves = ["U", "U'", "D", "D'", "R", "R'", "L", "L'", "F", "F'", "B", "B'"]
        scramble_moves = []
        for _ in range(num_moves):
            move = random.choice(moves)
            scramble_moves.append(move)
            self.apply_move(move)
        return scramble_moves

    def print_cube(self):
        face_names = ["UP", "DOWN", "FRONT", "BACK", "RIGHT", "LEFT"]
        for i, face in enumerate(self.faces):
            print(f"\n{face_names[i]} Face:")
            for row in face:
                print(" ".join([self.COLORS[color] for color in row]))

    def get_face_colors(self, face_idx):
        face = self.faces[face_idx]
        return [[self.COLORS[color] for color in row] for row in face]

    def get_color_counts(self):
        counts = {color_idx: 0 for color_idx in self.COLORS.keys()}
        for face in self.faces:
            for row in face:
                for color in row:
                    counts[color] += 1
        return counts

cube_bp = Blueprint('cube', __name__)

@cube_bp.route('/cube/new', methods=['POST'])
def create_new_cube():
    cube = RubiksCube()
    counts = cube.get_color_counts()
    return jsonify({
        'success': True,
        'cube_state': cube.get_state_string(),
        'is_solved': cube.is_solved(),
        'color_counts': counts,
        'faces': {
            'up': cube.get_face_colors(cube.UP),
            'down': cube.get_face_colors(cube.DOWN),
            'front': cube.get_face_colors(cube.FRONT),
            'back': cube.get_face_colors(cube.BACK),
            'right': cube.get_face_colors(cube.RIGHT),
            'left': cube.get_face_colors(cube.LEFT)
        }
    })

@cube_bp.route('/cube/scramble', methods=['POST'])
def scramble_cube():
    data = request.get_json()
    num_moves = data.get('num_moves', 20)
    cube = RubiksCube()
    scramble_moves = cube.scramble(num_moves)
    counts = cube.get_color_counts()
    return jsonify({
        'success': True,
        'scramble_moves': scramble_moves,
        'color_counts': counts,
        'cube_state': cube.get_state_string(),
        'is_solved': cube.is_solved(),
        'faces': cube.get_face_colors()
    })

@cube_bp.route('/cube/apply_move', methods=['POST'])
def apply_move():
    data = request.get_json()
    move = data.get('move')
    cube = RubiksCube()
    cube.apply_move(move)
    counts = cube.get_color_counts()
    return jsonify({
        'success': True,
        'move_applied': move,
        'color_counts': counts,
        'cube_state': cube.get_state_string(),
        'is_solved': cube.is_solved(),
        'faces': cube.get_face_colors()
    })

@cube_bp.route('/cube/solve', methods=['POST'])
def solve_cube():
    cube = RubiksCube()
    solver = RubiksCubeSolver()
    solution = solver.solve(cube)
    counts = cube.get_color_counts()
    return jsonify({
        'success': True,
        'solution': solution,
        'color_counts': counts,
        'solution_length': len(solution),
        'cube_state_after_solution': cube.get_state_string(),
        'is_solved': cube.is_solved()
    })

@cube_bp.route('/cube/validate_moves', methods=['POST'])
def validate_moves():
    data = request.get_json()
    moves = data.get('moves', [])
    valid_moves = ["U", "U'", "D", "D'", "R", "R'", "L", "L'", "F", "F'", "B", "B'"]
    invalid_moves = [move for move in moves if move not in valid_moves]
    return jsonify({
        'success': True,
        'valid': len(invalid_moves) == 0,
        'invalid_moves': invalid_moves
    })