__author__ = 'codesse'

from collections import Counter


class HighScoringWords:
    MAX_LEADERBOARD_LENGTH = 100  # the maximum number of items that can appear in the leaderboard
    MIN_WORD_LENGTH = 3  # words must be at least this many characters long
    letter_values = {}
    valid_words = []

    def __init__(self, validwords='wordlist.txt', lettervalues='letterValues.txt'):
        """
        Initialise the class with complete set of valid words and letter values by parsing text files containing the data
        :param validwords: a text file containing the complete set of valid words, one word per line
        :param lettervalues: a text file containing the score for each letter in the format letter:score one per line
        :return:
        """
        with open(validwords) as f:
            self.valid_words = f.read().splitlines()

        with open(lettervalues) as f:
            for line in f:
                (key, val) = line.split(':')
                self.letter_values[str(key).strip().lower()] = int(val)

    def _calculate_score(self, word: str) -> int:
        score = 0
        for ch in word:
            score += self.letter_values[ch]

        return score

    @staticmethod
    def _sort_leaderboard(words_scores: dict) -> list:
        return sorted(words_scores.items(), key=lambda x: (-x[1], x[0]))

    def build_leaderboard_for_word_list(self):
        """
        Build a leaderboard of the top scoring MAX_LEADERBOAD_LENGTH words from the complete set of valid words.
        :return: The list of top words.
        """
        words_scores = {word: self._calculate_score(word) for word in self.valid_words}
        words_scores_sorted = self._sort_leaderboard(words_scores)
        return list(item[0] for i, item in enumerate(words_scores_sorted) if i < self.MAX_LEADERBOARD_LENGTH)

    @staticmethod
    def _is_sub(word, counted_letters):
        counted_letters = counted_letters.copy()  # we are going to modify it locally
        for char in word:
            if char not in counted_letters:
                return False

            counted_letters[char] -= 1
            if counted_letters[char] == -1:
                return False

        return True

    def build_leaderboard_for_letters(self, starting_letters):
        """
        Build a leaderboard of the top scoring MAX_LEADERBOARD_LENGTH words that can be built using only the letters contained in the starting_letters String.
        The number of occurrences of a letter in the startingLetters String IS significant. If the starting letters are bulx, the word "bull" is NOT valid.
        There is only one l in the starting string but bull contains two l characters.
        Words are ordered in the leaderboard by their score (with the highest score first) and then alphabetically for words which have the same score.
        :param starting_letters: a random string of letters from which to build words that are valid against the contents of the wordlist.txt file
        :return: The list of top buildable words.
        """
        sub_words = {}
        counted = Counter(starting_letters)
        for word in self.valid_words:
            if len(word) <= len(starting_letters):
                if self._is_sub(word, counted):
                    sub_words[word] = self._calculate_score(word)

        words_scores_sorted = self._sort_leaderboard(sub_words)
        return list(item[0] for i, item in enumerate(words_scores_sorted) if i < self.MAX_LEADERBOARD_LENGTH)
