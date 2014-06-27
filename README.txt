SMART ON FHIR TEST DATA GENERATOR

This generator uses the data files in the 'data' directory to generate
FHIR test data.  The files in the data directory are tab-delimited 
tables that can be edited and extended with new data as needed.

All the python scripts are in the 'bin' directory, and should be run from
that directory.

The main script for general use is generate.py, the other files in 'bin' 
are basically modules supporting generate.py. The file 'testdata.py' 
contains most of the constant declarations and utility functions that
drive the system configuration. The file 'fhir.py' contains all 
the FHIR formatting code. 

From the 'bin' directory, run:

   python generate.py --help

To get a general help message.

To generate the test data files in the 'generated-data' directory:

   python generate.py --write-fhir ../generated-data 

And a 'summary.txt' file can be added to 'generated-data' by running:

   python generate.py --summary > ../generated-data/summary.txt

A good way to look at a single patient, with patient ID, PID, is:

   python generate.py --summary PID
