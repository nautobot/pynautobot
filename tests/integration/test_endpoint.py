class TestPagination:
    """Verify we can limit and offset results on an endpoint."""

    def test_all_content_types_with_offset(self, nb_client):
        limit = 10
        offset = 5
        offset_cts = nb_client.extras.content_types.all(limit=limit, offset=offset)
        assert len(offset_cts) == limit

    def test_all_content_types_with_limit(self, nb_client):
        content_types = nb_client.extras.content_types.all()
        limited_cts = nb_client.extras.content_types.all(limit=10)
        assert len(content_types) == len(limited_cts)

    def test_filter_content_types_with_offset(self, nb_client):
        limit = 10
        offset = 5
        offset_cts = nb_client.extras.content_types.filter(app_label="dcim", limit=limit, offset=offset)
        assert len(offset_cts) == limit

    def test_filter_content_types_with_limit(self, nb_client):
        content_types = nb_client.extras.content_types.filter(app_label="dcim")
        limited_cts = nb_client.extras.content_types.filter(app_label="dcim", limit=10)
        assert len(content_types) == len(limited_cts)
