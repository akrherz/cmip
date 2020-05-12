import subprocess

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

for m in models:
    cmd = "python hayhoe2coopdb.py %s a1b" % (m,)
    # subprocess.call(cmd, shell=True)
    cmd = "python arrm_fill_holes.py %s a1b" % (m,)
    subprocess.call(cmd, shell=True)
