# IoT
A Python script to simulate IoT devices sending data to EMQX

#location
cd ~/Desktop/Github 1/IoT

#venv-activate
source venv/bin/activate
#EMQX-activate
docker-compose up -d
#Code-activate
python device_simulator.py

#Saving
git add .
git commit -m "feat : "
git push

#sites
http://localhost:8086        #Influx
admin   adminpassword

http://localhost:18083       #EMQX
admin   emqxpassword

http://localhost:3000        #Grafana
admin   grafanapassword

#more
NGINX

from(bucket: "iot_bucket")
  |> range(start: v.timeRangeStart, stop: v.timeRangeStop)
  |> filter(fn: (r) => r["_measurement"] == "mqtt_consumer")
  |> filter(fn: (r) => r["_field"] == "vm_pu")
  |> group(columns: ["name"])
  |> aggregateWindow(every: v.windowPeriod, fn: mean, createEmpty: false)
  |> yield(name: "mean")
  
