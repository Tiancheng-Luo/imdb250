import sys
import os
import re
import errno
import json
from contextlib import closing
import xapian as _x
from fetch_data import fetch_movies


FIELDS = ['Title', 'Plot', "Actors", "Director", "Year", "Rated"]
RATED = ["G", "PG", "PG-13", "R"]

def _format_rated(rated):
    if rated not in RATED:
        return "N/A"
    return rated

def main():
    movies = fetch_movies()

    # try to make a db in pwd
    try:
        os.mkdir('./xdb/')
    except (OSError, IOError), e:
        if e.errno != errno.EEXIST:
            raise

    with closing(_x.WritableDatabase('./xdb/movies.db',
                                     _x.DB_CREATE_OR_OPEN)) as x_db:
        for rank, mov in movies:
            # make a new document
            x_doc = _x.Document()
            imdb_id = mov.get(u'imdbID')

            # Store the selected fields for display purposes.
            data = {sel: mov[sel] for sel in FIELDS}
            x_doc.set_data(json.dumps(data, encoding='utf8'))

            # setup indexer
            indexer = _x.TermGenerator()
            indexer.set_stemmer(_x.Stem("english"))
            indexer.set_document(x_doc)

            title = mov.get(u"Title")
            plot = mov.get(u"Plot")
            actors = mov.get(u'Actors')
            directors = mov.get(u"Director")
            year = mov.get(u'Year')
            rated = mov.get(u'Rated')
            
            x_doc.add_term(imdb_id)
            indexer.index_text(title, 1, "S")
            indexer.index_text(title)
            indexer.increase_termpos()
            indexer.index_text(plot)
            indexer.increase_termpos()
            indexer.index_text(actors)
            indexer.increase_termpos()
            indexer.index_text(directors)
            x_doc.add_term("XYEAR{}".format(year))
            #if value is uppercase, then add : between prefix and value
            x_doc.add_term("XRATED:{}".format(_format_rated(rated)))

            # save
            x_db.replace_document(rank, x_doc)


if __name__ == '__main__':
    sys.exit(main())