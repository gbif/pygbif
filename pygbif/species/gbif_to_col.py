"""
Convert GBIF Backbone taxon keys to COL Extended Release keys
"""

from pygbif.gbifutils import gbif_GET, gbif_baseurl


def gbif_to_col(
    key,
    **kwargs
):
    """
    Convert GBIF Backbone taxon keys to COL Extended Release keys

    :param key: [int/str/list] One or more GBIF Backbone numeric taxon keys to convert
        to COL Extended Release alpha-numeric keys. Can be a single value or a list of values.
    :param \\*\\*kwargs: Curl options passed to requests

    :return: If a single key is provided, returns a dictionary containing the full API response
        with keys:
        
        - ``gbif_key`` - The input GBIF Backbone key
        - ``usage`` - The matched COL taxon usage details (including the COL key)
        - ``classification`` - Full taxonomic classification path
        - ``diagnostics`` - Match quality information (matchType, confidence, etc.)
        - ``additionalStatus`` - Additional status information (e.g., IUCN status)
        - ``synonym`` - Whether the match is a synonym
        
        If multiple keys are provided, returns a list of such dictionaries.

    This function uses the GBIF species matching API with the ``scientificNameID`` parameter
    to resolve GBIF Backbone taxonomy keys to COL Extended Release keys. This is useful when
    migrating existing code from numeric GBIF Backbone keys to the new COL XR alpha-numeric keys.

    References: https://techdocs.gbif.org/en/openapi/v1/species

    Usage::

        from pygbif import species
        
        # Convert a single GBIF Backbone key to COL XR
        result = species.gbif_to_col(5231190)  # Passer domesticus (house sparrow)
        print(result['gbif_key'])              # 5231190
        print(result['usage']['key'])          # COL XR key: "4DXXM"
        print(result['usage']['name'])         # Passer domesticus (Linnaeus, 1758)
        print(result['classification'])        # Full taxonomic hierarchy
        print(result['diagnostics']['matchType'])    # Quality of match
        print(result['diagnostics']['confidence'])   # Confidence score

        # Convert multiple keys at once
        results = species.gbif_to_col([5231190, 2435099, 2877951])
        
        # Extract specific data from multiple results:
        col_keys = [r['usage']['key'] for r in results if r['usage']]
        names = [r['usage']['name'] for r in results if r['usage']]
    """
    # Validate input
    if key is None:
        raise ValueError("key parameter is required")

    # Handle single key vs list of keys
    single_key = not isinstance(key, (list, tuple))
    keys = [key] if single_key else key

    # Convert to strings
    keys = [str(k) for k in keys]

    # Process each key
    results = []
    for k in keys:
        # Build scientificNameID in GBIF format
        scientific_name_id = f"gbif:{k}"

        # Build API URL - use v2 API for COL Extended Release keys
        url = gbif_baseurl.replace("/v1/", "/v2/") + "species/match"

        # Build query arguments - always use COL Extended Release
        args = {
            "checklistKey": "7ddf754f-d193-4cc9-b351-99906754a03b",
            "scientificNameID": scientific_name_id
        }

        # Make the API call
        try:
            response = gbif_GET(url, args, **kwargs)
            # Add the original key to the response
            result = {"gbif_key": k}
            result.update(response)
            results.append(result)
        except Exception as e:
            # On error, return a result with null usage
            results.append({
                "gbif_key": k,
                "usage": None,
                "classification": None,
                "diagnostics": None,
                "additionalStatus": None,
                "synonym": None,
                "error": str(e)
            })

    # Return single dict or list based on input
    return results[0] if single_key else results
