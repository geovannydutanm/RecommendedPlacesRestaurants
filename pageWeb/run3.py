from flask import Flask, render_template

app = Flask(__name__)



@app.route('/')
def index():
    start_coords = (46.9540700, 142.7360300)
    folium_map = folium.Map(location=start_coords, zoom_start=14)
    folium_map.save()
    return render_template('index.html', folium_map=folium_map)


    if __name__ == '__main__':
    app.run(debug=True)