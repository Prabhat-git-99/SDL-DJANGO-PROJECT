from django.shortcuts import render , render_to_response
from django.http import HttpResponse
from bokeh.plotting import figure , show
from bokeh.embed import components
from bokeh.layouts import column
from bokeh.models import HoverTool, ColumnDataSource
import pandas
import numpy
from bokeh.io import export_png
from datetime import datetime
from bokeh.palettes import Spectral3
import csv
from bokeh.resources import CDN
from bokeh.embed import file_html   
import matplotlib.pyplot as plt 
# Create your views here.

def start(request):
    return render(request,'home.html')

def tool(request):
    return render(request,'pretool.html')

#---------------------TOP 10 GAINERS Acc. To ADJUSTED CLOSE------------------------

def Gainer(request):
    df = pandas.read_csv('data.csv',index_col = None)
    take = df.groupby('Company').mean()
    sort = take.sort_values(by = ['Adj Close'], ascending = False).reset_index().head(10)
    sort.index += 1
    table_content = sort.to_html(classes='table table-striped table-bordered table-hover table-condensed')
    context = {'table_content': table_content}
    return render(request, 'topgainer.html', context)

#-----------------TOP 10 Loser Acc. To ADJUSTED CLOSE------------------------

def Loser(request):
    df = pandas.read_csv('data.csv',index_col = None)
    take = df.groupby('Company').mean()
    sort = take.sort_values(by = ['Adj Close'], ascending = True).reset_index().head(10)
    sort.index += 1
    table_content = sort.to_html(classes='table table-striped table-bordered table-hover table-condensed')
    context = {'table_content': table_content}
    return render(request, 'toploser.html', context)

#-----------------------------MOST ACTIVE-----------------------------

def active(request):
    df = pandas.read_csv('data.csv',index_col = None)
    take = df.groupby('Company').mean()
    sort = take.sort_values(by = ['Volume'], ascending = False).reset_index().head(10)
    sort.index += 1
    table_content = sort.to_html(classes='table table-striped table-bordered table-hover table-condensed')
    context = {'table_content': table_content}
    return render(request, 'mostactive.html', context)

#-------------------------OUR RECCOMENDATION--------------------------


def reccommendation(request):
    df = pandas.read_csv('data.csv',index_col = None)
    take = df.groupby('Company').mean()
    diff_list = take
    sort_gainer = take.sort_values(by = ['Adj Close'], ascending = False).reset_index().head(15)
    sort_active = take.sort_values(by = ['Volume'], ascending = False).reset_index().head(15)
    diff_list['Difference'] = diff_list['High'] - diff_list['Low']
    sort_diff = diff_list.sort_values(by = ['Difference'], ascending = True).reset_index().head(15)
    temp = sort_gainer.merge(sort_active, how = 'inner')
    final = temp.merge(diff_list, how = 'inner')
    final.index += 1
    table_content = final.to_html(classes='table table-striped table-bordered table-hover table-condensed')
    context = {'table_content': table_content}
    return render(request, 'globalmarket.html', context)
    

#------------------------TOOL-----------------------

def input(request):
    #company = request.POST['company']
    if 'pass' in request.POST:
        fetch = request.POST['pass']
    else:
        fetch = False
    data = pandas.read_csv('data.csv',index_col = None)
    ref = data[data.Company== fetch]
    #take = df.groupby('Company').mean()
    #----------company mean--------------

    mean = ref.mean()
    conv = pandas.DataFrame(mean)
    trans = conv.T
    temp = trans.to_html(classes = 'table')
    #------mean stored in temp------------ END    
    
    #--------last 15 Days Trends-----------

    last_20 = ref.iloc[-10:]
    cut = last_20[last_20.columns[1:]]
    last_20f = cut.to_html(classes = 'table1')

    #-----------END------------
    #----------GRAPH----------------tempID 1067
    
    collection = pandas.read_csv('data.csv',parse_dates = ['Date'])
    gref = collection[collection.Company== fetch]
    ref = collection[collection.Company== fetch].tail(300)
    TOOLTIPS = [
    ("index", "$Company"),
    ("(x,y)", "($x, $y)"),
    ("desc", "@desc"),
]
    plot = figure(
        width = 700, height = 400, x_axis_type = 'datetime', title = 'AJA GRAPH AJA',tooltips = TOOLTIPS,
    )
    plot.ygrid.band_fill_alpha = 0.5
    plot.ygrid.band_fill_color = "grey"
    plot.line(
        ref['Date'],ref['Close'],color = 'red',alpha = 0.8, legend = "Close"
    )
    plot.line(
        ref['Date'],ref['Open'],color = 'green',alpha = 0.8, legend = 'Open'
    )
    cr = plot.circle(ref['Date'], ref['Open'], size=10,
             hover_fill_color="firebrick",
                fill_alpha = 0, hover_alpha=0.5,line_color = None,
                hover_line_color="white")

    plot.add_tools(HoverTool(tooltips=None, renderers=[cr], mode='hline'))
    plot.border_fill_color = "black"
    plot.legend.location = "top_left"
    plot.legend.background_fill_color = "red"
    plot.legend.background_fill_alpha = 0.3
    script , divi = components(plot)

    #---------------VBAR--------------------------
    yearly = gref.groupby(pandas.Grouper(key='Date', freq='Y'))['Open','Close','High','Low','Adj Close'].mean()
    #High_from = yearly['High']
    date_f = yearly.index
    year_sort = gref.groupby(pandas.Grouper(key = 'Date',freq = 'Y'))['Date','High','Adj Close','Volume'].mean()
    High_from = yearly['High']
    Low_from = yearly['Low']
    Adj_from = yearly['Adj Close']
    Vol_from = yearly['Close']
    year_sort_frame = pandas.DataFrame(year_sort)
    years = [2008,2009,2010,2011,2012,2013,2014,2015,2016,2017,2018]
    bar1 = figure(plot_width=400, plot_height=300)
    bar1.vbar(x = years, width=0.6, bottom=0,
       top=High_from, color="black", hover_fill_color="blue")
    bar1.add_tools(HoverTool(tooltips=None, mode='hline'))
    #--------------bar2--------------------
    bar2 = figure(plot_width=400, plot_height=300)
    bar2.vbar(x = years, width=0.6, bottom=0,
       top=Low_from, color="black", hover_fill_color="blue")
    bar2.add_tools(HoverTool(tooltips=None, mode='hline'))
    #--------------bar3-------------------
    bar3 = figure(plot_width=400, plot_height=300)
    bar3.vbar(x = years, width=0.6, bottom=0,
       top=Adj_from, color="black", hover_fill_color="blue")
    bar3.add_tools(HoverTool(tooltips=None, mode='hline'))
    #-------------bar4----------------------
    bar4 = figure(plot_width=400, plot_height=300)
    bar4.vbar(x = years, width=0.6, bottom=0,
       top=Vol_from, color="black", hover_fill_color="blue")
    bar4.add_tools(HoverTool(tooltips=None, mode='hline'))
   
    script1 , bar_high = components(bar1)
    script2 , bar_low = components(bar2)
    script3 , bar_adj = components(bar3)
    script4 , bar_vol = components(bar4)   

    
    return render(request,'result.html',{'company':fetch,'tabcontent':temp,'last_20':last_20f,'divi':divi,'script':script,'bar_high':bar_high,'script1':script1, 'bar_low':bar_low ,'bar_adj':bar_adj, 'bar_vol':bar_vol, 'script2':script2,'script3':script3,'script4':script4})


#-------------RESULT----------

def result(request):
    return render(request,'result.html')



    ''' yearly = gref.groupby(pandas.Grouper(key='Date', freq='Y'))['Open','Close'].mean()
    high_from = yearly['Close']
    date_f = yearly.index
    year_sort = gref.groupby(pandas.Grouper(key = 'Date',freq = 'Y'))['Date','High'].mean()
    year_sort_frame = pandas.DataFrame(year_sort)
    years = [2008,2009,2010,2011,2012,2013,2014,2015,2016,2017,2018]
    bar = figure(plot_width=500, plot_height=400)
    bar.vbar(x = years, width=0.8, bottom=0,
       top=high_from, color="firebrick", hover_fill_color="blue")
    bar.add_tools(HoverTool(tooltips=None, mode='hline'))
   
    script1 , bar_high = components(bar) 
    '''