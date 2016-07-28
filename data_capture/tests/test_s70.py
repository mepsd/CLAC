from unittest.mock import Mock, MagicMock, patch
from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.exceptions import ValidationError

from .common import path
from ..schedules import s70


S70_XLSX_PATH = path('static', 'data_capture', 's70_example.xlsx')

XLSX_CONTENT_TYPE = ('application/vnd.openxmlformats-'
                     'officedocument.spreadsheetml.sheet')


def uploaded_xlsx_file(content=None):
    if content is None:
        with open(S70_XLSX_PATH, 'rb') as f:
            content = f.read()

    return SimpleUploadedFile(
        'foo.xlsx',
        content,
        content_type=XLSX_CONTENT_TYPE
    )


class SafeCellStrValueTests(TestCase):
    def test_cell_value_index_errors_are_ignored(self):
        s = MagicMock()
        s.cell_value.side_effect = IndexError()

        self.assertEqual(s70.safe_cell_str_value(s, 99, 99), '')
        self.assertEqual(s.cell_value.call_count, 1)

    def test_coercer_value_errors_are_ignored(self):
        s = MagicMock()
        s.cell_value.return_value = 'blah'

        c = Mock()
        c.side_effect = ValueError()

        self.assertEqual(s70.safe_cell_str_value(s, 99, 99, c), 'blah')
        self.assertEqual(s.cell_value.call_count, 1)
        self.assertEqual(c.call_count, 1)

    def test_result_is_stringified(self):
        s = MagicMock()
        s.cell_value.return_value = 5

        self.assertEqual(s70.safe_cell_str_value(s, 1, 1), '5')

    def test_coercer_is_used(self):
        s = MagicMock()
        s.cell_value.return_value = 5.0

        self.assertEqual(s70.safe_cell_str_value(s, 1, 1, int), '5')


class GleanLaborCategoriesTests(TestCase):
    def test_rows_are_returned(self):
        rows = s70.glean_labor_categories_from_file(uploaded_xlsx_file())
        self.assertEqual(rows, [{
            'sin': '132-51',
            'labor_category': 'Project Manager',
            'education_level': 'Bachelors',
            'min_years_experience': '5',
            'commercial_list_price': '125.0',
            'unit_of_issue': 'Hour',
            'most_favored_customer': 'All Commercial Customers',
            'best_discount': '0.07',
            'mfc_price': '123.99',
            'gsa_discount': '0.1',
            'price_excluding_iff': '110.99',
            'price_including_iff': '115.99',
            'volume_discount': '0.15',
        }])

    def test_validation_error_raised_when_sheet_not_present(self):
        with self.assertRaisesRegexp(
            ValidationError,
            r'There is no sheet in the workbook called "foo"'
        ):
            s70.glean_labor_categories_from_file(
                uploaded_xlsx_file(),
                sheet_name='foo'
            )


class S70Tests(TestCase):
    @patch.object(s70, 'glean_labor_categories_from_file')
    def test_load_from_upload_reraises_validation_errors(self, m):
        m.side_effect = ValidationError('foo')

        with self.assertRaisesRegexp(ValidationError, r'foo'):
            s70.Schedule70PriceList.load_from_upload(uploaded_xlsx_file())

    def test_load_from_upload_raises_validation_error_on_corrupt_files(self):
        f = uploaded_xlsx_file(b'foo')

        with self.assertRaisesRegexp(
            ValidationError,
            r'An error occurred when reading your Excel data.'
        ):
            s70.Schedule70PriceList.load_from_upload(f)
