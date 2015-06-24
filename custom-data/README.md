## Custom data

To support ad-hoc sample apps that require more of the FHIR API than our simple
table-based generation scripts use, we allow sites to store FHIR .json or .xml
files right here. Files should be named after the sample app they're designed
to support, and can be automatically loaded along with generated sample data.


### For completeness/transparency...

If these files were generated, massaged, or "cleaned up" from some underlying
format, a per-file generation script can be created to capture any work that
went into that process. This script should be placed in
`raw/app-name/to-fhir.py` and should output (to stdout) a single FHIR bundle of
data for the app in question.

Calling `generate.sh` at this root level will automatically invoke all
`to-fhir` scripts and store their output here at the root.
