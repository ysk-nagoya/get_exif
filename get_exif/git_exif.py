import glob
import os

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


def _remove_duplicate(list_):
    return list(set(list_))


def _sort_dict(dict_):
    sorted_dict = sorted(dict_.items())  # 変更
    return dict((x, y) for x, y in sorted_dict)


def _remove_value_from_list(list_, remove_value_list):
    if not remove_value_list:
        return list_

    return [value for value in list_ if value not in remove_value_list]


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
    for path in path_list:
        exif_dict = _get_exif_dict_jp_name_key(path)
        focal_len_list.append(exif_dict.get("レンズ焦点距離"))
    return focal_len_list


def _get_count_dict_by_tens_digit(focal_len_list):
    round_downed_list = [int(focal_len / 10) * 10 for focal_len in focal_len_list]
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


def execute():
    parent_path = "D:\\趣味\\カメラ\\元データ"  # cspell: disable-line
    path_list = _get_image_path_list(parent_path)
    print({"file_count": len(path_list)})
    focal_len_list = _get_focal_len_list(path_list)
    focal_len_list = _remove_value_from_list(focal_len_list)
    count_dict = _get_count_dict_by_tens_digit(focal_len_list)
    _view_graph_image(count_dict)


execute()
