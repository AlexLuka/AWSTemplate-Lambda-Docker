import io
# import os
import numpy as np
import plotly.graph_objects as go


def make_plot():
    fig = go.Figure()

    # Plot 100 random data points
    fig.add_trace(
        go.Scatter(
            x=np.random.rand(100),
            y=np.random.rand(100),
            mode='markers',
            opacity=0.5,
            marker=dict(
                color='red',
                size=5
            )
        )
    )

    # Save chart as HTML to the attachments directory
    # fig.write_html(os.path.join(os.environ.get('LAMBDA_TASK_ROOT'), 'attachments', "plotly_chart3.html"))
    buffer = io.BytesIO()
    fig.write_image(buffer, format='png')
    buffer.seek(0)
    # fig.write_image(buffer, format="png")
    return buffer


if __name__ == "__main__":
    buf = make_plot()
    print(buf)
