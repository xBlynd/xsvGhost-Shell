import time
import random
import shutil

# Get terminal size
cols = shutil.get_terminal_size().columns

print("\033[32m") # Set color to Green
try:
    while True:
        # Generate random binary string
        line = "".join(random.choice(["0", "1", " ", " "]) for _ in range(cols))
        print(line)
        time.sleep(0.05)
except KeyboardInterrupt:
    print("\033[0m") # Reset color
    print("\n[SYSTEM BREACH DETECTED]")