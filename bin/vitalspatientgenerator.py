import random
from datetime import datetime, timedelta, date, time

f = """male,2,0.88,90,42
male,2.5,0.92,92,48
male,2.6666666666666665,0.96,94,45
male,3.1666666666666665,0.99,98,52
male,4,1.06,102,56
male,4.5,1.1,104,62
male,5,1.12,106,64
male,5.25,1.14,105,65
male,5.25,1.14,107,67
male,5.5,1.16,113,71
male,5.75,1.18,113,72
male,5.916666666666667,1.19,112,73
male,6.25,1.22,112,71
male,6.5,1.23,110,69
male,6.75,1.24,106,65
male,7,1.24,104,63
male,7.25,1.28,106,65
male,7.5,1.29,106,68
male,7.75,1.31,106,63
male,7,1.32,108,69"""

ll = f.split("\n");
stats = [[float(x) for x in l.split(',')[1:]] for l in ll]

start = stats[0][1]
finish = stats[-1][1]

def interpolate(t):
  for i in range(1, len(stats)):
    if stats[i-1][0] <= t and stats[i][0] > t:
      return ((t-stats[i-1][0])*1.0 / (stats[i][0]-stats[i-1][0]), stats[i-1], stats[i])

  assert false, "couldn't interpolate %s"%t

def fuzz(ratio, t1, t2):
  ret = []
  for i in range(len(t1)):
    v = (1.0-ratio) * t1[i] + 1.0*ratio* t2[i]
    if i >1:  # don't allow date or height to jitter randomly
      v += random.gauss(0, (t1[i] - t2[i])/3)
    ret.append(v)
  return ret

def add_years(d1, y):
  return d1 + timedelta(days=int(365*y))

def choose_random (optionA, optionB, probability):
    n = random.uniform(0, 1)
    if n < probability:
        return optionA
    return optionB

def generate_vital (v, birthday):
    e = {'date': add_years(birthday, v[0]).isoformat(),
         'start_date': add_years(birthday, v[0]).isoformat(),
         'end_date': add_years(birthday, v[0]).isoformat(),
         'type': choose_random ("inpatient", "ambulatory", .25)}
    
    if random.random()<0.2:
        return {'height': round(v[1] * 100,1), 'encounter': e}
    else:
        return {'sbp': int(v[2]),
                'dbp': int(v[3]),
                'site': choose_random ("right arm", "left thigh", .8),
                'method': choose_random ("auscultation", "machine", .5),
                'position': 'sitting',
                'encounter': e}

def generate_patient ():
    birthday = datetime.combine(date(2011, int(random.uniform(1, 13)), int(random.uniform(1, 26))), time(0, 0)) - timedelta(days=stats[-1][0]*365)

    a = []
    output = ""
    for p in range(50):
      t = random.uniform(stats[0][0], stats[-1][0])
      r,t1,t2 = interpolate(t)
      v = fuzz(r,t1,t2)
      a.append(v)

    a.sort(key=lambda x: x[0])
    
    patient = {'pid': '99912345', 'birthday': birthday.strftime("%Y-%m-%d"), 'vitals': []}
    
    for l in a:
      patient['vitals'].append( generate_vital(l, birthday) )
      
    return patient
