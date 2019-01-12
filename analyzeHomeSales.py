#%%
# load the necessary modules
import pandas as pd
import numpy as np
# Bokeh libraries
from bokeh.io import output_notebook
from bokeh.plotting import figure, show
from bokeh.models import ColumnDataSource, CDSView
from bokeh.models.widgets import RangeSlider


def cds_medianSalePriceOverTime(pandaDF):
    # find the median over time
    medianizedData = pd.pivot_table(pandaDF,
        values='Sales_Price',
        index='Sale_Date',
        aggfunc=np.median
        )

    # define the data source
    cdsMedianizedData = ColumnDataSource(medianizedData)
    return cdsMedianizedData

def retrieveAndCleanData():
    # read in the file data
    dataFrame = pd.read_csv(
        'C:\\Users\\Alex Trim\\Documents\\GitHub\\hello-world\\' + \
        'AtomPython\\HomeSalesAnalysis\\homeSalesData.txt'
        )
    # no index in file so reset it
    dataFrame.reset_index(inplace=True)
    # clean up the data
    dataFrame['Sale_Date'] = pd.to_datetime(
        dataFrame['Sale_Date'],
        yearfirst=True
        )

    dataFrame['Sales_Price'] = pd.to_numeric(
        dataFrame['Sales_Price'].str.strip('$').str.replace(',', '')
        ).apply(lambda x: x * .001)    
    
    return dataFrame


def addLineToFigure(figure, source, legend, color):
    # add data to the figure    
    figure.line(
        'Sale_Date',
        'Sales_Price',
        source=source,
        legend=legend,
        color=color,
        )


def addDotsToFigure(figure, source, legend, color):
    # add data to the figure
    figure.circle(
        'Sale_Date',
        'Sales_Price',
        source=source,
        legend=legend,
        color=color,
        alpha=.2
    )


#%%
output_notebook()
# determine the data sets
initialData = retrieveAndCleanData()
initialData = initialData[initialData['Style'] != 'Garden']
recentData = initialData[initialData['Sale_Date'] > '2016-01-01']
# recentData = recentData[recentData['Bedrooms'] == 3]

noGarage = recentData[recentData['Garage_1_Type'].isnull()]
withGarage = recentData[recentData['Garage_1_Type'].notnull()]

cds_MeanAll = cds_medianSalePriceOverTime(recentData)
cds_noGarage = cds_medianSalePriceOverTime(noGarage)
cds_withGarage = cds_medianSalePriceOverTime(withGarage)

cds_Raw = ColumnDataSource(recentData)

TOOLTIPS = [
    ('Address', '@Address'),
    ('Date', '$x'),
    ('Price', '@Sales_Price'),
    ('1st Size', '@Living_Area_1st_Floor_sq_ft'),
]

# build the figure
figure = figure(
    plot_height=400,
    plot_width=800,
    x_axis_type='datetime',
    x_axis_label='Sale Date',
    y_axis_label='Sales Price (x 1k)',
    tooltips=TOOLTIPS
    )
# add line
addLineToFigure(figure, cds_MeanAll, 'All', 'black')
# addDotsToFigure(figure, recentData, 'All', 'black')

addLineToFigure(figure, cds_noGarage, 'No G', 'blue')
addDotsToFigure(figure, noGarage, 'No G', 'blue')

addLineToFigure(figure, cds_withGarage, 'Has G', 'red')
addDotsToFigure(figure, withGarage, 'Has G', 'red')


# decide legend location
figure.legend.location = 'top_left'
range_slider = RangeSlider( 
    step=1, 
    title="Stuff")

# show figure
show(figure)
