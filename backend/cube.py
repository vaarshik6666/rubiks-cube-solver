"""
Rubik's Cube Data Structure and Move Engine

This module implements the core representation of a 3x3 Rubik's Cube
and provides methods for applying moves and tracking state.
"""

import copy
import random
from typing import List, Dict, Tuple


class RubiksCube:
    """
    Represents a 3x3 Rubik's Cube using face-based representation.
    
    Each face is represented as a 3x3 array where:
    - 0: White (Up)
    - 1: Yellow (Down) 
    - 2: Red (Front)
    - 3: Orange (Back)
    - 4: Green (Right)
    - 5: Blue (Left)
    """
    
    # Face indices
    UP = 0
    DOWN = 1
    FRONT = 2
    BACK = 3
    RIGHT = 4
    LEFT = 5
    
    # Color mapping for visualization
    COLORS = {
        0: 'W',  # White
        1: 'Y',  # Yellow
        2: 'R',  # Red
        3: 'O',  # Orange
        4: 'G',  # Green
        5: 'B'   # Blue
    }
    
    def __init__(self):
        """Initialize a solved cube."""
        self.faces = []
        for i in range(6):
            # Each face starts with all squares the same color
            face = [[i for _ in range(3)] for _ in range(3)]
            self.faces.append(face)
        
        # Track move history for solving
        self.move_history = []
    
    def copy(self):
        """Create a deep copy of the cube."""
        new_cube = RubiksCube()
        new_cube.faces = copy.deepcopy(self.faces)
        new_cube.move_history = self.move_history.copy()
        return new_cube
    
    def is_solved(self) -> bool:
        """Check if the cube is in solved state."""
        for face_idx, face in enumerate(self.faces):
            for row in face:
                for color in row:
                    if color != face_idx:
                        return False
        return True
    
    def get_state_string(self) -> str:
        """Get a string representation of the cube state."""
        state = ""
        for face in self.faces:
            for row in face:
                for color in row:
                    state += str(color)
        return state
    
    def _rotate_face_clockwise(self, face_idx: int):
        """Rotate a face 90 degrees clockwise."""
        face = self.faces[face_idx]
        # Transpose and reverse each row for 90-degree clockwise rotation
        rotated = [[face[2-j][i] for j in range(3)] for i in range(3)]
        self.faces[face_idx] = rotated
    
    def _rotate_face_counterclockwise(self, face_idx: int):
        """Rotate a face 90 degrees counterclockwise."""
        # Rotate clockwise 3 times = counterclockwise once
        for _ in range(3):
            self._rotate_face_clockwise(face_idx)
    
    def _cycle_edges(self, positions: List[Tuple[int, int, int]], clockwise: bool = True):
        """
        Cycle edge pieces between positions.
        positions: List of (face_idx, row, col) tuples
        """
        if not clockwise:
            positions = positions[::-1]
        
        # Store the first position's value
        temp = self.faces[positions[0][0]][positions[0][1]][positions[0][2]]
        
        # Cycle through positions
        for i in range(len(positions) - 1):
            curr_face, curr_row, curr_col = positions[i]
            next_face, next_row, next_col = positions[i + 1]
            self.faces[curr_face][curr_row][curr_col] = self.faces[next_face][next_row][next_col]
        
        # Set the last position to the stored value
        last_face, last_row, last_col = positions[-1]
        self.faces[last_face][last_row][last_col] = temp
    
    def U(self):
        """Up face clockwise rotation."""
        self._rotate_face_clockwise(self.UP)
        
        # Cycle the top row of adjacent faces
        positions = [
            (self.FRONT, 0, 0), (self.FRONT, 0, 1), (self.FRONT, 0, 2),
            (self.LEFT, 0, 0), (self.LEFT, 0, 1), (self.LEFT, 0, 2),
            (self.BACK, 0, 0), (self.BACK, 0, 1), (self.BACK, 0, 2),
            (self.RIGHT, 0, 0), (self.RIGHT, 0, 1), (self.RIGHT, 0, 2)
        ]
        
        # Group into sets of 3 for easier cycling
        edge_groups = [positions[i:i+3] for i in range(0, 12, 3)]
        
        # Store first group
        temp = [self.faces[pos[0]][pos[1]][pos[2]] for pos in edge_groups[0]]
        
        # Cycle groups
        for i in range(3):
            for j in range(3):
                face, row, col = edge_groups[i][j]
                next_face, next_row, next_col = edge_groups[(i + 1) % 4][j]
                self.faces[face][row][col] = self.faces[next_face][next_row][next_col]
        
        # Set last group to stored values
        for j in range(3):
            face, row, col = edge_groups[3][j]
            self.faces[face][row][col] = temp[j]
        
        self.move_history.append("U")
    
    def U_prime(self):
        """Up face counterclockwise rotation."""
        self._rotate_face_counterclockwise(self.UP)
        
        # Cycle the top row of adjacent faces (reverse direction)
        positions = [
            (self.FRONT, 0, 0), (self.FRONT, 0, 1), (self.FRONT, 0, 2),
            (self.RIGHT, 0, 0), (self.RIGHT, 0, 1), (self.RIGHT, 0, 2),
            (self.BACK, 0, 0), (self.BACK, 0, 1), (self.BACK, 0, 2),
            (self.LEFT, 0, 0), (self.LEFT, 0, 1), (self.LEFT, 0, 2)
        ]
        
        # Group into sets of 3 for easier cycling
        edge_groups = [positions[i:i+3] for i in range(0, 12, 3)]
        
        # Store first group
        temp = [self.faces[pos[0]][pos[1]][pos[2]] for pos in edge_groups[0]]
        
        # Cycle groups
        for i in range(3):
            for j in range(3):
                face, row, col = edge_groups[i][j]
                next_face, next_row, next_col = edge_groups[(i + 1) % 4][j]
                self.faces[face][row][col] = self.faces[next_face][next_row][next_col]
        
        # Set last group to stored values
        for j in range(3):
            face, row, col = edge_groups[3][j]
            self.faces[face][row][col] = temp[j]
        
        self.move_history.append("U'")
    
    def D(self):
        """Down face clockwise rotation."""
        self._rotate_face_clockwise(self.DOWN)
        
        # Cycle the bottom row of adjacent faces
        edge_groups = [
            [(self.FRONT, 2, 0), (self.FRONT, 2, 1), (self.FRONT, 2, 2)],
            [(self.RIGHT, 2, 0), (self.RIGHT, 2, 1), (self.RIGHT, 2, 2)],
            [(self.BACK, 2, 0), (self.BACK, 2, 1), (self.BACK, 2, 2)],
            [(self.LEFT, 2, 0), (self.LEFT, 2, 1), (self.LEFT, 2, 2)]
        ]
        
        # Store first group
        temp = [self.faces[pos[0]][pos[1]][pos[2]] for pos in edge_groups[0]]
        
        # Cycle groups
        for i in range(3):
            for j in range(3):
                face, row, col = edge_groups[i][j]
                next_face, next_row, next_col = edge_groups[(i + 1) % 4][j]
                self.faces[face][row][col] = self.faces[next_face][next_row][next_col]
        
        # Set last group to stored values
        for j in range(3):
            face, row, col = edge_groups[3][j]
            self.faces[face][row][col] = temp[j]
        
        self.move_history.append("D")
    
    def D_prime(self):
        """Down face counterclockwise rotation."""
        self._rotate_face_counterclockwise(self.DOWN)
        
        # Cycle the bottom row of adjacent faces (reverse direction)
        edge_groups = [
            [(self.FRONT, 2, 0), (self.FRONT, 2, 1), (self.FRONT, 2, 2)],
            [(self.LEFT, 2, 0), (self.LEFT, 2, 1), (self.LEFT, 2, 2)],
            [(self.BACK, 2, 0), (self.BACK, 2, 1), (self.BACK, 2, 2)],
            [(self.RIGHT, 2, 0), (self.RIGHT, 2, 1), (self.RIGHT, 2, 2)]
        ]
        
        # Store first group
        temp = [self.faces[pos[0]][pos[1]][pos[2]] for pos in edge_groups[0]]
        
        # Cycle groups
        for i in range(3):
            for j in range(3):
                face, row, col = edge_groups[i][j]
                next_face, next_row, next_col = edge_groups[(i + 1) % 4][j]
                self.faces[face][row][col] = self.faces[next_face][next_row][next_col]
        
        # Set last group to stored values
        for j in range(3):
            face, row, col = edge_groups[3][j]
            self.faces[face][row][col] = temp[j]
        
        self.move_history.append("D'")
    
    def R(self):
        """Right face clockwise rotation."""
        self._rotate_face_clockwise(self.RIGHT)
        
        # Cycle the right column of adjacent faces
        edge_groups = [
            [(self.FRONT, 0, 2), (self.FRONT, 1, 2), (self.FRONT, 2, 2)],
            [(self.UP, 0, 2), (self.UP, 1, 2), (self.UP, 2, 2)],
            [(self.BACK, 2, 0), (self.BACK, 1, 0), (self.BACK, 0, 0)],  # Back face is flipped
            [(self.DOWN, 0, 2), (self.DOWN, 1, 2), (self.DOWN, 2, 2)]
        ]
        
        # Store first group
        temp = [self.faces[pos[0]][pos[1]][pos[2]] for pos in edge_groups[0]]
        
        # Cycle groups
        for i in range(3):
            for j in range(3):
                face, row, col = edge_groups[i][j]
                next_face, next_row, next_col = edge_groups[(i + 1) % 4][j]
                self.faces[face][row][col] = self.faces[next_face][next_row][next_col]
        
        # Set last group to stored values
        for j in range(3):
            face, row, col = edge_groups[3][j]
            self.faces[face][row][col] = temp[j]
        
        self.move_history.append("R")
    
    def R_prime(self):
        """Right face counterclockwise rotation."""
        self._rotate_face_counterclockwise(self.RIGHT)
        
        # Cycle the right column of adjacent faces (reverse direction)
        edge_groups = [
            [(self.FRONT, 0, 2), (self.FRONT, 1, 2), (self.FRONT, 2, 2)],
            [(self.DOWN, 0, 2), (self.DOWN, 1, 2), (self.DOWN, 2, 2)],
            [(self.BACK, 2, 0), (self.BACK, 1, 0), (self.BACK, 0, 0)],  # Back face is flipped
            [(self.UP, 0, 2), (self.UP, 1, 2), (self.UP, 2, 2)]
        ]
        
        # Store first group
        temp = [self.faces[pos[0]][pos[1]][pos[2]] for pos in edge_groups[0]]
        
        # Cycle groups
        for i in range(3):
            for j in range(3):
                face, row, col = edge_groups[i][j]
                next_face, next_row, next_col = edge_groups[(i + 1) % 4][j]
                self.faces[face][row][col] = self.faces[next_face][next_row][next_col]
        
        # Set last group to stored values
        for j in range(3):
            face, row, col = edge_groups[3][j]
            self.faces[face][row][col] = temp[j]
        
        self.move_history.append("R'")
    
    def L(self):
        """Left face clockwise rotation."""
        self._rotate_face_clockwise(self.LEFT)
        
        # Cycle the left column of adjacent faces
        edge_groups = [
            [(self.FRONT, 0, 0), (self.FRONT, 1, 0), (self.FRONT, 2, 0)],
            [(self.DOWN, 0, 0), (self.DOWN, 1, 0), (self.DOWN, 2, 0)],
            [(self.BACK, 2, 2), (self.BACK, 1, 2), (self.BACK, 0, 2)],  # Back face is flipped
            [(self.UP, 0, 0), (self.UP, 1, 0), (self.UP, 2, 0)]
        ]
        
        # Store first group
        temp = [self.faces[pos[0]][pos[1]][pos[2]] for pos in edge_groups[0]]
        
        # Cycle groups
        for i in range(3):
            for j in range(3):
                face, row, col = edge_groups[i][j]
                next_face, next_row, next_col = edge_groups[(i + 1) % 4][j]
                self.faces[face][row][col] = self.faces[next_face][next_row][next_col]
        
        # Set last group to stored values
        for j in range(3):
            face, row, col = edge_groups[3][j]
            self.faces[face][row][col] = temp[j]
        
        self.move_history.append("L")
    
    def L_prime(self):
        """Left face counterclockwise rotation."""
        self._rotate_face_counterclockwise(self.LEFT)
        
        # Cycle the left column of adjacent faces (reverse direction)
        edge_groups = [
            [(self.FRONT, 0, 0), (self.FRONT, 1, 0), (self.FRONT, 2, 0)],
            [(self.UP, 0, 0), (self.UP, 1, 0), (self.UP, 2, 0)],
            [(self.BACK, 2, 2), (self.BACK, 1, 2), (self.BACK, 0, 2)],  # Back face is flipped
            [(self.DOWN, 0, 0), (self.DOWN, 1, 0), (self.DOWN, 2, 0)]
        ]
        
        # Store first group
        temp = [self.faces[pos[0]][pos[1]][pos[2]] for pos in edge_groups[0]]
        
        # Cycle groups
        for i in range(3):
            for j in range(3):
                face, row, col = edge_groups[i][j]
                next_face, next_row, next_col = edge_groups[(i + 1) % 4][j]
                self.faces[face][row][col] = self.faces[next_face][next_row][next_col]
        
        # Set last group to stored values
        for j in range(3):
            face, row, col = edge_groups[3][j]
            self.faces[face][row][col] = temp[j]
        
        self.move_history.append("L'")
    
    def F(self):
        """Front face clockwise rotation."""
        self._rotate_face_clockwise(self.FRONT)
        
        # Cycle the adjacent edges
        edge_groups = [
            [(self.UP, 2, 0), (self.UP, 2, 1), (self.UP, 2, 2)],
            [(self.RIGHT, 0, 0), (self.RIGHT, 1, 0), (self.RIGHT, 2, 0)],
            [(self.DOWN, 0, 2), (self.DOWN, 0, 1), (self.DOWN, 0, 0)],  # Down face is flipped
            [(self.LEFT, 2, 2), (self.LEFT, 1, 2), (self.LEFT, 0, 2)]   # Left face is flipped
        ]
        
        # Store first group
        temp = [self.faces[pos[0]][pos[1]][pos[2]] for pos in edge_groups[0]]
        
        # Cycle groups
        for i in range(3):
            for j in range(3):
                face, row, col = edge_groups[i][j]
                next_face, next_row, next_col = edge_groups[(i + 1) % 4][j]
                self.faces[face][row][col] = self.faces[next_face][next_row][next_col]
        
        # Set last group to stored values
        for j in range(3):
            face, row, col = edge_groups[3][j]
            self.faces[face][row][col] = temp[j]
        
        self.move_history.append("F")
    
    def F_prime(self):
        """Front face counterclockwise rotation."""
        self._rotate_face_counterclockwise(self.FRONT)
        
        # Cycle the adjacent edges (reverse direction)
        edge_groups = [
            [(self.UP, 2, 0), (self.UP, 2, 1), (self.UP, 2, 2)],
            [(self.LEFT, 2, 2), (self.LEFT, 1, 2), (self.LEFT, 0, 2)],   # Left face is flipped
            [(self.DOWN, 0, 2), (self.DOWN, 0, 1), (self.DOWN, 0, 0)],  # Down face is flipped
            [(self.RIGHT, 0, 0), (self.RIGHT, 1, 0), (self.RIGHT, 2, 0)]
        ]
        
        # Store first group
        temp = [self.faces[pos[0]][pos[1]][pos[2]] for pos in edge_groups[0]]
        
        # Cycle groups
        for i in range(3):
            for j in range(3):
                face, row, col = edge_groups[i][j]
                next_face, next_row, next_col = edge_groups[(i + 1) % 4][j]
                self.faces[face][row][col] = self.faces[next_face][next_row][next_col]
        
        # Set last group to stored values
        for j in range(3):
            face, row, col = edge_groups[3][j]
            self.faces[face][row][col] = temp[j]
        
        self.move_history.append("F'")
    
        def get_color_counts(self) -> Dict[int, int]:
            counts = {color_idx: 0 for color_idx in self.COLORS.keys()}
            for face in self.faces:
                for row in face:
                    for color in row:
                        counts[color] += 1
            return counts

    
    def B(self):
        """Back face clockwise rotation."""
        self._rotate_face_clockwise(self.BACK)
        
        # Cycle the adjacent edges
        edge_groups = [
            [(self.UP, 0, 2), (self.UP, 0, 1), (self.UP, 0, 0)],        # Up face is flipped
            [(self.LEFT, 0, 0), (self.LEFT, 1, 0), (self.LEFT, 2, 0)],
            [(self.DOWN, 2, 0), (self.DOWN, 2, 1), (self.DOWN, 2, 2)],
            [(self.RIGHT, 2, 2), (self.RIGHT, 1, 2), (self.RIGHT, 0, 2)] # Right face is flipped
        ]
        
        # Store first group
        temp = [self.faces[pos[0]][pos[1]][pos[2]] for pos in edge_groups[0]]
        
        # Cycle groups
        for i in range(3):
            for j in range(3):
                face, row, col = edge_groups[i][j]
                next_face, next_row, next_col = edge_groups[(i + 1) % 4][j]
                self.faces[face][row][col] = self.faces[next_face][next_row][next_col]
        
        # Set last group to stored values
        for j in range(3):
            face, row, col = edge_groups[3][j]
            self.faces[face][row][col] = temp[j]
        
        self.move_history.append("B")
    
    def B_prime(self):
        """Back face counterclockwise rotation."""
        self._rotate_face_counterclockwise(self.BACK)
        
        # Cycle the adjacent edges (reverse direction)
        edge_groups = [
            [(self.UP, 0, 2), (self.UP, 0, 1), (self.UP, 0, 0)],        # Up face is flipped
            [(self.RIGHT, 2, 2), (self.RIGHT, 1, 2), (self.RIGHT, 0, 2)], # Right face is flipped
            [(self.DOWN, 2, 0), (self.DOWN, 2, 1), (self.DOWN, 2, 2)],
            [(self.LEFT, 0, 0), (self.LEFT, 1, 0), (self.LEFT, 2, 0)]
        ]
        
        # Store first group
        temp = [self.faces[pos[0]][pos[1]][pos[2]] for pos in edge_groups[0]]
        
        # Cycle groups
        for i in range(3):
            for j in range(3):
                face, row, col = edge_groups[i][j]
                next_face, next_row, next_col = edge_groups[(i + 1) % 4][j]
                self.faces[face][row][col] = self.faces[next_face][next_row][next_col]
        
        # Set last group to stored values
        for j in range(3):
            face, row, col = edge_groups[3][j]
            self.faces[face][row][col] = temp[j]
        
        self.move_history.append("B'")
    
    def apply_move(self, move: str):
        """Apply a move to the cube."""
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
        else:
            raise ValueError(f"Invalid move: {move}")
    
    def apply_moves(self, moves: List[str]):
        """Apply a sequence of moves to the cube."""
        for move in moves:
            self.apply_move(move)
    
    def scramble(self, num_moves: int = 20):
        """Scramble the cube with random moves."""
        moves = ["U", "U'", "D", "D'", "R", "R'", "L", "L'", "F", "F'", "B", "B'"]
        scramble_moves = []
        
        for _ in range(num_moves):
            move = random.choice(moves)
            scramble_moves.append(move)
            self.apply_move(move)
        
        return scramble_moves
    
    def print_cube(self):
        """Print a visual representation of the cube."""
        face_names = ["UP", "DOWN", "FRONT", "BACK", "RIGHT", "LEFT"]
        
        for i, face in enumerate(self.faces):
            print(f"\n{face_names[i]} Face:")
            for row in face:
                print(" ".join([self.COLORS[color] for color in row]))
    
    def get_face_colors(self, face_idx: int) -> List[List[str]]:
        """Get the color representation of a face."""
        face = self.faces[face_idx]
        return [[self.COLORS[color] for color in row] for row in face]


if __name__ == "__main__":
    # Test the cube implementation
    cube = RubiksCube()
    print("Initial solved cube:")
    cube.print_cube()
    
    print(f"\nIs solved: {cube.is_solved()}")
    
    # Test some moves
    print("\nApplying moves: U R U' R'")
    cube.apply_moves(["U", "R", "U'", "R'"])
    cube.print_cube()
    
    print(f"\nIs solved: {cube.is_solved()}")
    
    # Test scrambling
    print("\nScrambling cube...")
    scramble_moves = cube.scramble(10)
    print(f"Scramble moves: {' '.join(scramble_moves)}")
    cube.print_cube()
    
    print(f"\nIs solved: {cube.is_solved()}")

