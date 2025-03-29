from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QMessageBox, QComboBox, QLabel
)
from PyQt5.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt
import seaborn as sns
import os

def show_bar_graph(app):
    """
    Displays the bar graph interface for visualizing resource access.
    """
    if not app.abac_data:
        QMessageBox.warning(app, "Warning", "Please upload an ABAC file first.")
        return

    # Hide other elements
    app.stats_widget.hide()
    app.perm_widget.hide()
    app.bar_graph_widget.hide()
    app.heat_map_widget.hide()
    app.rule_widget.hide()
    app.rule_perm_lbl.hide()
    app.rule_perm_btn.hide()
    app.heat_map_lbl.hide()
    app.heatmap_btn_page2.hide()
    app.perm_btn.hide()
    app.permissions_lbl.hide()
    app.bar_graph_btn.hide()
    app.bar_grph_lbl.hide()
    app.stats_container.hide()
    app.page2_label.hide()

    # Clear previous results
    app.clear_results_container()

    # Show the results area
    app.results_area_container.show()

    # Create a container for the bar graph
    container = QWidget()
    container.setStyleSheet("background-color: white;")
    container_layout = QVBoxLayout(container)

    # Create a top layout for the Back button and dropdown menu
    top_layout = QHBoxLayout()

    # Add the Back button to the top-left corner
    back_btn = QPushButton("Back")
    back_btn.setFixedSize(100, 40)
    back_btn.setStyleSheet("""
        QPushButton {
            background-color: #005F9E;
            color: white;
            border-radius: 5px;
            font-size: 16px;
        }
        QPushButton:hover {
            background-color: #003366;
        }
    """)

    back_btn.clicked.connect(app.show_page2)
    top_layout.addWidget(back_btn, alignment=Qt.AlignLeft)  # Align Back button to the left

    # Add a dropdown menu for file selection, centered
    if len(app.abac_data) > 1:
        dropdown_layout = QHBoxLayout()

        policy_label = QLabel("Policy:")
        policy_label.setStyleSheet("font-size: 25px; color: black;")
        dropdown_layout.addWidget(policy_label)

        file_dropdown = QComboBox()
        file_dropdown.setFixedWidth(200)  # Set a fixed width for the dropdown
        file_dropdown.setStyleSheet("font-size: 16px; color: black; border: 2px solid black")
        for file_path in app.abac_data.keys():
            file_dropdown.addItem(os.path.basename(file_path))
        file_dropdown.currentIndexChanged.connect(lambda index: display_bar_graph(app, list(app.abac_data.keys())[index]))
        dropdown_layout.addWidget(file_dropdown)
        
        # Add the dropdown to the top layout with centering
        top_layout.addStretch(5)  # Add stretchable space on the left
        top_layout.addLayout(dropdown_layout)  # Add dropdown
        top_layout.addStretch(6)  # Add stretchable space on the right

    # Add the top layout to the container layout
    container_layout.addLayout(top_layout)

    # Create a widget for the bar graph display
    app.bar_graph_display = QWidget()
    app.bar_graph_display_layout = QVBoxLayout(app.bar_graph_display)
    container_layout.addWidget(app.bar_graph_display)

    # Set the layout for the container
    container.setLayout(container_layout)

    # Add the container to the results layout
    app.results_layout.addWidget(container)

    # Show the scrollable area
    app.scroll_area.show()

    # Display the bar graph for the first file
    if app.current_abac_path and len(app.abac_data) > 1:
        file_dropdown.setCurrentIndex(app.uploaded_files.index(app.current_abac_path))
        display_bar_graph(app, app.current_abac_path)
    else:
        first_file = list(app.abac_data.keys())[0]
        display_bar_graph(app, first_file)

def generate_bar_graph_widget(app, file_path):
    """
    Generates a bar graph widget for the given ABAC file.
    """
    user_mgr, res_mgr, rule_mgr = app.abac_data[file_path]
    barData = {}
    all_actions = set()
    for rule in rule_mgr.rules:
        all_actions.update(rule.acts)
    for rid, resource in res_mgr.resources.items():
        resourceName = resource.get_name()
        barData[resourceName] = 0
        for uid, user in user_mgr.users.items():
            for rule in rule_mgr.rules:
                for action in all_actions:
                    if rule.evaluate(user, resource, action):
                        barData[resourceName] += 1
    sortedBarData = dict(sorted(barData.items(), key=lambda item: item[1], reverse=True))
    top_10_resources = list(sortedBarData.items())[:10]
    least_10_resources = list(sortedBarData.items())[-10:]
    fig, axes = plt.subplots(1, 2, figsize=(14, 8))
    fig.subplots_adjust(wspace=0.4)
    
    # Top 10 Graph
    if top_10_resources:
        resources_top, counts_top = zip(*top_10_resources)
        unique_top = sorted(set(counts_top), reverse=True)
        colors_top = sns.color_palette("Blues_r", len(unique_top))
        color_map_top = {val: colors_top[i] for i, val in enumerate(unique_top)}
        bar_colors_top = [color_map_top[c] for c in counts_top]
        sns.barplot(x=list(map(float, counts_top)), y=list(resources_top),
                    ax=axes[0], palette=bar_colors_top)
        axes[0].set_xlabel("Number of Subjects With Access")
        axes[0].set_ylabel("Resources")
        axes[0].set_title(f"Top 10 Resources with Highest Access for {os.path.basename(file_path)}")
    else:
        axes[0].text(0.5, 0.5, "No Data", horizontalalignment='center', verticalalignment='center')
    
    # Least 10 Graph
    if least_10_resources:
        resources_least, counts_least = zip(*least_10_resources)
        unique_least = sorted(set(counts_least), reverse=True)
        colors_least = sns.color_palette("Blues_r", len(unique_least))
        color_map_least = {val: colors_least[i] for i, val in enumerate(unique_least)}
        bar_colors_least = [color_map_least[c] for c in counts_least]
        sns.barplot(x=list(map(float, counts_least)), y=list(resources_least),
                    ax=axes[1], palette=bar_colors_least)
        axes[1].set_xlabel("Number of Subjects With Access")
        axes[1].set_ylabel("Resources")
        axes[1].set_title(f"Top 10 Resources with Least Access for {os.path.basename(file_path)}")
        axes[1].xaxis.set_major_locator(plt.MaxNLocator(integer=True))
    else:
        axes[1].text(0.5, 0.5, "No Data", horizontalalignment='center', verticalalignment='center')
    
    plt.tight_layout()
    annotations = {}
    for ax in axes:
        ann = ax.annotate("", xy=(0, 0), xytext=(20, 20),
                          textcoords="offset points",
                          bbox=dict(boxstyle="round", fc="w"),
                          arrowprops=dict(arrowstyle="->"))
        ann.set_visible(False)
        annotations[ax] = ann

    def on_hover(event):
        if event.inaxes is None:
            for ann in annotations.values():
                ann.set_visible(False)
            fig.canvas.draw_idle()
            return
        ax = event.inaxes
        if ax not in annotations:
            return
        found = False
        for bar in ax.patches:
            contains, _ = bar.contains(event)
            if contains:
                value = bar.get_width()
                x = value
                y = bar.get_y() + bar.get_height() / 2
                ann = annotations[ax]
                ann.xy = (x, y)
                ann.set_text(f'{value:.0f}')
                ann.set_visible(True)
                found = True
                break
        if not found:
            for ann in annotations.values():
                ann.set_visible(False)
        fig.canvas.draw_idle()

    fig.canvas.mpl_connect("motion_notify_event", on_hover)
    canvas = FigureCanvas(fig)
    return canvas

def visualizeBar(app, ax, data, title):
    """
    Visualizes the bar graph on the given axes.
    """
    if data:
        resources, accessCount = zip(*data)
        accessCount = list(map(float, accessCount))
        sns.barplot(x=accessCount, y=resources, ax=ax, palette="Blues_r")
        ax.set_xlabel("Number of Subjects")
        ax.set_ylabel("Resources")
        ax.set_title(title)
    else:
        ax.text(0.5, 0.5, "No Data", horizontalalignment='center', verticalalignment='center')

def display_bar_graph(app, file_path):
    """
    Displays the bar graph for the given file.
    """
    while app.bar_graph_display_layout.count():
        item = app.bar_graph_display_layout.takeAt(0)
        widget = item.widget()
        if widget is not None:
            widget.deleteLater()
    canvas = generate_bar_graph_widget(app, file_path)
    nav_toolbar = NavigationToolbar(canvas, app)
    nav_toolbar.setStyleSheet("background-color: gray; color: white;")
    app.bar_graph_display_layout.addWidget(nav_toolbar)
    app.bar_graph_display_layout.addWidget(canvas)