"""
THE DECK-CHECK COUNT, IN ONE PLACE.

A0 prints how many checks verify_deck.py runs, and A1 prints the command that produces it.
Both used to carry the number as a literal, which is how the deck ended up declaring 83 on one
appendix page and 105 on the next while the checker actually ran 106.

Now: build_full.py imports this to print it, and verify_deck.py asserts BOTH that its own
check list is this long AND that the number on A0 matches. Add a check without updating this
constant and verify_deck fails loudly instead of letting the slide drift.
"""
DECK_CHECK_COUNT = 167
