import time
import urllib.request, json
time = int(time.time())
print(time)
f = 'https://api.darksky.net/forecast/c260318659d78342a4f516ccfd74b27c/47.67228,9.384921,'
m = str(time)
l = '?exclude=daily,hourly,minutely,alerts,flags'
fml = f+m+l
#print(fml)
with urllib.request.urlopen(fml) as url:
    data = json.loads(url.read().decode())
    print(data)
    print(data['currently']['precipIntensity'])
    print(data['currently']['temperature'])
    print(data['currently']['windSpeed'])
    print(data['currently']['visibility'])
    print(data['currently']['humidity'])
    print(data['currently']['cloudCover'])
    print(data['currently']['pressure'])
