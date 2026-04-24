# Blackjack Strategy Trainer

A single-process web app for practicing blackjack basic strategy.

## Run

```bash
python3 app.py
```

Then open `http://127.0.0.1:8000`.

You can choose hard totals, soft totals, pairs, mixed hands, or review missed hands. The strategy model is for a 6-deck game where the dealer stands on soft 17, double after split is allowed, and surrender is not included.

## Drill modes

- Mixed hands: random hard totals, soft totals, and pairs.
- Hard totals: no ace is currently counted as 11. If the hand has an ace, it must be counted as 1 because 11 would put the hand over 21.
- Soft totals: an ace is counted as 11 because the hand total is still 21 or less.
- Pairs: two same-value starting cards where splitting may be correct.
- Review misses: repeats hands you answered incorrectly.

## Ace rule

An ace can count as 11 or 1. Start by counting it as 11. If that would make the hand total more than 21, count the ace as 1 instead. A "soft" hand has an ace still counted as 11; a "hard" hand does not.

## Face cards

The practice hand shows the actual cards you would see at a casino, including J, Q, and K. The strategy charts group 10, J, Q, and K into one `10` column because they are all worth 10 and use the same basic-strategy decisions.
