import sys
import random
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QLineEdit, 
    QPushButton, QListWidget, QHBoxLayout
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt, QTimer

class BagelsGame(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Bagels Game")
        self.setGeometry(100, 100, 600, 500)
        self.initUI()
        self.new_game()  # Start the first game (and set a random background color)

    def initUI(self):
        # Create the central widget and main layout.
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout(self.central_widget)

        # Title label with a stylish font.
        self.title_label = QLabel("Bagels Game", self)
        title_font = QFont("Arial", 28, QFont.Bold)
        self.title_label.setFont(title_font)
        self.title_label.setAlignment(Qt.AlignCenter)
        self.main_layout.addWidget(self.title_label)

        # Instructions.
        instructions = (
            "I am thinking of a 3-digit number. Try to guess what it is.\n\n"
            "Clues:\n"
            "  Pico  - One digit is correct but in the wrong position.\n"
            "  Fermi - One digit is correct and in the right position.\n"
            "  Bagels- No digit is correct.\n\n"
            "You have 10 guesses to get it."
        )
        self.instructions_label = QLabel(instructions, self)
        self.instructions_label.setWordWrap(True)
        self.instructions_label.setAlignment(Qt.AlignCenter)
        instr_font = QFont("Arial", 12)
        self.instructions_label.setFont(instr_font)
        self.main_layout.addWidget(self.instructions_label)

        # Input area (a QLineEdit and Submit button).
        self.input_layout = QHBoxLayout()
        self.guess_input = QLineEdit(self)
        self.guess_input.setMaxLength(3)
        input_font = QFont("Arial", 18)
        self.guess_input.setFont(input_font)
        self.guess_input.setAlignment(Qt.AlignCenter)
        self.input_layout.addWidget(self.guess_input)

        self.submit_button = QPushButton("Submit Guess", self)
        button_font = QFont("Arial", 16, QFont.Bold)
        self.submit_button.setFont(button_font)
        self.submit_button.clicked.connect(self.submit_guess)
        self.input_layout.addWidget(self.submit_button)
        self.main_layout.addLayout(self.input_layout)

        # A list widget to show the guess history.
        self.history_list = QListWidget(self)
        self.history_list.setFont(QFont("Arial", 12))
        self.main_layout.addWidget(self.history_list)

        # A label to display result messages or motivational feedback.
        self.result_label = QLabel("", self)
        self.result_label.setAlignment(Qt.AlignCenter)
        self.result_label.setFont(QFont("Arial", 14, QFont.Bold))
        self.main_layout.addWidget(self.result_label)

        # Restart button (disabled until game ends).
        self.restart_button = QPushButton("Restart Game", self)
        self.restart_button.setFont(button_font)
        self.restart_button.clicked.connect(self.new_game)
        self.main_layout.addWidget(self.restart_button)
        self.restart_button.setEnabled(False)

    def random_color(self):
        """Generate a random hex color string."""
        r = lambda: random.randint(0, 255)
        return '#{0:02X}{1:02X}{2:02X}'.format(r(), r(), r())

    def apply_styles(self):
        """
        Apply a stylesheet to the entire application.
        The main window's background color is randomized each time this is called.
        """
        bg_color = self.random_color()
        style = f"""
            QMainWindow {{
                background-color: {bg_color};
            }}
            QLabel {{
                color: #ecf0f1;
            }}
            QLineEdit {{
                background-color: #ecf0f1;
                border: 2px solid #3498db;
                border-radius: 8px;
                padding: 5px;
                color: #2c3e50;
            }}
            QPushButton {{
                background-color: #3498db;
                border: none;
                border-radius: 8px;
                padding: 8px;
                color: #ecf0f1;
            }}
            QPushButton:hover {{
                background-color: #2980b9;
            }}
            QPushButton:disabled {{
                background-color: #95a5a6;
            }}
            QListWidget {{
                background-color: #ecf0f1;
                border: 2px solid #3498db;
                border-radius: 8px;
                padding: 5px;
                color: #2c3e50;
            }}
        """
        self.setStyleSheet(style)

    def new_game(self):
        """Start a new game by generating a new number, resetting the state, and updating the style."""
        # Update the background with a random color.
        self.apply_styles()

        self.hidden_number = ''.join([str(random.randint(0, 9)) for _ in range(3)])
        self.guess_count = 0
        self.history_list.clear()
        self.result_label.setText("Game started! Enter your guess.")
        self.result_label.setStyleSheet("color: #ecf0f1;")
        self.guess_input.setEnabled(True)
        self.submit_button.setEnabled(True)
        self.restart_button.setEnabled(False)
        self.guess_input.clear()
        self.guess_input.setFocus()

    def submit_guess(self):
        guess = self.guess_input.text().strip()
        if len(guess) != 3 or not guess.isdigit():
            self.result_label.setText("Please enter a valid 3-digit number.")
            return

        self.guess_count += 1
        clues = self.get_clues(guess)
        self.history_list.addItem(f"Guess #{self.guess_count}: {guess}  =>  Clues: {clues}")

        if guess == self.hidden_number:
            self.result_label.setText("You got it! Congratulations!")
            self.result_label.setStyleSheet("color: #2ecc71; font-weight: bold;")
            self.end_game(win=True)
        elif self.guess_count >= 10:
            self.result_label.setText(f"You lose! The correct number was {self.hidden_number}.")
            self.result_label.setStyleSheet("color: #e74c3c; font-weight: bold;")
            self.end_game(win=False)
        else:
            # Playful motivational messages.
            messages = [
                "Keep going, you're doing great!",
                "Don't give up!",
                "You can do it!",
                "Almost there, try another guess!"
            ]
            self.result_label.setText(random.choice(messages))

        self.guess_input.clear()
        self.guess_input.setFocus()

    def get_clues(self, guess):
        """Return clues by comparing the guess to the hidden number."""
        clues = []
        for i in range(3):
            if guess[i] == self.hidden_number[i]:
                clues.append("Fermi")
            elif guess[i] in self.hidden_number:
                clues.append("Pico")
        if not clues:
            clues.append("Bagels")
        return " ".join(clues)

    def end_game(self, win):
        """Disable input and enable the restart button."""
        self.guess_input.setEnabled(False)
        self.submit_button.setEnabled(False)
        self.restart_button.setEnabled(True)
        # Optional: Reset the feedback label color after a short delay.
        QTimer.singleShot(3000, lambda: self.result_label.setStyleSheet("color: #ecf0f1;"))

def main():
    app = QApplication(sys.argv)
    window = BagelsGame()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
