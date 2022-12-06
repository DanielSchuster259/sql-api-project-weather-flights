SELECT date,
	   MAX(wind_speed_kph),
	   airport_code
FROM group_1_weather
WHERE date > '2005-08-22'
GROUP BY date, airport_code;