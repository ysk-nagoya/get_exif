import glob
import os
import re
import time
import unicodedata
from contextlib import contextmanager
from tkinter import filedialog

import matplotlib
from matplotlib import pyplot
from PIL import Image

from .constant import TAGS_JP

matplotlib.rcParams["axes.xmargin"] = 0
matplotlib.rcParams["axes.ymargin"] = 0

_NO_DATA = "no_data"


class _Base:
    def __init__(self):
        self.parent_path = ""
        self.path_list = []
        self.ignore_focus_len_list = []
        self.round_down_digit_num = 1
        self.show_count_zero = False

        self.count_dict = {}

    @contextmanager
    def _stop_watch(self):
        try:
            start_sec = time.time()
            yield
        finally:
            print(f"処理時間: {time.time() - start_sec}[sec]")

    def _remove_duplicate(self, list_):
        return list(set(list_))

    def _sort_dict(self, dict_: dict):
        no_data_values = dict_.pop(_NO_DATA, 0)
        sorted_dict = sorted(dict_.items())
        count_dict = dict((x, y) for x, y in sorted_dict)
        return ({_NO_DATA: no_data_values} if no_data_values else {}) | count_dict

    def _remove_value_from_list(self, list_, remove_value_list):
        return (
            [value for value in list_ if value not in remove_value_list]
            if remove_value_list
            else list_
        )

    @property
    def path_list_length(self):
        return len(self.path_list)


class _Input(_Base):
    def _input_values(self, description, example_text=""):
        print(f"{description}")
        if example_text:
            print(f"入力例）{example_text}")
        input_text = input(">")
        input_text = unicodedata.normalize("NFKC", input_text)
        input_text = input_text.lower()
        input_text = input_text.replace("、", ",")
        return re.sub(r"[ 　]+", "", input_text)

    def _input_ignore_focus_len_list(self):
        while 1:
            input_text = self._input_values(
                "除外したい焦点距離がある場合はカンマ区切りで入力",
                "24mmと70mmを除外したい場合：24,70",
            )
            try:
                return (
                    [int(text_focus_len) for text_focus_len in input_text.split(",")]
                    if input_text
                    else []
                )
            except (ValueError, TypeError):
                print("数字以外が入ってるかも。もう一度入力。")

    def _input_round_down_digit_num(self):
        while 1:
            input_text = self._input_values(
                "焦点距離を切り捨てる桁数（未入力の場合：1）",
                "2桁目まで切り捨てる場合：2",
            )
            try:
                return int(input_text) if input_text else 1
            except (ValueError, TypeError):
                print("数字以外が入力されたかも。もう一度入力。")

    def _input_show_count_zero(self):
        while 1:
            input_text = self._input_values(
                "結果に合計が0の焦点距離を表示するかどうか（未入力の場合：no）",
                "しない場合：0 もしくは n もしくは no、する場合：1 もしくは y もしくは yes",
            )
            if input_text in ["1", "y", "yes", "true"]:
                return True
            elif not input_text or input_text in ["0", "n", "no", "false"]:
                return False
            else:
                print("所定の文字以外が入力されたかも。もう一度入力。")


class _Get(_Input):
    def _get_exif_dict_jp_name_key(self, path):
        with Image.open(path) as image_:
            exif = image_.getexif()
        exif_dict = exif.get_ifd(0x8769)
        return {
            name: value
            for key, value in exif_dict.items()
            if (name := TAGS_JP.get(key))
        }

    def _get_focal_len_list_by_path_list(self):
        focal_len_list = []
        for index, path in enumerate(self.path_list):
            print("\r", f"{(index + 1):05}/{self.path_list_length:05}", end="")
            exif_dict = self._get_exif_dict_jp_name_key(path)
            focal_len_list.append(exif_dict.get("レンズ焦点距離"))
        print("\n")
        return focal_len_list

    def _get_count_dict_by_round_digit(self, focal_len_list):
        place_num = pow(10, self.round_down_digit_num)
        round_downed_list = [
            (
                int(focal_len / place_num) * place_num
                if focal_len is not None
                else _NO_DATA
            )
            for focal_len in focal_len_list
        ]
        result_dict = {}
        for num in round_downed_list:
            if not result_dict.get(num):
                result_dict[num] = 0
            result_dict[num] += 1
        return result_dict


class _GetExif(_Get):
    def _set_settings_by_input(self):
        print("写真の入っているフォルダを選択")
        self.parent_path = filedialog.askdirectory()
        print(f">{self.parent_path}")
        self.ignore_focus_len_list = self._input_ignore_focus_len_list()
        self.round_down_digit_num = self._input_round_down_digit_num()
        self.show_count_zero = self._input_show_count_zero()

    def _set_image_path_list_by_parent_path(self):
        search_path_pattern = os.path.join(self.parent_path, "**", "*.JPG")
        path_list = glob.glob(search_path_pattern, recursive=True)
        self.path_list = self._remove_duplicate(path_list)
        print(f"ファイル総数: {self.path_list_length}")

    def _count_focus_length(self):
        if self.path_list:
            focal_len_list = self._get_focal_len_list_by_path_list()
            focal_len_list = self._remove_value_from_list(
                focal_len_list, remove_value_list=self.ignore_focus_len_list
            )
            self.count_dict = self._get_count_dict_by_round_digit(focal_len_list)
        else:
            print("*.jpg画像が見つかりませんでした……")

    def _view_graph_image(self):
        if not self.count_dict:
            return
        values_dict = self._sort_dict(self.count_dict)
        if not self.show_count_zero:
            values_dict = {str(key): value for key, value in values_dict.items()}
        count_list = list(values_dict.values())
        bar_graph = pyplot.bar(list(values_dict.keys()), count_list, width=0.9)
        pyplot.bar_label(bar_graph, labels=count_list)
        pyplot.show()


class GetExif(_GetExif):
    def main(self):
        with self._stop_watch():
            print("中止したい場合は'Ctrl + C'を押すか、画面ごと閉じてね。")
            self._set_settings_by_input()
            self._set_image_path_list_by_parent_path()
            self._count_focus_length()
        self._view_graph_image()


if __name__ == "__main__":
    ge = GetExif()
    ge.main()
