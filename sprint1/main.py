import matplotlib

matplotlib.use("TkAgg")

from sprint1 import gol_basic_simulation as gl
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


def main():
    grid = gl.Grid()
    grid.loadstate(4)

    fig, ax = plt.subplots()
    image = ax.imshow(grid.grid, cmap="binary", vmin=0, vmax=1)

    def update(frame):
        grid.nextstate()
        image.set_data(grid.grid)
        ax.set_title(f"Generation {frame + 1}")
        return (image,)

    ani = FuncAnimation(fig, update, frames=200, interval=200, repeat=False)

    plt.show()


if __name__ == "__main__":
    main()
