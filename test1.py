str = "맑음(낮) 체감온도 9°"

weatherText2 = ""
for char in str:
    if char == "(":
        break
    weatherText2 = weatherText2 + char

print(weatherText2)