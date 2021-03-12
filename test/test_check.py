import unittest
import datetime

import check
from input import input_data, input_business_day_file


class TestCheck__get_days_with_no_data(unittest.TestCase):
    def test_case1(self):
        """
        引数のbegin_date, end_date間で、
        データがない日が正常に抽出されること
        """

        # パラメータの準備
        check_data = input_data('test/file/case1/price/', exclude=False)
        business_day = input_business_day_file('test/file/case1/business_day.csv')
        begin_date = datetime.datetime(2021, 3, 2)
        end_date = datetime.datetime(2021, 3, 4)

        # 期待値
        expected = {
            '1000': [datetime.datetime(2021, 3, 2)],
            '2000': [datetime.datetime(2021, 3, 3), datetime.datetime(2021, 3, 4)]
        }

        # 実行
        result = check.get_days_with_no_data(check_data, business_day, begin_date, end_date)

        # 検証
        self.assertEqual(expected, result)


if __name__ == '__main__':
    unittest.main()
