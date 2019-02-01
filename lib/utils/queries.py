#
# dashboard queries
COUNT_HEADER_BY_NAME = "SELECT " \
    "COUNT" \
        "(header_value_id) " \
    "FROM " \
        "header AS h " \
    "JOIN " \
        "header_name AS hn " \
    "ON " \
        "h.header_name_id = hn.header_name_id " \
    "WHERE " \
        "name = \"{header_name}\""
TOTAL_SITES = "SELECT COUNT(site) FROM site"
COUNT_HEADER_OPTION = "SELECT " \
    "COUNT(h.header_value_id) " \
    "FROM " \
        "header AS h " \
    "JOIN " \
        "header_name as hn " \
    "ON " \
        "h.header_name_id = hn.header_name_id " \
    "JOIN " \
        "header_value AS hv " \
    "ON " \
        "h.header_value_id = hv.header_value_id " \
    "WHERE " \
        "name = \"{}\" and value like \"{}\""
# x-content-type-options
QTD_XCTO_OTHER = "SELECT " \
    "COUNT(h.header_value_id) " \
    "FROM " \
        "header AS h " \
    "JOIN " \
        "header_name AS hn " \
    "ON " \
        "h.header_name_id = hn.header_name_id " \
    "JOIN " \
        "header_value AS hv " \
    "ON " \
        "h.header_value_id = hv.header_value_id " \
    "WHERE " \
        "name = 'x-content-type-options' AND value NOT LIKE '%nosniff%'"
# x-frame-options
QTD_XFO_OTHER = "SELECT " \
    "COUNT(h.header_value_id) " \
    "FROM " \
        "header AS h " \
    "JOIN " \
        "header_name AS hn " \
    "ON " \
        "h.header_name_id = hn.header_name_id " \
    "JOIN " \
        "header_value AS hv " \
    "ON " \
        "h.header_value_id = hv.header_value_id " \
    "WHERE " \
        "name = 'x-frame-options' " \
    "AND " \
        "(value NOT LIKE '%allow-from%' AND value <> 'deny' AND value <> 'sameorigin')"
# x-xss-protection
QTD_XSS_OTHER = "SELECT " \
        "count(h.header_value_id) " \
    "FROM " \
        "header AS h " \
    "JOIN " \
        "header_name AS hn " \
    "ON " \
        "h.header_name_id = hn.header_name_id " \
    "JOIN " \
        "header_value AS hv " \
    "ON " \
        "h.header_value_id = hv.header_value_id " \
    "WHERE " \
        "name = 'x-xss-protection' AND " \
    "(value NOT LIKE '%1%mode=block%' AND value NOT LIKE '%0%mode=block%' AND value NOT LIKE '%report%' AND value NOT LIKE '%0%' AND value NOT LIKE '%1%')"
#
# siteinfo queries
SELECT_SITE_HEADERS = "SELECT " \
        "name, value " \
    "FROM " \
        "site AS s " \
    "LEFT JOIN " \
        "header AS h " \
    "ON " \
        "s.site_id = h.site_id " \
    "LEFT JOIN " \
        "header_name AS hn " \
    "ON " \
        "h.header_name_id = hn.header_name_id " \
    "LEFT JOIN " \
        "header_value AS hv " \
    "ON " \
        "h.header_value_id = hv.header_value_id " \
    "WHERE " \
        "site = \"{site_name}\""
GET_HTTP_HEADER_PERCENT = "SELECT " \
        "(COUNT(h.header_value_id)*100 / " \
    "(SELECT COUNT(header_value_id) " \
    "FROM " \
        "header " \
    "JOIN " \
        "header_name " \
    "ON " \
        "header.header_name_id = header_name.header_name_id " \
    "WHERE " \
        "name = \"{header_name}\")) as percent " \
    "FROM header AS h " \
    "JOIN " \
        "header_name AS hn " \
    "ON " \
        "h.header_name_id = hn.header_name_id " \
    "JOIN " \
        "header_value AS hv " \
    "ON " \
        "h.header_value_id = hv.header_value_id " \
    "WHERE " \
        "name = \"{header_name}\" " \
    "AND " \
        "value = \"{header_value}\""