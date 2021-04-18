from flask import Flask, render_template, redirect, url_for
app = Flask(__name__)

@app.route("/")
def home():
    
    bokeh_width, bokeh_height = 1000,600
    lat, lon = 46.2437, 6.0251
    api_key = "AIzaSyB4y5u1q0_-4kVQpSMGkH_dxpnzn8PL-dQ"
    print(str(api_key))
    def plot(lat, lng, zoom=10, map_type='roadmap'):
        
        from bokeh.io import show
        from bokeh.plotting import gmap
        from bokeh.models import GMapOptions
        
        gmap_options = GMapOptions(lat=lat, lng=lng, 
                               map_type=map_type, zoom=zoom)
        p = gmap(api_key, gmap_options, title='Pays de Gex', 
                 width=bokeh_width, height=bokeh_height)
        # beware, longitude is on the x axis ;-)
        center = p.circle([lng], [lat], size=10, alpha=0.5, color='red')
        
        return p
    
    p = plot(lat, lon, map_type='roadmap')
    
    #---------------------------------------------------
    from bokeh.io import curdoc
    from bokeh.layouts import column
    from bokeh.models import Button, ColumnDataSource
    from bokeh.plotting import Figure
    
    from bokeh.embed import components
    from bokeh.resources import CDN
    
    from numpy.random import random
    
    xs = []
    ys = []
    points = ColumnDataSource(data={'x_coord':xs, 'y_coord':ys})
    
    plot = Figure(title="Random Lines", x_range=(0, 1), y_range=(0, 1))
    
    plot.line('x_coord', 'y_coord', source=points)
    
    button = Button(label="Click Me!")
    
    def add_random_line():
        """
        Adds a new random point to the line.
        """
        x, y = random(2)
    
        newxs = [*points.data['x_coord'], x]
        newys = [*points.data['y_coord'], y]
    
        points.data = {'x_coord': newxs, 'y_coord': newys}
    
    
    button.on_click(add_random_line)
    
    layout = column(button, plot)
    
    
    curdoc().add_root(layout)
    
    script1, div1, = components(p)
    cdn_js = CDN.js_files[0]
    cdn_css = CDN.css_files
    
    print(script1)
    print('\n============================================')
    print(div1)
    print('\n============================================')
    print(cdn_css)
    print('\n============================================')
    print(cdn_js)
    
    # return render_template("combine.html",script1=script1,div1=div1, cdn_css=cdn_css,cdn_js=cdn_js)
    
    data_val1 = 'Hard Coded value 1'
    data_val2 = 'Hard coded value 2'
    
    templateData = {
        'data1' : data_val1,
        'data2' : data_val2
        }
    
    return render_template("combine.html", **templateData, script1=script1,div1=div1, cdn_css=cdn_css,cdn_js=cdn_js)


if __name__ == "__main__":
	app.run(port=5000)
    
    
        