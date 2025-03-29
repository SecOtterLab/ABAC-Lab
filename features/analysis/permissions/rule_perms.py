from PyQt5.QtWidgets import QFileDialog, QComboBox, QMessageBox, QVBoxLayout, QLabel, QFrame, QInputDialog, QWidget, QPushButton, QScrollArea, QHBoxLayout
from PyQt5.QtCore import Qt
import os
import re
from core.rule import RuleManager

def show_permstats(app):
    """
    Displays the permissions statistics for each rule in the ABAC file.
    Allows file switching using a dropdown menu.
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
    app.page2_label.hide()
    app.rule_perm_lbl.hide()
    app.rule_perm_btn.hide()
    app.heat_map_lbl.hide()
    app.heatmap_btn_page2.hide()
    app.perm_btn.hide()
    app.permissions_lbl.hide()
    app.bar_graph_btn.hide()
    app.bar_grph_lbl.hide()
    app.stats_container.hide()

    # Clear the results container
    app.clear_results_container()

    # Show the results area container
    app.results_area_container.show()
    
    # Create a container for the results
    container = QWidget()
    container.setStyleSheet("background-color: white;")
    layout = QVBoxLayout(container)

    # Rule Permissions label
    rule_permissions_label = QLabel("Rule Permissions")
    rule_permissions_label.setStyleSheet("font-size: 30px; font-weight: bold; color: white; background-color: #003366; padding: 5px; border-radius: 5px;")
    layout.addWidget(rule_permissions_label, alignment=Qt.AlignTop | Qt.AlignCenter)

    # Create a top bar for the dropdown menu
    top_bar = QWidget()
    top_bar_layout = QHBoxLayout(top_bar)
    top_bar_layout.addStretch()
    
    # Policy label before the dropdown
    policy_label = QLabel("Policy:")
    policy_label.setStyleSheet("font-size: 30px; color: black;")
    top_bar_layout.addWidget(policy_label)

    # Add a dropdown menu for file switching
    app.permstats_file_dropdown = QComboBox()
    app.permstats_file_dropdown.setFixedSize(200, 40)
    app.permstats_file_dropdown.setStyleSheet("font-size: 16px; color: black; border: 2px solid black;")
    for file_path in app.abac_data.keys():
        app.permstats_file_dropdown.addItem(os.path.basename(file_path))
    app.permstats_file_dropdown.currentTextChanged.connect(app.on_permstats_file_dropdown_changed)
    top_bar_layout.addWidget(app.permstats_file_dropdown)
    top_bar_layout.addStretch()

    # Add the top bar to the container
    layout.addWidget(top_bar)

    # Create a scroll area for the rules and permissions
    app.permstats_scroll_area = QScrollArea()
    app.permstats_scroll_area.setWidgetResizable(True)
    app.permstats_scroll_area_widget = QWidget()
    app.permstats_scroll_area_layout = QVBoxLayout(app.permstats_scroll_area_widget)
    app.permstats_scroll_area.setWidget(app.permstats_scroll_area_widget)
    layout.addWidget(app.permstats_scroll_area)

    # Create a bottom bar for the back button
    bottom_bar = QWidget()
    bottom_bar_layout = QHBoxLayout(bottom_bar)
    bottom_bar_layout.addStretch()

    # Add a Back button
    app.back_btn = QPushButton("Back")
    app.back_btn.setFixedSize(100, 40)
    app.back_btn.setStyleSheet("""
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


    app.back_btn.clicked.connect(app.show_rule_choices)
    bottom_bar_layout.addWidget(app.back_btn)
    bottom_bar_layout.addStretch()

    # Add a Save button
    app.save_btn_permstats = QPushButton("Save")
    app.save_btn_permstats.setFixedSize(100, 40)
    app.save_btn_permstats.setStyleSheet("""
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

    app.save_btn_permstats.clicked.connect(lambda: save_permstats_results(app))
    bottom_bar_layout.addWidget(app.save_btn_permstats)

    # Add the bottom bar to the container
    layout.addWidget(bottom_bar)

    # Add the container to the results layout
    app.results_layout.addWidget(container)
    app.scroll_area.show()

    # Display the stats for the first file
    app.permstats_file_dropdown.setCurrentIndex(app.uploaded_files.index(app.current_abac_path))
    display_permstats(app, app.current_abac_path)

def display_permstats(app, file_path):
    """
    Displays the permissions statistics for the specified ABAC file.
    Shows the actual rule as it appears in the text file.
    """
    # Clear previous results from the layout
    while app.permstats_scroll_area_layout.count():
        item = app.permstats_scroll_area_layout.takeAt(0)
        widget = item.widget()
        if widget is not None:
            widget.deleteLater()

    # Get the ABAC data for the selected file
    user_mgr, res_mgr, rule_mgr = app.abac_data[file_path]

    # Read the ABAC file to extract rules
    with open(file_path, 'r') as file:
        lines = file.readlines()

    # Iterate over each rule and calculate the number of permissions granted
    rule_idx = 0  # Track the rule index
    for i, line in enumerate(lines):
        # Check if the line is a rule (starts with 'rule(')
        if line.strip().startswith('rule('):
            rule = rule_mgr.rules[rule_idx]  # Get the corresponding rule
            rule_idx += 1  # Increment the rule index

            # Create a container for the rule and its permissions
            rule_container = QWidget()
            rule_layout = QVBoxLayout(rule_container)

            # Display the actual rule as it appears in the text file
            rule_label = QLabel(f"Rule {rule_idx}: {line.strip()}")
            rule_label.setStyleSheet("font-size: 18px; font-weight: bold; color: black;")
            rule_label.setTextInteractionFlags(Qt.TextSelectableByMouse)  # Enable text selection
            rule_layout.addWidget(rule_label)

            # Calculate the number of permissions granted by this rule
            permissions_count = 0
            permissions_list = []  # Store detailed permissions

            # Iterate over all users, resources, and actions
            for user_name, user in user_mgr.users.items():
                for resource_name, resource in res_mgr.resources.items():
                    for action in rule.acts:
                        if rule.evaluate(user, resource, action):
                            permissions_count += 1
                            # Store the permission details
                            permissions_list.append(
                                f"User: {user_name}, Resource: {resource_name}, Action: {action}"
                            )

            # Display the number of permissions granted by this rule
            count_label = QLabel(f"Permissions Granted: {permissions_count}")
            count_label.setStyleSheet("font-size: 16px; color: black;")
            count_label.setTextInteractionFlags(Qt.TextSelectableByMouse)  # Enable text selection
            rule_layout.addWidget(count_label)

            # Display the detailed list of permissions
            if permissions_list:
                permissions_label = QLabel("Permissions:")
                permissions_label.setStyleSheet("font-size: 16px; font-weight: bold; color: black;")
                permissions_label.setTextInteractionFlags(Qt.TextSelectableByMouse)  # Enable text selection
                rule_layout.addWidget(permissions_label)

                # Add each permission to the layout
                for permission in permissions_list:
                    permission_label = QLabel(permission)
                    permission_label.setStyleSheet("font-size: 14px; color: black;")
                    permission_label.setTextInteractionFlags(Qt.TextSelectableByMouse)  # Enable text selection
                    rule_layout.addWidget(permission_label)

            # Add a separator between rules
            separator = QFrame()
            separator.setFrameShape(QFrame.HLine)
            separator.setFrameShadow(QFrame.Sunken)
            rule_layout.addWidget(separator)

            # Add the rule container to the layout
            app.permstats_scroll_area_layout.addWidget(rule_container)

    # Add a stretch to push all content to the top
    app.permstats_scroll_area_layout.addStretch()

def on_permstats_file_dropdown_changed(app, selected_file_name):
    """
    Handles the file dropdown menu change and switches the displayed file.
    """
    for file_path in app.abac_data.keys():
        if os.path.basename(file_path) == selected_file_name:
            display_permstats(app, file_path)
            break

def show_rulevu(app):
    """
    Allows the user to upload multiple text files containing rules and associate them with ABAC files.
    Displays the rules, number of permissions granted, and the permissions in a layout similar to the rule permissions page.
    Immediately shows the first file after file associations are done.
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
    app.page2_label.hide()
    app.rule_perm_lbl.hide()
    app.rule_perm_btn.hide()
    app.heat_map_lbl.hide()
    app.heatmap_btn_page2.hide()
    app.perm_btn.hide()
    app.permissions_lbl.hide()
    app.bar_graph_btn.hide()
    app.bar_grph_lbl.hide()
    app.stats_container.hide()
    app.clear_results_container()
    app.results_area_container.show()

    # Prompt the user to upload rule files
    options = QFileDialog.Options()
    rule_files, _ = QFileDialog.getOpenFileNames(
        app, "Select Rule Files", "", "Text Files (*.txt);;All Files (*)", options=options
    )

    # If no files are selected or the user cancels, return to the Rule Choices page
    if not rule_files:
        app.show_rule_choices()  # Go back to the Rule Choices page
        return

    rule_pattern = re.compile(r'^rule\([^;]*;[^;]*;[^;]*;[^;]*\)$')
    for rule_file in rule_files:
        with open(rule_file, 'r') as file:
            lines = file.readlines()
        for line_number, line in enumerate(lines, start=1):
            line = line.strip()
            if line.startswith("rule("):
                if not rule_pattern.match(line):
                    QMessageBox.critical(app, "Error", f"Invalid format in file {os.path.basename(rule_file)} at line {line_number}\n{line}\nExpected: rule(*;*;*;*)")
                    app.show_rule_choices()
                    return
            elif line:  # Check for lines that are not empty and do not start with "rule("
                QMessageBox.critical(app, "Error", f"Invalid format in file {os.path.basename(rule_file)} at line {line_number}\n{line}\nExpected: rule(*;*;*;*)")
                app.show_rule_choices()
                return

    # Create a dictionary to store the associations between rule files and ABAC files
    rule_abac_associations = {}

    # Prompt the user to associate each rule file with an ABAC file
    for rule_file in rule_files:
        abac_files = list(app.abac_data.keys())
        abac_file, ok = QInputDialog.getItem(
            app, "Associate ABAC File",
            f"Which ABAC file should be associated with {os.path.basename(rule_file)}?",
            [os.path.basename(f) for f in abac_files] + ["No Association"], 0, False
        )

        # If the user cancels the association dialog or chooses "No Association", skip this file
        if not ok or abac_file == "No Association":
            continue

        # Associate the rule file with the selected ABAC file
        rule_abac_associations[rule_file] = abac_files[[os.path.basename(f) for f in abac_files].index(abac_file)]

    # If no rule files are associated with any ABAC file, return to the Rule Choices page
    if not rule_abac_associations:
        QMessageBox.information(app, "Information", "No rule files were associated with an ABAC file.")
        app.show_rule_choices()
        return

    # Create a container for the results
    container = QWidget()
    container.setStyleSheet("background-color: white;")
    layout = QVBoxLayout(container)

    # --- New informational label above the dropdown ---
    info_label = QLabel()
    info_label.setStyleSheet("""
        font-size: 18px;
        font-weight: bold;
        padding: 10px;
        background-color: #f0f0f0;
        border-radius: 5px;
    """)
    info_label.setAlignment(Qt.AlignCenter)
    info_label.setTextFormat(Qt.RichText)  # Enables rich HTML formatting

    # Set initial text using the first associated rule file and its ABAC file
    first_rule_file = list(rule_abac_associations.keys())[0]
    first_abac_file = rule_abac_associations[first_rule_file]

    info_label.setText(
        f"Evaluating rules for {os.path.basename(first_rule_file)} "
        f"with policy {os.path.basename(first_abac_file)}"
    )

    layout.addWidget(info_label)


    # Create a dropdown to switch between rule files
    rule_file_dropdown = QComboBox()
    rule_file_dropdown.setFixedWidth(200)  # Set the width to match the dropdown in show_permstats
    rule_file_dropdown.setStyleSheet("font-size: 16px; color: black; border: 2px solid black;")
    for rule_file in rule_abac_associations.keys():
        rule_file_dropdown.addItem(os.path.basename(rule_file))
    # Pass the info_label to update its text upon dropdown changes
    rule_file_dropdown.currentTextChanged.connect(
        lambda selected: on_rule_file_dropdown_changed(app, rule_file_dropdown, rule_abac_associations, selected, info_label)
    )

    # Add the dropdown to the layout
    layout.addWidget(rule_file_dropdown, alignment=Qt.AlignCenter)  # Center the dropdown

    # Create a scroll area for the rules and permissions
    scroll_area = QScrollArea()
    scroll_area.setWidgetResizable(True)
    scroll_area_widget = QWidget()
    scroll_area_layout = QVBoxLayout(scroll_area_widget)
    scroll_area.setWidget(scroll_area_widget)
    # Store the scroll area widget reference for later use
    app.rulevu_scroll_area_widget = scroll_area_widget

    # Add the scroll area to the layout
    layout.addWidget(scroll_area)

    # Create a bottom bar for the Back and Save buttons
    bottom_bar = QWidget()
    bottom_bar_layout = QHBoxLayout(bottom_bar)

    # Add a stretch to push the Back button to the center
    bottom_bar_layout.addStretch()

    # Add a Back button
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

    back_btn.clicked.connect(app.show_rule_choices)  # Go back to the Rule Choices page
    bottom_bar_layout.addWidget(back_btn)

    # Add another stretch to push the Save button to the right
    bottom_bar_layout.addStretch()

    # Add a Save button
    save_btn = QPushButton("Save")
    save_btn.setFixedSize(100, 40)
    save_btn.setStyleSheet("""
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

    save_btn.clicked.connect(lambda: save_rulevu_results(app, rule_abac_associations))
    bottom_bar_layout.addWidget(save_btn)

    # Add the bottom bar to the layout
    layout.addWidget(bottom_bar)

    # Add the container to the results layout
    app.results_layout.addWidget(container)

    # Show the scrollable area
    app.scroll_area.show()

    # Immediately display the first file's rules and permissions
    on_rule_file_dropdown_changed(app, rule_file_dropdown, rule_abac_associations, os.path.basename(first_rule_file), info_label)

def on_rule_file_dropdown_changed(app, rule_file_dropdown, rule_abac_associations, selected_file_name=None, info_label=None):
    """
    Handles the file dropdown menu change and switches the displayed file.
    Shows the rule as it appears in the text file and updates the info label.
    """
    if not selected_file_name:
        selected_file_name = rule_file_dropdown.currentText()

    # If "Please choose a file" is selected, do nothing
    if selected_file_name == "Please choose a file":
        return

    # Find the selected rule file
    selected_rule_file = None
    for rule_file in rule_abac_associations.keys():
        if os.path.basename(rule_file) == selected_file_name:
            selected_rule_file = rule_file
            break

    if not selected_rule_file:
        return

    # Update the info label if provided
    if info_label is not None:
        abac_file = rule_abac_associations[selected_rule_file]
        info_label.setText(f"Evaluating rules for {os.path.basename(selected_rule_file)} for policy {os.path.basename(abac_file)}")

    # Get the associated ABAC file
    abac_file = rule_abac_associations[selected_rule_file]
    user_mgr, res_mgr, _ = app.abac_data[abac_file]

    # Clear previous results from the scroll area using the stored reference
    scroll_area_layout = app.rulevu_scroll_area_widget.layout()
    while scroll_area_layout.count():
        item = scroll_area_layout.takeAt(0)
        widget = item.widget()
        if widget is not None:
            widget.deleteLater()

    # Read the selected rule file and extract rules
    with open(selected_rule_file, 'r') as file:
        lines = file.readlines()
    count = 0
    # Display each rule as it appears in the text file
    for line in lines:
        line = line.strip()
        # Check if the line is a rule (starts with 'rule(')
        if line.startswith("rule("):
            count += 1
            # Create a container for each rule
            rule_container = QWidget()
            rule_layout = QVBoxLayout(rule_container)

            # Display the rule as it appears in the text file
            rule_label = QLabel(f"<b>Rule {count}: {line}</b>")
            rule_label.setStyleSheet("font-size: 16px; color: black;")
            rule_label.setTextInteractionFlags(Qt.TextSelectableByMouse)  # Enable text selection
            rule_layout.addWidget(rule_label)

            # Parse the rule to evaluate permissions
            rule_manager = RuleManager()
            rule_manager.parse_rule(line)
            rule = rule_manager.rules[0]  # Get the parsed rule

            # Calculate the number of permissions granted by this rule
            permissions_count = 0
            permissions_list = []  # Store detailed permissions

            # Iterate over all users, resources, and actions
            for user_name, user in user_mgr.users.items():
                for resource_name, resource in res_mgr.resources.items():
                    for action in rule.acts:
                        # Evaluate the rule
                        if rule.evaluate(user, resource, action):
                            permissions_count += 1
                            # Store the permission details
                            permissions_list.append(
                                f"User: {user_name}, Resource: {resource_name}, Action: {action}"
                            )

            # Display the number of permissions granted
            count_label = QLabel(f"Permissions Granted: {permissions_count}")
            count_label.setStyleSheet("font-size: 14px; color: black;")
            count_label.setTextInteractionFlags(Qt.TextSelectableByMouse)  # Enable text selection
            rule_layout.addWidget(count_label)

            # Display the detailed list of permissions
            if permissions_list:
                permissions_label = QLabel("Permissions:")
                permissions_label.setStyleSheet("font-size: 14px; font-weight: bold; color: black;")
                permissions_label.setTextInteractionFlags(Qt.TextSelectableByMouse)  # Enable text selection
                rule_layout.addWidget(permissions_label)

                for permission in permissions_list:
                    permission_label = QLabel(permission)
                    permission_label.setStyleSheet("font-size: 12px; color: black;")
                    permission_label.setTextInteractionFlags(Qt.TextSelectableByMouse)  # Enable text selection
                    rule_layout.addWidget(permission_label)

            # Add a separator between rules
            separator = QFrame()
            separator.setFrameShape(QFrame.HLine)
            separator.setFrameShadow(QFrame.Sunken)
            rule_layout.addWidget(separator)

            # Add the rule container to the scroll area layout
            scroll_area_layout.addWidget(rule_container)

    # Add a stretch to push all content to the top
    scroll_area_layout.addStretch()


def strip_html_tags(text):
    """Remove HTML tags from a string."""
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)

def save_permstats_results(app):
    """
    Saves the permissions statistics results to a .txt file.
    """
    # Get the current file path from the dropdown
    current_file_name = app.permstats_file_dropdown.currentText()
    current_file_path = None
    for file_path in app.abac_data.keys():
        if os.path.basename(file_path) == current_file_name:
            current_file_path = file_path
            break

    if not current_file_path:
        QMessageBox.warning(app, "Warning", "No file selected.")
        return

    # Collect the results from the scroll area
    results = []
    for i in range(app.permstats_scroll_area_layout.count()):
        item = app.permstats_scroll_area_layout.itemAt(i)
        widget = item.widget()
        if widget:
            for child in widget.children():
                if isinstance(child, QLabel):
                    results.append(strip_html_tags(child.text()))  # Strip HTML tags

    # Add the filename to the first line of the results
    results.insert(0, f"Results for file: {current_file_name}\n")

    # Save the results to a .txt file
    options = QFileDialog.Options()
    save_path, _ = QFileDialog.getSaveFileName(app, "Save Results", "", "Text Files (*.txt);;All Files (*)", options=options)
    if save_path:
        with open(save_path, 'w') as file:
            file.write("\n".join(results))
        QMessageBox.information(app, "Success", "Results saved successfully.")

def save_rulevu_results(app, rule_abac_associations):
    """
    Saves the rulevu results to a .txt file.
    """
    # Get the current rule file from the dropdown
    # Updated the index to 1 because index 0 now holds the info label
    current_rule_file_name = app.results_layout.itemAt(0).widget().layout().itemAt(1).widget().currentText()
    current_rule_file = None
    for rule_file in rule_abac_associations.keys():
        if os.path.basename(rule_file) == current_rule_file_name:
            current_rule_file = rule_file
            break

    if not current_rule_file:
        QMessageBox.warning(app, "Warning", "No rule file selected.")
        return

    # Collect the results from the scroll area
    scroll_area_widget = app.results_layout.itemAt(0).widget().layout().itemAt(2).widget().widget()
    scroll_area_layout = scroll_area_widget.layout()
    results = []
    for i in range(scroll_area_layout.count()):
        item = scroll_area_layout.itemAt(i)
        widget = item.widget()
        if widget:
            for child in widget.children():
                if isinstance(child, QLabel):
                    results.append(strip_html_tags(child.text()))  # Strip HTML tags

    # Add the filename to the first line of the results
    results.insert(0, f"Results for file: {current_rule_file_name}\n")

    # Save the results to a .txt file
    options = QFileDialog.Options()
    save_path, _ = QFileDialog.getSaveFileName(app, "Save Results", "", "Text Files (*.txt);;All Files (*)", options=options)
    if save_path:
        with open(save_path, 'w') as file:
            file.write("\n".join(results))
        QMessageBox.information(app, "Success", "Results saved successfully.")
