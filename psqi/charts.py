import plotly.graph_objs as go

def create_score_graph(evaluation_dates, scores):
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=evaluation_dates, 
        y=scores,
        mode='lines+markers',
        name='Pontuação global',
        line=dict(color='black'),
        marker=dict(size=6),
        hovertemplate= 
        '<b>Pontuação:</b> %{y}<extra></extra>'
    ))

    fig.update_layout(
        title={
            'text': 'Histórico de Avaliações',
            'font': {'size': 16, 'color': 'black'},
            'x': 0.5,
            'xanchor': 'center'
        },
        xaxis_title='Data',
        yaxis_title='Pontuação global',
        xaxis_tickformat='%d/%m/%Y', 
        plot_bgcolor='white',
        yaxis=dict(gridcolor='lightgrey', ),
        xaxis=dict(gridcolor='lightgrey'),
        autosize=True,
        hovermode='x unified',
    )

    fig.update_xaxes(type='date')

    fig.update_yaxes(
        tickmode='linear',
        tick0=0,
        dtick=1   
    )

    return fig.to_html(full_html=False)

