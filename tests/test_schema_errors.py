from drf_spectacular.generators import SchemaGenerator


def test_schema_no_errors() -> None:
    generator = SchemaGenerator()
    try:
        _, errors = generator.get_schema_with_errors()
    except AttributeError:
        generator.get_schema(request=None)
        errors = []
    assert not errors, f"drf-spectacular errors:\n{errors}"
