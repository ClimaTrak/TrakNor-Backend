from datetime import date, timedelta
from uuid import uuid4

from traknor.domain.metrics.kpi_calculator import _calc_mtbf, _calc_mttr
from traknor.domain.work_order import WorkOrder
from traknor.domain.constants import WorkOrderStatus


def _wo(closed: date, opened: date | None = None) -> WorkOrder:
    return WorkOrder(
        id=1,
        code=uuid4(),
        equipment_id=1,
        status=WorkOrderStatus.DONE.value,
        priority="Alta",
        scheduled_date=opened,
        completed_date=closed,
        created_by_id=1,
        description="",
        cost=0.0,
        revision=0,
        deleted_at=None,
    )


def test_calc_mttr():
    base = date(2025, 6, 1)
    wos = [
        _wo(base + timedelta(days=1), base),
        _wo(base + timedelta(days=3), base + timedelta(days=2)),
    ]
    assert _calc_mttr(wos) == 24.0


def test_calc_mtbf():
    base = date(2025, 6, 1)
    wos = [
        _wo(base + timedelta(days=2)),
        _wo(base + timedelta(days=5)),
    ]
    assert _calc_mtbf(wos, base) == 60.0
