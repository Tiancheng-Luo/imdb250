import sys
import os
import re
import errno
import json
from contextlib import closing
import xapian as _x
from imdb250data import fetch_movies




def _index_id(imdb_id):
    id_str = re.match('.*?([0-9]+)$', imdb_id).group(1)
    return int(id_str)

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
        for mov in movies:
            # make a new document
            x_doc = _x.Document()
            imdb_id = mov.get(u'imdbID')

            # Store the selected fields for display purposes.
            data = {sel: mov[sel] for sel in ['Title', 'Plot', "Actors"]}
            x_doc.set_data(json.dumps(data, encoding='utf8'))

            # setup indexer
            indexer = _x.TermGenerator()
            indexer.set_stemmer(_x.Stem("english"))
            indexer.set_document(x_doc)

            title = mov.get(u"Title")
            plot = mov.get(u"Plot")
            actors = mov.get(u'Actors')
            
            x_doc.add_term(imdb_id)
            indexer.index_text(title, 1, "S")
            indexer.index_text(title)
            indexer.increase_termpos()
            indexer.index_text(plot)
            indexer.index_text(actors)

            # save
            x_id = _index_id(imdb_id)
            x_db.replace_document(x_id, x_doc)
            print x_id

if __name__ == '__main__':
    sys.exit(main())