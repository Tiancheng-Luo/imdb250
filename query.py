import sys
import argparse
from contextlib import closing
import xapian as _x

from index import RATED

def _query_parser(x_db):
    '''parse and return a QueryParser query'''
    qp = _x.QueryParser()
    stemmer = _x.Stem("english")
    qp.set_stemmer(stemmer)
    qp.set_database(x_db)
    qp.set_stemming_strategy(_x.QueryParser.STEM_SOME)
    return qp

def _joinq(op, first, sec):
    if not first:
        return sec
    return _x.Query(op, first, sec)


def get_parser():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--keyword', required=True, type=str, help='search keyword')
    parser.add_argument('--rated', nargs='*', choices=RATED)
    parser.add_argument('--year_range', type=str, help='release year range(e.g: 1950..1975)')
    return parser


def main(args):
    keyword = args.get('keyword')
    rated_list = args.get('rated')
    year_range = args.get('year_range')
    x_query = None
    with closing(_x.Database('./xdb/movies.db')) as x_db:
        # setup the query
        qp = _query_parser(x_db)
        x_query = qp.parse_query(keyword)

        if rated_list:
            rated_queries = [_x.Query('XR:{}'.format(rated)) for rated in rated_list]
            rated_query = _x.Query(_x.Query.OP_OR, rated_queries)
            x_query = _joinq(_x.Query.OP_FILTER, x_query, rated_query)

        if year_range:
            qp.add_valuerangeprocessor(
                _x.NumberValueRangeProcessor(0, '')
            )
            year_range_query = qp.parse_query(year_range)
            x_query = _joinq(_x.Query.OP_FILTER, x_query, year_range_query)

        # setup the enquire object to perform the query
        enq = _x.Enquire(x_db)
        print str(x_query)
        enq.set_query(x_query)
        for res in enq.get_mset(0, x_db.get_doccount(), None, None):
            print res.document.get_data()
            print

if __name__ == '__main__':
    sys.exit(main(vars(get_parser().parse_args())))

