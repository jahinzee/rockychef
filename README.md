# rockychef

Generate delicious rock recipes.

Sources rock names from [Wikidata](https://www.wikidata.org/) (cached to minimise API calls), and
generates recipes with a [Tracery](https://tracery.io/) grammar definition.

## Usage

```text
usage: rockychef [-h] [-s] [-c COUNT] [-r] [-v]

Generate delicious rock recipes.

options:
  -h, --help            show this help message and exit
  -s, --sentence        format result as "Today's special is ..."
  -c COUNT, --count COUNT
                        the number of recipes to generate
  -r, --reload-rocks    clear cached rock database and reload from Wikidata
  -v, --verbose         output verbose error information
```
