import pytest

from gateway.activity_gateway import ActivityGateway, RecordNotFoundError
from use_cases.activity_manager import ActivityManager


class TestSearchUserActivities:

    def test_correct_user_activities_are_found_when_user_has_multiple_activities(
            self, test_sleeping_activity, test_working_activity, test_db):

        test_db.data = [test_sleeping_activity, test_working_activity]
        activities = ActivityGateway.activities()

        assert len(activities) == 2


    def test_no_user_activities_are_found_when_user_has_no_activities(self):
        activities = ActivityGateway.activities()
        assert len(activities) == 0


def test_new_activity_added_to_db(test_db, test_activity):
    assert len(ActivityGateway.activities()) == 1


class TestSearchUserActivitiesStartedToday:

    def test_no_activities_returned_when_nothing_started_today(self, test_db):
        assert len(ActivityGateway.activities_today()) == 0

    def test_one_activity_returned_when_only_one_started_today(self, test_db, test_activity):
        todays_activities = ActivityGateway.activities_today()
        assert len(todays_activities) == 1
        assert test_activity._id == todays_activities[0]._id

    def test_user_has_activities_on_different_days_but_only_1_today(self, test_user_with_multiple_activities_on_multiple_days, test_activity, test_db):
        todays_activities = ActivityGateway.activities_today()
        assert len(todays_activities) == 1
        assert test_activity._id == todays_activities[0]._id

    def test_user_has_more_than_one_activity_today_and_more_on_other_days(self, test_user_with_multiple_activities_on_multiple_days, test_db, test_activity):
        test_working_activity = ActivityManager.start_new_activity('working')
        ActivityGateway.add_new_activity_to_db(test_working_activity)

        todays_activities = ActivityGateway.activities_today()
        assert len(todays_activities) == 2
        _ids = [a._id for a in todays_activities]
        assert test_activity._id in _ids
        assert test_working_activity._id in _ids


class TestSearchForUserActivitiesWithSpecificCategoryStartedToday:

    def test_no_activities_returned_when_nothing_started_today(self, test_db):
        assert len(ActivityGateway.activities_today_in_this_category('working')) == 0

    def test_one_activity_returned_when_only_one_started_today(self, test_db, test_activity):
        todays_activities = ActivityGateway.activities_today_in_this_category(test_activity.category)
        assert len(todays_activities) == 1
        assert test_activity._id == todays_activities[0]._id

    def test_user_has_activities_on_different_days_but_only_1_today(self, test_user_with_multiple_activities_on_multiple_days, test_activity, test_db):
        todays_activities = ActivityGateway.activities_today_in_this_category(test_activity.category)
        assert len(todays_activities) == 1
        assert test_activity._id == todays_activities[0]._id

    def test_user_has_more_than_one_activity_today_but_only_one_is_what_we_want_and_more_activities_on_other_days(self, test_user_with_multiple_activities_on_multiple_days, test_db, test_activity):
        test_working_activity = ActivityManager.start_new_activity('working')
        ActivityGateway.add_new_activity_to_db(test_working_activity)

        todays_activities = ActivityGateway.activities_today_in_this_category('working')
        assert len(todays_activities) == 1
        assert test_working_activity._id == todays_activities[0]._id


class TestSearchForActivity:

    def test_correct_activity_is_found(self, test_activity, test_db):
        activity = ActivityGateway.fetch_activity(test_activity)
        assert activity._id == test_activity._id

    def test_exception_thrown_when_no_activity_found_in_db_with_that_id(self, test_db):
        a = ActivityManager.start_new_activity('test_activity')
        with pytest.raises(RecordNotFoundError):
            ActivityGateway.fetch_activity(a)
