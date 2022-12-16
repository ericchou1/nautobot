from django.test import TestCase

from nautobot.core.utilities import check_filter_for_display

from nautobot.dcim.filters import DeviceFilterSet
from nautobot.dcim.models import DeviceType, DeviceRedundancyGroup


class CheckFilterForDisplayTest(TestCase):
    """
    Validate the operation of check_filter_for_display().
    """

    def test_check_filter_for_display(self):

        device_filter_set_filters = DeviceFilterSet().get_filters()

        with self.subTest("Test invalid filter case (field_name not found)"):
            expected_output = ["fake_field_name", ["example_field_value"]]

            self.assertEqual(
                check_filter_for_display(device_filter_set_filters, "fake_field_name", ["example_field_value"]),
                expected_output,
            )

        with self.subTest("Test values are converted to list"):
            expected_output = ["fake_field_name", ["example_field_value"]]

            self.assertEqual(
                check_filter_for_display(device_filter_set_filters, "fake_field_name", "example_field_value"),
                expected_output,
            )

        with self.subTest("Test get field label, none exists (fallback)"):
            expected_output = ["id", ["example_field_value"]]

            self.assertEqual(
                check_filter_for_display(device_filter_set_filters, "id", ["example_field_value"]), expected_output
            )

        with self.subTest("Test get field label, exists"):
            expected_output = ["Has interfaces", ["example_field_value"]]

            self.assertEqual(
                check_filter_for_display(device_filter_set_filters, "has_interfaces", ["example_field_value"]),
                expected_output,
            )

        with self.subTest(
            "Test get value display, falls back to string representation (also NaturalKeyOrPKMultipleChoiceFilter)"
        ):
            example_obj = DeviceRedundancyGroup.objects.first()
            expected_output = ["Device Redundancy Groups (slug or ID)", [str(example_obj)]]

            self.assertEqual(
                check_filter_for_display(device_filter_set_filters, "device_redundancy_group", [str(example_obj.pk)]),
                expected_output,
            )

        with self.subTest("Test get value display (also legacy filter ModelMultipleChoiceFilter)"):
            example_obj = DeviceType.objects.first()
            expected_output = ["Device type (ID)", [example_obj.display]]

            self.assertEqual(
                check_filter_for_display(device_filter_set_filters, "device_type_id", [str(example_obj.pk)]),
                expected_output,
            )

        with self.subTest("Test skip non-UUID value display (legacy, ex: ModelMultipleChoiceFilter)"):
            expected_output = ["Manufacturer (slug)", ["fake_slug"]]

            self.assertEqual(
                check_filter_for_display(device_filter_set_filters, "manufacturer", ["fake_slug"]), expected_output
            )
