import unittest

from cangku_api import CangkuApi


class MyTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.test_item = CangkuApi()
        self.SEARCH_TERM = '猫'
        self.BAD_SEARCH_TERM = 'qwerrewqrewqrhqiwurhqlweruq'
        self.NO_ERROR = 'No Error'

    def test_get_search_string(self):
        result = self.test_item.get_search_string(self.SEARCH_TERM)
        self.assertTrue(result)

    def test_get_nothing(self):
        result = self.test_item.get_search_string(self.BAD_SEARCH_TERM)
        self.assertFalse(result)

    def test_get_error(self):
        _ = self.test_item.get_search_string(self.BAD_SEARCH_TERM)
        test_info_by_index = self.test_item.get_info_by_index('11')
        self.assertNotEqual(test_info_by_index.get_error(), self.NO_ERROR)

    def test_get_by_index(self):
        _ = self.test_item.get_search_string(self.SEARCH_TERM)
        test_info_by_index = self.test_item.get_info_by_index('4')
        self.assertTrue(test_info_by_index.get_data())
        self.assertEqual(test_info_by_index.get_error(), self.NO_ERROR)
        self.assertTrue(isinstance(test_info_by_index.get_data(), dict))

    def test_get_by_index_too_large(self):
        _ = self.test_item.get_search_string(self.SEARCH_TERM)
        test_info_by_index = self.test_item.get_info_by_index('999')
        self.assertFalse(test_info_by_index.get_data())
        self.assertNotEqual(test_info_by_index.get_error(), self.NO_ERROR)
        self.assertEqual(test_info_by_index.get_error(), '索引位置大于搜索结果最大数')

    def test_get_by_bad_index(self):
        _ = self.test_item.get_search_string(self.SEARCH_TERM)
        test_info_by_index = self.test_item.get_info_by_index('abce')
        self.assertFalse(test_info_by_index.get_data())
        self.assertNotEqual(test_info_by_index.get_error(), self.NO_ERROR)
        self.assertEqual(test_info_by_index.get_error(), '输入非数字')

    def test_get_information(self):
        _ = self.test_item.get_search_string(self.SEARCH_TERM)
        test_info_by_index = self.test_item.get_info_by_index('4')
        test_dissect_to_string = self.test_item.anaylze_dissected_data(test_info_by_index)
        self.assertTrue(test_dissect_to_string)
        self.assertTrue(isinstance(test_dissect_to_string, str))


if __name__ == '__main__':
    unittest.main()
