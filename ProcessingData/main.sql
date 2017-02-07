SELECT #`index_day_historical_data`.`id`,
    #`index_day_historical_data`.`type`,
    `index_day_historical_data`.`date`,
    `index_day_historical_data`.`total_value`,
    #`index_day_historical_data`.`update_time`,
    sum(`total_value`) AS total_value2
FROM index_day_historical_data WHERE `date`>='2004-12-30' group by `date`
