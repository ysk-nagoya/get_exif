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

TYPICAL_FOCAL_LENGTH_LIST = [
    11,
    14,
    16,
    17,
    18,
    20,
    24,
    28,
    35,
    40,
    50,
    70,
    85,
    90,
    100,
    105,
    135,
    180,
    200,
    300,
    400,
    500,
    600,
    800,
    1000,
    1200,
    1600,
    2000,
    2400,
    3000,
]


class _Mode:
    TYPICAL = "typical"
    BY_IMAGE = "by_image"


MODE = _Mode()
