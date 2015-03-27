# Execute all tests that can run without any dependencies

export PYTHONPATH=".."

python test_range_helper.py
python test_scan_settings.py
python test_commands.py
python test_table_scan.py
python -m doctest test_ndim.txt