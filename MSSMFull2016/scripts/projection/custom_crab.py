def custom_crab(config):
  print '>> Customising the crab config'
#  config.User.voGroup = 'dcms'
#  config.Site.storageSite = 'T2_DE_DESY'
  config.Site.storageSite = 'T2_AT_Vienna'
  config.Site.blacklist = ['T2_FI_HIP', 'T1_ES_PIC', 'T1_UK_RAL', 'T2_FR_CCIN2P3', 'T2_US_Nebraska', 'T1_IT_CNAF', 'T2_US_Vanderbilt', 'T3_US_Baylor', 'T3_US_UMiss' , 'T3_US_UCR' , 'T2_EE_Estonia' , 'T2_RU_PNPI' , 'T3_IT_Trieste' , 'T2_US_Wisconsin','T3_TW_NCU' ]
  # config.JobType.maxMemoryMB = 4500
