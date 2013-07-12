# Download netcdf data

for i in $(seq 1981 2000); do
	#wget ftp://gdo-dcp.ucllnl.org/pub/dcp/archive/bcca/miroc3_2_medres.gregorian/20c3m/run1/pr/bcca/miroc3_2_medres.gregorian.20c3m.run1.pr.BCCA_0.125deg.${i}.nc
	#wget ftp://gdo-dcp.ucllnl.org/pub/dcp/archive/bcca/miroc3_2_medres.gregorian/20c3m/run1/pr/bc/miroc3_2_medres.gregorian.20c3m.run1.pr.BC_2deg.${i}.nc
	#wget ftp://gdo-dcp.ucllnl.org/pub/dcp/archive/bcca/miroc3_2_medres.gregorian/20c3m/run1/pr/regrid/miroc3_2_medres.gregorian.20c3m.run1.pr.REGRID_2deg.${i}.nc

	#wget ftp://gdo-dcp.ucllnl.org/pub/dcp/archive/bcca/cccma_cgcm3_1.gregorian/20c3m/run1/pr/bcca/cccma_cgcm3_1.gregorian.20c3m.run1.pr.BCCA_0.125deg.${i}.nc
	#wget ftp://gdo-dcp.ucllnl.org/pub/dcp/archive/bcca/cccma_cgcm3_1.gregorian/20c3m/run1/pr/bc/cccma_cgcm3_1.gregorian.20c3m.run1.pr.BC_2deg.${i}.nc
	#wget ftp://gdo-dcp.ucllnl.org/pub/dcp/archive/bcca/cccma_cgcm3_1.gregorian/20c3m/run1/pr/regrid/cccma_cgcm3_1.gregorian.20c3m.run1.pr.REGRID_2deg.${i}.nc

	#wget ftp://gdo-dcp.ucllnl.org/pub/dcp/archive/bcca/gfdl_cm2_0.gregorian/20c3m/run1/pr/bcca/gfdl_cm2_0.gregorian.20c3m.run1.pr.BCCA_0.125deg.${i}.nc
	#wget ftp://gdo-dcp.ucllnl.org/pub/dcp/archive/bcca/gfdl_cm2_0.gregorian/20c3m/run1/pr/bc/gfdl_cm2_0.gregorian.20c3m.run1.pr.BC_2deg.${i}.nc
	#wget ftp://gdo-dcp.ucllnl.org/pub/dcp/archive/bcca/gfdl_cm2_0.gregorian/20c3m/run1/pr/regrid/gfdl_cm2_0.gregorian.20c3m.run1.pr.REGRID_2deg.${i}.nc

	#wget ftp://gdo-dcp.ucllnl.org/pub/dcp/archive/bcca/gfdl_cm2_1.gregorian/20c3m/run1/pr/bcca/gfdl_cm2_1.gregorian.20c3m.run1.pr.BCCA_0.125deg.${i}.nc
	#wget ftp://gdo-dcp.ucllnl.org/pub/dcp/archive/bcca/gfdl_cm2_1.gregorian/20c3m/run1/pr/bc/gfdl_cm2_1.gregorian.20c3m.run1.pr.BC_2deg.${i}.nc
	#wget ftp://gdo-dcp.ucllnl.org/pub/dcp/archive/bcca/gfdl_cm2_1.gregorian/20c3m/run1/pr/regrid/gfdl_cm2_1.gregorian.20c3m.run1.pr.REGRID_2deg.${i}.nc
	
	#wget ftp://gdo-dcp.ucllnl.org/pub/dcp/archive/bcca/mpi_echam5.gregorian/20c3m/run1/pr/bcca/mpi_echam5.gregorian.20c3m.run1.pr.BCCA_0.125deg.${i}.nc
	#wget ftp://gdo-dcp.ucllnl.org/pub/dcp/archive/bcca/mpi_echam5.gregorian/20c3m/run1/pr/bc/mpi_echam5.gregorian.20c3m.run1.pr.BC_2deg.${i}.nc
	#wget ftp://gdo-dcp.ucllnl.org/pub/dcp/archive/bcca/mpi_echam5.gregorian/20c3m/run1/pr/regrid/mpi_echam5.gregorian.20c3m.run1.pr.REGRID_2deg.${i}.nc

	#wget ftp://gdo-dcp.ucllnl.org/pub/dcp/archive/bcsd/yearly/miroc3_2_medres.1/miroc3_2_medres.1.sresa1b.monthly.Prcp.${i}.nc
	#wget ftp://gdo-dcp.ucllnl.org/pub/dcp/archive/bcsd/yearly/cccma_cgcm3_1.1/cccma_cgcm3_1.1.sresa1b.monthly.Prcp.${i}.nc
	#wget ftp://gdo-dcp.ucllnl.org/pub/dcp/archive/bcsd/yearly/gfdl_cm2_0.1/gfdl_cm2_0.1.sresa1b.monthly.Prcp.${i}.nc
	#wget ftp://gdo-dcp.ucllnl.org/pub/dcp/archive/bcsd/yearly/gfdl_cm2_1.1/gfdl_cm2_1.1.sresa1b.monthly.Prcp.${i}.nc
	wget ftp://gdo-dcp.ucllnl.org/pub/dcp/archive/bcsd/yearly/mpi_echam5.1/mpi_echam5.1.sresa1b.monthly.Prcp.${i}.nc


done