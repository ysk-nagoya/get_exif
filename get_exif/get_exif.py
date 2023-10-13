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

matplotlib.rcParams["axes.xmargin"] = 0
matplotlib.rcParams["axes.ymargin"] = 0

TAGS_JP = {
    33434: "露出時間",  # ExposureTime
    33437: "F ナンバー",  # FNumber
    34850: "露出プログラム",  # ExposureProgram
    34852: "スペクトル感度",  # SpectralSensitivity
    34855: "撮影感度",  # PhotographicSensitivity
    34856: "光電変換関数",  # OECF
    34864: "感度種別",  # SensitivityType
    34865: "標準出力感度",  # StandardOutputSensitivity
    34866: "推奨露光指数",  # RecommendedExposureIndex
    34867: "ISO スピード",  # ISOSpeed
    34868: "ISO スピードラチチュード yyy",  # ISOSpeedLatitudeyyy
    34869: "ISO スピードラチチュード zzz",  # ISOSpeedLatitudezzz
    37377: "シャッタースピード",  # ShutterSpeedValue APEX値
    37378: "絞り値",  # ApertureValue APEX値
    37379: "輝度値",  # BrightnessValue APEX値
    37380: "露光補正値",  # ExposureBiasValue APEX値
    37381: "レンズ最小Ｆ値",  # MaxApertureValue APEX値
    37382: "被写体距離",  # SubjectDistance
    37383: "測光方式",  # MeteringMode
    37384: "光源",  # LightSource
    37385: "フラッシュ",  # Flash
    37386: "レンズ焦点距離",  # FocalLength
    37396: "被写体領域",  # SubjectArea
    41483: "フラッシュ強度",  # FlashEnergy
    41484: "空間周波数応答",  # SpatialFrequencyResponse
    41486: "焦点面の幅の解像度",  # FocalPlaneXResolution
    41487: "焦点面の高さの解像度",  # FocalPlaneYResolution
    41488: "焦点面解像度単位",  # FocalPlaneResolutionUnit
    41492: "被写体位置",  # SubjectLocation
    41493: "露出インデックス",  # ExposureIndex
    41495: "センサ方式",  # SensingMethod
    41728: "ファイルソース",  # FileSource
    41729: "シーンタイプ",  # SceneType
    41730: "CFA パターン",  # CFAPattern
    41985: "個別画像処理",  # CustomRendered
    41986: "露出モード",  # ExposureMode
    41987: "ホワイトバランス",  # WhiteBalance
    41988: "デジタルズーム倍率",  # DigitalZoomRatio
    41989: "35mm 換算レンズ焦点距離",  # FocalLengthIn35mmFilm
    41990: "撮影シーンタイプ",  # SceneCaptureType
    41991: "ゲイン制御",  # GainControl
    41992: "撮影コントラスト",  # Contrast
    41993: "撮影彩度",  # Saturation
    41994: "撮影シャープネス",  # Sharpness
    41995: "撮影条件記述情報",  # DeviceSettingDescription
    41996: "被写体距離レンジ",  # SubjectDistanceRange
}


@contextmanager
def _stop_watch():
    try:
        print("start")
        start_sec = time.time()
        yield
    finally:
        print(f"処理時間: {time.time() - start_sec}[sec]")


def _remove_duplicate(list_):
    return list(set(list_))


def _sort_dict(dict_: dict):
    no_data_values = dict_.pop("no_data", 0)
    sorted_dict = sorted(dict_.items())
    count_dict = dict((x, y) for x, y in sorted_dict)
    return ({"no_data": no_data_values} if no_data_values else {}) | count_dict


def _get_image_path_list(parent_path):
    search_path_pattern = os.path.join(parent_path, "**", "*.JPG")
    path_list = glob.glob(search_path_pattern, recursive=True)
    return _remove_duplicate(path_list)


def _get_exif_dict_jp_name_key(path):
    with Image.open(path) as image_:
        exif = image_.getexif()
    exif_dict = exif.get_ifd(0x8769)
    return {
        name: value for key, value in exif_dict.items() if (name := TAGS_JP.get(key))
    }


def _get_focal_len_list(path_list):
    focal_len_list = []
    for index, path in enumerate(path_list):
        print("\r", f"{(index + 1):05}/{len(path_list):05}", end="")
        exif_dict = _get_exif_dict_jp_name_key(path)
        focal_len_list.append(exif_dict.get("レンズ焦点距離"))
    print("\n")
    return focal_len_list


def _remove_value_from_list(list_, remove_value_list):
    return (
        [value for value in list_ if value not in remove_value_list]
        if remove_value_list
        else list_
    )


def _get_count_dict_by_tens_digit(focal_len_list, digit):
    place_num = pow(10, digit)
    round_downed_list = [
        (int(focal_len / place_num) * place_num if focal_len is not None else "no_data")
        for focal_len in focal_len_list
    ]
    result_dict = {}
    for num in round_downed_list:
        if not result_dict.get(num):
            result_dict[num] = 0
        result_dict[num] += 1
    return result_dict


def _view_graph_image(values_dict, show_count_zero=False):
    values_dict = _sort_dict(values_dict)
    if not show_count_zero:
        values_dict = {str(key): value for key, value in values_dict.items()}
    label_list = list(values_dict.keys())
    count_list = list(values_dict.values())
    bar_graph = pyplot.bar(label_list, count_list, width=0.9)
    pyplot.bar_label(bar_graph, labels=count_list)
    pyplot.show()


def _input_values(description, example_text=""):
    print(f"{description}")
    if example_text:
        print(f"入力例）{example_text}")
    input_text = input(">")
    input_text = unicodedata.normalize("NFKC", input_text)
    input_text = input_text.lower()
    input_text = input_text.replace("、", ",")
    return re.sub(r"[ 　]+", "", input_text)


def _input_ignore_focus_len_list():
    while 1:
        input_text = _input_values(
            "除外したい焦点距離がある場合はカンマ区切りで入力",
            "24mmと70mmを除外したい場合：24,70",
        )
        if not input_text:
            return []
        try:
            return [int(text_focus_len) for text_focus_len in input_text.split(",")]
        except (ValueError, TypeError):
            print("数字以外が入ってるかも。もう一度入力。")


def _input_round_down_digit_num():
    while 1:
        input_text = _input_values(
            "焦点距離を切り捨てる桁数（未入力の場合：1）",
            "2桁目まで切り捨てる場合：2",
        )
        if not input_text:
            return 1
        try:
            return int(input_text)
        except (ValueError, TypeError):
            print("数字以外が入力されたかも。もう一度入力。")


def _input_show_count_zero():
    while 1:
        input_text = _input_values(
            "結果に合計が0の焦点距離を表示するかどうか（未入力の場合：no）",
            "しない場合：0 もしくは n もしくは no、する場合：1 もしくは y もしくは yes",
        )
        if input_text in ["1", "y", "yes", "true"]:
            return True
        elif not input_text or input_text in ["0", "n", "no", "false"]:
            return False
        else:
            print("所定の文字以外が入力されたかも。もう一度入力。")


def _input_setting_values():
    print("写真の入っているフォルダを選択")
    parent_path = filedialog.askdirectory()
    print(f">{parent_path}")
    ignore_focus_len_list = _input_ignore_focus_len_list()
    round_down_digit_num = _input_round_down_digit_num()
    show_count_zero = _input_show_count_zero()
    return (
        parent_path,
        ignore_focus_len_list,
        round_down_digit_num,
        show_count_zero,
    )


def main():
    with _stop_watch():
        print("中止したい場合は'Ctrl + C'を押すか、画面ごと閉じてね。")
        (
            parent_path,
            ignore_focus_len_list,
            round_down_digit_num,
            show_count_zero,
        ) = _input_setting_values()

        if path_list := _get_image_path_list(parent_path):
            print(f"ファイル総数: {len(path_list)}")
            focal_len_list = _get_focal_len_list(path_list)
            focal_len_list = _remove_value_from_list(
                focal_len_list, remove_value_list=ignore_focus_len_list
            )
            count_dict = _get_count_dict_by_tens_digit(
                focal_len_list, round_down_digit_num
            )
        else:
            print("*.jpg画像が見つかりませんでした……")
    _view_graph_image(count_dict, show_count_zero=show_count_zero)


if __name__ == "__main__":
    main()
