
from cube import RubiksCube
import random

def run_tests():
    print("--- Testing Cube Initialization ---")
    cube = RubiksCube()
    initial_counts = cube.get_color_counts()
    print(f"Initial color counts: {initial_counts}")
    assert all(count == 9 for count in initial_counts.values()), "Initial color counts are not 9 for all colors!"
    print("Initial color distribution: OK")
    assert cube.validate_face_uniformity(), "Initial faces are not uniform!"
    print("Initial face uniformity: OK")

    print("\n--- Testing Scramble and Color Preservation ---")
    moves = ["U", "U_prime", "D", "D_prime", "R", "R_prime", "L", "L_prime", "F", "F_prime", "B", "B_prime"]
    num_scrambles = 20
    for _ in range(num_scrambles):
        move = random.choice(moves)
        getattr(cube, move)()
    
    scrambled_counts = cube.get_color_counts()
    print(f"Color counts after {num_scrambles} scrambles: {scrambled_counts}")
    assert all(count == 9 for count in scrambled_counts.values()), "Color counts are not 9 after scramble!"
    print("Color distribution after scramble: OK")

    print("\n--- Testing Solve and Final State ---")
    # This part assumes a solver exists. For now, we'll just check if it's not solved.
    # In a real scenario, you'd call a solver here and then verify the solved state.
    if not cube.is_solved():
        print("Cube is scrambled (as expected).")
    else:
        print("Cube is unexpectedly solved after scramble.")

    # For demonstration, let's re-initialize and check solved state
    cube_solved = RubiksCube()
    print(f"Color counts after re-initialization (solved): {cube_solved.get_color_counts()}")
    assert cube_solved.is_solved(), "Re-initialized cube is not solved!"
    print("Re-initialized cube is solved: OK")
    assert cube_solved.validate_color_balance(), "Re-initialized cube color balance is off!"
    print("Re-initialized cube color balance: OK")
    assert cube_solved.validate_face_uniformity(), "Re-initialized cube face uniformity is off!"
    print("Re-initialized cube face uniformity: OK")

    print("\nAll tests passed!")

if __name__ == "__main__":
    run_tests()


