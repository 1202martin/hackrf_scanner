# hackrf_scanner
Python-based software to scan Radio Frequency signals using HackRF and to update the information onto a Database- involves a bit of Flask to control the device running hackrf

- hackrf_scan_live.py : File defining a Scanner class composed of multiple functions that allow the user to scan a frequency range based on central frequency or start && end of a frequency range. Also contains a function to update the scanned rf data onto a local database.
- hackrf_scan_live_ssh.py : Similar to hackrf_scan_live.py, this file defines a Scanner class that supports frequency range scanning- the difference is in how the database is accessed to update the signal strength. In hackrf_scan_live_ssh.py, connection to database is made through ssh tunneling.
- hackrf_scan_live_ssh_v2.py : An updated version of hackrf_scan_live_ssh.py; there has been a change in how the frequency tables are created and maintained.
    ㄴ signal_str table from the previous version is renamed as full_range_scan
    ㄴ each sub-frequencies (433,915,2400,5000 MHz) maintain their own tables. These tables have 5000 bins by default.
    ㄴ The tables no longer just maintain the latest signal strength data for each channel. Instead, they maintain a record of signal strength at each channel on a timely basis.
- sdr_server_hackrf.py : Flask based web application to make the Scanner objects accessible by the user.  
- sdr_server_hackrf_v2.py: A newer version of sdr_server_hackrf.py, which will soon be taking inputs to apply custom frequency ranges to scan; still needs work on this area- not much has changed.
