import pandas as pd
from bokeh.models import ColumnDataSource, CustomJS, Slider
from bokeh.plotting import figure, output_file, save
from bokeh.transform import factor_cmap
from bokeh.layouts import row


def create_sim_plot(log_df: pd.DataFrame, size: float):
   data_source = ColumnDataSource(log_df)
   starting_data = {}
   for col in log_df.columns:
      starting_data[col] = log_df[col][0:30]
   empty_source = ColumnDataSource(data=starting_data)

   fig = figure(width=800, height=800, x_range=(-3.14, 3.14), y_range=(-3.14, 3.14))
   output_file("RRRadar_Performance.html", title="Flyout_Performance")
   map = factor_cmap('detect', palette=["red", "green"], factors=sorted(log_df.detect.unique()))
   fig.scatter('scan_az', 'scan_el', size=size*10, source=empty_source, fill_color=map, alpha=0.5)
   fig.scatter('true_az', 'true_el', size=1*10, source=empty_source, color="grey")

   
   time = Slider(start=log_df.time.min(), end=log_df.time.max(), value=log_df.time.min()+30, step=1, title="Time")

   callback = CustomJS(args = dict(data_source = data_source, empty_source = empty_source), code = """
      console.log("Starting")
      var data = data_source.data;
      var fill_data = empty_source.data;
      var time_val = cb_obj.value;
      console.log("finding index")
      var new_index = 0;
      for (let index = 0; index < data['time'].length; index++) {
            if (data['time'][index] > (time_val-0.5) && data['time'][index] < (time_val+0.5)) {
               new_index = index; 
               break;
            }
         }
      console.log("found index")
      console.log(new_index)
      fill_data['scan_az']=data['scan_az'].slice(new_index-30,new_index);
      fill_data['scan_el']=data['scan_el'].slice(new_index-30,new_index);
      fill_data['true_az']=data['true_az'].slice(new_index-30,new_index);
      fill_data['true_el']=data['true_el'].slice(new_index-30,new_index);
      fill_data['detect']=data['detect'].slice(new_index-30,new_index);
      fill_data['time']=data['time'].slice(new_index-30,new_index);
      console.log("filled data")
      empty_source.data = fill_data;
      empty_source.change.emit() ;
      """)
   time.js_on_change('value', callback)
   
   save(row(fig, time))