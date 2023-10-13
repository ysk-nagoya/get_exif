@echo off

set output_dir=%1\compile\sg-ami_process
set python_file=%1\get_exif\get_exif.py

call activate ""
nuitka %python_file% --standalone --remove-output --show-modules --mingw64 --follow-imports --plugin-enable=pyside6 --include-qt-plugins=platforms --output-dir=%output_dir%

@REM nuitka=1.5.0
@REM mingw64=v11.3.0