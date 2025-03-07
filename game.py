import numpy as np

X_GAME_SIZE = 7
Y_GAME_SIZE = 6


class Game:
    def __init__(self):
        self.board = np.zeros((Y_GAME_SIZE, X_GAME_SIZE), dtype=int)  # 0: leer, 1: Spieler 1, -1: Spieler 2
        self.current_player = 1

    def reset(self):
        self.board = np.zeros((Y_GAME_SIZE, X_GAME_SIZE), dtype=int)
        self.current_player = 1
        return self.board.flatten()

    def get_available_actions(self):
        """Gibt eine Liste aller möglichen Züge (freie Felder) zurück."""
        available_actions = []
        for j in range(X_GAME_SIZE):
            for i in range(Y_GAME_SIZE - 1, -1, -1):  # Iterate from bottom to top
                if self.board[i, j] == 0:
                    available_actions.append((i, j))
                    break  # Only add the bottom-most free cell
        return available_actions


    def check_winner(self):
        """Prüft, ob es einen Gewinner gibt. Gibt 1 oder -1 zurück, wenn ja, sonst 0."""
        # Zeilen
        for i in range(Y_GAME_SIZE):
            for j in range(X_GAME_SIZE - 3):
                if (self.board[i, j] != 0 and
                        self.board[i, j] == self.board[i, j + 1] and
                        self.board[i, j] == self.board[i, j + 2] and
                        self.board[i, j] == self.board[i, j + 3]):
                    return self.board[i, j]

        # Spalten
        for j in range(X_GAME_SIZE):
            for i in range(Y_GAME_SIZE - 3):
                if (self.board[i, j] != 0 and
                        self.board[i, j] == self.board[i + 1, j] and
                        self.board[i, j] == self.board[i + 2, j] and
                        self.board[i, j] == self.board[i + 3, j]):
                    return self.board[i, j]

        # Diagonalen (von links oben nach rechts unten)
        for i in range(Y_GAME_SIZE - 3):
            for j in range(X_GAME_SIZE - 3):
                if (self.board[i, j] != 0 and
                        self.board[i, j] == self.board[i + 1, j + 1] and
                        self.board[i, j] == self.board[i + 2, j + 2] and
                        self.board[i, j] == self.board[i + 3, j + 3]):
                    return self.board[i, j]

        # Diagonalen (von rechts oben nach links unten)
        for i in range(Y_GAME_SIZE - 3):
            for j in range(3, X_GAME_SIZE):
                if (self.board[i, j] != 0 and
                        self.board[i, j] == self.board[i + 1, j - 1] and
                        self.board[i, j] == self.board[i + 2, j - 2] and
                        self.board[i, j] == self.board[i + 3, j - 3]):
                    return self.board[i, j]

        # Unentschieden
        if not np.any(self.board == 0):
            return 0  # Unentschieden

        return None



    def is_done(self):
        """Prüft, ob das Spiel beendet ist (Gewinner oder Unentschieden)."""
        return self.check_winner() is not None

    def make_move(self, action):
        """Führt einen Zug aus und wechselt den Spieler."""
        i, j = action

        if self.board[i, j] != 0:
            raise ValueError("Ungültiger Zug: Feld ist bereits belegt.")
        self.board[i, j] = self.current_player
        self.current_player *= -1

    def map_number_to_action(self, number):
        """Ordnet eine Spalte (1-7) einem (Zeile, Spalte)-Tupel zu."""
        col = number - 1  # Adjust for 0-based indexing

        if not 0 <= col < X_GAME_SIZE:
            raise ValueError("Ungültige Spaltennummer.")

        for row in range(Y_GAME_SIZE -1, -1, -1):  # Iterate from bottom to top
            if self.board[row, col] == 0:
                return (row, col)

        raise ValueError("Spalte ist voll.")

    def render(self):
        """Gibt das Spielfeld in der Konsole aus."""
        YELLOW = '\033[93m'  # Gelb
        RED = '\033[91m'  # Rot
        RESET = '\033[0m'  # Zurücksetzen der Farbe

        symbols = {0: ' ', 1: YELLOW + 'X' + RESET, -1: RED + 'O' + RESET}
        for i in range(Y_GAME_SIZE):
            row_str = ' | '.join(symbols[self.board[i, j]] for j in range(X_GAME_SIZE))
            print(row_str)
            if i < Y_GAME_SIZE - 1:
                print('-------------------------')

    def get_state(self):
        """Gibt den aktuellen Zustand des Spiels zurück (als flaches Array)."""
        return self.board.flatten()


if __name__ == '__main__':
    game = Game()

    while not game.is_done():
        game.render()
        player = 1 if game.current_player == 1 else 2  # Zuordnen von 1 und -1 zu Spieler 1 und 2
        while True:
            try:
                #print (game.get_available_actions())
                move = int(input(f"Spieler {player}, gib die Nummer der Spalte ein (1-7): "))
                if 1 <= move <= 7:
                    action = game.map_number_to_action(move)
                    if game.board[action[0], action[1]] == 0:
                        print(action)
                        break
                    else:
                        print("Ungültiger Zug. Bitte wähle ein freies Feld.")
                else:
                    print("Ungültige Eingabe. Bitte gib eine Zahl zwischen 1 und 7 ein.")
            except ValueError as e:
                print(f"Ungültige Eingabe: {e}")

        game.make_move(action)

    game.render()
    winner = game.check_winner()
    if winner == 1:
        print('\033[93m' + "Spieler 1 hat gewonnen!")
    elif winner == -1:
        print('\033[91m' + "Spieler 2 hat gewonnen!")
    else:
        print("Unentschieden!")