# FitFindr

> ### 👋 Start here
>
> **New to this repo? Read [RUNNING.md](RUNNING.md) first** — setup, every
> command, and what to do when something breaks.
>
> Once `python test.py` passes:
>
> ```bash
> python app.py listings --full -n 6      # read the data (Milestone 1)
> python app.py fields                    # what you can filter on
> python app.py ask 'vintage graphic tee under $30'
> ```
>
> All three tools are stubs, so that last command will do nothing useful yet.
> That's the starting position.
>
> **The rest of this file is your submission.** Fill it in as you go.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     HOW TO USE THIS FILE

     This is your submission. Fill each section in as you finish the milestone
     it belongs to — don't leave it all to the end.

     Unit 3 asks for the first five sections. Unit 4 adds the five below them.
     Leave the unit 4 sections alone until then; they're here so you know
     what's coming.

     Everything is pasted as TEXT. No screenshots, no images, no video links.
     A typed block of output gets full credit; a picture of the same output
     gets none.
     ───────────────────────────────────────────────────────────────────────── -->

<!-- ═══════════════════════ UNIT 3 — THE BUILD ═══════════════════════ -->

## What This Does
FitFindr takes a plain-language request for a thrift item, including an optional
size and maximum price. It searches a local listings collection and selects the
best keyword match. It then combines that item with pieces in the user's
wardrobe and returns an outfit suggestion plus a short, post-ready fit card.
<!-- Three or four sentences: what a user asks for, and what they get back. -->



---

## Tool Inventory

<!-- Four lines per tool. This is worth 2 points and it's the single most
     common place students lose them.

     "Returns a list" earns NOTHING. The description has to say what is IN
     the list.

     The empty case isn't optional either — it's the thing your loop branches
     on, and if you don't decide it here you'll discover it as a crash in
     Milestone 5. -->

### `search_listings`

- **What it does:** Filters local thrift listings and ranks them by keyword overlap.
- **Inputs:** `description` (`str`), `size` (`str | None`), and `max_price` (`float | None`).
- **Returns:** A list of at most 10 listing dictionaries, best match first. Each dictionary includes `id`, `title`, `description`, `category`, `style_tags`, `size`, `condition`, `price`, `colors`, `brand`, and `platform`.
- **When it has nothing:** Returns an empty list.

### `suggest_outfit`

- **What it does:** Uses the selected listing and saved wardrobe to suggest one or two outfits.
- **Inputs:** `new_item` (`dict`) and `wardrobe` (`dict` with an `items` list).
- **Returns:** A non-empty string containing specific outfit ideas that name saved wardrobe pieces.
- **When it has nothing:** If the wardrobe is empty, returns general styling advice for the new item instead of failing.

### `create_fit_card`

- **What it does:** Turns the selected listing and outfit suggestion into a social caption.
- **Inputs:** `outfit` (`str`) and `new_item` (`dict`).
- **Returns:** A two-to-four-sentence string naming the item, price, platform, and outfit vibe.
- **When it has nothing:** If `outfit` is empty or whitespace, returns a descriptive message explaining that a fit card cannot be created.

---

## Planning Loop

<!-- Your branch rule, stated as a rule — the condition AND both paths — plus
     the file and function that holds it.

     Like this:
       "If search_listings returns an empty list, put a message in the session
        and stop. Otherwise take the first result and go to suggest_outfit."
        — agent.py::run_agent

     The grader checks your code against what you claim here, so the file and
     function have to be real. -->

**Branch rule:** If `search_listings` returns an empty list, store a message that
names filters the user can change and stop. Otherwise, select the first result,
pass it through session state to `suggest_outfit`, then call `create_fit_card`.

**Where it lives:** `agent.py::run_agent`

**How the query is parsed:** Regular expressions extract `under $PRICE` and
`size SIZE`; the remaining cleaned words become the description.

**What moves through the session:** `parsed` feeds `search_results`; the first
result becomes `selected_item`; that item and `wardrobe` produce
`outfit_suggestion`; the outfit and same selected item produce `fit_card`.

---

## Sample Run

<!-- Two things go here.

     1. One FULL query and its output, pasted as text.
     2. Your three per-tool terminal tests — the command and what it printed. -->

**One full query**

```
$ python app.py ask 'vintage graphic tee under $30'

  Found:    Graphic Tee — 2003 Tour Bootleg Style — $24.0 on depop

  Outfit:   Pair the Graphic Tee — 2003 Tour Bootleg Style with Baggy
  straight-leg jeans, dark wash and Black combat boots for a relaxed grunge
  look. Add the Vintage black denim jacket for another textured layer.

  Fit card: Found this Graphic Tee — 2003 Tour Bootleg Style for $24.00 on
  depop. I’m pairing it with baggy dark-wash jeans, black combat boots, and the
  cropped vintage denim jacket for an easy grunge-streetwear vibe. The faded
  graphic does all the work.

2 model calls this session

```

**The three tools, tested one at a time**

```
$ python -c "from tools import search_listings; print([(x['title'], x['price'], x['size'], x['platform']) for x in search_listings('graphic tee', max_price=30)])"

[('Graphic Tee — 2003 Tour Bootleg Style', 24.0, 'L', 'depop'),
 ('Y2K Baby Tee — Butterfly Print', 18.0, 'S/M', 'depop'),
 ('Vintage Band Tee — Faded Grey', 19.0, 'L', 'depop'),
 ('Vintage Graphic Hoodie — Faded Black', 26.0, 'L', 'depop'),
 ('Mesh Long-Sleeve Top — Black', 15.0, 'S/M', 'depop'),
 ('Low-Rise Cargo Pants — Khaki', 27.0, 'W29', 'poshmark')]
```

```
$ python -c "from tools import suggest_outfit; from utils.data_loader import get_example_wardrobe, load_listings; print(suggest_outfit(load_listings()[5], get_example_wardrobe()))"

Pair the Graphic Tee — 2003 Tour Bootleg Style with Baggy straight-leg jeans,
dark wash and Black combat boots for a relaxed grunge look. Add the Vintage
black denim jacket for another textured layer.
```

```
$ python -c "from tools import create_fit_card; from utils.data_loader import load_listings; print(create_fit_card('Baggy jeans and black combat boots.', load_listings()[5]))"

Found this Graphic Tee — 2003 Tour Bootleg Style for $24.00 on depop. I’m
pairing it with baggy dark-wash jeans, black combat boots, and the cropped
vintage denim jacket for an easy grunge-streetwear vibe. The faded graphic does
all the work.
```

---

## How I Used AI

<!-- Two specific moments. What you asked, what came back, what you changed.

     "I used Claude to help me code" is not enough.

     "I gave Claude my search_listings spec. It returned None on no match
     instead of an empty list, so I changed it" is the level we want. -->

**Moment 1**

- *What I asked for:* I asked Codex to test whether each acceptance criterion
  could be checked using only the words in the criterion.
- *What came back:* It pointed out that my state criterion needed to compare a
  concrete identifier at both sides of the tool boundary.
- *What I changed:* I made criterion 3 compare the first search result's ID,
  `session["selected_item"]["id"]`, and the ID passed to `suggest_outfit`.

**Moment 2**

- *What I asked for:* I asked Codex to check my planned size-matching rule for
  edge cases in the provided listing data.
- *What came back:* It showed that substring matching would treat `S` as part
  of `US 9` and `L` as part of `XL`.
- *What I changed:* I split both size values into complete tokens and compare
  those tokens, while still allowing `M` to match combined sizes such as `S/M`.

**Moment 3**

- *What I asked for:* I asked Codex to argue against my Unit 4 verdicts using
  the five recorded tries and the original targets.
- *What came back:* It could not support marking criteria 1 or 4 as met because
  every run lacked a fit card, even though search and state still worked.
- *What I changed:* I kept both verdicts as MISSED and diagnosed their shared
  cause at the `suggest_outfit` model call instead of blaming search or session
  state.

<!-- ═══════════════════════ UNIT 4 — THE TEST ═══════════════════════

     Don't fill these in during unit 3.
     ═══════════════════════════════════════════════════════════════════ -->

---

## Run Log — Before

<!-- Five criteria, five tries each, in this exact format.

     Five, because your criteria are written out of five. Mark each try PASS
     or FAIL, count the passes, and read that count against your target — a
     row targeting 4 of 5 with three PASS cells is MISSED (3/5).

     `python run_eval.py --label before` runs everything and writes the table
     into results/. Paste it here and fill in the verdicts. -->

| Criterion | Target | Try 1 | Try 2 | Try 3 | Try 4 | Try 5 | Verdict |
|---|---|---|---|---|---|---|---|
| 1. Full three-tool run returns a fit card | 4 of 5 | FAIL | FAIL | FAIL | FAIL | FAIL | MISSED (0/5) |
| 2. Empty search stops before tool 2 | 5 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 3. Selected item stays the same across tools | 5 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 4. Fit card has title, price, platform, and 2–4 sentences | 4 of 5 | FAIL | FAIL | FAIL | FAIL | FAIL | MISSED (0/5) |
| 5. Search respects size and maximum price | 5 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |

**Real output from one try**, pasted as text, naming the file and function
that produced it:

Produced by `run_eval.py::main` in
`results/run_2026-10-21_1952_before.md`; each session came from
`agent.py::run_agent`.

```text
Criterion 1, try 1
selected_item: lst_006 | Graphic Tee — 2003 Tour Bootleg Style
search_results: 10
[1] search_listings (via MCP)
      in:  description='vintage graphic tee', size=None, max_price=30.0
      out: 10 items: lst_006: Graphic Tee — 2003 Tour Bootleg Style, ...
      →    branch: matches found; continue
[2] suggest_outfit
      in:  new_item_id='lst_006', wardrobe_items=10
      out: The styling model is unavailable. Check GEMINI_API_KEY in .env...
      →    model unavailable; stopping

Criterion 2, try 1
[1] search_listings (via MCP)
      in:  description='designer ballgown', size='XXS', max_price=5.0
      out: [] (empty)
      →    branch: empty; stopping
error: No listings matched. Try a larger budget, another size, or fewer
description words.

Criterion 3, try 1
selected_item: lst_004 | 90s Track Jacket — Navy/White Stripe
[1] search_listings (via MCP)
      out: 3 items: lst_004: 90s Track Jacket — Navy/White Stripe, ...
[2] suggest_outfit
      in:  new_item_id='lst_004', wardrobe_items=10

Criterion 4, try 1
selected_item: lst_013 | 90s Silk Slip Dress — Floral, Midi Length
fit_card: (none; styling model unavailable before create_fit_card)

Criterion 5, try 1
[1] search_listings (via MCP)
      in:  description='graphic tee', size='L', max_price=25.0
      out: lst_006 (size L, $24.0), lst_033 (size L, $19.0)
```

---

## Verdicts and Diagnoses

<!-- MET or MISSED per criterion against LAST UNIT's target, plus a sentence on
     how you decided.

     Then, for every miss: which of the four places it happened — a tool, the
     loop's branch, the session, or the model's output — AND the mechanism.

     Not a diagnosis:  "The fit card was bad."
     A diagnosis:      "The fit card criterion missed on 2 of 5 items. Both had
                        an empty brand field. My prompt puts the brand in the
                        first sentence, so the card opened with a blank and read
                        like a fragment. The tool worked; the prompt assumed a
                        field that isn't always there."

     Look for a pattern. Three misses on the same tool is one problem, not
     three. -->

| # | Criterion | Target | Verdict | How I decided |
|---|---|---|---|---|
| 1 | Full three-tool run returns a fit card | 4 of 5 | MISSED (0/5) | All five runs stopped in `suggest_outfit`, so none reached `create_fit_card`. |
| 2 | Empty search stops before tool 2 | 5 of 5 | MET (5/5) | All five MCP searches returned `[]`; every run stopped with an actionable message and no selected item. |
| 3 | Selected item stays the same across tools | 5 of 5 | MET (5/5) | In all five traces, first result `lst_004`, `session["selected_item"]`, and `suggest_outfit` input were `lst_004`. |
| 4 | Fit card has required details and length | 4 of 5 | MISSED (0/5) | No run produced a fit card, so none could meet the content or length checks. |
| 5 | Search respects size and maximum price | 5 of 5 | MET (5/5) | Every run returned only `lst_006` (L, $24) and `lst_033` (L, $19), both within size L and $25. |

**Diagnoses**

Criteria 1 and 4 share one failure. The failure occurred in the model-backed
`suggest_outfit` tool, before `create_fit_card`. `generate.py` could not find a
`GEMINI_API_KEY`, raised `ModelUnavailable`, and the planning loop stopped with
an actionable message. Search, MCP transport, branch logic, and session state
continued to behave as specified. This was an environment/configuration
failure, not model-output variation or a prompt-quality failure.

The empty-wardrobe diagnostic reached `suggest_outfit` with
`wardrobe_items=0`, but the missing key prevented the model from returning the
general advice. The handler correctly reported what broke and told the user to
add the key and retry.


---

## Loop Trace

<!-- One full run, printed step by step, with the MCP call visible in it.

     `python app.py ask '...' --trace` once you've added the trace.step()
     calls in Milestone 2.

     Worth pasting BOTH the happy path and the empty-search path. The empty
     one should be visibly shorter, because it stops. If your two traces are
     the same length, your branch isn't working — and this is the fastest way
     anyone will ever find that out. -->

**Attempted happy path**

```text
[1] search_listings (via MCP)
      in:  description='vintage graphic tee', size=None, max_price=30.0
      out: 10 items: lst_006: Graphic Tee — 2003 Tour Bootleg Style,
           lst_033: Vintage Band Tee — Faded Grey,
           lst_015: Vintage Graphic Hoodie — Faded Black … +7 more
      →    branch: matches found; continue
[2] suggest_outfit
      in:  new_item_id='lst_006',
           new_item_title='Graphic Tee — 2003 Tour Bootleg Style',
           wardrobe_items=10
      out: The styling model is unavailable. Check GEMINI_API_KEY in .env
           and your internet connection, then try again.
      →    model unavailable; stopping
```

This trace is shorter than a successful three-tool run because no API key was
available. It records the exact stopping point instead of inventing model
output.

**Empty search**

```text
[1] search_listings (via MCP)
      in:  description='designer ballgown', size='XXS', max_price=5.0
      out: [] (empty)
      →    branch: empty; stopping
```

**On the MCP move:** `search_listings` is registered in `mcp_server.py`, and
`agent.py::run_agent` now calls it through `mcp_client.call_tool`. Its native
return shape remained `list[dict]`; matching queries returned the same ranked
items and impossible queries still returned `[]`. Only the call boundary and
trace label changed.


---

## The Improvement

<!-- What you changed, why your diagnosis pointed at it, and the after-run in
     the same table format. One change, measured properly.

     `python run_eval.py --label after` -->

**What I changed:** I changed model-error classification in `generate.py` and
the handler text in `agent.py`. A missing key now says no key is configured and
gives the exact `.env` recovery step. It no longer claims the provider rejected
a key that does not exist.

**Which failure it was meant to fix:** The baseline's model-unavailable message
identified the wrong mechanism: “The model rejected your API key.” The trace
showed that this environment had no key at all.

### Run Log — After

| Criterion | Target | Try 1 | Try 2 | Try 3 | Try 4 | Try 5 | Verdict |
|---|---|---|---|---|---|---|---|
| 1. Full three-tool run returns a fit card | 4 of 5 | FAIL | FAIL | FAIL | FAIL | FAIL | MISSED (0/5) |
| 2. Empty search stops before tool 2 | 5 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 3. Selected item stays the same across tools | 5 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 4. Fit card has title, price, platform, and 2–4 sentences | 4 of 5 | FAIL | FAIL | FAIL | FAIL | FAIL | MISSED (0/5) |
| 5. Search respects size and maximum price | 5 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |

**Did it help, and how do I know:** It improved the failure message in all five
model-dependent tries. Before: “The model rejected your API key.” After: “No
GEMINI_API_KEY is configured. Copy .env.example to .env, add your key, and try
again.” Acceptance counts did not change because message quality cannot replace
the missing model. The after evidence is
`results/run_2026-10-21_1953_after.md`, produced by `run_eval.py::main`.

<!-- If it made things worse, say that. Honestly reported, that earns full
     credit and is more interesting than one that worked. -->



---

## What's Still Broken
Criteria 1 and 4 remain missed because this checkout has no `GEMINI_API_KEY`.
I would add the key to ignored `.env`, run `python test.py`, then rerun
`python run_eval.py --label after-key` to measure real outfit and fit-card
outputs. I stopped because inventing model output or committing a secret would
make the evidence invalid.

The empty-wardrobe branch reached `suggest_outfit` with zero wardrobe items,
but the same missing key prevented general advice from being generated. A full
three-tool happy-path trace is therefore also still missing; the committed
trace honestly shows the exact stopping point.
<!-- For each criterion still missed: what you'd do, and why you stopped where
     you did. "I ran out of time" is fine if it's true. Pretending nothing is
     left is not. -->



<!-- ═════════════════════════════════════════════════════════════════════

     SUBMISSION CHECKLIST — unit 3

       [ ] criteria.md has five numbered criteria, each with a target
       [ ] Each criterion has a reason underneath it
       [ ] All five unit 3 sections above have real content
       [ ] Tool Inventory: all three tools, inputs WITH TYPES, a specific
           return value, and the empty case
       [ ] Planning Loop names the branch rule and agent.py::run_agent
       [ ] Sample Run: one full query plus the three per-tool tests, as text
       [ ] At least four new commits
       [ ] Repository URL submitted — WRITE IT DOWN, you submit the same one
           next unit

     SUBMISSION CHECKLIST — unit 4

       [ ] mcp_server.py exists with one tool registered
           (or a written record of exactly where the rewire broke)
       [ ] Run Log — Before, five criteria, five tries each
       [ ] Real output pasted underneath, naming file and function
       [ ] A verdict on every criterion
       [ ] A diagnosis for every miss, naming a place AND a mechanism
       [ ] Loop Trace, with the MCP call visible in it
       [ ] All three failure modes triggered and handled
       [ ] One improvement, with Run Log — After in the same format
       [ ] What's Still Broken
       [ ] At least four new commits
       [ ] The SAME repository URL as last unit

     Do not delete and recreate this repository. Your commit history is what
     shows your criteria existed before your results did.
     ═════════════════════════════════════════════════════════════════════ -->

---

📖 **How to run this project: [RUNNING.md](RUNNING.md)**
