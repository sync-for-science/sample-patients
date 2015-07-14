import glob
import json
import re

patients = glob.glob("./Patient*")
#patients = sorted(glob.glob("./Patient*"))

types = ["AllergyIntolerance", "Condition", "Encounter", "MedicationPrescription", "DiagnosticReport", "Immunization", "Observation"]

resources = []
def add_resource(rid, r):
    r['id'] = rid
    resources.append({'resource': r})

resource_num = 1000
def generate_ids(r_type, base=None):
    global resource_num
    if base == None:
        resource_num += 1
        base = resource_num
    id = "rheum-pacer-sample-data-%s" % base
    return ("%s/%s"%(r_type,id),id)

id_map = {}
def add_remap(old_id, new_rid):
    id_map[old_id] = new_rid

def set_id(r, r_type):
    (rid,id) = generate_ids(r_type)
    if 'id' in r:
        add_remap("%s/%s"%(r_type, r['id']), rid)
        del r['id']
    return (id, r)


substances = {
    'Substance/QE1QX6B99R': ["Peanut", "http://fda.gov/UNII/", "QE1QX6B99R"],
    'Substance/EYO007VX98': ["Dust", "http://fda.gov/UNII/", "EYO007VX98"],
    'Substance/1191': ["Aspirin", "http://www.nlm.nih.gov/research/umls/rxnorm", "1191"],
    'Substance/4053': ["Erythromycin", "http://www.nlm.nih.gov/research/umls/rxnorm", "4053"]
}

def resource_cleanup(r):
    if r['resourceType'] == 'MedicationPrescription':
        contained_med_ref = '#' + r['medication']['reference']
        r['medication']['reference'] = contained_med_ref
        r['contained'][0]['text'] = {
             "status": "generated",
             "div": "<div>%s</div>"%r['contained'][0]['text']['id']}
    if r['resourceType'] == 'AllergyIntolerance' and 'reference' in r['substance']:
        substance_label, substance_system, substance_code = substances[r['substance']['reference']]
        r['substance']['reference'] = "#substance"
        r['contained'] = [{
          "resourceType": "Substance",
          "id": "substance",
          "text": {
            "status": "generated",
            "div": "<div>%s</div>"%substance_label
          },
          "type": {
            "coding": [
              {
                "system": substance_system,
                "code": substance_code,
                "display": substance_label
              }
            ]
          }
        }]

bad_date_regex = re.compile("(\d+)/(\d+)/(\d+)")
def is_bad_date(d):
    return bad_date_regex.match(d)

def fix_bad_date(d):
    m,d,y = bad_date_regex.match(d).groups()
    return "%s-%s-%s"%(y, m.rjust(2,'0'), d.rjust(2,'0'))


def cleanup(data, path = None, depth=0):
    if path == None: path = []
    if type(data) is list:
        for i,d in enumerate(data):
            cleanup(d, path + [i], depth+1)
        return data
    elif type(data) is dict:
        for (k,v) in data.iteritems():
            data[k] = cleanup(v, path + [k], depth+1)
        return data
    elif type(data) is unicode:
        if data in id_map:
            return id_map[data]
        if is_bad_date(data):
            return fix_bad_date(data)
        return data
    else: 
        return data

for p in patients:
    patient = json.load(open("%s/Patient.txt"%p))
    patient['id'] = patient['identifier'][0]['value']
    pid, patient = set_id(patient, "Patient")
    add_resource(pid, patient)
    
    for r_type in types:
        t_file = json.load(open("%s/%s.txt"%(p, r_type)))
        rs = [t_file]
        if 'entry' in t_file: rs = [r['content'] for r in t_file['entry']]
        for one_resource in rs:
            id, r = set_id(one_resource, r_type)
            resource_cleanup(r)
            add_resource(id, r)

cleanup(resources)
feed = {
  'resourceType': 'Bundle',
  'entry': resources
}

#for r in resources:
#    print r['id']
print json.dumps(feed, indent=2)
