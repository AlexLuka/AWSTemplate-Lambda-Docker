import io
# import os
import numpy as np
import plotly.graph_objects as go
import matplotlib.pyplot as plt


def make_plot():
    fig = go.Figure()

    # Plot 100 random data points
    n = 100
    fig.add_trace(
        go.Scatter(
            x=np.random.rand(n),
            y=np.random.rand(n),
            mode='markers',
            opacity=0.5,
            marker=dict(
                color='red',
                size=np.random.rand(n) * 25
            )
        )
    )
    # fig.show()

    # Save image to a buffer
    #   This one fails in Lambda for some reason. Need more detailed debugging!
    buffer = io.BytesIO()
    fig.write_image(buffer, format='webp')
    buffer.seek(0)
    # fig.write_image(buffer, format="png")
    return buffer


def make_plot_mpl():

    fig, ax = plt.subplots(figsize=(10, 8))

    n = 100
    ax.scatter(
        x=np.random.rand(n),
        y=np.random.rand(n),
        s=np.random.rand(n) * 50,
        c='red'
    )

    # plt.show()

    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    return buffer


if __name__ == "__main__":
    # buf = make_plot()
    # buf.seek(0)
    # print(buf)

    buf = make_plot_mpl()
    buf.seek(0)
    print(buf)
