# -*- coding: utf-8 -*-


def win_rate(wins, battles):
    if battles <= 0:
        return 0.0
    return round(float(wins) * 100.0 / float(battles), 2)


def wins_to_target(wins, battles, target):
    if battles <= 0 or target >= 100.0:
        return 0
    if float(wins) * 100.0 / float(battles) >= target:
        return 0

    t = float(target) / 100.0
    n = int(max(0.0, (t * battles - wins) / (1.0 - t)))
    while float(wins + n) * 100.0 / float(battles + n) < target:
        n += 1
    return n


def targets(wins, battles):
    wr = win_rate(wins, battles)
    half = (int(wr * 2.0) + 1) / 2.0
    whole = int(wr) + 1
    return {
        'wr': wr,
        'halfTarget': half,
        'halfWins': wins_to_target(wins, battles, half),
        'wholeTarget': whole,
        'wholeWins': wins_to_target(wins, battles, whole)
    }
