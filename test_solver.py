from backend.cube import RubiksCube
from backend.solver import RubiksCubeSolver

def test_solver():
    cube = RubiksCube()
    solver = RubiksCubeSolver()

    print("Initial cube state:")
    cube.print_cube()
    print(f"Is solved: {cube.is_solved()}")

    scramble_moves = cube.scramble(5)
    print("\nScrambled with {} moves: {}".format(len(scramble_moves), " ".join(scramble_moves)))
    print("Cube state after scramble:")
    cube.print_cube()
    print(f"Is solved after scramble: {cube.is_solved()}")

    solution = solver.solve(cube)
    print("\nSolution moves: {}".format(" ".join(solution)))
    print(f"Cube is solved after solution: {cube.is_solved()}")

if __name__ == "__main__":
    test_solver()


