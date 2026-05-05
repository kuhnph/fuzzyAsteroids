from pathlib import Path


def append_csv_row(x, y, filename):
    """
    Append a simple x,y row to a text file.
    """
    path = Path(filename)
    with path.open("a", encoding="utf-8") as file:
        file.write(f"{x},{y}\n")


def write_generation_cost(generation, best_cost, filename="generation_cost.txt"):
    append_csv_row(generation, best_cost, filename)


def write_velocity_sample(time_step, velocity, filename="velocity_time.txt"):
    append_csv_row(time_step, velocity, filename)


def write_position_error_sample(time_step, position_error, filename="positionError_time.txt"):
    append_csv_row(time_step, position_error, filename)