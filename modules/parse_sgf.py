from os import listdir
from sgfmill.sgf import Sgf_game


class SGFUtil:
    def divide_corners(game):
        top_left = []
        top_right = []
        bottom_left = []
        bottom_right = []

        # Skip the root node which has general information of game.
        # Start looking at moves.
        for move in game.get_main_sequence()[1:]:

            m, coordinate = move.get_move()
            x, y = coordinate

            if x < 9 and y < 9:
                top_left.append(move)
            elif x < 9 and y > 9:
                bottom_left.append(move)
            elif x > 9 and y < 9:
                top_right.append(move)
            elif x > 9 and y > 9:
                bottom_right.append(move)

        return [top_left, bottom_left, top_right, bottom_right]

    def align_corner(corner):

        # Check first node
        color, coordinate = corner[0].get_move()

        # If first node not in top right corner, reflect corner
        if coordinate[0] > 9 or coordinate[1] > 9:
            corner = SGFUtil.reflect_corner(corner)

        # If first node is white, reflect colors
        if color == "w":
            corner = SGFUtil.reflect_color(corner)

        # If first non-axis move starts on lower bound, reflect coordinates
        # TODO: handle case where first non axis move is None
        color, coordinate = SGFUtil.first_non_axis(corner).get_move()
        if coordinate[1] > coordinate[0]:
            corner = SGFUtil.reflect_coordinate(corner)

        return corner

    def reflect_corner(corner):
        for i in range(len(corner)):
            color, coordinate = corner[i].get_move()
            x, y = coordinate
            new_x, new_y = x, y

            if x > 9:
                new_x = 18 - x

            if y > 9:
                new_y = 18 - y

            corner[i].set_move(color, (new_x, new_y))

        return corner

    def reflect_coordinate(corner):
        for i in range(len(corner)):
            color, coordinate = corner[i].get_move()
            x, y = coordinate

            corner[i].set_move(color, (y, x))

        return corner

    def reflect_color(corner):
        for i in range(len(corner)):
            color, coordinate = corner[i].get_move()

            if color == "w":
                corner[i].set_move("b", coordinate)

            if color == "b":
                corner[i].set_move("w", coordinate)

        return corner

    def first_non_axis(corner):
        for move in corner:
            _, coordinate = move.get_move()
            if coordinate[0] != coordinate[1]:
                return move

        return None


if __name__ == "__main__":

    files = listdir("../data")
    file = "../data/" + files[-1]
    with open(file, "rb") as f:
        game = Sgf_game.from_bytes(f.read())

        corners = SGFUtil.divide_corners(game)
        print(len(corners))
        for corner in corners:
            test = SGFUtil.align_corner(corner)
            print("-" * 20)
            for move in test:
                print(move.get_move())
            print("-" * 20)
