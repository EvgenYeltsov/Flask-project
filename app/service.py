import requests

def weather_app():
	appid = "fc00fa7fab519f8e6bb68be3f364cb43"
	res = requests.get("http://api.openweathermap.org/data/2.5/weather?q=Zaporizhzhia",
				 params={'units': 'metric', 'lang': 'ru', 'APPID': appid})
	data = res.json()

	temp1 = data['weather'][0]['description']
	temp2 = data['main']['temp']
	return f"Zaporozhye conditions: {temp1} , temp: {temp2} C"
