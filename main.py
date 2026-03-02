import math
from collections import deque

from textual.app import App, ComposeResult
from textual.containers import Vertical
from textual.widgets import Static
from textual_plotext import PlotextPlot


class MarketApp(App):

    BINDINGS = [
        ("1", "show_view1", "Show Single Plot View"),
        ("2", "show_view2", "Show Double Plot View"),
    ]

    def compose(self) -> ComposeResult:
        # --- Single plot view ---
        self.single_plot = PlotextPlot()
        self.single_plot.display = True  # visible initially

        # --- Double plot view ---
        self.double_plot1 = PlotextPlot()
        self.double_plot2 = PlotextPlot()

        # Stack the two double plots vertically
        self.double_container = Vertical(self.double_plot1, self.double_plot2)
        self.double_container.display = False

        # Yield all views to the UI (visibility controlled by display)
        yield self.single_plot
        yield self.double_container

        # Data for updating
        self.t = 0
        self.data_single = deque(maxlen=200)
        self.data_single2 = deque(maxlen=200)
        self.data_double1 = deque(maxlen=200)
        self.data_double2 = deque(maxlen=200)
        self.data_double3 = deque(maxlen=200)
        self.data_double4 = deque(maxlen=200)

    def on_mount(self) -> None:
        # Update plots every 0.5 seconds
        self.set_interval(0.5, self.update_plots)

    def update_plots(self) -> None:
        self.t += 1

        # --- Update single plot ---
        self.data_single.append(math.sin(self.t / 10))
        self.data_single2.append(math.sin(self.t / 15 + 1))
        plot = self.single_plot.plt
        plot.clf()
        plot.plot(self.data_single, label="Sine A")
        plot.plot(self.data_single2, label="Sine B")
        plot.ylim(-1.2, 1.2)
        plot.title("Single Plot View")
        self.single_plot.refresh()

        # --- Update double plots ---
        self.data_double1.append(math.sin(self.t / 8))
        self.data_double2.append(math.sin(self.t / 12 + 1))
        self.data_double3.append(math.cos(self.t / 10))
        self.data_double4.append(math.cos(self.t / 15 + 0.5))

        # Top plot
        p1 = self.double_plot1.plt
        p1.clf()
        p1.plot(self.data_double1, label="Sine A")
        p1.plot(self.data_double2, label="Sine B")
        p1.ylim(-1.2, 1.2)
        p1.title("Top Plot in Double View")
        self.double_plot1.refresh()

        # Bottom plot
        p2 = self.double_plot2.plt
        p2.clf()
        p2.plot(self.data_double3, label="Cos A")
        p2.plot(self.data_double4, label="Cos B")
        p2.ylim(-1.2, 1.2)
        p2.title("Bottom Plot in Double View")
        self.double_plot2.refresh()

    # --- Hotkey actions ---
    def action_show_view1(self) -> None:
        self.single_plot.display = True
        self.double_container.display = False

    def action_show_view2(self) -> None:
        self.single_plot.display = False
        self.double_container.display = True


if __name__ == "__main__":
    MarketApp().run()
