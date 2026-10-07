"""
The three FitFindr tools.

Each one is a standalone function you can call and test on its own, before any
of them are wired into the loop. Build and test them one at a time — three
untested tools joined by a loop is one problem that looks like six, because you
can't tell which layer is lying to you.

    search_listings(description, size, max_price)  → list[dict]
    suggest_outfit(new_item, wardrobe)             → str
    create_fit_card(outfit, new_item)              → str

All three are stubs right now. They run and they do nothing — that's the
starting position and it's deliberate.

⚠️ Before you write any of them, fill in the **Tool Inventory** section of your
README (Milestone 2). Four lines per tool: what it does, each input with its
type, exactly what it returns, and what it returns when it has nothing to give.
That last line is what your loop branches on. "Returns a list" earns nothing —
the description has to say what is *in* the list.
"""

import re

import config
from generate import generate
from utils.data_loader import load_listings


_SEARCH_STOP_WORDS = {
    "a", "an", "and", "for", "i", "in", "is", "looking", "me", "of",
    "please", "some", "the", "want", "with",
}


def _words(value: str) -> set[str]:
    """Return normalized search words, excluding words with no search value."""
    return {
        word
        for word in re.findall(r"[a-z0-9]+", value.lower())
        if word not in _SEARCH_STOP_WORDS
    }


def _size_tokens(value: str) -> set[str]:
    """Split size labels without treating S as part of US or L as part of XL."""
    aliases = {
        "extra small": "xs",
        "small": "s",
        "medium": "m",
        "large": "l",
        "extra large": "xl",
    }
    normalized = value.strip().lower()
    normalized = aliases.get(normalized, normalized)
    return set(re.findall(r"[a-z]+|\d+(?:\.\d+)?", normalized))


def _matches_size(listing_size: str, requested_size: str) -> bool:
    requested = _size_tokens(requested_size)
    available = _size_tokens(listing_size)
    return bool(requested) and requested.issubset(available)


def _score_listing(listing: dict, query_words: set[str]) -> int:
    """Favor title and style-tag matches over incidental description words."""
    title_score = len(query_words & _words(listing.get("title", ""))) * 3
    tag_score = len(
        query_words & _words(" ".join(listing.get("style_tags", [])))
    ) * 2
    other_fields = " ".join(
        [
            listing.get("description", ""),
            listing.get("category", ""),
            " ".join(listing.get("colors", [])),
            listing.get("brand") or "",
        ]
    )
    return title_score + tag_score + len(query_words & _words(other_fields))


# ── Tool 1: search_listings ───────────────────────────────────────────────────

def search_listings(
    description: str,
    size: str | None = None,
    max_price: float | None = None,
) -> list[dict]:
    """
    Search the listings data for items matching a description, and optionally a
    size and a price ceiling.

    This is the tool that doesn't call the model, which makes it the easiest one
    to test and the one to move onto MCP in unit 4.

    Args:
        description: keywords describing what the user wants
                     (e.g. "vintage graphic tee").
        size:        a size string to filter by, or None to skip size filtering.
                     Match case-insensitively — "M" should match "S/M".

                     ⚠️ Read the sizes in the data before you reach for a plain
                     substring test. `"s" in "us 9"` is True, and so is
                     `"l" in "xl"`. A filter that returns shoes when someone
                     asked for a small top reads like a broken search, and it
                     will quietly cost you in unit 4 when you test criterion 1.
                     What counts as a size match is part of your spec — decide
                     it and write it into your Tool Inventory.
        max_price:   maximum price, inclusive, or None to skip price filtering.

    Returns:
        A list of matching listing dicts, best match first.
        **Returns an empty list when nothing matches — an empty list, not None,
        and not an exception.** Your loop branches on this.

    Each listing dict has these fields:
        id, title, description, category, style_tags (list), size,
        condition, price (float), colors (list), brand (str or None), platform

    Note that `brand` is None for most listings. That is deliberate and
    realistic — thrift listings often have no brand. If something you write
    assumes a brand is always there, you will find out in unit 4.

    TODO:
        1. Load every listing with load_listings().
        2. Filter by max_price and by size, when each is provided.
        3. Score what's left by keyword overlap with `description`.
        4. Drop anything scoring zero.
        5. Sort by score, highest first, and return the listing dicts —
           at most config.SEARCH_RESULT_LIMIT of them.

    Test it from a terminal before you move on:
        python -c "from tools import search_listings; print(search_listings('graphic tee', max_price=30))"
    """
    query_words = _words(description)
    if not query_words:
        return []

    scored: list[tuple[int, dict]] = []
    for listing in load_listings():
        if max_price is not None and listing["price"] > max_price:
            continue
        if size is not None and not _matches_size(listing["size"], size):
            continue

        score = _score_listing(listing, query_words)
        if score:
            scored.append((score, listing))

    scored.sort(key=lambda result: (-result[0], result[1]["price"], result[1]["id"]))
    return [listing for _, listing in scored[: config.SEARCH_RESULT_LIMIT]]


# ── Tool 2: suggest_outfit ────────────────────────────────────────────────────

def suggest_outfit(new_item: dict, wardrobe: dict) -> str:
    """
    Given a thrifted item and the user's wardrobe, suggest one or two outfits.

    This one calls the model, through `generate()`. You don't need to think
    about rate limits — the adapter handles pacing for you.

    Args:
        new_item: a listing dict — the item the user is considering.
        wardrobe: a wardrobe dict with an 'items' key holding a list of items.
                  **It may be empty.** Handle that.

    Returns:
        A non-empty string with outfit suggestions.
        With an empty wardrobe, return general styling advice rather than
        raising or returning "". Unit 4 has you trigger the empty wardrobe on
        purpose, so decide now what it should do.

    TODO:
        1. Check whether wardrobe['items'] is empty.
        2. If it is, ask the model for general styling ideas for this item.
        3. If it isn't, format the wardrobe items into the prompt and ask for
           specific combinations naming pieces the user already owns.
        4. Return the model's response.

    Test it from a terminal before you move on:
        python -c "from tools import suggest_outfit; from utils.data_loader import get_example_wardrobe, load_listings; print(suggest_outfit(load_listings()[0], get_example_wardrobe()))"
    """
    wardrobe_items = wardrobe.get("items", [])
    item_details = (
        f"{new_item['title']} ({', '.join(new_item['colors'])}), "
        f"size {new_item['size']}, with style tags "
        f"{', '.join(new_item['style_tags'])}"
    )

    if not wardrobe_items:
        prompt = (
            f"The new thrift find is {item_details}. Suggest one or two concise "
            "outfits using common wardrobe basics. Give practical general "
            "styling advice because the user has no saved wardrobe items."
        )
    else:
        saved_pieces = "\n".join(
            f"- {item['name']} ({', '.join(item['colors'])}; "
            f"{', '.join(item['style_tags'])})"
            for item in wardrobe_items
        )
        prompt = (
            f"The new thrift find is {item_details}.\n\n"
            f"The user's saved wardrobe contains:\n{saved_pieces}\n\n"
            "Suggest one or two concise outfits. Name the saved pieces exactly "
            "so the user can find them, and explain the overall vibe."
        )

    return generate(
        prompt,
        system=(
            "You are a practical thrift stylist. Use only saved pieces listed "
            "in the prompt when a wardrobe is provided. Return plain text."
        ),
    ).strip()


# ── Tool 3: create_fit_card ───────────────────────────────────────────────────

def create_fit_card(outfit: str, new_item: dict) -> str:
    """
    Write a short caption someone would actually post about the find.

    This calls the model too.

    Args:
        outfit:   the outfit suggestion string from suggest_outfit().
        new_item: the listing dict for the item.

    Returns:
        A two-to-four sentence caption.
        If `outfit` is empty or whitespace, return a descriptive message rather
        than raising.

    The caption should read like a real post rather than a product description,
    mention the item and its price and platform once each, and be specific about
    the vibe.

    It should also come out **differently for different inputs**. If you run
    this three times on the same item and get three word-for-word identical
    strings, it's one of two things, and both are near the top of `config.py`:

        • CACHE_ENABLED — the adapter handed back an answer it already had
        • TEMPERATURE   — at 0.0 the model gives the same words every time

    TODO:
        1. Guard against an empty or whitespace-only `outfit`.
        2. Build a prompt with the item details and the outfit.
        3. Call generate() and return the response.

    Test it from a terminal before you move on:
        python -c "from tools import create_fit_card; from utils.data_loader import load_listings; print(create_fit_card('jeans and white sneakers', load_listings()[0]))"
    """
    if not outfit or not outfit.strip():
        return "A fit card cannot be created until an outfit suggestion is available."

    price = f"${new_item['price']:.2f}"
    prompt = (
        f"Write a social caption for this thrift find.\n"
        f"Exact item title: {new_item['title']}\n"
        f"Exact price: {price}\n"
        f"Exact platform: {new_item['platform']}\n"
        f"Outfit idea: {outfit.strip()}\n\n"
        "Write two to four sentences. Mention the exact item title, exact price, "
        "and platform once each. Make the outfit vibe specific and natural."
    )
    return generate(
        prompt,
        system=(
            "You write concise, post-ready thrift captions. Follow every "
            "required detail and return only the caption."
        ),
    ).strip()
