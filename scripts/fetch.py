import urllib2
from pyiem.network import Table as NetworkTable

nt = NetworkTable("CSCAP")

models = [
    "miroc_hi",
    "cgcm3_t47",
    "cgcm3_t63",
    "hadcm3",
    "giss_aom",
    "hadgem",
    "echam5",
    "echo",
    "cnrm",
    "pcm",
]

models = ["cgcm3_t47", "cgcm3_t63", "echam5", "hadgem", "echo", "cnrm"]


# for sid in ['BDMARI', 'BDCLOV', 'BDLOSL', 'BDTUCU', 'BDRENO', 'BDFALL']:
for sid in nt.sts.keys():
    climatesite = nt.sts[sid]["climate_site"]
    for model in models:
        print "Running %s %s %s" % (model, "bogus", sid)
        uri = (
            "http://iem.local/cgi-bin/request/coop.py?network=%sCLIMATE&"
            "station[]=%s&year1=1961&month1=1&day1=1&"
            "year2=2099&month2=1&day2=1&vars[]=daycent&"
            "hayhoe_scenario=a1b&hayhoe_model=%s&"
            "what=view&delim=comma&gis=no"
        ) % ("IA", climatesite, model)

        data = urllib2.urlopen(uri).read()

        outfn = "data/%s_%s_%s.txt" % (sid, model, "a1b")
        o = open(outfn, "w")
        o.write(data)
        o.close()
