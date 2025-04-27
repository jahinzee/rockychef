#!/usr/bin/env python3

# rockychef - Generate delicious rock recipes.
#
# Author: Jahin Z. <jahinzee@proton.me>
#
# Sources rock names from Wikidata (cached to minimise API calls), and
# generates recipes with a Tracery grammar definition.
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import re
import sys

from cachier import cachier
from qwikidata.sparql import return_sparql_query_results
from tracery import Grammar, modifiers
from argparse import ArgumentParser, Namespace


def get_args() -> Namespace:
    parser = ArgumentParser("rockychef", description="Generate delicious rock recipes.")
    parser.add_argument(
        "-s",
        "--sentence",
        action="store_true",
        help='format result as "Today\'s special is ..."',
    )
    parser.add_argument(
        "-c",
        "--count",
        type=int,
        required=False,
        default=1,
        help="the number of recipes to generate",
    )
    parser.add_argument(
        "-r",
        "--reload-rocks",
        action="store_true",
        help="clear cached rock database and reload from Wikidata",
    )
    parser.add_argument(
        "-v", "--verbose", action="store_true", help="output verbose error information"
    )
    return parser.parse_args()


@cachier()
def get_rocks() -> list[str]:
    """
    Query Wikidata for all subclasses of "rock".

    Results are also cached with cachier.

    Returns:
        list[str]: the list of rocks.
    """
    # Make a SPARQL query to Wikidata for all rock types.
    IS_A_SUBCLASS = "wdt:P279*"
    ROCK = "wd:Q8063"
    result = return_sparql_query_results(
        (
            "SELECT ?rockLabel "
            "WHERE { "
            f"   ?rock {IS_A_SUBCLASS} {ROCK}. "
            "   SERVICE wikibase:label { "
            '       bd:serviceParam wikibase:language "en" }}'
        )
    )["results"]["bindings"]

    # Extract the labels.
    labels = (r["rockLabel"]["value"] for r in result)

    # Remove anything that doesn't have a valid English label,
    # those just have the Q-value as the label, so we can just
    # regex it out.
    labels_clean = (r for r in labels if not re.match("^Q[0-9]+$", r))

    return list(labels_clean)


def make_recipe(rocks: list[str], sentence: bool = False) -> str:
    """
    Creates a randomly-generated rock recipe.

    Args:
        rocks (list[str]): A list of rocks, loaded from `get_rocks`
        sentence (bool, optional): Use sentence case ("Today's special is ..."). Defaults to False.

    Returns:
        str: The generated string
    """
    grammar = Grammar(
        {
            "origin-sentence": "Today's special is #origin#.",
            "origin": "#prep# #rock##side?##topping?#",
            "prep": ["boiled", "sauteéd", "fried", "deep fried", "fromage du"],
            "rock": rocks,
            "side?": ["", " with a side of #side#"],
            "side": "#rock# #sideprep#",
            "sideprep": ["chips", "soup", "salad", "dip", "fondue", "flakes"],
            "topping?": ["", ", topped off with some #topping#"],
            "topping": [
                "#rock# juice",
                "sriracha",
                "chocolate sauce",
            ],
        }
    )
    grammar.add_modifiers(modifiers.base_english)

    target = "#origin-sentence#" if sentence else "#origin#"
    return grammar.flatten(target)


def main():
    args = get_args()
    try:
        if args.reload_rocks:
            get_rocks.clear_cache()
        rocks = get_rocks()
    except Exception as e:
        display = str(type(e).__name__ if not args.verbose else e)
        print(f"error fetching rock values: {display}", file=sys.stderr)
        if not args.verbose:
            print(
                "help: use `-v` for more detailed error information.", file=sys.stderr
            )
        exit(1)

    for _ in range(args.count):
        print(make_recipe(rocks, sentence=args.sentence))


if __name__ == "__main__":
    main()
