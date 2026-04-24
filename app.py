from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import argparse


APP_HTML = r"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Blackjack Strategy Trainer</title>
  <style>
    :root {
      color-scheme: light;
      --felt: #0f6a4f;
      --felt-dark: #084133;
      --ink: #17211f;
      --muted: #5d6b67;
      --line: #d8dedb;
      --panel: #ffffff;
      --soft: #eaf6f1;
      --warn: #fff4d8;
      --bad: #ffe7e4;
      --good: #e5f6ea;
      --red: #b42318;
      --blue: #1c5d99;
      --shadow: 0 14px 42px rgba(9, 38, 31, 0.18);
    }

    * {
      box-sizing: border-box;
    }

    html,
    body {
      height: 100%;
    }

    body {
      margin: 0;
      font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      color: var(--ink);
      background: #f5f7f6;
      overflow: hidden;
    }

    button, select {
      font: inherit;
    }

    .app {
      height: 100vh;
      display: grid;
      grid-template-columns: minmax(0, 1fr) 370px;
      overflow: hidden;
    }

    .table {
      height: 100vh;
      padding: 28px;
      background:
        radial-gradient(circle at 22% 18%, rgba(255,255,255,0.14), transparent 28%),
        radial-gradient(circle at 82% 16%, rgba(255,209,102,0.14), transparent 24%),
        linear-gradient(145deg, var(--felt), var(--felt-dark));
      color: #fff;
      display: flex;
      flex-direction: column;
      gap: 22px;
      overflow-y: auto;
      min-width: 0;
    }

    .topbar {
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 16px;
    }

    h1 {
      margin: 0;
      font-size: clamp(30px, 4vw, 54px);
      line-height: 0.96;
      letter-spacing: 0;
    }

    .subtitle {
      margin: 8px 0 0;
      color: rgba(255,255,255,0.78);
      max-width: 720px;
      font-size: 16px;
    }

    .score {
      display: grid;
      grid-template-columns: repeat(3, 76px);
      gap: 8px;
    }

    .score div {
      border: 1px solid rgba(255,255,255,0.22);
      background: rgba(255,255,255,0.12);
      border-radius: 8px;
      padding: 10px;
      text-align: center;
      min-height: 68px;
    }

    .score strong {
      display: block;
      font-size: 24px;
      line-height: 1.1;
    }

    .score span {
      display: block;
      margin-top: 4px;
      color: rgba(255,255,255,0.72);
      font-size: 12px;
    }

    .felt-layout {
      flex: 1;
      display: grid;
      grid-template-columns: minmax(0, 1fr) 300px;
      gap: 22px;
      align-items: stretch;
    }

    .practice {
      border: 1px solid rgba(255,255,255,0.24);
      border-radius: 8px;
      background: rgba(4, 31, 24, 0.24);
      box-shadow: var(--shadow);
      padding: 22px;
      display: grid;
      grid-template-rows: auto 1fr auto;
      gap: 26px;
      min-height: 760px;
    }

    .hand-row {
      display: grid;
      gap: 10px;
    }

    .hand-label {
      display: flex;
      align-items: baseline;
      justify-content: space-between;
      color: rgba(255,255,255,0.78);
      font-size: 13px;
      text-transform: uppercase;
      letter-spacing: 0.08em;
    }

    .hand-help {
      margin: -4px 0 0;
      border: 1px solid rgba(255,255,255,0.22);
      border-radius: 8px;
      background: rgba(255,255,255,0.1);
      color: rgba(255,255,255,0.84);
      padding: 10px 12px;
      font-size: 14px;
      line-height: 1.35;
    }

    .hand-help strong {
      color: #fff;
    }

    .total {
      color: #fff;
      font-size: 15px;
      letter-spacing: 0;
      text-transform: none;
    }

    .cards {
      min-height: 270px;
      display: flex;
      align-items: center;
      gap: 24px;
      flex-wrap: wrap;
    }

    .card {
      width: 176px;
      height: 248px;
      border-radius: 8px;
      background: #fff;
      color: #16211e;
      box-shadow: 0 18px 36px rgba(0,0,0,0.26);
      padding: 18px;
      display: grid;
      grid-template-rows: auto 1fr auto;
      border: 1px solid rgba(0,0,0,0.12);
      user-select: none;
    }

    .card.red {
      color: #b42318;
    }

    .pip {
      font-size: 44px;
      font-weight: 800;
      line-height: 1;
    }

    .suit {
      align-self: center;
      justify-self: center;
      font-size: 82px;
      line-height: 1;
    }

    .pip.bottom {
      justify-self: end;
      transform: rotate(180deg);
    }

    .decision {
      display: grid;
      gap: 12px;
      align-content: end;
    }

    .actions {
      display: grid;
      grid-template-columns: repeat(4, minmax(0, 1fr));
      gap: 14px;
    }

    .action {
      height: 104px;
      border: 0;
      border-radius: 8px;
      color: #10231e;
      background: #fff;
      cursor: pointer;
      font-weight: 800;
      font-size: 22px;
      box-shadow: 0 8px 18px rgba(0,0,0,0.18);
    }

    .action:hover {
      background: #f0f7f4;
    }

    .action:disabled {
      opacity: 0.46;
      cursor: not-allowed;
    }

    .prompt,
    .result {
      min-height: 112px;
      border-radius: 8px;
      padding: 16px;
      background: rgba(255,255,255,0.12);
      border: 1px solid rgba(255,255,255,0.22);
      color: rgba(255,255,255,0.88);
      line-height: 1.45;
    }

    .prompt {
      min-height: 86px;
      background: rgba(255,255,255,0.16);
    }

    .prompt strong,
    .result strong {
      display: block;
      color: #fff;
      font-size: 22px;
      margin-bottom: 6px;
    }

    .result.good {
      background: rgba(23, 111, 57, 0.38);
      border-color: rgba(177, 236, 190, 0.48);
    }

    .result.bad {
      background: rgba(138, 30, 24, 0.34);
      border-color: rgba(255, 192, 184, 0.48);
    }

    .side-tools {
      display: grid;
      gap: 14px;
      align-content: start;
    }

    .tool-panel {
      background: rgba(255,255,255,0.94);
      color: var(--ink);
      border-radius: 8px;
      padding: 16px;
      border: 1px solid rgba(255,255,255,0.4);
    }

    .tool-panel h2 {
      margin: 0 0 12px;
      font-size: 17px;
    }

    .mode-grid {
      display: grid;
      gap: 8px;
    }

    .mode {
      border: 1px solid var(--line);
      background: #fff;
      color: var(--ink);
      border-radius: 8px;
      min-height: 64px;
      padding: 10px;
      cursor: pointer;
      text-align: left;
      display: grid;
      gap: 3px;
    }

    .mode.active {
      border-color: #0f6a4f;
      background: var(--soft);
      font-weight: 800;
    }

    .mode strong {
      display: block;
      font-size: 14px;
      line-height: 1.15;
    }

    .mode span {
      display: block;
      color: var(--muted);
      font-size: 12px;
      line-height: 1.3;
      font-weight: 500;
    }

    .mode.active span {
      color: #41514c;
    }

    .settings {
      display: grid;
      gap: 10px;
      color: var(--muted);
      font-size: 14px;
    }

    .settings label {
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 10px;
    }

    select {
      border: 1px solid var(--line);
      background: #fff;
      border-radius: 8px;
      padding: 7px 8px;
      color: var(--ink);
      min-width: 112px;
    }

    .primary {
      border: 0;
      border-radius: 8px;
      min-height: 44px;
      padding: 0 14px;
      background: #ffd166;
      color: #2d2410;
      font-weight: 900;
      cursor: pointer;
    }

    .secondary {
      border: 1px solid var(--line);
      border-radius: 8px;
      min-height: 40px;
      padding: 0 12px;
      background: #fff;
      color: var(--ink);
      font-weight: 700;
      cursor: pointer;
    }

    .sidebar {
      border-left: 1px solid var(--line);
      background: var(--panel);
      height: 100vh;
      padding: 22px;
      overflow-y: auto;
      min-width: 0;
    }

    .chart {
      margin-top: 22px;
      padding-top: 18px;
      border-top: 1px solid var(--line);
    }

    .chart h2 {
      margin: 0 0 8px;
      font-size: 21px;
    }

    .chart p {
      margin: 0 0 14px;
      color: var(--muted);
      line-height: 1.45;
      font-size: 14px;
    }

    table {
      border-collapse: collapse;
      width: 100%;
      table-layout: fixed;
      font-size: 12px;
    }

    th, td {
      border: 1px solid var(--line);
      padding: 6px 3px;
      text-align: center;
      height: 30px;
    }

    th {
      background: #eef3f1;
      color: #31413c;
      font-weight: 900;
    }

    td {
      font-weight: 900;
      color: #17211f;
    }

    .H { background: #e7f0ff; color: var(--blue); }
    .S { background: var(--good); color: #176f39; }
    .D { background: var(--warn); color: #7a4d00; }
    .P { background: #efe7ff; color: #6842b8; }

    .legend {
      display: grid;
      grid-template-columns: repeat(2, 1fr);
      gap: 8px;
      margin-top: 14px;
      color: var(--muted);
      font-size: 13px;
    }

    .legend span {
      display: inline-flex;
      align-items: center;
      gap: 6px;
    }

    .swatch {
      width: 22px;
      height: 16px;
      border-radius: 4px;
      border: 1px solid var(--line);
    }

    .hint-list {
      display: grid;
      gap: 10px;
      margin: 0;
      padding: 0;
      list-style: none;
      color: var(--muted);
      line-height: 1.4;
      font-size: 14px;
    }

    .hint-list strong {
      color: var(--ink);
    }

    .beginner-note {
      margin: 0 0 14px;
      border-left: 4px solid #ffd166;
      padding: 10px 12px;
      background: #fff8e6;
      color: #4d3a0d;
      font-size: 14px;
      line-height: 1.45;
    }

    .rules-panel {
      margin-top: 22px;
      padding-top: 18px;
      border-top: 1px solid var(--line);
    }

    .rules-panel h2 {
      margin: 0 0 10px;
      font-size: 21px;
    }

    .rules-list {
      display: grid;
      gap: 12px;
      margin: 0;
      padding: 0;
      list-style: none;
      color: var(--muted);
      font-size: 14px;
      line-height: 1.45;
    }

    .rules-list strong {
      display: block;
      color: var(--ink);
      font-weight: 900;
      margin-bottom: 2px;
    }

    .rules-settings {
      margin-top: 16px;
      border-top: 1px solid var(--line);
      padding-top: 12px;
      color: var(--muted);
      font-size: 13px;
      line-height: 1.45;
    }

    @media (max-width: 1120px) {
      body {
        overflow: auto;
      }

      .app {
        grid-template-columns: 1fr;
        height: auto;
        min-height: 100vh;
        overflow: visible;
      }

      .table {
        height: auto;
        min-height: 100vh;
        overflow: visible;
      }

      .sidebar {
        height: auto;
        min-height: auto;
        border-left: 0;
        overflow: visible;
      }
    }

    @media (max-width: 820px) {
      .table {
        padding: 18px;
      }

      .topbar, .felt-layout {
        grid-template-columns: 1fr;
        display: grid;
      }

      .score {
        grid-template-columns: repeat(3, minmax(0, 1fr));
      }

      .practice {
        min-height: auto;
        gap: 20px;
      }

      .actions {
        grid-template-columns: repeat(2, minmax(0, 1fr));
      }

      .action {
        height: 78px;
        font-size: 18px;
      }

      .cards {
        min-height: 190px;
        gap: 16px;
      }

      .card {
        width: 128px;
        height: 180px;
        padding: 14px;
      }

      .pip {
        font-size: 32px;
      }

      .suit {
        font-size: 60px;
      }
    }
  </style>
</head>
<body>
  <main class="app">
    <section class="table">
      <div class="topbar">
        <div>
          <h1>Blackjack Strategy Trainer</h1>
          <p class="subtitle">Practice total-dependent basic strategy for a 6-deck, dealer-stands-soft-17 game with double after split. Surrender is excluded.</p>
        </div>
        <div class="score" aria-label="Session score">
          <div><strong id="correct">0</strong><span>Correct</span></div>
          <div><strong id="missed">0</strong><span>Missed</span></div>
          <div><strong id="streak">0</strong><span>Streak</span></div>
        </div>
      </div>

      <div class="felt-layout">
        <section class="practice" aria-label="Practice hand">
          <div class="hand-row">
            <div class="hand-label">Dealer upcard <span class="total" id="dealerTotal"></span></div>
            <div class="cards" id="dealerCards"></div>
          </div>

          <div class="hand-row">
            <div class="hand-label">Your hand <span class="total" id="playerTotal"></span></div>
            <div class="cards" id="playerCards"></div>
            <div class="hand-help" id="handHelp"></div>
          </div>

          <div class="decision">
            <div class="prompt" id="prompt" aria-live="polite">
              <strong>Choose the best play.</strong>
              <span>Use the dealer upcard, your total, and whether your hand is hard, soft, or a pair.</span>
            </div>
            <div class="actions" id="actions">
              <button class="action" data-action="H">Hit [1]</button>
              <button class="action" data-action="S">Stand [2]</button>
              <button class="action" data-action="D">Double [3]</button>
              <button class="action" data-action="P">Split [4]</button>
            </div>
            <div class="result" id="result" aria-live="polite">
              <strong>Last hand feedback appears here.</strong>
              <span>Pick an action to see whether it matched basic strategy.</span>
            </div>
          </div>
        </section>

        <aside class="side-tools" aria-label="Practice controls">
          <section class="tool-panel">
            <h2>Drill Mode</h2>
            <div class="mode-grid" id="modes">
              <button class="mode active" data-mode="mixed">
                <strong>Mixed hands</strong>
                <span>Random hard totals, soft totals, and pairs in one drill.</span>
              </button>
              <button class="mode" data-mode="hard">
                <strong>Hard totals</strong>
                <span>No ace is counted as 11. A hit can bust the hand.</span>
              </button>
              <button class="mode" data-mode="soft">
                <strong>Soft totals</strong>
                <span>An ace is counted as 11 because the total is 21 or less.</span>
              </button>
              <button class="mode" data-mode="pair">
                <strong>Pairs</strong>
                <span>Two same-value starting cards where splitting may be correct.</span>
              </button>
              <button class="mode" data-mode="weak">
                <strong>Review misses</strong>
                <span>Repeats hands you missed; falls back to mixed if none exist.</span>
              </button>
            </div>
          </section>

          <section class="tool-panel">
            <h2>Table Rules</h2>
            <div class="settings">
              <label>Decks <select disabled><option>6 decks</option></select></label>
              <label>Dealer <select disabled><option>Stands soft 17</option></select></label>
              <label>DAS <select disabled><option>Allowed</option></select></label>
              <button class="primary" id="next">Next Hand</button>
              <button class="secondary" id="reset">Reset Score</button>
            </div>
          </section>

          <section class="tool-panel">
            <h2>Action Guide</h2>
            <ul class="hint-list">
              <li><strong>1 Hit:</strong> take one more card.</li>
              <li><strong>2 Stand:</strong> stop taking cards and keep this total.</li>
              <li><strong>3 Double:</strong> on a two-card hand, double the bet, take exactly one more card, then stop.</li>
              <li><strong>4 Split:</strong> if your first two cards have the same value, separate them into two hands.</li>
            </ul>
          </section>

          <section class="tool-panel">
            <h2>Fast Rules</h2>
            <ul class="hint-list">
              <li><strong>Ace rule:</strong> start by counting an ace as 11. If that would make the hand over 21, count that ace as 1 instead.</li>
              <li><strong>Hard 12-16:</strong> stand against dealer 2-6, otherwise hit.</li>
              <li><strong>Soft 18:</strong> stand against 2, 7, 8; double against 3-6; hit against 9-A.</li>
              <li><strong>Always split:</strong> aces and 8s. Never split 5s or 10s.</li>
            </ul>
          </section>
        </aside>
      </div>
    </section>

    <aside class="sidebar" aria-label="Strategy reference">
      <p class="beginner-note"><strong>Ace basics:</strong> an ace can be 11 or 1. It is 11 only when the hand total stays 21 or less. A hand with an ace still counted as 11 is called soft.</p>
      <p class="beginner-note"><strong>Casino cards vs charts:</strong> the practice hand shows the actual cards you would see at a table, including J, Q, and K. The charts use one <strong>10</strong> column because 10, J, Q, and K are all worth 10 and use the same strategy.</p>
      <section class="chart" id="chart-hard"></section>
      <section class="chart" id="chart-soft"></section>
      <section class="chart" id="chart-pair"></section>
      <div class="legend">
        <span><i class="swatch H"></i> H hit</span>
        <span><i class="swatch S"></i> St stand</span>
        <span><i class="swatch D"></i> D double</span>
        <span><i class="swatch P"></i> Sp split</span>
      </div>
      <section class="rules-panel" aria-label="Game rules">
        <h2>Game Rules</h2>
        <ul class="rules-list">
          <li><strong>Goal</strong> Beat the dealer by ending with a higher hand total than the dealer without going over 21.</li>
          <li><strong>Card values</strong> Number cards count as shown. J, Q, and K count as 10. An ace counts as 11 unless that would put the hand over 21, then it counts as 1.</li>
          <li><strong>Blackjack</strong> Your first two cards are an ace plus any 10-value card. This is the best starting hand.</li>
          <li><strong>Bust</strong> If your total goes over 21, you lose immediately.</li>
          <li><strong>Hit</strong> Take one more card. You can keep hitting until you stand or bust.</li>
          <li><strong>Stand</strong> Stop taking cards. Your current total is the total you will compare against the dealer.</li>
          <li><strong>Double</strong> On a two-card hand, double the bet, take exactly one more card, then your turn ends. Basic strategy uses this when one-card improvement is valuable.</li>
          <li><strong>Split</strong> If your first two cards have the same value, separate them into two hands. Each card starts a new hand with its own next card.</li>
          <li><strong>Dealer turn</strong> After players finish, the dealer draws by fixed rules. In this trainer, the dealer stands on soft 17.</li>
          <li><strong>Why strategy charts work</strong> You only need your hand type and the dealer upcard. The chart tells the best long-run play for that situation.</li>
        </ul>
        <p class="rules-settings"><strong>Trainer settings:</strong> 6 decks, dealer stands on soft 17, double after split allowed, surrender not included. In the charts, dealer 10 means 10, J, Q, or K.</p>
      </section>
    </aside>
  </main>

  <script>
    const dealerValues = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11];
    const dealerLabels = { 11: "A" };
    const suits = ["♠", "♥", "♦", "♣"];
    const drillModes = ["mixed", "hard", "soft", "pair", "weak"];
    const savedMode = localStorage.getItem("blackjackTrainerMode");
    const state = {
      mode: drillModes.includes(savedMode) ? savedMode : "mixed",
      hand: null,
      answered: false,
      stats: JSON.parse(localStorage.getItem("blackjackTrainerStats") || '{"correct":0,"missed":0,"streak":0}'),
      misses: JSON.parse(localStorage.getItem("blackjackTrainerMisses") || "[]")
    };

    function label(value) {
      return dealerLabels[value] || String(value);
    }

    function cardName(value) {
      if (value === 11) return "A";
      if (value === 10) return ["10", "J", "Q", "K"][Math.floor(Math.random() * 4)];
      return String(value);
    }

    function handTotal(cards) {
      let total = cards.reduce((sum, card) => sum + (card.value === 11 ? 11 : card.value), 0);
      let aces = cards.filter(card => card.value === 11).length;
      while (total > 21 && aces > 0) {
        total -= 10;
        aces -= 1;
      }
      return total;
    }

    function rawAceHighTotal(cards) {
      return cards.reduce((sum, card) => sum + (card.value === 11 ? 11 : card.value), 0);
    }

    function aceCount(cards) {
      return cards.filter(card => card.value === 11).length;
    }

    function isSoft(cards) {
      let total = rawAceHighTotal(cards);
      let aces = aceCount(cards);
      while (total > 21 && aces > 0) {
        total -= 10;
        aces -= 1;
      }
      return aces > 0;
    }

    function isPair(cards) {
      return cards.length === 2 && cards[0].value === cards[1].value;
    }

    function hardMove(total, dealer) {
      if (total >= 17) return "S";
      if (total >= 13) return dealer >= 2 && dealer <= 6 ? "S" : "H";
      if (total === 12) return dealer >= 4 && dealer <= 6 ? "S" : "H";
      if (total === 11) return "D";
      if (total === 10) return dealer >= 2 && dealer <= 9 ? "D" : "H";
      if (total === 9) return dealer >= 3 && dealer <= 6 ? "D" : "H";
      return "H";
    }

    function softMove(total, dealer) {
      if (total >= 20) return "S";
      if (total === 19) return dealer === 6 ? "D" : "S";
      if (total === 18) {
        if (dealer >= 3 && dealer <= 6) return "D";
        if (dealer === 2 || dealer === 7 || dealer === 8) return "S";
        return "H";
      }
      if (total === 17) return dealer >= 3 && dealer <= 6 ? "D" : "H";
      if (total === 16 || total === 15) return dealer >= 4 && dealer <= 6 ? "D" : "H";
      if (total === 14 || total === 13) return dealer >= 5 && dealer <= 6 ? "D" : "H";
      return "H";
    }

    function pairMove(pairValue, dealer) {
      if (pairValue === 11 || pairValue === 8) return "P";
      if (pairValue === 10) return "S";
      if (pairValue === 9) return [2,3,4,5,6,8,9].includes(dealer) ? "P" : "S";
      if (pairValue === 7) return dealer >= 2 && dealer <= 7 ? "P" : "H";
      if (pairValue === 6) return dealer >= 2 && dealer <= 6 ? "P" : "H";
      if (pairValue === 5) return dealer >= 2 && dealer <= 9 ? "D" : "H";
      if (pairValue === 4) return dealer === 5 || dealer === 6 ? "P" : "H";
      if (pairValue === 3 || pairValue === 2) return dealer >= 2 && dealer <= 7 ? "P" : "H";
      return "H";
    }

    function canDouble(cards) {
      return cards.length === 2;
    }

    function canSplit(cards) {
      return cards.length === 2 && isPair(cards);
    }

    function availableActions(cards) {
      return {
        H: true,
        S: true,
        D: canDouble(cards),
        P: canSplit(cards)
      };
    }

    function totalMove(cards, dealer) {
      if (isSoft(cards)) return softMove(handTotal(cards), dealer);
      return hardMove(handTotal(cards), dealer);
    }

    function doubleFallbackMove(cards) {
      if (!isSoft(cards)) return "H";
      return handTotal(cards) >= 18 ? "S" : "H";
    }

    function bestMove(cards, dealer) {
      if (canSplit(cards)) return pairMove(cards[0].value, dealer);
      const move = totalMove(cards, dealer);
      if (move === "D" && !canDouble(cards)) return doubleFallbackMove(cards);
      return move;
    }

    function handKind(cards) {
      if (canSplit(cards)) return "pair";
      if (isSoft(cards)) return "soft";
      return "hard";
    }

    function actionName(move) {
      return { H: "Hit", S: "Stand", D: "Double", P: "Split" }[move] || "Unknown";
    }

    function chartMoveLabel(move) {
      return { H: "H", S: "St", D: "D", P: "Sp" }[move] || move;
    }

    function handSummary(cards) {
      const kind = handKind(cards);
      const total = handTotal(cards);
      if (kind === "pair") {
        return `Pair ${label(cards[0].value)}s`;
      }
      return `${kind[0].toUpperCase() + kind.slice(1)} ${total}`;
    }

    function upcardSummary(card) {
      if (card.value === 10 && card.rank !== "10") {
        return `Upcard ${card.rank} (value 10)`;
      }
      return `Upcard ${card.rank}`;
    }

    function handHelp(cards) {
      const total = handTotal(cards);
      const aces = aceCount(cards);
      const rawTotal = rawAceHighTotal(cards);
      const decisionNote = cards.length > 2 ? " This is a later decision after one or more hits, so Double and Split are not available." : "";
      if (canSplit(cards)) {
        return `<strong>Pair hand:</strong> because both starting cards have the same value, check the Pairs chart first. If the best play is not Split, the app still shows the correct basic-strategy action.`;
      }
      if (aces === 0) {
        return `<strong>Hard ${total}:</strong> there is no ace, so the total is fixed. A hit can bust this hand if the new card pushes it over 21.${decisionNote}`;
      }
      if (isSoft(cards)) {
        return `<strong>Soft ${total}:</strong> the ace is counted as 11 because ${rawTotal} is not over 21. If a later card would bust you, that ace can switch to 1.${decisionNote}`;
      }
      return `<strong>Hard ${total}:</strong> this hand has an ace, but counting it as 11 would make ${rawTotal}, which is over 21. Count the ace as 1 instead.${decisionNote}`;
    }

    function describe(cards, dealer, move) {
      const kind = handKind(cards);
      const total = handTotal(cards);
      if (kind === "pair") {
        const pair = label(cards[0].value);
        return `Pair of ${pair}s vs dealer ${label(dealer)}: check pair strategy before treating the cards as a regular total. ${actionName(move)} is the basic-strategy play.`;
      }
      if (kind === "soft") {
        if (!canDouble(cards) && totalMove(cards, dealer) === "D") {
          return `Soft ${total} vs dealer ${label(dealer)}: the chart would double on a two-card hand, but this later decision cannot double. ${actionName(move)} is the best available play.`;
        }
        return `Soft ${total} vs dealer ${label(dealer)}: the ace counts as 11 because the total is still 21 or less. Use the soft-total chart.`;
      }
      if (!canDouble(cards) && totalMove(cards, dealer) === "D") {
        return `Hard ${total} vs dealer ${label(dealer)}: the chart would double on a two-card hand, but this later decision cannot double. Hit is the best available play.`;
      }
      if (aceCount(cards) > 0) {
        return `Hard ${total} vs dealer ${label(dealer)}: the ace has to count as 1 because counting it as 11 would bust the hand. Use the hard-total chart.`;
      }
      return `Hard ${total} vs dealer ${label(dealer)}: there is no ace counted as 11, so use the hard-total chart.`;
    }

    function makeCard(value) {
      const suit = suits[Math.floor(Math.random() * suits.length)];
      return { value, rank: cardName(value), suit, red: suit === "♥" || suit === "♦" };
    }

    function randomDealer() {
      return dealerValues[Math.floor(Math.random() * dealerValues.length)];
    }

    function randomHard() {
      const total = 5 + Math.floor(Math.random() * 13);
      let first = Math.min(10, Math.max(2, total - (2 + Math.floor(Math.random() * Math.min(8, total - 3)))));
      let second = total - first;
      if (second < 2 || second > 10 || first === second) return randomHard();
      return [makeCard(first), makeCard(second)];
    }

    function randomHardDecision() {
      if (Math.random() < 0.55) return randomHard();
      const total = 7 + Math.floor(Math.random() * 14);
      const cardCount = Math.random() < 0.75 ? 3 : 4;
      const values = splitTotal(total, cardCount);
      if (!values) return randomHardDecision();
      return values.map(makeCard);
    }

    function randomSoft() {
      const low = 2 + Math.floor(Math.random() * 8);
      return [makeCard(11), makeCard(low)];
    }

    function randomSoftDecision() {
      if (Math.random() < 0.55) return randomSoft();
      const total = 13 + Math.floor(Math.random() * 8);
      const lowTotal = total - 11;
      const values = splitTotal(lowTotal, Math.random() < 0.8 ? 2 : 3, 2, 7);
      if (!values) return randomSoftDecision();
      return [makeCard(11), ...values.map(makeCard)];
    }

    function randomPair() {
      const value = [2,3,4,5,6,7,8,9,10,11][Math.floor(Math.random() * 10)];
      return [makeCard(value), makeCard(value)];
    }

    function splitTotal(total, cardCount, minValue = 2, maxValue = 10) {
      const values = [];
      let remaining = total;
      for (let i = 0; i < cardCount; i += 1) {
        const slotsLeft = cardCount - i - 1;
        const min = Math.max(minValue, remaining - slotsLeft * maxValue);
        const max = Math.min(maxValue, remaining - slotsLeft * minValue);
        if (min > max) return null;
        const value = min + Math.floor(Math.random() * (max - min + 1));
        values.push(value);
        remaining -= value;
      }
      return remaining === 0 ? values : null;
    }

    function newHandFromMode(mode) {
      if (mode === "weak" && state.misses.length) {
        const missed = state.misses[Math.floor(Math.random() * state.misses.length)];
        return {
          dealer: missed.dealer,
          dealerCard: makeCard(missed.dealer),
          player: missed.player.map(card => makeCard(card.value))
        };
      }
      const useMode = mode === "mixed" || mode === "weak"
        ? ["hard", "soft", "pair"][Math.floor(Math.random() * 3)]
        : mode;
      const makers = { hard: randomHardDecision, soft: randomSoftDecision, pair: randomPair };
      const dealer = randomDealer();
      return { dealer, dealerCard: makeCard(dealer), player: makers[useMode]() };
    }

    function renderCard(card) {
      return `<div class="card ${card.red ? "red" : ""}" aria-label="${card.rank}${card.suit}">
        <div class="pip">${card.rank}</div>
        <div class="suit">${card.suit}</div>
        <div class="pip bottom">${card.rank}</div>
      </div>`;
    }

    function renderHand() {
      const hand = state.hand;
      document.getElementById("dealerCards").innerHTML = renderCard(hand.dealerCard);
      document.getElementById("playerCards").innerHTML = hand.player.map(renderCard).join("");
      document.getElementById("dealerTotal").textContent = upcardSummary(hand.dealerCard);
      document.getElementById("playerTotal").textContent = handSummary(hand.player);
      document.getElementById("handHelp").innerHTML = handHelp(hand.player);
      const legalActions = availableActions(hand.player);
      document.querySelectorAll(".action[data-action]").forEach(button => {
        const action = button.dataset.action;
        button.disabled = !legalActions[action];
        button.title = legalActions[action] ? "" : `${actionName(action)} is not available for this decision.`;
      });
    }

    function setPrompt(title, detail) {
      const prompt = document.getElementById("prompt");
      prompt.innerHTML = `<strong>${title}</strong><span>${detail}</span>`;
    }

    function setFeedback(kind, title, detail) {
      const result = document.getElementById("result");
      result.className = `result ${kind}`;
      result.innerHTML = `<strong>${title}</strong><span>${detail}</span>`;
    }

    function save() {
      localStorage.setItem("blackjackTrainerStats", JSON.stringify(state.stats));
      localStorage.setItem("blackjackTrainerMisses", JSON.stringify(state.misses.slice(-30)));
    }

    function updateScore() {
      document.getElementById("correct").textContent = state.stats.correct;
      document.getElementById("missed").textContent = state.stats.missed;
      document.getElementById("streak").textContent = state.stats.streak;
    }

    function updateModeButtons() {
      document.querySelectorAll(".mode").forEach(item => {
        item.classList.toggle("active", item.dataset.mode === state.mode);
      });
    }

    function nextHand() {
      state.hand = newHandFromMode(state.mode);
      state.answered = false;
      renderHand();
      setPrompt("Choose the best play.", `${handSummary(state.hand.player)} vs dealer ${label(state.hand.dealer)}. Read the hand note above, then pick the basic-strategy action.`);
    }

    function answer(move) {
      if (state.answered) return;
      if (!availableActions(state.hand.player)[move]) return;
      const correct = bestMove(state.hand.player, state.hand.dealer);
      const detail = describe(state.hand.player, state.hand.dealer, correct);
      state.answered = true;
      if (move === correct) {
        state.stats.correct += 1;
        state.stats.streak += 1;
        setFeedback("good", "Correct.", detail);
      } else {
        state.stats.missed += 1;
        state.stats.streak = 0;
        state.misses.push({
          dealer: state.hand.dealer,
          player: state.hand.player.map(card => ({ value: card.value }))
        });
        setFeedback("bad", `Best play: ${actionName(correct)}.`, `You chose ${actionName(move)}. ${detail}`);
      }
      save();
      updateScore();
      nextHand();
    }

    function buildChart(kind) {
      const titles = {
        hard: ["Hard Totals", "Use this when your hand has no ace counted as 11."],
        soft: ["Soft Totals", "Use this when an ace can still count as 11 without busting."],
        pair: ["Pairs", "Use this before evaluating the hand as a hard or soft total."]
      };
      const rows = {
        hard: [17,16,15,14,13,12,11,10,9,8],
        soft: [21,20,19,18,17,16,15,14,13],
        pair: [11,10,9,8,7,6,5,4,3,2]
      }[kind];
      const body = rows.map(row => {
        const cells = dealerValues.map(dealer => {
          let move;
          if (kind === "hard") move = hardMove(row, dealer);
          if (kind === "soft") move = softMove(row, dealer);
          if (kind === "pair") move = pairMove(row, dealer);
          return `<td class="${move}">${chartMoveLabel(move)}</td>`;
        }).join("");
        const rowLabel = kind === "soft" ? `A,${row - 11}` : kind === "pair" ? `${label(row)},${label(row)}` : row === 17 ? "≥17" : row === 8 ? "≤8" : row;
        return `<tr><th>${rowLabel}</th>${cells}</tr>`;
      }).join("");
      return `<h2>${titles[kind][0]}</h2><p>${titles[kind][1]}</p>
        <table aria-label="${titles[kind][0]} strategy chart">
          <thead><tr><th>Hand</th>${dealerValues.map(value => `<th>${label(value)}</th>`).join("")}</tr></thead>
          <tbody>${body}</tbody>
        </table>`;
    }

    function bind() {
      document.getElementById("actions").addEventListener("click", event => {
        const button = event.target.closest("button[data-action]");
        if (button) answer(button.dataset.action);
      });
      document.getElementById("next").addEventListener("click", nextHand);
      document.getElementById("reset").addEventListener("click", () => {
        state.stats = { correct: 0, missed: 0, streak: 0 };
        state.misses = [];
        save();
        updateScore();
        nextHand();
      });
      document.getElementById("modes").addEventListener("click", event => {
        const button = event.target.closest("button[data-mode]");
        if (!button) return;
        state.mode = button.dataset.mode;
        localStorage.setItem("blackjackTrainerMode", state.mode);
        updateModeButtons();
        nextHand();
      });
      window.addEventListener("keydown", event => {
        const keyMap = { h: "H", "1": "H", s: "S", "2": "S", d: "D", "3": "D", p: "P", "4": "P" };
        const move = keyMap[event.key.toLowerCase()];
        if (move) {
          event.preventDefault();
          answer(move);
        }
      });
    }

    document.getElementById("chart-hard").innerHTML = buildChart("hard");
    document.getElementById("chart-soft").innerHTML = buildChart("soft");
    document.getElementById("chart-pair").innerHTML = buildChart("pair");
    bind();
    updateModeButtons();
    updateScore();
    nextHand();
  </script>
</body>
</html>
"""


class AppHandler(BaseHTTPRequestHandler):
    def send_app_response(self, include_body):
        if self.path not in ("/", "/index.html"):
            payload = b"Not found"
            self.send_response(404)
            self.send_header("Content-Type", "text/plain; charset=utf-8")
            self.send_header("Content-Length", str(len(payload)))
            self.end_headers()
            if include_body:
                self.wfile.write(payload)
            return

        payload = APP_HTML.encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        if include_body:
            self.wfile.write(payload)

    def do_GET(self):
        self.send_app_response(include_body=True)

    def do_HEAD(self):
        self.send_app_response(include_body=False)

    def log_message(self, format, *args):
        print("%s - %s" % (self.address_string(), format % args))


def main():
    parser = argparse.ArgumentParser(description="Run the Blackjack Strategy Trainer web app.")
    parser.add_argument("--host", default="127.0.0.1", help="Host to bind. Defaults to 127.0.0.1.")
    parser.add_argument("--port", default=8000, type=int, help="Port to bind. Defaults to 8000.")
    args = parser.parse_args()

    server = ThreadingHTTPServer((args.host, args.port), AppHandler)
    print(f"Blackjack Strategy Trainer running at http://{args.host}:{args.port}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down.")
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
