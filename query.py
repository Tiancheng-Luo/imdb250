import sys
import argparse
from contextlib import closing
import xapian as _x

def _parseq(x_db, query, prefix=''):
    '''parse and return a QueryParser query'''
    qp = _x.QueryParser()
    stemmer = _x.Stem("english")
    qp.set_stemmer(stemmer)
    qp.set_database(x_db)
    qp.set_stemming_strategy(_x.QueryParser.STEM_SOME)
    return qp.parse_query(query, 0, prefix)


def get_parser():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--keyword', required=True, type=str, help='search keyword')
    return parser


def main(args):
    query = args.get('keyword')
    x_query = None
    with closing(_x.Database('./xdb/movies.db')) as x_db:
        # setup the query
        if query:
            x_query = _x.Query(_parseq(x_db, query))

        # setup the enquire object to perform the query
        enq = _x.Enquire(x_db)
        print str(x_query)
        enq.set_query(x_query)
        for res in enq.get_mset(0, x_db.get_doccount(), None, None):
            print res.document.get_data()
            print

if __name__ == '__main__':
    try:
        sys.exit(main(vars(get_parser().parse_args())))
    except Exception:
        sys.exit(3)
