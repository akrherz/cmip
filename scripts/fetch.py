import urllib2

xref = {'MO1791': 'BRADFORD',
        'IA6719': 'GILMORE',
        'IA0200': 'ISUAG',
        'IN6435': 'SEPAC',
        'MI3504': 'KELLOGG'}

models = ['miroc_hi',
 'cgcm3_t47',
 'cgcm3_t63',
 'hadcm3',
 'giss_aom',
 'hadgem',
 'echam5',
 'echo',
 'cnrm', 
 'pcm']

for model in models:
    for station in xref.keys():
        print 'Running %s %s' % (model, station)
        uri = ("http://iem.local/cgi-bin/request/coop.py?network=%sCLIMATE&"
         +"station[]=%s&year1=2005&month1=1&day1=1&"
         +"year2=2099&month2=1&day2=1&vars[]=daycent&"
         +"hayhoe_scenario=a1b&hayhoe_model=%s&"
         +"what=view&delim=comma&gis=no&scenario_year=2013") % (station[:2],
                                                              station, model)
         
        data = urllib2.urlopen(uri).read()
        
        outfn = "data/%s_%s_%s.txt" % (xref[station], model, 'a1b')
        o = open(outfn, 'w')
        o.write(data)
        o.close()