# rockychef

Generate delicious rock recipes.

Sources rock names from [Wikidata](https://www.wikidata.org/) (cached to minimise API calls), and
generates recipes with a [Tracery](https://tracery.io/) grammar definition.

## Examples

```text
deep fried skarn
sauteéd Leitha limestone
deep fried calc-silicate rock, topped off with some Liesberg limestone juice
deep fried rudite with a side of cantera soup
fromage du red Main sandstone with a side of gritstone salad, topped off with some chocolate sauce
fromage du cataclasite with a side of urtite salad, topped off with some sriracha
boiled baryte stone, topped off with some Saltholm limestone juice
fromage du granitoid with a side of niobium ore dip, topped off with some chocolate sauce
sauteéd Iron-rich sedimentary rocks with a side of nepheline-bearing diorite fondue
fried foid-bearing latite with a side of Pesač limestone salad, topped off with some quartz latite juice
```

## Installation and Usage

Requires Python 3.12 (earlier versions may work, but I haven't tested them).

Install to your system with `pipx`:

```sh
pipx install git+https://github.com/jahinzee/rockychef
```

```sh
$ rockychef --help  
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
