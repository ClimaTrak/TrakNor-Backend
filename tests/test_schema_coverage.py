from rest_framework.test import APIRequestFactory
from django.urls import get_resolver
from drf_spectacular.generators import SchemaGenerator

COVERAGE_THRESHOLD = 0.90


def test_openapi_coverage() -> None:
    generator = SchemaGenerator()
    schema = generator.get_schema(request=APIRequestFactory().get("/"))
    documented_paths = set(schema["paths"].keys())
    all_api_paths = {
        route.pattern.regex.pattern.rstrip("$")
        for route in get_resolver().url_patterns
        if "/api/" in str(route.pattern)
    }
    coverage = len(documented_paths) / len(all_api_paths)
    assert coverage >= COVERAGE_THRESHOLD, (
        f"OpenAPI coverage {coverage:.0%} is below {COVERAGE_THRESHOLD:.0%}"
    )
