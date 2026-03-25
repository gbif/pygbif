# import external libraries

# import internal libraries
from ..gbifutils import gbif_GET, gbif_baseurl, stop


def download_stats(
    fromDate=None,
    toDate=None,
    publishingCountry=None,
    datasetKey=None,
    publishingOrgKey=None,
    limit=20,
    offset=0,
    **kwargs
):
    """
    Get download statistics for downloads matching the provided criteria.
    
    Returns counts by year, month and dataset of the total number of downloads, 
    and the total number of records included in those downloads.

    :param fromDate: [str] Date to start from (YYYY-MM-DD format)
    :param toDate: [str] Date to end at (YYYY-MM-DD format)
    :param publishingCountry: [str] ISO 3166-2 country code
    :param datasetKey: [str] Dataset UUID
    :param publishingOrgKey: [str] Publishing organization UUID
    :param limit: [int] Number of records to return. Default: ``20``
    :param offset: [int] Record number to start at. Default: ``0``
    :param **kwargs: Further named arguments passed on to ``requests.get``

    :return: A dictionary of results

    Usage::

        from pygbif import occurrences as occ
        
        # Get all download statistics
        occ.download_stats()
        
        # Filter by date range
        occ.download_stats(fromDate='2023-01-01', toDate='2023-12-31')
        
        # Filter by publishing country
        occ.download_stats(publishingCountry='US')
        
        # Filter by dataset
        occ.download_stats(datasetKey='50c9509d-22c7-4a22-a47d-8c48425ef4a7')
        
        # Combine filters
        occ.download_stats(
            fromDate='2023-01-01', 
            toDate='2023-12-31',
            publishingCountry='US',
            limit=50
        )
    """
    url = gbif_baseurl + "occurrence/download/statistics"
    args = {
        "fromDate": fromDate,
        "toDate": toDate,
        "publishingCountry": publishingCountry,
        "datasetKey": datasetKey,
        "publishingOrgKey": publishingOrgKey,
        "limit": limit,
        "offset": offset,
    }
    # Remove None values
    args = {k: v for k, v in args.items() if v is not None}
    return gbif_GET(url, args, **kwargs)

def download_stats_user_country(
    fromDate=None, 
    toDate=None, 
    userCountry=None, 
    **kwargs
):
    """
    Get counts of user downloads by month, grouped by the user's country.

    Provides counts of user downloads by month, grouped by the user's 
    ISO 3166-2 country, territory or island.

    :param fromDate: [str] The year and month (YYYY-MM) to start from
    :param toDate: [str] The year and month (YYYY-MM) to end at
    :param userCountry: [str] The ISO 3166-2 code for the user's country, territory or island
    :param **kwargs: Further named arguments passed on to ``requests.get``

    :return: A dictionary of results

    Usage::

        from pygbif import occurrences as occ
        
        # Get all download counts by user country
        occ.download_stats_user_country()
        
        # Filter by date range
        occ.download_stats_user_country(
            fromDate='2023-01', 
            toDate='2023-12'
        )
        
        # Filter by specific user country
        occ.download_stats_user_country(userCountry='US')
        
        # Combine filters
        occ.download_stats_user_country(
            fromDate='2023-01',
            toDate='2023-12',
            userCountry='US'
        )
    """
    url = gbif_baseurl + "occurrence/download/statistics/downloadsByUserCountry"
    args = {
        "fromDate": fromDate,
        "toDate": toDate,
        "userCountry": userCountry,
    }
    # Remove None values
    args = {k: v for k, v in args.items() if v is not None}
    return gbif_GET(url, args, **kwargs)


def download_stats_records_by_dataset(
    fromDate=None,
    toDate=None,
    publishingCountry=None,
    datasetKey=None,
    publishingOrgKey=None,
    **kwargs
):
    """
    Get counts of downloaded records by dataset.

    Returns the number of occurrence records downloaded from each dataset 
    for downloads matching the provided criteria.

    :param fromDate: [str] Date to start from (YYYY-MM-DD format)
    :param toDate: [str] Date to end at (YYYY-MM-DD format)
    :param publishingCountry: [str] ISO 3166-2 country code
    :param datasetKey: [str] Dataset UUID
    :param publishingOrgKey: [str] Publishing organization UUID
    :param **kwargs: Further named arguments passed on to ``requests.get``

    :return: A dictionary of results

    Usage::

        from pygbif import occurrences as occ
        
        # Get downloaded records by dataset
        occ.download_stats_records_by_dataset()
        
        # Filter by date range
        occ.download_stats_records_by_dataset(
            fromDate='2023-01-01',
            toDate='2023-12-31'
        )
        
        # Filter by country
        occ.download_stats_records_by_dataset(publishingCountry='US')
    """
    url = gbif_baseurl + "occurrence/download/statistics/downloadedRecordsByDataset"
    args = {
        "fromDate": fromDate,
        "toDate": toDate,
        "publishingCountry": publishingCountry,
        "datasetKey": datasetKey,
        "publishingOrgKey": publishingOrgKey,
    }
    # Remove None values
    args = {k: v for k, v in args.items() if v is not None}
    return gbif_GET(url, args, **kwargs)


def download_stats_by_dataset(
    fromDate=None,
    toDate=None,
    publishingCountry=None,
    datasetKey=None,
    publishingOrgKey=None,
    **kwargs
):
    """
    Get download counts by dataset.

    Returns the number of downloads that included records from each dataset 
    for downloads matching the provided criteria.

    :param fromDate: [str] Date to start from (YYYY-MM-DD format)
    :param toDate: [str] Date to end at (YYYY-MM-DD format)
    :param publishingCountry: [str] ISO 3166-2 country code
    :param datasetKey: [str] Dataset UUID
    :param publishingOrgKey: [str] Publishing organization UUID
    :param **kwargs: Further named arguments passed on to ``requests.get``

    :return: A dictionary of results

    Usage::

        from pygbif import occurrences as occ
        
        # Get download counts by dataset
        occ.download_stats_by_dataset()
        
        # Filter by date range
        occ.download_stats_by_dataset(
            fromDate='2023-01-01',
            toDate='2023-12-31'
        )
        
        # Filter by publishing country
        occ.download_stats_by_dataset(publishingCountry='DK')
        
        # Filter by dataset
        occ.download_stats_by_dataset(
            datasetKey='50c9509d-22c7-4a22-a47d-8c48425ef4a7'
        )
    """
    url = gbif_baseurl + "occurrence/download/statistics/downloadsByDataset"
    args = {
        "fromDate": fromDate,
        "toDate": toDate,
        "publishingCountry": publishingCountry,
        "datasetKey": datasetKey,
        "publishingOrgKey": publishingOrgKey,
    }
    # Remove None values
    args = {k: v for k, v in args.items() if v is not None}
    return gbif_GET(url, args, **kwargs)


def download_stats_by_source(
    fromDate=None,
    toDate=None,
    source=None,
    **kwargs
):
    """
    Get download statistics by source.

    Returns download statistics grouped by source for downloads matching 
    the provided criteria.

    :param fromDate: [str] The year and month (YYYY-MM) to start from
    :param toDate: [str] The year and month (YYYY-MM) to end at
    :param source: [str] Source name to filter by (e.g., 'pygbif', 'rgbif')
    :param **kwargs: Further named arguments passed on to ``requests.get``

    :return: A dictionary of results

    Usage::

        from pygbif import occurrences as occ
        
        # Get download statistics by source
        occ.download_stats_by_source()
        
        # Filter by date range
        occ.download_stats_by_source(
            fromDate='2023-01',
            toDate='2023-12'
        )
        
        # Filter by source
        occ.download_stats_by_source(source='pygbif')
    """
    url = gbif_baseurl + "occurrence/download/statistics/downloadsBySource"
    args = {
        "fromDate": fromDate,
        "toDate": toDate,
        "source": source,
    }
    # Remove None values
    args = {k: v for k, v in args.items() if v is not None}
    return gbif_GET(url, args, **kwargs)
