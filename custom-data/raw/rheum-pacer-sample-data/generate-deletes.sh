for r in `python to-fhir.py`; do echo "curl -X DELETE https://fhir-open-api.smarthealthit.org/$r"; done
