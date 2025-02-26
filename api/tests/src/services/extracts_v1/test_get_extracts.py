from datetime import date, datetime, timezone

import pytest

from src.constants.lookup_constants import ExtractType
from src.db.models.extract_models import ExtractMetadata
from src.pagination.pagination_models import PaginationParams, SortDirection
from src.search.search_models import DateSearchFilter
from src.services.extracts_v1.get_extracts import ExtractFilters, ExtractListParams, get_extracts
from tests.src.db.models.factories import ExtractMetadataFactory


@pytest.fixture(autouse=True)
def clear_extracts(db_session):
    db_session.query(ExtractMetadata).delete()
    db_session.commit()
    yield


def test_get_extracts_no_filters(
    enable_factory_create,
    db_session,
):
    ExtractMetadataFactory.create_batch(3)

    params = ExtractListParams(
        pagination=PaginationParams(
            page_size=10,
            page_offset=1,
            order_by="created_at",
            sort_direction=SortDirection.ASCENDING,
        )
    )

    extracts, pagination_info = get_extracts(db_session, params)
    assert len(extracts) == 3
    assert pagination_info.total_records == 3


def test_get_extracts_with_type_filter(
    enable_factory_create,
    db_session,
):
    ExtractMetadataFactory.create_batch(3, extract_type=ExtractType.OPPORTUNITIES_CSV)
    ExtractMetadataFactory.create_batch(3, extract_type=ExtractType.OPPORTUNITIES_JSON)

    params = ExtractListParams(
        pagination=PaginationParams(
            page_size=10,
            page_offset=1,
            order_by="created_at",
            sort_direction=SortDirection.ASCENDING,
        ),
        filters=ExtractFilters(extract_type="opportunities_json"),
    )

    extracts, _ = get_extracts(db_session, params)
    assert len(extracts) == 3
    assert all(r.extract_type == "opportunities_json" for r in extracts)


def test_get_extracts_with_date_filter(enable_factory_create, db_session):
    ExtractMetadataFactory.create_batch(3, created_at=datetime(2024, 1, 15))
    ExtractMetadataFactory.create_batch(3, created_at=datetime(2024, 1, 25))

    params = ExtractListParams(
        pagination=PaginationParams(
            page_size=10,
            page_offset=1,
            order_by="created_at",
            sort_direction=SortDirection.ASCENDING,
        ),
        filters=ExtractFilters(
            created_at=DateSearchFilter(
                start_date=date(2024, 1, 10),
                end_date=date(2024, 1, 20),
                sort_direction=SortDirection.ASCENDING,
            )
        ),
    )

    extracts, _ = get_extracts(db_session, params)
    assert len(extracts) == 3
    assert extracts[0].created_at == datetime(2024, 1, 15, tzinfo=timezone.utc)


def test_get_extracts_pagination(enable_factory_create, db_session):
    ExtractMetadataFactory.create_batch(3)

    params = ExtractListParams(
        pagination=PaginationParams(
            page_size=2,
            page_offset=1,
            order_by="created_at",
            sort_direction=SortDirection.ASCENDING,
        )
    )

    extracts, pagination_info = get_extracts(db_session, params)
    assert len(extracts) == 2
    assert pagination_info.total_records == 3
    assert pagination_info.total_pages == 2

    # Test second page
    params.pagination.page_offset = 2
    extracts, pagination_info = get_extracts(db_session, params)
    assert len(extracts) == 1
