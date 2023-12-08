"""Tests for analytics/datasets/percent_complete.py."""

from analytics.datasets.deliverable_tasks import DeliverableTasks
from analytics.metrics.percent_complete import DeliverablePercentComplete, Unit


def task_row(
    deliverable: int,
    task: int | None,
    points: int | None = 1,
    status: str | None = "open",
) -> dict:
    """Create a sample row of the DeliverableTasks dataset."""
    return {
        "deliverable_number": deliverable,
        "deliverable_title": f"Deliverable {deliverable}",
        "issue_number": task,
        "issue_title": f"Task {task}" if task else None,
        "points": points,
        "status": status,
    }


class TestDeliverablePercentComplete:
    """Test the DeliverablePercentComplete metric."""

    def test_percent_complete_based_on_task_count(self):
        """Check that percent completion is correct when tasks are the unit."""
        # setup - create test dataset
        test_rows = [
            task_row(deliverable=1, task=1, status="open"),
            task_row(deliverable=1, task=2, status="closed"),
            task_row(deliverable=2, task=3, status="open"),
        ]
        test_data = DeliverableTasks.from_dict(test_rows)
        # execution
        df = DeliverablePercentComplete(test_data, unit=Unit.issues).results
        df = df.set_index("deliverable_title")
        # validation - check number of rows returned
        assert len(df) == 2
        # validation - check totals
        assert df.loc["Deliverable 1", "total"] == 2
        assert df.loc["Deliverable 2", "total"] == 1
        # validation - check open
        assert df.loc["Deliverable 1", "open"] == 1
        assert df.loc["Deliverable 2", "open"] == 1
        # validation - check closed
        assert df.loc["Deliverable 1", "closed"] == 1
        assert df.loc["Deliverable 2", "closed"] == 0
        # validation - check percent complete
        assert df.loc["Deliverable 1", "percent_complete"] == 0.5
        assert df.loc["Deliverable 2", "percent_complete"] == 0.0

    def test_percent_complete_based_on_points(self):
        """Check that percent completion is correct when points are the unit."""
        # setup - create test dataset
        test_rows = [
            task_row(deliverable=1, task=1, points=1, status="open"),
            task_row(deliverable=1, task=2, points=3, status="closed"),
            task_row(deliverable=2, task=3, points=5, status="open"),
        ]
        test_data = DeliverableTasks.from_dict(test_rows)
        # execution
        df = DeliverablePercentComplete(test_data, unit=Unit.points).results
        df = df.set_index("deliverable_title")
        # validation - check number of rows returned
        assert len(df) == 2
        # validation - check totals
        assert df.loc["Deliverable 1", "total"] == 4
        assert df.loc["Deliverable 2", "total"] == 5
        # validation - check open
        assert df.loc["Deliverable 1", "open"] == 1
        assert df.loc["Deliverable 2", "open"] == 5
        # validation - check closed
        assert df.loc["Deliverable 1", "closed"] == 3
        assert df.loc["Deliverable 2", "closed"] == 0
        # validation - check percent complete
        assert df.loc["Deliverable 1", "percent_complete"] == 0.75
        assert df.loc["Deliverable 2", "percent_complete"] == 0.0

    def test_show_0_pct_for_deliverables_without_tasks(self):
        """Deliverables without tasks should show 0% complete instead of throwing an error."""
        # setup - create test dataset where deliverable 2 has no tasks
        test_rows = [
            task_row(deliverable=1, task=2, status="closed"),
            task_row(deliverable=2, task=None, status=None),
        ]
        test_data = DeliverableTasks.from_dict(test_rows)
        # execution - use tasks as the unit
        df = DeliverablePercentComplete(test_data, unit=Unit.issues).results
        df = df.set_index("deliverable_title")
        # validation - check number of rows returned
        assert len(df) == 2
        # validation - check totals
        assert df.loc["Deliverable 1", "total"] == 1
        assert df.loc["Deliverable 2", "total"] == 1
        # validation - check open
        assert df.loc["Deliverable 1", "open"] == 0
        assert df.loc["Deliverable 2", "open"] == 1
        # validation - check closed
        assert df.loc["Deliverable 1", "closed"] == 1
        assert df.loc["Deliverable 2", "closed"] == 0
        # validation - check percent complete
        assert df.loc["Deliverable 1", "percent_complete"] == 1.0
        assert df.loc["Deliverable 2", "percent_complete"] == 0.0

    def test_show_0_pct_for_deliverables_without_points(self):
        """Deliverables without points should show 0% complete instead of throwing an error."""
        # setup - create test dataset where deliverable 2 has no points
        test_rows = [
            task_row(deliverable=1, task=2, points=2, status="closed"),
            task_row(deliverable=2, task=None, points=None, status=None),
        ]
        test_data = DeliverableTasks.from_dict(test_rows)
        # execution - use points as the unit
        df = DeliverablePercentComplete(test_data, unit=Unit.points).results
        df = df.set_index("deliverable_title")
        # validation - check number of rows returned
        assert len(df) == 2
        # validation - check totals
        assert df.loc["Deliverable 1", "total"] == 2
        assert df.loc["Deliverable 2", "total"] == 0
        # validation - check open
        assert df.loc["Deliverable 1", "open"] == 0
        assert df.loc["Deliverable 2", "open"] == 0
        # validation - check closed
        assert df.loc["Deliverable 1", "closed"] == 2
        assert df.loc["Deliverable 2", "closed"] == 0
        # validation - check percent complete
        assert df.loc["Deliverable 1", "percent_complete"] == 1.0
        assert df.loc["Deliverable 2", "percent_complete"] == 0.0


class TestGetStats:
    """Test the DeliverablePercentComplete.get_stats() method."""

    def test_all_issues_are_pointed(self):
        """Test that stats show 100% of issues are pointed if all have points."""
        # setup - create test dataset
        test_rows = [
            task_row(deliverable=1, task=1, points=2, status="open"),
            task_row(deliverable=1, task=2, points=1, status="closed"),
            task_row(deliverable=2, task=3, points=3, status="open"),
            task_row(deliverable=2, task=3, points=1, status="open"),
        ]
        test_data = DeliverableTasks.from_dict(test_rows)
        # execution
        output = DeliverablePercentComplete(test_data, unit=Unit.issues)
        # validation
        assert len(output.stats) == 2
        for deliverable in ["Deliverable 1", "Deliverable 2"]:
            stat = output.stats.get(deliverable)
            assert stat.value == 100
            assert stat.suffix == f"% of {Unit.issues.value} pointed"

    def test_some_issues_are_not_pointed(self):
        """Test that stats are calculated correctly if not all issues are pointed."""
        # setup - create test dataset
        test_rows = [
            task_row(deliverable=1, task=1, points=2, status="open"),
            task_row(deliverable=1, task=2, points=0, status="closed"),
            task_row(deliverable=2, task=3, points=3, status="open"),
            task_row(deliverable=2, task=3, points=None, status="open"),
        ]
        test_data = DeliverableTasks.from_dict(test_rows)
        # execution
        output = DeliverablePercentComplete(test_data, unit=Unit.issues)
        # validation
        assert len(output.stats) == 2
        for deliverable in ["Deliverable 1", "Deliverable 2"]:
            stat = output.stats.get(deliverable)
            assert stat.value == 50
            assert stat.suffix == f"% of {Unit.issues.value} pointed"

    def test_deliverables_without_tasks_have_0_pct_pointed(self):
        """Deliverables without tasks should have 0% pointed in stats."""
        # setup - create test dataset
        test_rows = [
            task_row(deliverable=1, task=1, points=2, status="open"),
            task_row(deliverable=1, task=2, points=1, status="closed"),
            task_row(deliverable=2, task=None, points=None, status=None),
        ]
        test_data = DeliverableTasks.from_dict(test_rows)
        # execution
        output = DeliverablePercentComplete(test_data, unit=Unit.issues)
        # validation
        assert len(output.stats) == 2
        assert output.stats.get("Deliverable 1").value == 100
        assert output.stats.get("Deliverable 2").value == 0


class TestFormatSlackMessage:
    """Test the DeliverablePercentComplete.format_slack_message()."""

    def test_slack_message_contains_right_number_of_lines(self):
        """Message should contain one line for the title and one for each deliverable."""
        # setup - create test dataset
        test_rows = [
            task_row(deliverable=1, task=1, points=2, status="open"),
            task_row(deliverable=2, task=2, points=1, status="closed"),
            task_row(deliverable=3, task=3, points=3, status="open"),
        ]
        test_data = DeliverableTasks.from_dict(test_rows)
        # execution
        output = DeliverablePercentComplete(test_data, unit=Unit.issues)
        lines = output.format_slack_message().splitlines()
        # validation
        assert len(lines) == 4

    def test_title_includes_issues_when_unit_is_issue(self):
        """Test that the title is formatted correctly when unit is issues."""
        # setup - create test dataset
        test_rows = [
            task_row(deliverable=1, task=1, points=2, status="open"),
            task_row(deliverable=2, task=2, points=1, status=None),
        ]
        test_data = DeliverableTasks.from_dict(test_rows)
        # execution
        output = DeliverablePercentComplete(test_data, unit=Unit.issues)
        title = output.format_slack_message().splitlines()[0]
        # validation
        assert Unit.issues.value in title

    def test_title_includes_points_when_unit_is_points(self):
        """Test that the title is formatted correctly when unit is points."""
        # setup - create test dataset
        test_rows = [
            task_row(deliverable=1, task=1, points=2, status="open"),
            task_row(deliverable=2, task=2, points=1, status=None),
        ]
        test_data = DeliverableTasks.from_dict(test_rows)
        # execution
        output = DeliverablePercentComplete(test_data, unit=Unit.points)
        title = output.format_slack_message().splitlines()[0]
        # validation
        assert Unit.points.value in title