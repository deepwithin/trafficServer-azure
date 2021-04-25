from flask import Flask, render_template, redirect, url_for
app = Flask(__name__)

import pandas as pd

from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure

def plot_graph(df2):
    times, temps, hums = df2['date/time'], df2['No_Green'], df2['No_Red']
    dt = times[-20:-1]
    ng = temps[-20:-1]
    nr = hums[-20:-1]
    fig = Figure()
    axis = fig.add_subplot(1, 1, 1)
    axis.set_title("Traffic Density")
    axis.set_ylabel("No. of Vehicles")
    axis.set_xlabel("Time stamp")
    axis.grid(True)
    
    xs = dt
    axis.plot(xs, ng)
    axis.plot(xs, nr)
    
    axis.tick_params(axis='x', labelrotation = 20)
    fig.legend(["Normal Vehicles", "Emergency Vehicles"])
    fig.set_size_inches(20,10)
    
    fig.savefig('./static/assets/foo.png')
    
    return

def vehicle_dots(vehicles_green=2, vehicles_red=1):
    from numpy.random import random
    lat, lon = 28.38972, 77.336715
    lat_max = 28.3915
    lon_max = 77.336725
    lon_min = 77.336705
    
    car_coords = [[0,0]]
    car_coords_x = [0]
    car_coords_y = [0]
    red_x = []
    red_y = []
    
    car_coords_x[0] = round(lat+(lat_max-lat)*random(), 6)
    car_coords[0][1] = car_coords_x[0]
    car_coords_y[0] = round(lon_min+(lon-lon_min)*random(), 6)
    car_coords[0][0] = car_coords_y[0]
    
    for i in range(vehicles_green*5):
        y = round(lat+(lat_max-lat)*random(), 6)
        x = round(lon_min+(lon-lon_min)*random(), 6)
        car_coords_x.append(x)
        car_coords_y.append(y)
        car_coords.append([x,y])
        
    if vehicles_red != 0:
        y = round(lat+(lat_max-lat)*random(), 6)
        x = round(lon_min+(lon-lon_min)*random(), 6)
        red_x.append(x)
        red_y.append(y)
        
    return car_coords, car_coords_x, car_coords_y, red_x, red_y

def plot(lat, lng, zoom=17, map_type='roadmap'):
        
    from bokeh.io import show
    from bokeh.plotting import gmap
    from bokeh.models import GMapOptions
    bokeh_width, bokeh_height = 1000,600
    api_key = "AIzaSyB4y5u1q0_-4kVQpSMGkH_dxpnzn8PL-dQ"
    
    gmap_options = GMapOptions(lat=lat, lng=lng, 
                           map_type=map_type, zoom=zoom)
    p = gmap(api_key, gmap_options, title='Pays de Gex', 
             width=bokeh_width, height=bokeh_height)
    # beware, longitude is on the x axis ;-)
    center = p.circle([lng], [lat], size=10, alpha=0.5, color='yellow')
    
    
    car_coords, car_coords_x, car_coords_y, red_x, red_y = vehicle_dots()
    print(car_coords)
    # see how we set radius instead of size:
    center = p.circle(car_coords_x, car_coords_y, size=10, alpha=0.5, 
                      color='blue')
    center = p.circle(red_x, red_y, size=10, alpha=0.5, 
                      color='red')
    
    return p

@app.route("/")
def home():
    
    bokeh_width, bokeh_height = 1000,600
    lat, lon = 28.38972, 77.33672
    api_key = "AIzaSyB4y5u1q0_-4kVQpSMGkH_dxpnzn8PL-dQ"
    # print(str(api_key))
    
    
    p = plot(lat, lon, map_type='roadmap')
    
    
    #---------------------------------------------------
    from bokeh.io import curdoc
    from bokeh.layouts import column
    from bokeh.models import Button, ColumnDataSource
    from bokeh.plotting import Figure
    
    from bokeh.embed import components
    from bokeh.resources import CDN
    
    url = 'https://docs.google.com/spreadsheets/d/1YwfjtMZMRtv9pflrrPjVqj4OIHv6RmEccHKCHCrwKqQ/export?format=csv&gid=0'
    df = pd.read_csv(url)
    plot_graph(df)
    
    script1, div1, = components(p)
    cdn_js = CDN.js_files[0]
    cdn_css = CDN.css_files
    
    # print(script1)
    # print('\n============================================')
    # print(div1)
    # print('\n============================================')
    # print(cdn_css)
    # print('\n============================================')
    # print(cdn_js)
    
    
    # return render_template("combine.html",script1=script1,div1=div1, cdn_css=cdn_css,cdn_js=cdn_js)
    
    data_val1 = df.iat[-4,1]
    data_val2 = df.iat[-3,1]
    data_val3 = df.iat[-2,1]
    data_val4 = df.iat[-1,1]
    em_val1 = df.iat[-4,2]
    em_val2 = df.iat[-3,2]
    em_val3 = df.iat[-2,2]
    em_val4 = df.iat[-1,2]
    t_val1 = df.iat[-4,0]
    t_val2 = df.iat[-3,0]
    t_val3 = df.iat[-2,0]
    t_val4 = df.iat[-1,0]
    
    templateData = {
        'data1' : data_val1,
        'data2' : data_val2,
        'data3' : data_val3,
        'data4' : data_val4,
        'em1' : em_val1,
        'em2' : em_val2,
        'em3' : em_val3,
        'em4' : em_val4,
        't1' : t_val1,
        't2' : t_val2,
        't3' : t_val3,
        't4' : t_val4
        }
    
    return render_template("combine.html", **templateData, script1=script1,div1=div1, cdn_css=cdn_css,cdn_js=cdn_js)


if __name__ == "__main__":
	app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=True)
    
    
        