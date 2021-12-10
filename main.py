import string

from highscoringwords import HighScoringWords

if __name__ == '__main__':
    h = HighScoringWords()
    a = (h.build_leaderboard_for_word_list())
    b = (h.build_leaderboard_for_letters("".join([a * 30 for a in string.ascii_lowercase])))

    print(a == b)
