import glob
import os
import time
from contextlib import contextmanager

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
        print(f"{time.time() - start_sec}[sec]")


def _remove_duplicate(list_):
    return list(set(list_))


def _sort_dict(dict_):
    sorted_dict = sorted(dict_.items())
    return dict((x, y) for x, y in sorted_dict)


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
    len_ = len(path_list)
    for index, path in enumerate(path_list):
        print(f"{index + 1}/{len_}")
        exif_dict = _get_exif_dict_jp_name_key(path)
        focal_len_list.append(exif_dict.get("レンズ焦点距離"))
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
        int(focal_len / place_num) * place_num for focal_len in focal_len_list
    ]
    result_dict = {}
    for num in round_downed_list:
        if not result_dict.get(num):
            result_dict[num] = 0
        result_dict[num] += 1
    return result_dict


def _view_graph_image(values_dict, show_count_zero_values=False):
    values_dict = _sort_dict(values_dict)
    if not show_count_zero_values:
        values_dict = {str(key): value for key, value in values_dict.items()}
    label_list = list(values_dict.keys())
    count_list = list(values_dict.values())
    bar_graph = pyplot.bar(label_list, count_list, width=0.9)
    pyplot.bar_label(bar_graph, labels=count_list)
    pyplot.show()


def execute(
    parent_path,
    exclusion_focus_len_list=[],
    round_down_digit_num=1,
    show_count_zero_values=False,
):
    with _stop_watch():
        path_list = _get_image_path_list(parent_path)
        print({"file_count": len(path_list)})
        focal_len_list = _get_focal_len_list(path_list)
        focal_len_list = _remove_value_from_list(
            focal_len_list, remove_value_list=exclusion_focus_len_list
        )
        count_dict = _get_count_dict_by_tens_digit(focal_len_list, round_down_digit_num)
    _view_graph_image(count_dict, show_count_zero_values=show_count_zero_values)


"""
parent_path:写真データが入っているフォルダのパス。
    このパスの直下と1階層下のサブフォルダまでOK。

exclusion_focus_length_list:除外する焦点距離のリスト。
    初期値は空。

round_down_digit_num:焦点距離を切り捨てる桁数。
    初期値は1桁目切り捨て。

show_count_zero_values:カウントが0の焦点距離を表示するか。
    初期値は非表示。
"""
execute(
    "D:\\趣味\\カメラ\\元データ",
    exclusion_focus_len_list=[],
    round_down_digit_num=1,
    show_count_zero_values=False,
)
