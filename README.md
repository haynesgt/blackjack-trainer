# Blackjack Strategy Trainer

A single-process web app for practicing blackjack basic strategy.

## Run

```bash
python3 app.py
```

Then open `http://127.0.0.1:8000`.

You can choose hard totals, soft totals, pairs, mixed hands, or review missed hands. The strategy model is for a 6-deck game where the dealer stands on soft 17, double after split is allowed, and surrender is not included.

## Blackjack rules

The goal is to beat the dealer by ending with a higher total without going over 21. Number cards count as shown, J/Q/K count as 10, and an ace counts as 11 unless that would put the hand over 21.

If your total goes over 21, you bust and lose immediately. After players finish, the dealer draws by fixed rules; this trainer uses dealer stands on soft 17.

Player actions:

- Hit: take one more card. Shortcut: `1` or `H`.
- Stand: stop taking cards and keep your current total. Shortcut: `2` or `S`.
- Double: on a two-card hand, double the bet, take exactly one more card, then stop. If a chart play is Double but the hand has more than two cards, hit instead. Shortcut: `3` or `D`.
- Split: if your first two cards have the same value, separate them into two hands. Shortcut: `4` or `P`.

## Drill modes

- Mixed hands: random hard totals, soft totals, and pairs.
- Hard totals: no ace is currently counted as 11. If the hand has an ace, it must be counted as 1 because 11 would put the hand over 21.
- Soft totals: an ace is counted as 11 because the hand total is still 21 or less.
- Pairs: two same-value starting cards where splitting may be correct.
- Review misses: repeats hands you answered incorrectly.

Hard, soft, and mixed drills can include 3+ card decision scenarios like you might see after hitting in a real hand. In those later decisions, Double and Split are not available.

## Ace rule

An ace can count as 11 or 1. Start by counting it as 11. If that would make the hand total more than 21, count the ace as 1 instead. A "soft" hand has an ace still counted as 11; a "hard" hand does not.

## Face cards

The practice hand shows the actual cards you would see at a casino, including J, Q, and K. The strategy charts group 10, J, Q, and K into one `10` column because they are all worth 10 and use the same basic-strategy decisions.

## Chart notes

The hard-total `≥17` row covers any hard total of 17 or above. The hard-total `≤8` row covers any hard total of 8 or below. The soft-total chart includes `A,10`, which is blackjack or soft 21 depending on context. The app's strategy assumes 6 decks, dealer stands on soft 17, double after split is allowed, and surrender is not included.
