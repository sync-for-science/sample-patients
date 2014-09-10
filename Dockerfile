FROM dockerfile/python
RUN pip install jinja2
ADD . /code
WORKDIR /code/bin
CMD ["--write-fhir","/generated"]
ENTRYPOINT  ["python", "generate.py"]
