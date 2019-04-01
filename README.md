cmip (not maintained)
=====================

1) MIROC 3.2 medres
2) HADCM3
3) ECHAM5
4) CSIRO
5) CGCM3 
6) GFDL

Found not enough data, so we went with

1) MIROC 3.2 medres
2) mri_cgcm2_3_2a  non_tp_deltas_done
3) cnrm_cm3

http://cida.usgs.gov/thredds/fileServer/dcp/files/Hayhoe_USGS_downscaled_database_final_report.pdf


 In CMIP5, the A1, B1, etc. "storylines" are replace
with representative concentration pathways. The RCPs are designated after
the radiative forcing they produce at the year 2100.  Of these, RCP 8.5 is
closest at mid-century to the A1B scenario we used in the JSWC paper.

Codes related to the work on CMIP3 / CMIP5 and BCCA / BCSD

Resulting plots go here:
http://mesoscale.agron.iastate.edu/downscale/

Here are my marching orders:

Obs for both BCCA CMIP3 and BCCA CMIP5

CMIP3             BCCA    BC    BCSD   RAW  REGRID
miroc3_2_medres     x     x      x      x     x
cccma-cgcm3_1       x     x      x      x     x
gfdl_cm2_0          x     x      x      x     x
gfdl_cm2_1          x     x      x      x     x
mpi_echam5          x     x      x      x     x

CMIP5
gfdl-cm3            x     x      x      x     x
miroc5              x     x      x      x     x
mpi-esm-lr          x     x      x      x     x
mpi-esm-mr          x     x      x      x     x

Plots:
# raw
# bias corrected (bc)
# BCCA 
# BCSD
# BCSD - BCCA


Notes:

7 March 2014
 - the Canadian model I previously had noted is cgcm3
 - I'm supplying the monthly deltas (temp change and precip multiplier)
  - 
