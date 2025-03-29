import csv
import os
import random
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QFileDialog, QMessageBox
)
from core.res import ResourceManager
from core.rule import RuleManager
from core.user import UserManager

def generate_logs(app):
    # Get the selected policy file
    selected_file = app.page4_current_uploaded_files.currentText()
    if not selected_file:
        QMessageBox.warning(app, "Warning", "No policy file selected.")
        return
    
    # Validate the input numbers
    try:
        num_logs = int(app.page4_integer_text_edit.text())
        if num_logs <= 0:
            raise ValueError("Number of logs must be greater than zero.")
    except ValueError as e:
        QMessageBox.warning(app, "Invalid Input", str(e))
        return

    try:
        percentage_permits = int(app.page4_percentage_text_edit.text()) if app.page4_percentage_text_edit.text() else None
        if percentage_permits is not None and not (0 <= percentage_permits <= 100):
            raise ValueError("Percentage of permits must be between 0 and 100.")
    except ValueError as e:
        QMessageBox.warning(app, "Invalid Input", str(e))
        return

    file_path = None
    for path in app.uploaded_files:
        if os.path.basename(path) == selected_file:
            file_path = path
            break

    if not file_path:
        QMessageBox.warning(app, "Warning", "Selected file not found.")
        return

    # Get the ABAC data for the selected file
    user_mgr, res_mgr, rule_mgr = app.abac_data[file_path]

    # Collect all valid users, resources, and actions
    users = list(user_mgr.users.values())
    resources = list(res_mgr.resources.values())
    actions = set()
    for rule in rule_mgr.rules:
        actions.update(rule.acts)
    actions = list(actions)

    if not users or not resources or not actions:
        QMessageBox.warning(app, "Warning", "The policy file does not contain valid users, resources, or actions.")
        return

    # Generate logs
    logs = []
    if percentage_permits is not None:
        num_permits = int((percentage_permits / 100) * num_logs)
        num_denies = num_logs - num_permits

        permits_generated = 0
        denies_generated = 0

        while permits_generated < num_permits or denies_generated < num_denies:
            user = random.choice(users)
            resource = random.choice(resources)
            action = random.choice(actions)
            decision = "Permit" if any(rule.evaluate(user, resource, action) for rule in rule_mgr.rules) else "Deny"
            if decision == "Permit" and permits_generated < num_permits:
                logs.append([user.get_attribute("uid"), resource.get_attribute("rid"), action, decision])
                permits_generated += 1
            elif decision == "Deny" and denies_generated < num_denies:
                logs.append([user.get_attribute("uid"), resource.get_attribute("rid"), action, decision])
                denies_generated += 1
    else:
        for _ in range(num_logs):
            user = random.choice(users)
            resource = random.choice(resources)
            action = random.choice(actions)
            decision = "Permit" if any(rule.evaluate(user, resource, action) for rule in rule_mgr.rules) else "Deny"
            logs.append([user.get_attribute("uid"), resource.get_attribute("rid"), action, decision])

    # Shuffle the logs to mix permits and denies
    random.shuffle(logs)

    # Export logs as a CSV file
    save_file_name, _ = QFileDialog.getSaveFileName(
        app,
        "Save Generated Logs",
        "",
        "CSV Files (*.csv);;All Files (*)",
        options=QFileDialog.Options(),
    )
    if save_file_name:
        try:
            with open(save_file_name, 'w', newline='') as csvfile:
                log_writer = csv.writer(csvfile)
                log_writer.writerow(["User", "Resource", "Action", "Decision"])
                log_writer.writerows(logs)
            QMessageBox.information(app, "Success", f"Logs generated and saved successfully.\nSaved as {save_file_name}")
        except Exception as e:
            QMessageBox.critical(app, "Error", f"Failed to save logs:\n{str(e)}")
    else:
        QMessageBox.warning(app, "Warning", "No output file selected for saving logs. Generation cancelled.")