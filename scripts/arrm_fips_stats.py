"""Need to compute


"""
import psycopg2
import pyiem.reference as reference
from pyiem.datatypes import distance, temperature
import requests
from tqdm import tqdm
import pandas as pd
import json
import os
import datetime
import numpy as np
import sys

model = sys.argv[1]

pgconn = psycopg2.connect(database="postgis")
cursor = pgconn.cursor()

fips_info = {}
for line in open("/tmp/FIPS_UMRBOTRB.csv"):
    line = line.strip()
    stcode = int(line[:-3])
    cntycode = line[-3:]
    ugc = "%sC%s" % (reference.state_fips[stcode], cntycode)
    cursor.execute(
        """SELECT ST_x(ST_Centroid(geom)), st_y(ST_Centroid(geom))
    from ugcs where ugc = %s and end_ts is null""",
        (ugc,),
    )
    (lon, lat) = cursor.fetchone()
    fips_info[line] = {"ugc": ugc, "lat": lat, "lon": lon}

D8 = [0.0625, 0.1875, 0.3125, 0.4375, 0.5625, 0.6875, 0.8125, 0.9375]


def compute_fn(lon, lat):
    """Figure out our nearest point"""
    p = lat - float(int(lat))
    d = np.digitize([p], D8)
    if d[0] == 8:
        d = [7]
    p = abs(lon) + float(int(lon))
    d2 = np.digitize([p], D8)
    if d2[0] == 8:
        d2 = [7]
    fn = "%.4f_%.4f" % (
        float(int(lon)) - D8[d2[0]],
        float(int(lat)) + D8[d[0]],
    )
    return fn


processed = []
for fips, info in tqdm(fips_info.items()):
    # figure out our closest point, hmmm
    basefn = compute_fn(info["lon"], info["lat"])
    # print basefn, info['lon'], info['lat']
    # load precip
    fn = "../arrm/swatfiles_%s/%s.pcp" % (model, basefn)
    if not os.path.isfile(fn):
        continue
    obs = {}
    for line in open(fn):
        if not line.startswith("20"):
            continue
        if line.find("-99.0") > 0:
            line = line.replace("-99.0", "  0.0")
        valid = datetime.datetime.strptime(line[:7], "%Y%j")
        obs[valid] = {
            "valid": valid,
            "precip_in": distance(float(line[7:12]), "MM").value("IN"),
        }
    fn = "../arrm/swatfiles_%s/%s.tmp" % (model, basefn)
    for line in open(fn):
        if not line.startswith("20"):
            continue
        if line.find("-99.0") > 0:
            continue
        valid = datetime.datetime.strptime(line[:7], "%Y%j")
        obs[valid]["high_f"] = temperature(float(line[7:12]), "C").value("F")
        obs[valid]["low_f"] = temperature(float(line[12:17]), "C").value("F")

    res = {"fips": fips}
    rows = []
    for key, row in obs.iteritems():
        rows.append(row)
    df = pd.DataFrame(rows)
    df["avgt_f"] = (df["high_f"] + df["low_f"]) / 2.0
    df.set_index("valid", inplace=True)
    df["high_f86"] = df["high_f"]
    df.at[df["high_f86"] < 50, ["high_f86"]] = 50.0
    df.at[df["high_f86"] > 86, ["high_f86"]] = 86.0
    df["low_f86"] = df["low_f"]
    df.at[df["low_f86"] < 50, ["low_f86"]] = 50.0
    df.at[df["low_f86"] > 86, ["low_f86"]] = 86.0
    df["gdd50"] = (df["high_f86"] + df["low_f86"]) / 2.0 - 50.0
    df["sdd86"] = df["high_f"] - 86
    df["heavyrain5cm"] = 0
    df.at[df["sdd86"] < 0, ["sdd86"]] = 0
    df.at[df["precip_in"] > 1.97, ["heavyrain5cm"]] = 1
    mmeans = df.resample("M", how="mean")
    mmeans["month"] = mmeans.index.month
    mmeans0711 = mmeans["2046-01-01":"2066-01-01"]
    mmeans0711m = mmeans0711.groupby("month").mean()
    mmeanss = mmeans.groupby("month").std()

    msums = df.resample("M", how="sum")
    msums["month"] = msums.index.month
    msums0711 = msums["2046-01-01":"2066-01-01"]
    msums0711m = msums0711.groupby("month").mean()
    msumss = msums.groupby("month").std()
    # 1) April thru Sept GDD50 average for 2007-2011
    res["season_gdd"] = msums0711m.loc[4:9, "gdd50"].sum()
    # 2) April thru Sept monthly average GDD50
    res["apr_avg_gdd"] = msums0711m.loc[4, "gdd50"]
    res["may_avg_gdd"] = msums0711m.loc[5, "gdd50"]
    res["jun_avg_gdd"] = msums0711m.loc[6, "gdd50"]
    res["jul_avg_gdd"] = msums0711m.loc[7, "gdd50"]
    res["aug_avg_gdd"] = msums0711m.loc[8, "gdd50"]
    res["sep_avg_gdd"] = msums0711m.loc[9, "gdd50"]
    # 3) Average Precip for each month
    res["apr_avg_precip"] = msums0711m.loc[4, "precip_in"]
    res["may_avg_precip"] = msums0711m.loc[5, "precip_in"]
    res["jun_avg_precip"] = msums0711m.loc[6, "precip_in"]
    res["jul_avg_precip"] = msums0711m.loc[7, "precip_in"]
    res["aug_avg_precip"] = msums0711m.loc[8, "precip_in"]
    res["sep_avg_precip"] = msums0711m.loc[9, "precip_in"]
    # 4) monthly Arridity Index
    tstd = mmeanss["high_f"]
    pstd = msumss["precip_in"]
    for idx, row in mmeans0711.iterrows():
        t = row["high_f"]
        p = msums0711.loc[idx, "precip_in"]
        month = idx.month
        tavg = mmeans0711m.loc[month, "high_f"]
        pavg = msums0711m.loc[month, "precip_in"]
        tstd = mmeanss.loc[month, "high_f"]
        pstd = msumss.loc[month, "precip_in"]
        arridity = (t - tavg) / tstd - (p - pavg) / pstd
        res["arridity_%s" % (idx.strftime("%Y%m"),)] = arridity
    # 5) Heat Stress Days
    res["apr_avg_sdd"] = msums0711m.loc[4, "sdd86"]
    res["may_avg_sdd"] = msums0711m.loc[5, "sdd86"]
    res["jun_avg_sdd"] = msums0711m.loc[6, "sdd86"]
    res["jul_avg_sdd"] = msums0711m.loc[7, "sdd86"]
    res["aug_avg_sdd"] = msums0711m.loc[8, "sdd86"]
    res["sep_avg_sdd"] = msums0711m.loc[9, "sdd86"]
    # 6) monthy average Tmax for April - Sept
    res["apr_avg_high"] = mmeans0711m.loc[4, "high_f"]
    res["may_avg_high"] = mmeans0711m.loc[5, "high_f"]
    res["jun_avg_high"] = mmeans0711m.loc[6, "high_f"]
    res["jul_avg_high"] = mmeans0711m.loc[7, "high_f"]
    res["aug_avg_high"] = mmeans0711m.loc[8, "high_f"]
    res["sep_avg_high"] = mmeans0711m.loc[9, "high_f"]
    # 7) Days over 5cm precip
    res["apr_rain5cm_days"] = msums0711m.loc[4, "heavyrain5cm"]
    res["may_rain5cm_days"] = msums0711m.loc[5, "heavyrain5cm"]
    res["jun_rain5cm_days"] = msums0711m.loc[6, "heavyrain5cm"]
    res["jul_rain5cm_days"] = msums0711m.loc[7, "heavyrain5cm"]
    res["aug_rain5cm_days"] = msums0711m.loc[8, "heavyrain5cm"]
    res["sep_rain5cm_days"] = msums0711m.loc[9, "heavyrain5cm"]
    # 8) Average monthly temp
    res["apr_avg_temp"] = mmeans0711m.loc[4, "avgt_f"]
    res["may_avg_temp"] = mmeans0711m.loc[5, "avgt_f"]
    res["jun_avg_temp"] = mmeans0711m.loc[6, "avgt_f"]
    res["jul_avg_temp"] = mmeans0711m.loc[7, "avgt_f"]
    res["aug_avg_temp"] = mmeans0711m.loc[8, "avgt_f"]
    res["sep_avg_temp"] = mmeans0711m.loc[9, "avgt_f"]
    processed.append(res)

df = pd.DataFrame(processed)
df.set_index("fips", inplace=True)
df.to_csv("fips_%s.csv" % (model,))
