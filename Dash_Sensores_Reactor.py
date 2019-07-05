import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import dash_daq as daq
import serial
import time
from collections import deque
import plotly.graph_objs as go
import numpy as np
import random
import socket

#external_scripts = ['https://cdnjs.cloudflare.com/ajax/libs/materialize/0.100.2/js/materialize.min.js']
#external_stylesheets = ['https://cdnjs.cloudflare.com/ajax/libs/materialize/0.100.2/css/materialize.min.css']

#app = dash.Dash(__name__,external_scripts=external_scripts, external_stylesheets=external_stylesheets)
app = dash.Dash()
server = app.server


#ARDUINO
#ser = serial.Serial('COM4', baudrate=9600,timeout=5)
#ser.flush()

##arduino = serial.Serial('/dev/ttyACM0', baudrate=9600, timeout=1.0)
##arduino.setDTR(False)
##arduino.flushInput()
##time.sleep(1)
##arduino.setDTR(True)


# MODO LOCAL

app.css.config.serve_locally=True
app.scripts.config.serve_locally=True



#TAMAÑO ARREGLOS

tamaño = 50
tiempo = deque(maxlen=tamaño)
tiempo.append(0)
Concentracion_H2 = deque(maxlen=tamaño)
Flujo_H2 = deque(maxlen=tamaño)
Presion_T = deque(maxlen=tamaño)
Generacion_V = deque(maxlen=tamaño)
Generacion_I = deque(maxlen=tamaño)
Generacion_P = deque(maxlen=tamaño)
Consumo_V = deque(maxlen=tamaño)
Consumo_I = deque(maxlen=tamaño)
Consumo_P = deque(maxlen=tamaño)


#DEFINICIONES


colores = {'fondo': '#FFFFFF','texto': '#111111'}#7FDBFF

variables_1 = {"Concentracion de hidrogeno":Concentracion_H2,
"Flujo de hidrogeno":Flujo_H2,
"Presion del tanque":Presion_T}

variables_2 = {"Generacion panel v": Generacion_V,
"Generacion panel i": Generacion_I,
"Generacion panel p": Generacion_P,}

variables_3 = {"Consumo reactor v":Consumo_V,
"Consumo reactor i":Consumo_I,
"Consumo reactor p":Consumo_P,}

unidades = {"Concentracion de hidrogeno":"%H2",
"Flujo de hidrogeno":"m3/s",
"Presion del tanque": "PSI [lbf/in2]",
"Generacion panel v": "Voltios[v]",
"Generacion panel i": "Amperios[i]",
"Generacion panel p": "Vatios[W]",
"Consumo reactor v": "Voltios[v]",
"Consumo reactor i": "Amperios[i]",
"Consumo reactor p": "Vatios[W]"}

relleno = {"Concentracion de hidrogeno":"#B7E4F6",
"Flujo de hidrogeno":"#C9C2FF",
"Presion del tanque": "#DADADA",
"Generacion panel v": "#FCDEB8",
"Generacion panel i": "#EFF6C3",
"Generacion panel p": "#F2B2B2",
"Consumo reactor v": "#FCDEB8",
"Consumo reactor i": "#EFF6C3",
"Consumo reactor p": "#F2B2B2"}

linea = {"Concentracion de hidrogeno":"#4C8DA8",
"Flujo de hidrogeno":"#4C4DA8",
"Presion del tanque": "#838383",
"Generacion panel v": "#A8804C",
"Generacion panel i": "#92A245",
"Generacion panel p": "#B64444",
"Consumo reactor v": "#A8804C",
"Consumo reactor i": "#92A245",
"Consumo reactor p": "#B64444"}

tabs_styles = {'height': '44px'}

tab_style = {'borderBottom': '1px solid #d6d6d6',
'padding': '6px','fontWeight': 'bold'}

tab_selected_style = {'borderTop': '1px solid #d6d6d6',
'borderBottom': '1px solid #d6d6d6',
'backgroundColor': '#119DFF',
'color': 'white',
'padding': '6px'}

grid = {0:'col s12 m6 l4', 1: 'col s12', 2: 'col s12 m6 l6', 3: 'col s12 m6 l4'}



#LECTURA DE DATOS


def datos_sensores(Concentracion_H2,Flujo_H2,Presion_T,Generacion_V,Generacion_I,Generacion_P,Consumo_V,Consumo_I,Consumo_P):

        #Recibir cadena de datos arduino
        #string_datos= ser.readline()
        #(H,F,G)= string_datos.decode().split(';')
        
        #Definir y truncar valores
        #CH ="{0:.1f}".format(float(H))
        #FH ="{0:.3f}".format(float(F))
        #GV =int(G)
        
        
        #Valores para grafica
        tiempo.append(tiempo[-1]+1)
        Concentracion_H2.append(random.randrange(0,20))
        Flujo_H2.append(5)
        Presion_T.append(tiempo[-1])
        Generacion_V.append(tiempo[-1])
        Generacion_I.append(10)
        Generacion_P.append(Generacion_V[-1]*Generacion_I[-1])
        Consumo_V.append(15)
        Consumo_I.append(random.randrange(0,12))
        Consumo_P.append(Consumo_V[-1]*Consumo_I[-1])
        

        return Concentracion_H2,Flujo_H2,Presion_T,Generacion_V,Generacion_I,Generacion_P,Consumo_V,Consumo_I,Consumo_P

Concentracion_H2,Flujo_H2,Presion_T,Generacion_V,Generacion_I,Generacion_P,Consumo_V,Consumo_I,Consumo_P = datos_sensores(Concentracion_H2,Flujo_H2,Presion_T,Generacion_V,Generacion_I,Generacion_P,Consumo_V,Consumo_I,Consumo_P)




#DISEÑO APLICACION 

app.layout = html.Div([

  dcc.Loading( id="loading-int",
  children=[html.Div([html.Div(id="loading-tab")])],
  fullscreen=True,
  type="cube"),
   dcc.Tabs(id="tabs",children=[
    

      ##TAB1
      
      dcc.Tab(value='tab-1',label='Almacenamiento H2',style=tab_style,selected_style=tab_selected_style,
              children=[
           html.Div([
                html.H3('Sensores Hidrogeno',
                style={'float': 'left','margin-bottom': '45px','margin-top': '25px',
                       'color': colores['texto']}),
                ]),

    daq.LEDDisplay(
        id='led1',
        label="Concentracion H2",
        labelPosition='bottom',
        backgroundColor=colores['fondo'],
        value=0,
        size=35,
        style={'position': 'relative','float': 'left','left': '20px',
               'height': '40px','margin-top': '10px','margin-bottom': '50px'} ),

    daq.LEDDisplay(
        id='led2',
        label="Flujo H2",
        labelPosition='bottom',
        backgroundColor=colores['fondo'],
        value=0,
        size=35,
        style={'position': 'relative','float': 'left','left': '40px',
               'height': '40px','margin-top': '10px','margin-bottom': '50px'} ),



    
     daq.LEDDisplay(
        id='led3',
        label="Presion T",
        labelPosition='bottom',
        backgroundColor=colores['fondo'],
        value=0,
        size=35,
        style={'position': 'relative','float': 'left','left': '60px',
               'height': '40px','margin-top':'10px','margin-bottom': '50px'}

        ),


   html.Div([ daq.GraduatedBar(
       id='tanque_bar',
       label="Tanque",
       labelPosition='top',
       size=200,
       step=2,
       color={"gradient":True,"ranges":{"green":[0,80],"yellow":[80,150],"red":[150,200]}},
       showCurrentValue=True,
       min=0,
       max=200,
       value=0,
       
       ),
        ],style = {'position': 'absolute','margin-left':'770px',
                 'margin-bottom':'15px',}),

  html.Div([html.Div(children='Zoom'),
        dcc.Slider(
        id='slider_1',
        min=0,
        max=20,
        step=5,
        value=0,
        updatemode='drag',
        marks={
              0: {'label': '0X'},
              5: {'label': '5X'},
              10: {'label': '10X'},
              15: {'label': '15X'},
              20: {'label': '20X'},
              }
        )],style = {'width': '200px','margin-left': '770px',
                 'margin-top':'55px','margin-bottom': '0px'}),

   daq.PowerButton(
        id='Inicio',
        color='#FF5E5E',
        label='Play/Stop',
        on=True,
        size=50,
        #className='btn-floating pulse',
        style = {'position': 'absolute','float': 'left','left':'1050px',
                     'margin-top':'-85px','margin-bottom': '10px'}),
           
  daq.Indicator(
        id='indicador',
        label="Control",
        value=False,
        style={'position': 'absolute','float': 'left','left': '1155px'
               ,'margin-top':'-85px'}
    ),
    html.Button(
        'On/Off',
        id='Control',
        n_clicks=0,
        style={'position': 'absolute','float': 'left','left': '1150px',
               'height': '30px','margin-top':'-30px','margin-bottom': '10px'}
        
    ),
           
    
    dcc.Dropdown(id='tipo_sensor_1',
                 options=[{'label': s, 'value': s}
                          for s in variables_1.keys()],
                 value=['Concentracion de hidrogeno','Flujo de hidrogeno','Presion del tanque'],
                 placeholder="Seleccionar sensor",
                 clearable=True,
                 multi=True,
                 style={'backgroundColor': colores['fondo']}
                 ),
           
    dcc.Loading(id="loading",
              children=[html.Div([html.Div(id="loading-output")])],
              type="default",
              #style={'display': 'none'}
              style={'position': 'absolute','float': 'left','left': '690px',
                      'margin-top':'-50px','margin-bottom': '10px'}
                ),


    
    html.Div(children=html.Div(id='graficas_1'), className='row', style={'backgroundColor': colores['fondo']}),
  
           
        dcc.Interval(
        id='actualizar_1',
        interval=1000,
        n_intervals=0,
        )

    ],className="container"),
      
      ##TAB 2

      dcc.Tab(value='tab-2',label='Generacion Panel',style=tab_style, selected_style=tab_selected_style,
              children=[
           html.Div([
                html.H2('Sensores Panel',
                style={'float': 'left','margin-bottom': '35px','margin-top': '10px',
                       'color': colores['texto']}),
                ]),


    daq.LEDDisplay(
        id='led4',
        label="Generacion V",
        labelPosition='bottom',
        backgroundColor=colores['fondo'],
        value=0,
        size=40,
        style={'position': 'relative','float': 'left','left': '20px',
               'height': '75px','margin-top':'10px','margin-bottom': '35px'}

        ),
    
     daq.LEDDisplay(
        id='led5',
        label="Generacion I",
        labelPosition='bottom',
        backgroundColor=colores['fondo'],
        value=0,
        size=40,
        style={'position': 'relative','float': 'left','left': '40px',
               'height': '75px','margin-top':'10px','margin-bottom': '35px'}

        ),
    
    daq.LEDDisplay(
        id='led6',
        label="Generacion P",
        labelPosition='bottom',
        backgroundColor=colores['fondo'],
        value=0,
        size=40,
        style={'position': 'relative','float': 'left','left': '60px',
               'height': '75px','margin-top':'10px','margin-bottom': '35px'}),
    
    
    dcc.Dropdown(id='tipo_sensor_2',
                 options=[{'label': s, 'value': s}
                          for s in variables_2.keys()],
                 value=['Generacion panel v','Generacion panel i','Generacion panel p'],
                 placeholder="Seleccionar sensor",
                 clearable=False,
                 multi=True,
                 style={'backgroundColor': colores['fondo']}
                 ),
           
   dcc.Loading( id="loading_2",
                 children=[html.Div([html.Div(id="loading-output-2")])],
                 type="dot",
                 style={'position': 'absolute','float': 'left','left': '1060px',
                 'margin-top':'-100px','margin-bottom': '30px'}
                 ),
    
    html.Div(html.Div(id='graficas_2'), className='row', style={'backgroundColor': colores['fondo']}),

      dcc.Interval(
        id='actualizar_2',
        interval=1*1000,
        n_intervals=0
        )
    

    ], className="container"),

     ##TAB 3

      dcc.Tab(value='tab-3',label='Consumo Reactor',style=tab_style, selected_style=tab_selected_style,
              children=[
           html.Div([
                html.H2('Sensores Reactor',
                style={'float': 'left','margin-bottom': '35px','margin-top': '10px',
                       'color': colores['texto']}),
                ]),


    daq.LEDDisplay(
        id='led7',
        label="Consumo V",
        labelPosition='bottom',
        backgroundColor=colores['fondo'],
        value=0,
        size=40,
        style={'position': 'relative','float': 'left','left': '20px',
               'height': '75px','margin-top':'10px','margin-bottom': '35px'}

        ),
    
     daq.LEDDisplay(
        id='led8',
        label="Consumo I",
        labelPosition='bottom',
        backgroundColor=colores['fondo'],
        value=0,
        size=40,
        style={'position': 'relative','float': 'left','left': '40px',
               'height': '75px','margin-top':'10px','margin-bottom': '35px'}

        ),
    
    daq.LEDDisplay(
        id='led9',
        label="Consumo P",
        labelPosition='bottom',
        backgroundColor=colores['fondo'],
        value=0,
        size=40,
        style={'position': 'relative','float': 'left','left': '60px',
               'height': '75px','margin-top':'10px','margin-bottom': '35px'}

        ),
    
    
    dcc.Dropdown(id='tipo_sensor_3',
                 options=[{'label': s, 'value': s}
                          for s in variables_3.keys()],
                 value=['Consumo reactor v','Consumo reactor i','Consumo reactor p'],
                 placeholder="Seleccionar sensor",
                 clearable=False,
                 multi=True,
                 style={'backgroundColor': colores['fondo']}
                 ),
                      
    dcc.Loading( id="loading_3",
                 children=[html.Div([html.Div(id="loading-output-3")])],
                 type="dot",
                 style={'position': 'absolute','float': 'left','left': '1060px',
                 'margin-top':'-100px','margin-bottom': '30px'}
                 ),
    
    html.Div(html.Div(id='graficas_3'), className='row', style={'backgroundColor': colores['fondo']}),

      dcc.Interval(
        id='actualizar_3',
        interval=1*1000,
        n_intervals=0
        )
    

    ], className="container")


  ],style=tabs_styles)
   

],style={'width':'97%','height':'100%','margin-left':10,'margin-right':10,'max-width':50000,
                                    'backgroundColor': colores['fondo']})


#ACTUALIZACION DE GRAFICAS Y FUNCIONES


@app.callback(
    [Output('led1', 'value'),
     Output('led2', 'value'),
     Output('led3', 'value')],
    [Input('actualizar_1', 'n_intervals')]) #Leds 1

def update_output(n):
    value=Concentracion_H2[-1]
    value1=Flujo_H2[-1]
    value2=Presion_T[-1]
    return str(value),str(value1),str(value2)

@app.callback(
    Output('actualizar_1', 'max_intervals'),
    [Input('Inicio', 'on')])
def update_output(on):
    if on is True:
       max_intervals=1000000000000
    else:
       max_intervals=0
    return max_intervals


@app.callback(
     Output('tanque_bar', 'value'),
    [Input('actualizar_1', 'n_intervals')]) #Tanque

def update_output(n):
    value=Presion_T[-1]
    return value

@app.callback(
     Output('indicador', 'value'),
    [Input('Control', 'n_clicks')] #Control
)
def update_output(value):
    if value % 2 is 0:
        value = True
    else: 
        value = False
    return value


@app.callback(
    [Output('led4', 'value'),
     Output('led5', 'value'),
     Output('led6', 'value')],
    [Input('actualizar_2', 'n_intervals')]) # Leds 2

def update_output(n):
    value3=Generacion_V[-1]
    value4=Generacion_I[-1]
    value5=Generacion_P[-1]
    return str(value3),str(value4),str(value5)

@app.callback(
    [Output('led7', 'value'),
     Output('led8', 'value'),
     Output('led9', 'value')],
    [Input('actualizar_3', 'n_intervals')]) #Leds 3

def update_output(n):
    value6=Consumo_V[-1]
    value7=Consumo_I[-1]
    value8=Consumo_P[-1]
    return str(value6),str(value7),str(value8)


@app.callback(
    Output('graficas_1','children'),
    [Input('tipo_sensor_1', 'value'),Input('slider_1', 'value'),Input('actualizar_1', 'n_intervals')])

def update_graph(data_names,zoom,n):
    graficas_1 = []
    datos_sensores(Concentracion_H2,Flujo_H2,Presion_T,Generacion_V,Generacion_I,Generacion_P,Consumo_V,Consumo_I,Consumo_P)
    for data_name in data_names:
        
        data = go.Scatter(
            x=list(tiempo),
            y=list(variables_1[data_name]),
            name='Datos',
            mode= 'markers',
            fill="tozeroy",
            marker=dict(color=(linea[data_name])),
            fillcolor=(relleno[data_name])
        
            )
 
        
        graficas_1.insert(0,html.Div(dcc.Graph(
            id=data_name,
            animate=True,
            figure={'data': [data],'layout' : go.Layout(paper_bgcolor=colores['fondo'],
                                                        plot_bgcolor='rgba(0,0,0,0)',
                                                        font={'color': colores['texto']},
                                                        uirevision=True,
                                                        autosize=True,
                                                        #transition={'duration': 500,'easing': 'cubic-in-out'},
                                                        xaxis=dict(range=[min(tiempo)+zoom,max(tiempo)-zoom],title='Tiempo [s]', ticklen= 3,autorange=False, zeroline=False, gridwidth= 1),
                                                        yaxis=dict(range=[min(variables_1[data_name]),max(variables_1[data_name])],autorange=False,title=(unidades[data_name]),ticklen= 5, gridwidth= 2),
                                                        margin={'l':50,'r':10,'t':80,'b':40},
                                                        title='{}'.format(data_name))}
                                                        
         
            ),className=grid[len(data_names)]))

    #graficas_1.reverse()

    return graficas_1

@app.callback(Output("loading-output", "children"), [Input("tipo_sensor_1", "value")])
def delay(value):
    time.sleep(0.3)
    return None


@app.callback(
     Output('graficas_2','children'),
    [Input('tipo_sensor_2', 'value'),Input('actualizar_2', 'n_intervals')])

def update_graph(data_names,n):
    graficas_2 = []
    graficas_2.clear()
    datos_sensores(Concentracion_H2,Flujo_H2,Presion_T,Generacion_V,Generacion_I,Generacion_P,Consumo_V,Consumo_I,Consumo_P)
    
    for data_name in data_names:
        
        data = go.Scatter(
            x=list(tiempo),
            y=list(variables_2[data_name]),
            name='Datos',
            mode= 'lines',
            fill="tozeroy",
            marker=dict(color=(linea[data_name])),
            fillcolor=(relleno[data_name])
        
            )
        
        
        graficas_2.insert(0,html.Div(dcc.Graph(
            id=data_name,
            animate=True,
            figure={'data': [data],'layout' : go.Layout(paper_bgcolor=colores['fondo'],
                                                        plot_bgcolor='rgba(0,0,0,0)',
                                                        font={'color': colores['texto']},
                                                        uirevision=True,
                                                        autosize=True,
                                                        transition={'duration': 500,'easing': 'cubic-in-out'},
                                                        xaxis=dict(range=[min(tiempo),max(tiempo)],title='Tiempo [s]', ticklen= 3,autorange=False, zeroline=False, gridwidth= 1),
                                                        yaxis=dict(range=[min(variables_2[data_name]),max(variables_2[data_name])],autorange=False,title=(unidades[data_name]),ticklen= 5, gridwidth= 2),
                                                        margin={'l':50,'r':10,'t':100,'b':40},
                                                        title='{}'.format(data_name))}
                                                        
         
            ),className=grid[len(data_names)]))
    

    return graficas_2

@app.callback(Output("loading-output-2", "children"), [Input("tipo_sensor_2", "value")])
def delay(value):
    time.sleep(0.3)
    return None


@app.callback(
     Output('graficas_3','children'),
    [Input('tipo_sensor_3', 'value'),Input('actualizar_3', 'n_intervals')])

def update_graph(data_names,n):
    graficas_3 = []
    graficas_3.clear()
    datos_sensores(Concentracion_H2,Flujo_H2,Presion_T,Generacion_V,Generacion_I,Generacion_P,Consumo_V,Consumo_I,Consumo_P)
          
    for data_name in data_names:
        
        data = go.Scatter(
            x=list(tiempo),
            y=list(variables_3[data_name]),
            name='Datos',
            mode= 'lines+markers',
            fill="tozeroy",
            marker=dict(color=(linea[data_name])),
            fillcolor=(relleno[data_name])
        
            )
        
        
        graficas_3.insert(0,html.Div(dcc.Graph(
            id=data_name,
            animate=True,
            figure={'data': [data],'layout' : go.Layout(paper_bgcolor=colores['fondo'],
                                                        plot_bgcolor='rgba(0,0,0,0)',
                                                        font={'color': colores['texto']},
                                                        uirevision=True,
                                                        autosize=True,
                                                        transition={'duration': 500,'easing': 'cubic-in-out'},
                                                        xaxis=dict(range=[min(tiempo),max(tiempo)],title='Tiempo [s]', ticklen= 3, autorange=False,zeroline=False, gridwidth= 1),
                                                        yaxis=dict(range=[min(variables_3[data_name]),max(variables_3[data_name])],autorange=False,title=(unidades[data_name]),ticklen= 5, gridwidth= 2),
                                                        margin={'l':50,'r':10,'t':100,'b':40},
                                                        title='{}'.format(data_name))}
                                                        
         
            ),className=grid[len(data_names)]))


    return graficas_3


@app.callback(Output("loading-output-3", "children"), [Input("tipo_sensor_3", "value")])
def delay(value):
    time.sleep(0.3)
    return None

@app.callback(
        [Output("loading-tab", "children"),Output("loading-int", "type")], [Input("tabs", "value")])
def delay(tab):
    type='graph'
    time.sleep(0.5)        
    return None,type


#host = socket.gethostbyname(socket.gethostname())

if __name__ == '__main__':
    app.run_server(debug=True, use_reloader=True) ##host=host
