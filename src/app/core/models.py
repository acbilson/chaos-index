from collections import namedtuple

Site = namedtuple('Site', 'id author url partial_links link_query title_query content_query')
File = namedtuple('File', 'id link path site_id')

Metadata = namedtuple('Metadata', 'url author title content')
