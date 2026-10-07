# Acceptance criteria — FitFindr

Five criteria that say what "working" means for this agent, written in unit 3
**before** any results existed.

An acceptance criterion names a target: a number, a count, a rate, or something
a person could plainly observe. *"The agent handles errors"* is an opinion.
*"When search returns nothing, the agent stops before calling the second tool,
in 5 of 5 tries"* is a criterion.

Under each one, write a sentence or two on **why that target** and not a
stricter one. A reason that says something about your tools, your loop, or the
data earns credit; *"80% seemed reasonable"* does not.

> Missing your own targets next unit costs you nothing. Setting a target so
> easy you can't miss it does.

**Two are written for you. You write three.**

---

## 1. A matching query completes all three tools

Given a query that matches at least one listing, the agent completes all three
tool calls and returns a fit card — in at least 4 of 5 tries.

**Why this target:**
I chose 4 of 5 because the search uses keyword overlap instead of a model, so
an unusual phrasing can miss a listing even when a person sees the connection.

---

## 2. An impossible query stops before the second tool

Given a query that matches no listings, the agent stops before calling
`suggest_outfit` and returns a message naming what to change — 5 of 5 tries.

**Why this target:**
I chose 5 of 5 because this branch checks a deterministic empty list. It should
never send `None` or a made-up item to the next tool.

---

## 3. The selected listing stays the same across tools

For five matching queries, `session["selected_item"]["id"]` equals the first
search result's ID and the `new_item` passed to `suggest_outfit` has that same
ID — 5 of 5 tries.



**Why this target:**
I chose 5 of 5 because the planning loop copies this value through session
state. No model judgment or random output is involved.


---

## 4. The fit card includes useful listing details

For five matching queries, the fit card is two to four sentences and mentions
the selected item's title, price, and platform — in at least 4 of 5 tries.



**Why this target:**
I chose 4 of 5 because the caption comes from a model and wording can vary. A
single miss is acceptable, but repeated missing details would make the card
unhelpful.


---

## 5. Search respects size and price filters

For five searches that include a size and maximum price, every returned listing
matches the requested size and costs no more than the maximum — 5 of 5 tries.



**Why this target:**
I chose 5 of 5 because size and price filters are deterministic comparisons.
Returning an unaffordable or wrong-size item would violate the user's explicit
request.


---

<!-- ─────────────────────────────────────────────────────────────────────────
     UNIT 4 — read this before you change anything above.

     If a criterion turns out to be BROKEN rather than merely unmet, you can
     revise it, and that earns credit. But never delete or edit the original
     line. Add the revision underneath it, like this:

         ## 4. Something about the fit card

         The fit card is different every time.

         **Why this target:** ...

         > **Revised in unit 4:** For 5 different items, the 5 fit cards share
         > no opening sentence.
         >
         > **Why revised:** "different" wasn't checkable — two cards that
         > differed by one word still counted. The new version is something I
         > can actually score.

     That's a revision because the criterion couldn't be MEASURED.

     Lowering a target because you missed it is not a revision, and it costs
     you the point:

         ✗ "I said the empty search stops it 5 of 5 times, but I got 3 of 5,
            so 3 of 5 is more realistic."

     A number you missed stays where it is, gets diagnosed, and gets a fix
     attempted. That's where the points are.
     ───────────────────────────────────────────────────────────────────────── -->
