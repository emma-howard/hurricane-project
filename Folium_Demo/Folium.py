import folium
from folium import IFrame
text = 'actual path'
def add_text(text,point):
    iframe = folium.IFrame(text, width=150, height=50)
    popup = folium.Popup(iframe, max_width=150)

    Text = folium.Marker(location=point, popup=popup,
                        icon=folium.Icon(icon_color='white'))
    return Text
def plot_path_actual(points,map):
    #add a markers
    for each in points:  
        folium.Marker(each).add_to(map)
    
    #fadd lines
    folium.PolyLine(points, color="red", weight=2.5, opacity=1).add_to(map)

    # add text marker
    Text = add_text("Actual Path",points[0])
    map.add_child(Text)

def plot_path_predicted(points,map):

    #add a markers
    for each in points:  
        folium.Marker(each).add_to(map)

    #fadd lines
    folium.PolyLine(points, color="blue", weight=2.5, opacity=1).add_to(map)
    Text = add_text("predicted Path",points[0])
    map.add_child(Text)

actual = [
    (13.1,-19),
    (13.3,-19.3),
    (13.6,-19.6),
    (14.1,-20)
]
predicted  = [
    (13.4,-19),
    (13.7,-19.3),
    (13.9,-19.6),
    (14.3,-20)
]

print(actual)
ave_lat = sum(p[0] for p in actual)/len(actual)
ave_lon = sum(p[1] for p in actual)/len(actual)

# Load map centred on average coordinates
my_map = folium.Map(location=[ave_lat, ave_lon], zoom_start=8)

plot_path_actual(actual,my_map)
plot_path_predicted(predicted,my_map)


# Save map
my_map.save("./map.html")
