class TestPagination:
    """Verify we can limit and offset results on an endpoint."""

    def test_all_content_types_with_offset(self, nb_client):
        offset = 10
        content_types = nb_client.extras.content_types.all()
        offset_cts = nb_client.extras.content_types.all(limit=10, offset=offset)
        assert (len(content_types) - len(offset_cts)) == offset

    def test_all_content_types_with_limit(self, nb_client):
        content_types = nb_client.extras.content_types.all()
        limited_cts = nb_client.extras.content_types.all(limit=10)
        assert len(content_types) == len(limited_cts)

    def test_filter_content_types_with_offset(self, nb_client):
        offset = 10
        content_types = nb_client.extras.content_types.filter(app_label="dcim")
        offset_cts = nb_client.extras.content_types.filter(app_label="dcim", limit=10, offset=offset)
        assert (len(content_types) - len(offset_cts)) == offset

    def test_filter_content_types_with_limit(self, nb_client):
        content_types = nb_client.extras.content_types.filter(app_label="dcim")
        limited_cts = nb_client.extras.content_types.filter(app_label="dcim", limit=10)
        assert len(content_types) == len(limited_cts)
