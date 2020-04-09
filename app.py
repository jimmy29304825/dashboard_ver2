import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import dash_daq as daq
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import datetime

themeColor = px.colors.sequential.PuRd

def get_numbers(df_yesterday):
    visits = {
        'YC': {
            'all': df_yesterday[df_yesterday['訪問網站'] == '房仲網']['訪問人次'].sum(),
            'member': df_yesterday[df_yesterday['訪問網站'] == '房仲網'][df_yesterday['是否為會員'] == '會員']['訪問人次'].sum(),
            'userid': df_yesterday[df_yesterday['訪問網站'] == '房仲網'][df_yesterday['是否為會員'] == '非會員']['訪問人次'].sum(),
            'unique': df_yesterday[df_yesterday['訪問網站'] == '房仲網'][df_yesterday['是否為會員'] == '會員']['訪問用戶'].sum(),
        }, 
        'HF': {
            'all': df_yesterday[df_yesterday['訪問網站'] == '好房網']['訪問人次'].sum(),     
            'member': df_yesterday[df_yesterday['訪問網站'] == '好房網'][df_yesterday['是否為會員'] == '會員']['訪問人次'].sum(),
            'userid': df_yesterday[df_yesterday['訪問網站'] == '好房網'][df_yesterday['是否為會員'] == '非會員']['訪問人次'].sum(),
            'unique': df_yesterday[df_yesterday['訪問網站'] == '好房網'][df_yesterday['是否為會員'] == '會員']['訪問用戶'].sum(),
        }
    }
    return visits['YC']['all']+visits['HF']['all'], visits['YC']['all'], visits['HF']['all'], visits['YC']['member']+visits['HF']['member'], visits['YC']['member'], visits['HF']['member'], visits['YC']['userid']+visits['HF']['userid'], visits['YC']['userid'], visits['HF']['userid'], visits['YC']['unique']+visits['HF']['unique'], visits['YC']['unique'], visits['HF']['unique']

def draw_fig_time_YC(df_yesterday):
    # YC time plot
    df_yesterday_time_YC = df_yesterday[df_yesterday['訪問網站'] == '房仲網'].groupby('使用裝置').sum()
    df_yesterday_time_YC = df_yesterday_time_YC.iloc[:, [i for i in range(2, 26)]].reset_index()
    df_yesterday_time_YC = df_yesterday_time_YC.melt(id_vars=["使用裝置"], var_name="時段", value_name="訪問人次")
    fig_time_YC = px.bar(df_yesterday_time_YC, x="時段", y="訪問人次", color='使用裝置', barmode='group')
    fig_time_YC.update_layout(
        font_size=18, 
        font_family='Microsoft JhengHei', 
        font_color='white',
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        
        legend=dict(x=0, y=1.1, bgcolor='rgba(255,255,255,0)', bordercolor='rgba(255,255,255,0)', orientation='h'),
    )
    return fig_time_YC


def draw_fig_time_HF(df_yesterday):
    # HF time plot
    df_yesterday_time_HF = df_yesterday[df_yesterday['訪問網站'] == '好房網'].groupby('使用裝置').sum()
    df_yesterday_time_HF = df_yesterday_time_HF.iloc[:, [i for i in range(2, 26)]].reset_index()
    df_yesterday_time_HF = df_yesterday_time_HF.melt(id_vars=["使用裝置"], var_name="時段", value_name="訪問人次")
    fig_time_HF = px.bar(df_yesterday_time_HF, x="時段", y="訪問人次", color='使用裝置', barmode='group')
    fig_time_HF.update_layout(
        font_size=18, 
        font_family='Microsoft JhengHei', 
        font_color='white',
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        legend=dict(x=0, y=1.1, bgcolor='rgba(255,255,255,0)', bordercolor='rgba(255,255,255,0)', orientation='h'),
    )
    return fig_time_HF


def draw_fig_referer(df_yesterday):
    # sunburst for referer
    df_yesterday_referer = df_yesterday.iloc[:, [1,4,5]].groupby(['訪問網站', '訪問來源']).sum().reset_index()
    fig_referer = px.sunburst(df_yesterday_referer, 
                      path=['訪問網站', '訪問來源'],  # 分類變數
                      values='訪問人次',  # 面積依據資料
                      color='訪問網站',  # 分色變數
#                       hover_data=['訪問網站'],  # 游標顯示資料
                     )
    fig_referer.update_traces(
        marker=dict(
#             colors=themeColor,
            line=dict(color='#ffffff', width=2)
        )
    )
    fig_referer.update_layout(
        margin=dict(l=10, r=10, t=10, b=10),  # 圖形在畫布的邊界設定
        paper_bgcolor="rgba(0,0,0,0)",   # 畫布背景顏色
        plot_bgcolor="rgba(0,0,0,0)",  # 圖形背景顏色
        autosize=True,  # 自動調整大小
        font_color='white',  # 文字顏色
        font_size=20,  # 文字大小
        font_family='Microsoft JhengHei',  # 字體
    )
    return fig_referer


def draw_fig_ad(df_yesterday):
    # sunburst for ad click
    df_yesterday_ad = df_yesterday.iloc[:, [1, -2,-1]].groupby('訪問網站').sum().reset_index().melt(id_vars=["訪問網站"], 
                                                          var_name="行為", 
                                                          value_name="人次")
    fig_ad = px.sunburst(df_yesterday_ad, 
                      path=['訪問網站', '行為'],  # 分類變數
                      values='人次',  # 面積依據資料
                      color='訪問網站',  # 分色變數
#                       hover_data=['訪問網站'],  # 游標顯示資料
                     )
    fig_ad.update_traces(
        marker=dict(
#             colors=themeColor, 
            line=dict(color='#ffffff', width=2)
        )
    )
    fig_ad.update_layout(
        margin=dict(l=10, r=10, t=10, b=10),  # 圖形在畫布的邊界設定
        paper_bgcolor="rgba(0,0,0,0)",   # 畫布背景顏色
        plot_bgcolor="rgba(0,0,0,0)",  # 圖形背景顏色
        autosize=True,  # 自動調整大小
        font_color='white',  # 文字顏色
        font_size=20,  # 文字大小
        font_family='Microsoft JhengHei',  # 字體
    )
    return fig_ad


def draw_fig_function_YC(df_yesterday):
    # barplot for function YC
    df_yesterday_function_YC = df_yesterday[df_yesterday['訪問網站'] == '房仲網'].iloc[:, [1,2,33,35,37,38,40,41]].groupby(['訪問網站', '使用裝置']).sum().reset_index()
    df_yesterday_function_YC = df_yesterday_function_YC.melt(id_vars=['訪問網站', '使用裝置'], var_name="功能", value_name="人次")
    df_yesterday_function_YC = df_yesterday_function_YC.sort_values(by=['人次','訪問網站', '使用裝置', '功能'], ascending=True).reset_index(drop=True)

    fig_function_YC = go.Figure()
    fig_function_YC.add_trace(go.Bar(
        y=df_yesterday_function_YC['功能'].unique(),
        x=df_yesterday_function_YC[df_yesterday_function_YC['使用裝置'] == 'Web版']['人次'],
        name='Web版',
        orientation='h',
        marker=dict(
            color="#00cc96",
            line=dict(color='white', width=1)
        )
    ))
    fig_function_YC.add_trace(go.Bar(
        y=df_yesterday_function_YC['功能'].unique(),
        x=df_yesterday_function_YC[df_yesterday_function_YC['使用裝置'] == '手機M版']['人次'],
        name='手機M版',
        orientation='h',
        marker=dict(
            color="#ef553b",
            line=dict(color='white', width=1)
        )
    ))
    fig_function_YC.add_trace(go.Bar(
        y=df_yesterday_function_YC['功能'].unique(),
        x=df_yesterday_function_YC[df_yesterday_function_YC['使用裝置'] == 'App']['人次'],
        name='App',
        orientation='h',
        marker=dict(
            color="#636dfa",
            line=dict(color='white', width=1)
        )
    ))
    fig_function_YC.update_layout(
        barmode='stack', 
        height=1000, 
        legend=dict(x=0, y=1.05, bgcolor='rgba(255,255,255,0)', bordercolor='rgba(255,255,255,0)', orientation='h'), 
        font_size=18, 
        font_color='white', 
        font_family='Microsoft JhengHei',
        paper_bgcolor="rgba(0,0,0,0)", 
        plot_bgcolor="rgba(0,0,0,0)"
    )
    return fig_function_YC


def draw_fig_function_HF(df_yesterday):
    # barplot for function HF
    df_yesterday_function_HF = df_yesterday[df_yesterday['訪問網站'] == '好房網'].iloc[:, [1,2,33,35,37,38,41,43,45]].groupby(['訪問網站', '使用裝置']).sum().reset_index()
    df_yesterday_function_HF = df_yesterday_function_HF.melt(id_vars=['訪問網站', '使用裝置'], var_name="功能", value_name="人次")
    df_yesterday_function_HF = df_yesterday_function_HF.sort_values(by=['人次','訪問網站', '使用裝置', '功能'], ascending=True).reset_index(drop=True)

    fig_function_HF = go.Figure()
    fig_function_HF.add_trace(go.Bar(
        y=df_yesterday_function_HF['功能'].unique(),
        x=df_yesterday_function_HF[df_yesterday_function_HF['使用裝置'] == 'Web版']['人次'],
        name='Web版',
        orientation='h',
        marker=dict(
            color="#00cc96",
            line=dict(color='white', width=1)
        )
    ))
    fig_function_HF.add_trace(go.Bar(
        y=df_yesterday_function_HF['功能'].unique(),
        x=df_yesterday_function_HF[df_yesterday_function_HF['使用裝置'] == '手機M版']['人次'],
        name='手機M版',
        orientation='h',
        marker=dict(
            color="#ef553b",
            line=dict(color='white', width=1)
        )
    ))
    fig_function_HF.add_trace(go.Bar(
        y=df_yesterday_function_HF['功能'].unique(),
        x=df_yesterday_function_HF[df_yesterday_function_HF['使用裝置'] == 'App']['人次'],
        name='App',
        orientation='h',
        marker=dict(
            color="#636dfa",
            line=dict(color='white', width=1)
        )
    ))
    
    fig_function_HF.update_layout(
        barmode='stack', 
        height=1000, 
        legend=dict(x=0, y=1.05, bgcolor='rgba(255,255,255,0)', bordercolor='rgba(255,255,255,0)', orientation='h'), 
        font_size=18, 
        font_color='white', 
        font_family='Microsoft JhengHei',
        paper_bgcolor="rgba(0,0,0,0)", 
        plot_bgcolor="rgba(0,0,0,0)"
    )
    return fig_function_HF


def draw_fig_timeSeries_YC(df_timeSeries):
    df_timeSeries_YC = df_timeSeries[df_timeSeries['訪問網站'] == '房仲網'].groupby(['訪問日期', '使用裝置']).sum().reset_index().iloc[:, [0,1,2]]
    df_timeSeries_YC_app = df_timeSeries_YC[df_timeSeries_YC['使用裝置'] == 'App']
    df_timeSeries_YC_MobilePhone = df_timeSeries_YC[df_timeSeries_YC['使用裝置'] == '手機M版']
    df_timeSeries_YC_Desktop = df_timeSeries_YC[df_timeSeries_YC['使用裝置'] == 'Web版']
    fig_timeSeries_YC = go.Figure()
    fig_timeSeries_YC.add_trace(go.Scatter(x=df_timeSeries_YC_app['訪問日期'], y=df_timeSeries_YC_app['訪問人次'],
                        mode='lines+markers',
                        name='App'))
    fig_timeSeries_YC.add_trace(go.Scatter(x=df_timeSeries_YC_MobilePhone['訪問日期'], y=df_timeSeries_YC_MobilePhone['訪問人次'],
                        mode='lines+markers',
                        name='手機M版'))
    fig_timeSeries_YC.add_trace(go.Scatter(x=df_timeSeries_YC_Desktop['訪問日期'], y=df_timeSeries_YC_Desktop['訪問人次'],
                        mode='lines+markers',
                        name='Web版'))
    fig_timeSeries_YC.update_layout(
        font_size=18, 
        font_family='Microsoft JhengHei', 
        font_color='white', 
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        legend=dict(x=0, y=1.2, bgcolor='rgba(255,255,255,0)', bordercolor='rgba(255,255,255,0)', orientation='h'),
    )
    return fig_timeSeries_YC


def draw_fig_timeSeries_HF(df_timeSeries):
    df_timeSeries_HF = df_timeSeries[df_timeSeries['訪問網站'] == '好房網'].groupby(['訪問日期', '使用裝置']).sum().reset_index().iloc[:, [0,1,2]]
    df_timeSeries_HF_app = df_timeSeries_HF[df_timeSeries_HF['使用裝置'] == 'App']
    df_timeSeries_HF_MobilePhone = df_timeSeries_HF[df_timeSeries_HF['使用裝置'] == '手機M版']
    df_timeSeries_HF_Desktop = df_timeSeries_HF[df_timeSeries_HF['使用裝置'] == 'Web版']
    fig_timeSeries_HF = go.Figure()
    fig_timeSeries_HF.add_trace(go.Scatter(x=df_timeSeries_HF_app['訪問日期'], y=df_timeSeries_HF_app['訪問人次'],
                        mode='lines+markers',
                        name='App'))
    fig_timeSeries_HF.add_trace(go.Scatter(x=df_timeSeries_HF_MobilePhone['訪問日期'], y=df_timeSeries_HF_MobilePhone['訪問人次'],
                        mode='lines+markers',
                        name='手機M版'))
    fig_timeSeries_HF.add_trace(go.Scatter(x=df_timeSeries_HF_Desktop['訪問日期'], y=df_timeSeries_HF_Desktop['訪問人次'],
                        mode='lines+markers',
                        name='Web版'))
    fig_timeSeries_HF.update_layout(
        font_size=18, 
        font_family='Microsoft JhengHei', 
        font_color='white', 
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        legend=dict(x=0, y=1.2, bgcolor='rgba(255,255,255,0)', bordercolor='rgba(255,255,255,0)', orientation='h'),
    )
    return fig_timeSeries_HF


# local資料使用    
df = pd.read_csv(
    './matomo_new.csv'
)  # 讀取資料
df['訪問日期'] = pd.to_datetime(
    df['訪問日期']
)  # 轉換日期格式

maxdate = datetime.datetime.fromtimestamp(
    datetime.datetime.timestamp(
        df['訪問日期'].max()
    )
)
mindate = datetime.datetime.fromtimestamp(
    datetime.datetime.timestamp(
        df['訪問日期'].min()
    )
)

app = dash.Dash(
    __name__
)
app.layout = html.Div(
    id="big-app-container",
    children=[
        html.H1(
            id="header",
            children='''Matomo 線上用戶行為儀表板''', 
        ),  
        html.Div(
            id='version',
            children='''ver 1.0''', 
        ),  
        html.Div(
            id="time_range_title", 
            children='''選擇時間區間：''', 
        ),  
        dcc.DatePickerSingle(
            id='time_range',
            min_date_allowed=mindate,
            max_date_allowed=maxdate,
            initial_visible_month=maxdate,
            date=str(maxdate.date()),
            style=dict(bgcolor='blue')
        ),
        html.Br(),
        html.Div(
            id="numbers_data",
            className="row",
            children=[
                html.Div(
                    id="site",
                    children=[
                        html.Br(),
                        html.H5(
                            "網站"
                        ),
                        html.Br(),
                        html.H6(
                            id="total",
                            className="banner_title",
                            children='總計',
                       ),
                        html.Br(),
                        html.H6(
                            id="yc",
                            className="banner_yc",
                            children='房仲網',
                        ),
                        html.Br(),
                        html.H6(
                            id="hf",
                            className="banner_hf",
                            children='好房網',
                        ),
                    ],
                ),
                html.Div(
                    id="sum",
                    children=[
                        html.Br(),
                        html.H5(
                            "瀏覽人次"
                        ),
                        html.Br(),
                        html.H6(
                            id="total_sum",
                            className="banner_title",
                            children='99999',
                        ),
                        html.Br(),
                        html.H6(
                            id="yc_sum",
                            className="banner_yc",
                            children='99999',
                        ),
                        html.Br(),
                        html.H6(
                            id="hf_sum",
                            className="banner_hf",
                            children='99999',
                        ),
                    ],
                ),
                html.Div(
                    id="member",
                    children=[
                        html.Br(),
                        html.H5(
                            "會員瀏覽人次"
                        ),
                        html.Br(),
                        html.H6(
                            id="total_member",
                            className="banner_title",
                            children='666666',
                        ),
                        html.Br(),
                        html.H6(
                            id="yc_member",
                            className="banner_yc",
                            children='66666',
                        ),
                        html.Br(),
                        html.H6(
                            id="hf_member",
                            className="banner_hf",
                            children='66666',
                        ),
                    ],
                ),
                html.Div(
                    id="userid",
                    children=[
                        html.Br(),
                        html.H5(
                            "非會員瀏覽人次"
                        ),
                        html.Br(),
                        html.H6(
                            id="total_userid",
                            className="banner_title",
                            children='33333',
                        ),
                        html.Br(),
                        html.H6(
                            id="yc_userid",
                            className="banner_yc",
                            children='33333',
                        ),
                        html.Br(),
                        html.H6(
                            id="hf_userid",
                            className="banner_hf",
                            children='33333',
                        ),
                    ],
                ),
                html.Div(
                    id="unique",
                    children=[
                        html.Br(),
                        html.H5(
                            "訪問會員人數"
                        ),
                        html.Br(),
                        html.H6(
                            id="total_unique",
                            className="banner_title",
                            children='11111',
                        ),
                        html.Br(),
                        html.H6(
                            id="yc_unique",
                            className="banner_yc",
                            children='11111',
                        ),
                        html.Br(),
                        html.H6(
                            id="hf_unique",
                            className="banner_hf",
                            children='11111',
                        ),
                    ],
                ),
            ]
        ),
        html.Div(
            id='date_and_days',
            children=[
                html.H2(
                    id='date_and_days_title',
                    children='''近期瀏覽量趨勢''', 
                    className="section-banner"
                ),
                dcc.RadioItems(
                    id='days_picker',
                    options=[
                        {
                            'label': '過去30天', 
                            'value': '30'
                        },
                        {
                            'label': '過去一年', 
                            'value': '365'
                        },
                    ],
                    value='30',
                    labelStyle={
                        'display': 'inline-block'
                    }
                ),
                dcc.Graph(
                    id="time_series_graph_yc",
                    className='graph',
                ),
                dcc.Graph(
                    id="time_series_graph_hf",
                    className='graph',
                ),
            ]
        ),
        html.Br(),
        html.Br(),
        html.Div(
            id='graph_area',
            children=[
                html.Div(
                    id="graph_left_top",
                    children=[
                        html.H2(
                            children='''圖1''', 
                            className="section-banner"
                        ),  
                        dcc.Graph(
                            id="graph1",
                            className='graph',
                        ),
                    ],
                ),
                html.Div(
                    id="graph_right_top",
                    children=[
                        html.H2(
                            children='''圖2''', 
                            className="section-banner"
                        ),  
                        dcc.Graph(
                            id="graph2",
                            className='graph',
                        ),
                    ],
                ),
                html.Div(
                    id="graph_left_bottom",
                    children=[
                        html.H2(
                            children='''圖3''', 
                            className="section-banner"
                        ),  
                        dcc.Graph(
                            id="graph3",
                            className='graph',
                        ),
                    ],
                ),
                html.Div(
                    id="graph_right_bottom",
                    children=[
                        html.H2(
                            children='''圖4''', 
                            className="section-banner"
                        ),  
                        dcc.Graph(
                            id="graph4",
                            className='graph',                           
                        ),
                    ],
                ),
            ]
        ),
        html.Div(
            id='function_area',
            children=[
                html.Div(
                    id="function_yc",
                    children=[
                        html.H2(
                            children='''圖1''', 
                            className="section-banner"
                        ),  
                        dcc.Graph(
                            id="function_yc_graph",
                            className='graph',
                        ),
                    ],
                ),
                html.Div(
                    id="function_hf",
                    children=[
                        html.H2(
                            children='''圖2''', 
                            className="section-banner"
                        ),  
                        dcc.Graph(
                            id="function_hf_graph",
                            className='graph',
                        ),
                    ],
                ),
            ]
        ),
    ]
)


# 指定日期數據呈現
@app.callback(
    [
        dash.dependencies.Output('total_sum', 'children'),
        dash.dependencies.Output('yc_sum', 'children'),
        dash.dependencies.Output('hf_sum', 'children'),
        
        dash.dependencies.Output('total_member', 'children'),
        dash.dependencies.Output('yc_member', 'children'),
        dash.dependencies.Output('hf_member', 'children'),
        
        dash.dependencies.Output('total_userid', 'children'),
        dash.dependencies.Output('yc_userid', 'children'),
        dash.dependencies.Output('hf_userid', 'children'),
        
        dash.dependencies.Output('total_unique', 'children'),
        dash.dependencies.Output('yc_unique', 'children'),
        dash.dependencies.Output('hf_unique', 'children'),
        
        dash.dependencies.Output('graph1', 'figure'),
        dash.dependencies.Output('graph2', 'figure'),
        dash.dependencies.Output('graph3', 'figure'),
        dash.dependencies.Output('graph4', 'figure'),
        
        dash.dependencies.Output('function_yc_graph', 'figure'),
        dash.dependencies.Output('function_hf_graph', 'figure'),
    ],
    [dash.dependencies.Input('time_range', 'date')]
)
def select_date(date):
    df_yesterday = df.query("訪問日期 == '%s'" % pd.Timestamp(date))
    total_sum, yc_sum, hf_sum, total_member, yc_member, hf_member, total_userid, yc_userid, hf_userid, total_unique, yc_unique, hf_unique = get_numbers(df_yesterday)
    graph1 = draw_fig_time_YC(df_yesterday)
    graph2 = draw_fig_time_HF(df_yesterday)
    graph3 = draw_fig_referer(df_yesterday)
    graph4 = draw_fig_ad(df_yesterday)
    function_yc_graph = draw_fig_function_YC(df_yesterday)
    function_hf_graph = draw_fig_function_HF(df_yesterday)
    return total_sum, yc_sum, hf_sum, total_member, yc_member, hf_member, total_userid, yc_userid, hf_userid, total_unique, yc_unique, hf_unique, graph1, graph2, graph3, graph4, function_yc_graph, function_hf_graph
 

# 趨勢圖資料
@app.callback(
    [
        dash.dependencies.Output('time_series_graph_yc', 'figure'),
        dash.dependencies.Output('time_series_graph_hf', 'figure'),
    ],
    [
        dash.dependencies.Input('time_range', 'date'),
        dash.dependencies.Input('days_picker', 'value'),
    ]
)
def select_date_and_days(date, days):
    date_max = pd.Timestamp(date)
    date_min = pd.Timestamp(date) - datetime.timedelta(days=int(days))
    df_timeSeries = df.query("訪問日期 <= '%s' and 訪問日期 >= '%s'" % (date_max, date_min))
    
    fig_timeSeries_HF = draw_fig_timeSeries_HF(df_timeSeries)
    fig_timeSeries_YC = draw_fig_timeSeries_YC(df_timeSeries)
   
    return fig_timeSeries_YC, fig_timeSeries_HF

   
if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port=8050, debug=True)