@echo off
powershell.exe -Command "& { influx delete --org Private --bucket IOT_PROJECT --start '1970-01-01T00:00:00Z' --stop '2029-12-31T23:59:59Z' --host https://eu-central-1-1.aws.cloud2.influxdata.com/ --token lGBO6gmsxGWnyV1wi929YTfZMIfhitIWtjUhbT-rH7XwfHqbNk8hMGeD4GdBEd1N5sF4OhgUZb5roCdudia8TQ==}"
echo Data cleared. Press any key to close...
pause > nul