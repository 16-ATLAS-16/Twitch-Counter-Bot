from requests import get

def getUserAge(username: str):
	t = [a.split(" ") for a in get(f"https://decapi.me/twitch/accountage/{username}").text.split(", ")]
	days = 0
	for a in t:
		if a[1] == "days":
			days += int(a[0])
		elif a[1] == "months":
			days += int(a[0]) * 30
		elif a[1] == "years":
			days += int(a[0]) * 365
	return days