def parsed_list_sql_validator(ref, res, out):
    """
    This is a convenience callback for validating lists of parsed results against
    a reference list. The comparison of out to ref is done item by item as opposed
    to the default validator (which compares res). Comparison is done item to item.
    """

    if (len(out) != len(res)):
        assert False
    try:
        for i, v in enumerate(res):
            assert v == out[i], "fail_output_result"
    except IndexError:
        raise AssertionError

def test_validator(ref, res, out):
    try:
        assert res == 1, "value_non_unique"
    except AssertionError:
        raise AssertionError

def duplicate_validator(ref, res, out):
    try:
        assert not len(res) != len(set(res)), "value_non_unique"

    except AssertionError:
        raise AssertionError