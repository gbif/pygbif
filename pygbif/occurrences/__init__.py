"""
GBIF occurrences APIs methods

* `search`: Search GBIF occurrences
* `get`: Gets details for a single, interpreted occurrence
* `get_verbatim`: Gets a verbatim occurrence record without any interpretation
* `get_fragment`: Get a single occurrence fragment in its raw form (xml or json)
* `count`: Returns occurrence counts for a predefined set of dimensions
* `count_basisofrecord`: Lists occurrence counts by basis of record
* `count_year`: Lists occurrence counts by year
* `count_datasets`: Lists occurrence counts for datasets that cover a given taxon or country
* `count_countries`: Lists occurrence counts for all countries covered by the data published by the given country
* `count_schema`: List the supported metrics by the service
* `count_publishingcountries`: Lists occurrence counts for all countries that publish data about the given country
* `download`: Spin up a download request for GBIF occurrence data
* `download_meta`: Retrieve occurrence download metadata by unique download key
* `download_list`: Lists the downloads created by a user
* `download_get`: Get a download from GBIF
* `download_cancel`: Cancel a download from GBIF
* `download_citation`: Get citation from a download key
* `download_stats`: Get download statistics
* `download_stats_user_country`: Get download counts by user country
* `download_stats_records_by_dataset`: Get downloaded records counts by dataset
* `download_stats_by_dataset`: Get download counts by dataset
* `download_stats_by_source`: Get download statistics by source
"""

from .search import search
from .get import get, get_verbatim, get_fragment
from .count import (
    count,
    count_basisofrecord,
    count_year,
    count_datasets,
    count_countries,
    count_schema,
    count_publishingcountries,
)
from .download import (
    download,
    download_meta,
    download_list,
    download_get,
    download_cancel,
    download_describe,
    download_sql,
    download_citation,
    GbifDownloadError,
)
from .download_stats import (
    download_stats,
    download_stats_user_country,
    download_stats_records_by_dataset,
    download_stats_by_dataset,
    download_stats_by_source,
)
