def parsed_list_sql_validator(ref, res, out):
    """
    This is a convenience callback for validating lists of parsed results against 
    a reference list. The comparison of out to ref is done item by item as opposed 
    to the default validator (which compares res). Comparison is done item to item.
    """

    try:
        for i, v in enumerate(res):
            assert v == out[i], "fail_output_result"
    except IndexError:
        raise AssertionError