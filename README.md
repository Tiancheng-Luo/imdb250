# Xapian Search Application for IMDB 250 

### Installation
1. Download Xapian
  - Get the latest stable tar ball from [its download page](http://xapian.org/download) 
  - Install its Python bindings
    - `pip install xapian`
2. Installing Xapian
  - Follow the steps in its [install page](http://xapian.org/docs/install.html)


### Index Xapian Database
- `git clone git@github.com:jingle3276/imdb250.git`
- `cd imdb250`
- Run `python index.py`


### Query the Search Engine
- Simple keyword query: `python query.py --keyword 'dream'`
- Phrase query: `python query.py --keyword '"once again"'`
- Movie title: `python query.py --title 'king'`
- Facets on result movies' rating: `python query.py --keyword 'love' --show_facets`
- Search moives contains word 'love' and rated PG-13 and released between year 1990 to 2000 `python query.py --keyword 'love' --rated PG-13 --year_range '1990..2000'`
