# hackrf_scanner
Python-based software to scan Radio Frequency signals using HackRF and to update the information onto a Database- involves a bit of Flask to control the device running hackrf

- hackrf_scan_live.py : File defining a Scanner class composed of multiple functions that allow the user to scan a frequency range based on central frequency or start && end of a frequency range. Also contains a function to update the scanned rf data onto a local database.
- hackrf_scan_live_ssh.py : Similar to hackrf_scan_live.py, this file defines a Scanner class that supports frequency range scanning- the difference is in how the database is accessed to update the signal strength. In hackrf_scan_live_ssh.py, connection to database is made through ssh tunneling.
- sdr_server_hackrf.py : Flask based web application to make the Scanner objects accessible by the user.  
