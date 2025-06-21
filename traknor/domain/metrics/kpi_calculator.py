from __future__ import annotations

from dataclasses import dataclass
from datetime import date, timedelta
from typing import Iterable, List, Optional

from traknor.domain.work_order import WorkOrder


@dataclass
class KPISeries:
    """Time series data for KPIs."""

    labels: List[str]
    mtbf: List[float]
    mttr: List[float]
    closed: List[int]


@dataclass
class KPIResult:
    """KPI data for a given range."""

    range_from: date
    range_to: date
    mtbf: float
    mttr: float
    open_workorders: int
    closed_workorders: int
    series: Optional[KPISeries] = None


def _calc_mtbf(workorders: Iterable[WorkOrder], start: date) -> float:
    """Mean time between failures in hours."""

    closed: List[WorkOrder] = [w for w in workorders if w.completed_date]
    if not closed:
        return 0.0
    closed.sort(key=lambda w: w.completed_date or start)
    prev = start
    spans: List[float] = []
    for wo in closed:
        assert wo.completed_date is not None
        spans.append((wo.completed_date - prev).total_seconds() / 3600)
        prev = wo.completed_date
    return sum(spans) / len(spans)


def _calc_mttr(workorders: Iterable[WorkOrder]) -> float:
    durations = []
    for w in workorders:
        if w.completed_date and w.scheduled_date:
            durations.append(
                (w.completed_date - w.scheduled_date).total_seconds() / 3600
            )
    return sum(durations) / len(durations) if durations else 0.0


def _series_labels(start: date, end: date, group_by: str) -> List[date]:
    labels: List[date] = []
    cur = start
    if group_by == "day":
        step = timedelta(days=1)
        while cur <= end:
            labels.append(cur)
            cur += step
    elif group_by == "week":
        # align to week start (Monday)
        cur -= timedelta(days=cur.weekday())
        step = timedelta(days=7)
        while cur <= end:
            labels.append(cur)
            cur += step
    else:  # month
        cur = cur.replace(day=1)
        while cur <= end:
            labels.append(cur)
            if cur.month == 12:
                cur = cur.replace(year=cur.year + 1, month=1)
            else:
                cur = cur.replace(month=cur.month + 1)
    return labels


def compute(
    workorders: Iterable[WorkOrder],
    start: date,
    end: date,
    *,
    group_by: str | None = None,
    open_count: int = 0,
    closed_count: int = 0,
) -> KPIResult:
    """Compute KPI values for the given work orders."""

    mtbf = _calc_mtbf(workorders, start)
    mttr = _calc_mttr(workorders)
    series_obj: KPISeries | None = None
    if group_by:
        labels_dates = _series_labels(start, end, group_by)
        labels: List[str] = []
        mtbf_list: List[float] = []
        mttr_list: List[float] = []
        closed_list: List[int] = []
        for idx, label_date in enumerate(labels_dates):
            if group_by == "day":
                next_date = label_date + timedelta(days=1)
                label = label_date.isoformat()
            elif group_by == "week":
                next_date = label_date + timedelta(days=7)
                iso_year, iso_week, _ = label_date.isocalendar()
                label = f"{iso_year}-W{iso_week:02d}"
            else:
                if label_date.month == 12:
                    next_date = label_date.replace(year=label_date.year + 1, month=1)
                else:
                    next_date = label_date.replace(month=label_date.month + 1)
                label = label_date.strftime("%Y-%m")

            subset = [
                w
                for w in workorders
                if w.completed_date and label_date <= w.completed_date < next_date
            ]
            labels.append(label)
            mtbf_list.append(_calc_mtbf(subset, label_date))
            mttr_list.append(_calc_mttr(subset))
            closed_list.append(len(subset))
        series_obj = KPISeries(
            labels=labels, mtbf=mtbf_list, mttr=mttr_list, closed=closed_list
        )

    return KPIResult(
        range_from=start,
        range_to=end,
        mtbf=mtbf,
        mttr=mttr,
        open_workorders=open_count,
        closed_workorders=closed_count,
        series=series_obj,
    )
