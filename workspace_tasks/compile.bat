@echo off

set python_file=D:\my_repositories\get_exif\get_exif\get_exif.py
set output_dir=D:\my_repositories\get_exif\compile\get_exif_compile

call activate get-exif
nuitka %python_file% --onefile --remove-output --show-modules --mingw64 --follow-imports --enable-plugin=tk-inter --output-dir=%output_dir%
