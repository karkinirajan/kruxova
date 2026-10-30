# ********************************
# IMPORTS python
# ********************************
import math


def util_cal_paging_slice(param_total_items_count, param_items_per_page, param_page):
    """
    calculate sql LIMIT statement offset,limit values

    Args:
        :param param_total_items_count: the count of total items
        :param param_items_per_page: the items to get per page
        :param param_page: the page to process
    """
    items_per_page = int(param_items_per_page)
    page = int(param_page)

    # get the required number of pages to display
    no_of_pages = math.ceil(param_total_items_count / items_per_page)

    # calculate where to start retrieving
    sql_offset = (items_per_page * page) - items_per_page
    sql_limit = items_per_page

    """
    calculate array slice values for paging values
    """
    ArraySliceStart = sql_offset
    ArraySliceEnd = sql_offset + items_per_page
    ValuesDict = {}
    ValuesDict["total_pages"] = no_of_pages
    ValuesDict["sql_offset"] = sql_offset
    ValuesDict["sql_limit"] = sql_limit
    ValuesDict["slice_start"] = ArraySliceStart
    ValuesDict["slice_end"] = ArraySliceEnd

    return ValuesDict
