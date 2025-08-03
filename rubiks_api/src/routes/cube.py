"""
Rubik's Cube API Routes

This module provides REST API endpoints for the Rubik's Cube solver.
"""

from flask import Blueprint, request, jsonify
import sys
import os

# Add the parent directory to the path to import our cube modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..'))

from backend.cube import RubiksCube
from backend.solver import RubiksCubeSolver

cube_bp = Blueprint('cube', __name__)

@cube_bp.route('/cube/new', methods=['POST'])
def create_new_cube():
    """Create a new solved Rubik's Cube."""
    try:
        cube = RubiksCube()
        return jsonify({
            'success': True,
            'cube_state': cube.get_state_string(),
            'is_solved': cube.is_solved(),
            'faces': {
                'up': cube.get_face_colors(cube.UP),
                'down': cube.get_face_colors(cube.DOWN),
                'front': cube.get_face_colors(cube.FRONT),
                'back': cube.get_face_colors(cube.BACK),
                'right': cube.get_face_colors(cube.RIGHT),
                'left': cube.get_face_colors(cube.LEFT)
            }
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@cube_bp.route('/cube/scramble', methods=['POST'])
def scramble_cube():
    """Scramble a Rubik's Cube."""
    try:
        data = request.get_json()
        num_moves = data.get('num_moves', 20)
        
        cube = RubiksCube()
        scramble_moves = cube.scramble(num_moves)
        
        return jsonify({
            'success': True,
            'scramble_moves': scramble_moves,
            'cube_state': cube.get_state_string(),
            'is_solved': cube.is_solved(),
            'faces': {
                'up': cube.get_face_colors(cube.UP),
                'down': cube.get_face_colors(cube.DOWN),
                'front': cube.get_face_colors(cube.FRONT),
                'back': cube.get_face_colors(cube.BACK),
                'right': cube.get_face_colors(cube.RIGHT),
                'left': cube.get_face_colors(cube.LEFT)
            }
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@cube_bp.route('/cube/apply_move', methods=['POST'])
def apply_move():
    """Apply a single move to the cube."""
    try:
        data = request.get_json()
        cube_state = data.get('cube_state')
        move = data.get('move')
        
        if not cube_state or not move:
            return jsonify({'success': False, 'error': 'Missing cube_state or move'}), 400
        
        # Create cube from state (simplified - in a real app, you'd reconstruct the cube)
        cube = RubiksCube()
        # For now, we'll just apply the move to a new cube
        # In a real implementation, you'd reconstruct the cube from the state string
        cube.apply_move(move)
        
        return jsonify({
            'success': True,
            'move_applied': move,
            'cube_state': cube.get_state_string(),
            'is_solved': cube.is_solved(),
            'faces': {
                'up': cube.get_face_colors(cube.UP),
                'down': cube.get_face_colors(cube.DOWN),
                'front': cube.get_face_colors(cube.FRONT),
                'back': cube.get_face_colors(cube.BACK),
                'right': cube.get_face_colors(cube.RIGHT),
                'left': cube.get_face_colors(cube.LEFT)
            }
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@cube_bp.route('/cube/solve', methods=['POST'])
def solve_cube():
    """Solve a Rubik's Cube."""
    try:
        data = request.get_json()
        cube_state = data.get('cube_state')
        
        if not cube_state:
            return jsonify({'success': False, 'error': 'Missing cube_state'}), 400
        
        # Create cube from state (simplified)
        cube = RubiksCube()
        # For demonstration, let's scramble it first
        cube.scramble(5)
        
        solver = RubiksCubeSolver()
        solution = solver.solve(cube)
        
        return jsonify({
            'success': True,
            'solution': solution,
            'solution_length': len(solution),
            'cube_state_after_solution': cube.get_state_string(),
            'is_solved': cube.is_solved()
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@cube_bp.route('/cube/validate_moves', methods=['POST'])
def validate_moves():
    """Validate a sequence of moves."""
    try:
        data = request.get_json()
        moves = data.get('moves', [])
        
        valid_moves = ["U", "U'", "D", "D'", "R", "R'", "L", "L'", "F", "F'", "B", "B'"]
        invalid_moves = [move for move in moves if move not in valid_moves]
        
        return jsonify({
            'success': True,
            'valid': len(invalid_moves) == 0,
            'invalid_moves': invalid_moves,
            'valid_moves': valid_moves
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

