'''
Wordle Glob

The user inputs a glob pattern, and the program returns a list of words that match the pattern.
We follow the Unix glob pattern rules, where:
- '*' matches any number of characters
- '?' matches exactly one character
- 'a' matches the character 'a'

We also follow the 5 letter wordle constraint, where all words are 5 letters long.
'''

import json
import fnmatch
from rich import print
from rich.prompt import Prompt
from rich.traceback import install
from rich.panel import Panel
import pdb
import os
import logging
from rich.markdown import Markdown

install()

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

log_path = os.path.join("logs", "wordle_glob.log")
os.makedirs(os.path.dirname(log_path), exist_ok=True)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
file_handler = logging.FileHandler(log_path)
file_handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)
logger.addHandler(console_handler)
logger.addHandler(file_handler)


def load_words() -> set[str]:
    with open('data/dwyl_5l_set.json') as f:
        return set(json.load(f))

def match_pattern(pattern: str, words: set[str]) -> list[str]:
    """Return a list of words that match the given glob pattern."""
    return [word for word in words if fnmatch.fnmatch(word, pattern) and len(word) == 5]

instructions = """
This program uses "Glob" patterns to find wordle words.
- '*' matches any number of characters
- '?' matches exactly one character
- 'a' matches the character 'a' (case insensitive)

Ex: 'h?t' matches 'hat', 'hot', 'hit', etc.
    't*e' matches 'tale', 'time', 'tree', etc.

After entering your pattern, you can also blacklist letters or specify yellow letters.

"""

def main() -> None:
    print("[bold]Welcome to Wordle Glob![/bold]")

    print(instructions)
    
    words = load_words()
    logger.debug(f"Loaded {len(words)} words")

    pattern = Prompt.ask("Enter a glob pattern").lower()
    blacklist_letters = set(Prompt.ask("Enter any letters to [bold black]blacklist").lower())
    yellow_letters = set(Prompt.ask("Enter any [bold yellow]yellow[/bold yellow] letters (non-positional)").lower())
    matches = match_pattern(pattern, words)
    
    
    if blacklist_letters:
        matches = [word for word in matches if not any(letter in blacklist_letters for letter in word)]

    if yellow_letters:
        matches = [word for word in matches if yellow_letters.issubset(set(word))]


    matches_with_no_repeat_letters = [word for word in matches if len(set(word)) == len(word)]    

    matches_with_repeat_letters = [word for word in matches if len(set(word)) != len(word)]

    if matches:
        matches_count = len(matches)
        print(Panel(f"Words matching '{pattern}': [bold green]{', '.join(matches)}", title=f"All Results [green bold]{matches_count}[/green bold]", expand=False))
    else:
        print(Panel(f"[bold red]No words match the pattern: [/bold red]'{pattern}'", title="Results", style="bold red", expand=False))
    
    if matches_with_no_repeat_letters:
        matches_no_repeat_letters_count = len(matches_with_no_repeat_letters)
        print(Panel(f"Words matching '{pattern}' with no repeating letters: [bold green]{', '.join(matches_with_no_repeat_letters)}", title=f"Results (No Repeats) [bold green]{matches_no_repeat_letters_count}[/bold green]", style="bold", expand=False))
    
    if matches_with_repeat_letters:
        matches_with_repeat_letters_count = len(matches_with_repeat_letters)
        print(Panel(f"Words matching '{pattern}' with repeating letters: [bold green]{', '.join(matches_with_repeat_letters)}", title=f"Results (Repeats) [bold green]{matches_with_repeat_letters_count}[/bold green]", style="bold yellow", expand=False))
    
    input("Press Enter to exit...")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("[green]Exiting program...")
    except Exception as e:
        logger.exception(f"An error occurred: {e}")
        print(f"[bold red]An error occurred: {e}")
        print("[bold red]Entering debugger mode...")
        pdb.post_mortem()
