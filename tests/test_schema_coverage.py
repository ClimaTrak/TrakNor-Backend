from django.urls import get_resolver
import pytest
from drf_spectacular.generators import SchemaGenerator

COVERAGE_THRESHOLD = 0.85


def test_openapi_coverage() -> None:
    generator = SchemaGenerator()
    schema = generator.get_schema(request=None)
    documented_paths = set(schema.get("paths", {}).keys())
    all_api_paths = {
        getattr(route.pattern, "regex", route.pattern).pattern.rstrip("$")
        for route in get_resolver().url_patterns
        if "/api/" in str(route.pattern)
    }
    if not all_api_paths:
        pytest.skip("No API paths found")
    coverage = len(documented_paths) / len(all_api_paths)
    assert coverage >= COVERAGE_THRESHOLD, (
        f"OpenAPI coverage {coverage:.0%} is below {COVERAGE_THRESHOLD:.0%}"
    )
