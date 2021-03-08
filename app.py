import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import plotly.express as px
import pandas as pd

# This dataframe has 244 lines, but 4 distinct values for `day`
# the dataframe used 


## ======================================== Data Processing ===================================================
#df = px.data.tips()

# df not including components consumption
df_bom = pd.read_csv('bill_of_quantity.csv')
df_bom = df_bom[df_bom['ORDER_YEAR_MONTH']>='2019-01']
# df including components consumption
df_bom_2 = pd.read_csv('bill_of_quantity_2.csv')
df_bom_2 = df_bom_2[df_bom_2['ORDER_DATE']>='2019-01-01']
df_bom_2 = df_bom_2[['SALE_ORDER','CUSTOMER','INFINITI160610397','INFINITI160610323','INFINITI160610398','INFINITI160610399']]

pdt = df_bom['PDT_MODEL'].unique()
pdt = pdt.tolist()
pdt.append('ALL_MODEL')

cus_ls = df_bom_2['CUSTOMER'].unique()
cus_ls = cus_ls.tolist()
cus_ls.append('ALL_CUSTOMERS')

df_agg_date_price = df_bom[['ORDER_YEAR_MONTH','SALE_PRICE','PDT_MODEL']].groupby(['PDT_MODEL','ORDER_YEAR_MONTH']).sum().reset_index()
#df_agg_date_price = pd.DataFrame({'YEAR_MONTH':df_agg_date_price.index,'SALES':df_agg_date_price.values})
df_agg_date_length = df_bom[['ORDER_YEAR_MONTH','TOTAL_LENGTH','PDT_MODEL']].groupby(['PDT_MODEL','ORDER_YEAR_MONTH']).sum().reset_index()


df_agg_order_model = df_bom_2.groupby(['SALE_ORDER','CUSTOMER']).sum().reset_index()
modular_sum = {'SALES_ORDER':'IN TOTAL','CUSTOMER':'IN TOTAL',
            'INFINITI160610397':df_agg_order_model['INFINITI160610397'].sum(),
            'INFINITI160610323':df_agg_order_model['INFINITI160610323'].sum(),
            'INFINITI160610398':df_agg_order_model['INFINITI160610398'].sum(),
            'INFINITI160610399':df_agg_order_model['INFINITI160610399'].sum()
        }
df_modular_sum = pd.DataFrame(modular_sum,columns=['SALES_ORDER','CUSTOMER','INFINITI160610397','INFINITI160610323','INFINITI160610398','INFINITI160610399'],index=[0])

df_agg_customer_price = df_bom[['CUSTOMER','SALE_PRICE']].groupby(['CUSTOMER']).sum().reset_index()

# Highest Sales - Customer 
best_customer = df_agg_customer_price[df_agg_customer_price['SALE_PRICE'] == df_agg_customer_price['SALE_PRICE'].max()].CUSTOMER

# KPI Calculation
kpi_mc = df_bom['TOTAL_LENGTH'].sum()
kpi_tsales= df_bom['SALE_PRICE'].sum()
kpi_highsales_cus = df_agg_customer_price[df_agg_customer_price['SALE_PRICE'] == df_agg_customer_price['SALE_PRICE'].max()].CUSTOMER.values
kpi_highsales_price = df_agg_customer_price['SALE_PRICE'].max()

#  Tests
print(kpi_mc)
print(kpi_tsales)
print(kpi_highsales_price)
#print(df_modular_sum.head(1))
#print(df_bom.head(1))

## ========================================== App =================================================
app = dash.Dash(__name__)
server = app.server

## ========================================== Internel CSS =================================================
colors = {
        'background':'#111111',
        'text':'#7FDBFF'
}

app.layout = html.Div([
    
    # heading Module
    html.Div([
        # Pictures  

        # header 1 module
        html.Div([
            html.Img(src=app.get_asset_url('icons8-ceiling-light-64.png'),
                     id='head-image',
                     style={
                         "height": "60px",
                         "width": "auto",
                         "text-align": "center",
                         "margin-top": "15px",
                         "margin-right": "20px",
                         "margin-bottom": "10px",
                     },),  
            html.Div([
                html.H3(
                    'INFINITI LINEAR SYSTEM ',style={"margin-bottom": "-10px", 'color': 'black'}
                    ),
                html.H6(
                    'Material Comsumption Analysis',style={"margin-top": "0px", 'color': 'black'}
                    )
            ],className = 'main_greeting'),         

        ],
        className = 'one-half columns',id = 'title'
        #style={'width': '48%', 'display': 'inline-block'}
        ),

        #header 2 module 
        html.Div([
            html.A(
                html.Button(
                    'Learn More',
                    id = 'learnMore'
                ),
                href='',
                className= 'two columns'),
        ],
        className = 'one-third',id = 'title1'
        ),
    ],
    id ='header',
    className = 'row flex-display',
    style={"margin-bottom": "25px"}
    #style={'columnCount': 2}
    #style={'width': '60%', 'float': 'right', 'display': 'inline-block'}
    ),

     ## ========================================== KPI Cards =================================================       
    html.Div([
        html.Div([
            html.H6(
                'Report Summary: ',style={"margin-top": "-10px", 'color': 'black','font-weight':'bold'}
                ),
            html.P('The company encounters issues with materials purchasing overseas for our linear lighting system. The assembling parts need to be shipped from east Europe, which is estimated with three months lead time arriving in Australia. Management and engineering team are struggling to calculate the purchasing amount. This report will show management the insights regarding product model selection, mian-component selection, annual sales reports '
            ,style={'font-weight': 200,'fontSize': 20,'margin-top': '-10px','color': 'black'}),  
        ],
        className = 'summary_text',id = 'kpi_title'
        #style={'width': '48%', 'display': 'inline-block'}
        ),
    ],className='row flex-display',),

    # KPI Module Card
    html.Div([
        # KPI 1
        html.Div([
            html.Div([
                html.Div([
                    html.P('{0:,.0f}'.format(kpi_mc)+' M',style={'textAlign': 'center','font-weight': 200,'fontSize': 20,'margin-top': '20px','color': 'red'}),    
                    html.P(children = 'EXTRUSION ',style={'textAlign': 'center','color': 'black','fontSize': 15,'margin-top':'-10px'}),
                ],className  = 'card_text'),
                html.Img(src=app.get_asset_url('icons8-length-50.png'),
                            className='set_img',
                            style={
                                    "height": "60px",
                                    "width": "auto",
                                    "text-align": "center",
                                    "margin-top": "15px",
                                    "margin-right": "20px",
                                    "margin-bottom": "10px",
                                    'aria-hidden': True, 
                                    'margin-left': '-5px'}),
            ],className='row flex-display'),

        ],className = 'card_container three columns'),
        
        # KPI 2
        html.Div([
            html.Div([
                html.Div([
                    html.P('$ '+'{0:,.0f}'.format(kpi_tsales),style={'textAlign': 'center','font-weight': 200,'fontSize': 20,'margin-top': '20px','color': 'red'}),    
                    html.P(children = 'REVENUE',style={'textAlign': 'center','color': 'black','fontSize': 15,'margin-top':'-10px'}),
                ],className  = 'card_text'),
                html.Img(src=app.get_asset_url('icons8-dollar-coin-64.png'),
                            className='set_img',
                            style={
                                    "height": "60px",
                                    "width": "auto",
                                    "text-align": "center",
                                    "margin-top": "15px",
                                    "margin-right": "20px",
                                    "margin-bottom": "10px",
                                    'aria-hidden': True, 
                                    'margin-left': '-5px'}),                
            ],className = 'row flex-display'),           
        ],className = 'card_container three columns'),

        # KPI 3
        html.Div([
            html.Div([
                html.Div([
                    html.P('$ '+'{0:,.0f}'.format(kpi_highsales_price),style={'textAlign': 'center','font-weight': 200,'fontSize': 20,'margin-top': '20px','color': 'red'}),
                    html.P(f"{kpi_highsales_cus}",style={'textAlign': 'center','font-weight': 100,'fontSize': 10,'margin-top': '-10px','color': 'red'}),     
                    html.P(children = 'BEST SALES',style={'textAlign': 'center','color': 'black','fontSize': 15,'margin-top':'-10px'}),
                ],className  = 'card_text'),
                html.Img(src=app.get_asset_url('icons8-customer-insight-80.png'),
                            className='set_img',
                            style={
                                    "height": "60px",
                                    "width": "auto",
                                    "text-align": "center",
                                    "margin-top": "15px",
                                    "margin-right": "20px",
                                    "margin-bottom": "10px",
                                    'aria-hidden': True, 
                                    'margin-left': '-5px'}),                
            ],className = 'row flex-display'), 
  
        ],className = 'card_container three columns'),

    ],className = 'row flex-display',
    #style={'columnCount': 3}
    #style={"display": "flex","flex-direction": "column"}
    ),
    ## ========================================== Control Panel 1 =================================================
    ##html.Div([
        # Select Control 2


    ##],className = 'row flex-display'),
    
    ## ========================================== Chart & Control 1 Display =================================================  
    # the Pie Chart &
    html.Div([

        html.Div([
            ## --------------- Select Bar 1(By Customer) ------------------------
            html.Div([
                html.P("Select Customer:"),
                dcc.Dropdown(
                    id='cus_select', 
                    value='ALL_CUSTOMERS', 
                    options=[{'value': x, 'label': x} 
                            for x in cus_ls],
                    clearable=False
                ),
                html.P('Model Analysis and main-component modulars analysis charts reveal the material usage precentage/ratio. It could help percument department to make decisions on purchasing tasks'
                ,style={'font-weight': 200,'fontSize': 13,'margin-top': '15px','color': 'black'}), 
            ],className = 'control_container three columns',id = 'select-filter-options-2'),

            # The bar Chart - Model Comparison
            html.Div([
                dcc.Graph(
                    id="pie-chart",
                ),
            ],className = 'graph_container six columns'),
            
            # The bar Chart - Model Comparison
            html.Div([
                dcc.Graph(
                    id = "bar-chart-3",
                ), 
            ],className = 'graph_container six columns'),
            
        ],className = 'row flex-display'),

    ],className = 'chart_container_1'),
    ## ========================================== Control Panel 2 =================================================
    #html.Div([

    #],className = 'row flex-display'),

    ## ========================================== Chart Display 2 =================================================  

    html.Div([

        html.Div([
            ## --------------- Select Bar 2(By Product Model) ------------------------
            html.Div([
                html.P("Select Product Model:"),
                dcc.Dropdown(
                    id='product_type', 
                    value='INFINITI C80-S', 
                    options=[{'value': x, 'label': x} 
                            for x in pdt],
                    clearable=False
                ),
                html.P('Infiniti System contains models such as C80-S (Surface Mounted), C80-P (Pendant), C80-R (Recessed), From the bar chart diagram, We can observe the greatest sale happening in April and September'
                ,style={'font-weight': 200,'fontSize': 13,'margin-top': '15px','color': 'black'}),  
            ],className = 'control_container three columns',id = 'select-filter-options-1'),
            # The bar Chart - Sales VS Time
            html.Div([
                dcc.Graph(
                    id = "bar-chart-1",
                ),
            ],className = 'graph_container six columns'),

            # The bar Chart - Sales VS Length 
            html.Div([
                dcc.Graph(
                    id = "bar-chart-2",
                ),
            ],className = 'graph_container six columns'),

        ],className = 'row flex-display'),
    ],className = 'chart_container_2'),


],id= 'mainContainer')

## ========================================== Call Back Function =================================================

@app.callback(
    Output("pie-chart", "figure"), 
    [Input("cus_select", "value")],)

 #Input("values", "value")
def generate_pie_chart(cus_select):
    if cus_select == 'ALL_CUSTOMERS':
        fig_1 = px.pie(df_bom, values='SALE_PRICE', names='PDT_MODEL')
        return fig_1
    
    else:
        mask_df_1 = df_bom[df_bom['CUSTOMER']==cus_select]
        fig_1 = px.pie(mask_df_1, values='SALE_PRICE', names='PDT_MODEL')
        return fig_1

@app.callback(
    Output("bar-chart-1", "figure"), 
    [Input("product_type", "value")],)

def generate_bar_chart_1(product_type):

    if product_type =='ALL_MODEL':
        fig_bar_1 = go.Figure(data=[go.Bar(x=df_agg_date_price.ORDER_YEAR_MONTH, y=df_agg_date_price.SALE_PRICE)])
        fig_bar_1.update_traces(marker_color='rgb(255,165,0)', marker_line_color='rgb(8,48,107)',
                    marker_line_width=1, opacity=0.8)
        fig_bar_1.update_layout(title_text='From 2019 Jan - 2019 Dec Sales Report')
        return fig_bar_1
    else:
        mask_df = df_agg_date_price[df_agg_date_price['PDT_MODEL']==product_type]
        fig_bar_1 = go.Figure(data=[go.Bar(x=mask_df.ORDER_YEAR_MONTH, y=mask_df.SALE_PRICE)])
        fig_bar_1.update_traces(marker_color='rgb(255,165,0)', marker_line_color='rgb(8,48,107)',
                    marker_line_width=1, opacity=0.8)
        fig_bar_1.update_layout(title_text='From 2019 Jan - 2019 Dec Sales Report')
        return fig_bar_1

@app.callback(
    Output("bar-chart-2", "figure"), 
    [Input("product_type", "value")],)

def generate_bar_chart_2(product_type):
    if product_type =='ALL_MODEL':
        fig_bar_2 = go.Figure(data=[go.Bar(x=df_agg_date_length.ORDER_YEAR_MONTH, y=df_agg_date_length.TOTAL_LENGTH)])
        fig_bar_2.update_traces(marker_color='rgb(135,206,250)', marker_line_color='rgb(8,48,107)',
                    marker_line_width=1, opacity=0.8)
        fig_bar_2.update_layout(title_text='From 2019 Jan - 2019 Dec Sales Report')
        return fig_bar_2
    else:
        mask_df_2 = df_agg_date_length[df_agg_date_length['PDT_MODEL']==product_type]
        fig_bar_2 = go.Figure(data=[go.Bar(x=mask_df_2.ORDER_YEAR_MONTH, y=mask_df_2.TOTAL_LENGTH)])
        fig_bar_2.update_traces(marker_color='rgb(135,206,250)', marker_line_color='rgb(8,48,107)',
                    marker_line_width=1, opacity=0.8)
        fig_bar_2.update_layout(title_text='From 2019 Jan - 2019 Dec Material Comsumption')
        return fig_bar_2

@app.callback(
    Output("bar-chart-3", "figure"), 
    [Input("cus_select", "value")],)

def generate_bar_chart_3(cus_select):

    if cus_select == 'ALL_CUSTOMERS':
        fig_3 = go.Figure(data=[
            go.Bar(name = '2L Modular',x=df_modular_sum.CUSTOMER, y=df_modular_sum.INFINITI160610397),
            go.Bar(name = '4L Modular',x=df_modular_sum.CUSTOMER, y=df_modular_sum.INFINITI160610323),
            go.Bar(name = '5L Modular',x=df_modular_sum.CUSTOMER, y=df_modular_sum.INFINITI160610398),
            go.Bar(name = '6L Modular',x=df_modular_sum.CUSTOMER, y=df_modular_sum.INFINITI160610399)
        ])
        fig_3.update_traces(marker_line_width=2, opacity=0.8, marker_line_color='rgb(0,0,0)')
        fig_3.update_layout(title_text='Models Analysis')     
        return fig_3 
    
    else:
        mask_df_3 = df_agg_order_model[df_agg_order_model['CUSTOMER']==cus_select]
        fig_3 = go.Figure(data=[
            go.Bar(name = '2L Modular',x=mask_df_3.CUSTOMER, y=mask_df_3.INFINITI160610397),
            go.Bar(name = '4L Modular',x=mask_df_3.CUSTOMER, y=mask_df_3.INFINITI160610323),
            go.Bar(name = '5L Modular',x=mask_df_3.CUSTOMER, y=mask_df_3.INFINITI160610398),
            go.Bar(name = '6L Modular',x=mask_df_3.CUSTOMER, y=mask_df_3.INFINITI160610399)
        ])
        fig_3.update_traces(marker_line_width=2, opacity=0.8, marker_line_color='rgb(0,0,0)')
        fig_3.update_layout(title_text='Modular Analysis')
        return fig_3


# run server app
if __name__ == "__main__":
    app.run_server(debug=True)
