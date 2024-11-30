import os
import json
import shutil
import zipfile
from datetime import datetime
import matplotlib.pyplot as plt

class RiskManagementSystem:
    def __init__(self):
        self.reports = {}
        self.current_report = None
        self.cache = {}

    def create_new_report(self, report_name):
        if report_name in self.reports:
            print(f"Report '{report_name}' already exists.")
            return
        self.reports[report_name] = {"risks": [], "comments": [], "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
        self.current_report = report_name
        print(f"New report '{report_name}' created.")

    def add_risk_data(self, risk_name, probability, impact):
        if not self.current_report:
            print("No active report. Create a report first.")
            return
        risk_data = {
            "name": risk_name,
            "probability": probability,
            "impact": impact,
            "added_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }
        self.reports[self.current_report]["risks"].append(risk_data)
        print(f"Risk '{risk_name}' added to report '{self.current_report}'.")

    def add_comment(self, comment):
        """Додає коментар до звіту."""
        if not self.current_report:
            print("No active report to add a comment.")
            return
        self.reports[self.current_report]["comments"].append({
            "comment": comment,
            "added_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        })
        print(f"Comment added to report '{self.current_report}'.")

    def create_charts(self):
        if not self.current_report or not self.reports[self.current_report]["risks"]:
            print("No data to create charts. Add risks first.")
            return

        risks = self.reports[self.current_report]["risks"]
        names = [risk["name"] for risk in risks]
        probabilities = [risk["probability"] for risk in risks]
        impacts = [risk["impact"] for risk in risks]

        plt.figure(figsize=(12, 6))

        # Probability chart
        plt.subplot(1, 2, 1)
        plt.bar(names, probabilities, color="skyblue")
        plt.title("Risk Probabilities")
        plt.xlabel("Risks")
        plt.ylabel("Probability")

        # Impact chart
        plt.subplot(1, 2, 2)
        plt.bar(names, impacts, color="salmon")
        plt.title("Risk Impacts")
        plt.xlabel("Risks")
        plt.ylabel("Impact")

        plt.tight_layout()
        plt.show()

    def save_report(self):
        """Зберігає звіт у форматі HTML."""
        if not self.current_report:
            print("No active report to save.")
            return

        report = self.reports[self.current_report]
        filename = f"{self.current_report}.html"

        # Генерація HTML-контенту
        html_content = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Report: {self.current_report}</title>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    margin: 20px;
                }}
                h1 {{
                    color: #333;
                }}
                table {{
                    width: 100%;
                    border-collapse: collapse;
                    margin-bottom: 20px;
                }}
                th, td {{
                    border: 1px solid #ddd;
                    padding: 8px;
                    text-align: left;
                }}
                th {{
                    background-color: #f4f4f4;
                }}
            </style>
        </head>
        <body>
            <h1>Report: {self.current_report}</h1>
            <p><strong>Created At:</strong> {report['created_at']}</p>

            <h2>Risks</h2>
            <table>
                <thead>
                    <tr>
                        <th>#</th>
                        <th>Name</th>
                        <th>Probability</th>
                        <th>Impact</th>
                    </tr>
                </thead>
                <tbody>
        """

        for idx, risk in enumerate(report["risks"], start=1):
            html_content += f"""
                    <tr>
                        <td>{idx}</td>
                        <td>{risk['name']}</td>
                        <td>{risk['probability']}</td>
                        <td>{risk['impact']}</td>
                    </tr>
            """

        html_content += """
                </tbody>
            </table>

            <h2>Comments</h2>
            <ul>
        """

        for comment in report["comments"]:
            html_content += f"<li>{comment['comment']} (Added At: {comment['added_at']})</li>"

        html_content += """
            </ul>
        </body>
        </html>
        """

        # Збереження HTML-файлу
        with open(filename, "w", encoding="utf-8") as file:
            file.write(html_content)

        print(f"Report '{self.current_report}' saved as '{filename}'.")

    def create_backup(self):
        if not self.current_report:
            print("No active report to backup.")
            return
        backup_folder = "backups"
        os.makedirs(backup_folder, exist_ok=True)
        filename = f"{self.current_report}.json"
        backup_file = os.path.join(backup_folder, f"{self.current_report}_backup.json")
        if os.path.exists(filename):
            shutil.copy(filename, backup_file)
            print(f"Backup for '{self.current_report}' created at '{backup_file}'.")
        else:
            print(f"Original report file '{filename}' not found. Save the report first.")

    def clear_cache(self):
        """Очистити кеш."""
        self.cache.clear()
        print("Cache cleared successfully.")

    def calculate_financial_impact(self, financial_loss_per_unit):
        """Розрахувати фінансовий вплив на основі ймовірності та впливу."""
        if not self.current_report:
            print("No active report to calculate financial impact.")
            return
        risks = self.reports[self.current_report]["risks"]
        total_impact = 0
        for risk in risks:
            impact = risk["probability"] * risk["impact"] * financial_loss_per_unit
            total_impact += impact
            print(f"Risk: {risk['name']}, Financial Impact: {impact:.2f}")
        print(f"Total Financial Impact: {total_impact:.2f}")
        return total_impact

    def archive_versions(self):
        """Архівувати всі звіти в zip-файл."""
        archive_name = f"reports_archive_{datetime.now().strftime('%Y%m%d%H%M%S')}.zip"
        with zipfile.ZipFile(archive_name, 'w') as archive:
            for report_name, report_data in self.reports.items():
                filename = f"{report_name}.json"
                with open(filename, 'w') as file:
                    json.dump(report_data, file, indent=4)
                archive.write(filename)
                os.remove(filename)  # Видалити файл після архівації
        print(f"All reports archived to '{archive_name}'.")

    def view_report(self, report_name):
        """Переглянути дані звіту."""
        if report_name not in self.reports:
            print(f"Report '{report_name}' does not exist.")
            return
        report = self.reports[report_name]
        print(f"\n--- Report: {report_name} ---")
        print(f"Created At: {report['created_at']}")
        print("Risks:")
        for idx, risk in enumerate(report["risks"], start=1):
            print(f"  {idx}. Name: {risk['name']}, Probability: {risk['probability']}, Impact: {risk['impact']}")
        print("Comments:")
        for idx, comment in enumerate(report["comments"], start=1):
            print(f"  {idx}. {comment['comment']} (Added At: {comment['added_at']})")
        print("-" * 30)


def menu():
    system = RiskManagementSystem()

    while True:
        print("\n--- Risk Management System Menu ---")
        print("1. Create New Report")
        print("2. Add Risk Data")
        print("3. Add Comment")
        print("4. Create Charts")
        print("5. Calculate Financial Impact")
        print("6. View Report")
        print("7. Save Report")
        print("8. Create Backup")
        print("9. Clear Cache")
        print("10. Archive Versions")
        print("11. Exit")

        choice = input("Enter your choice (1-11): ")

        if choice == "1":
            report_name = input("Enter report name: ")
            system.create_new_report(report_name)
        elif choice == "2":
            if not system.reports:
                print("No reports available. Create a report first.")
                continue
            report_name = input(f"Enter report name from available reports {list(system.reports.keys())}: ")
            if report_name not in system.reports:
                print(f"Report '{report_name}' does not exist.")
                continue
            system.current_report = report_name
            risk_name = input("Enter risk name: ")
            probability = float(input("Enter risk probability (0-1): "))
            impact = int(input("Enter risk impact (1-10): "))
            system.add_risk_data(risk_name, probability, impact)
        elif choice == "3":
            if not system.reports:
                print("No reports available. Create a report first.")
                continue
            report_name = input(f"Enter report name from available reports {list(system.reports.keys())}: ")
            if report_name not in system.reports:
                print(f"Report '{report_name}' does not exist.")
                continue
            system.current_report = report_name
            comment = input("Enter your comment: ")
            system.add_comment(comment)
        elif choice == "4":
            if not system.reports:
                print("No reports available. Create a report first.")
                continue
            report_name = input(f"Enter report name from available reports {list(system.reports.keys())}: ")
            if report_name not in system.reports:
                print(f"Report '{report_name}' does not exist.")
                continue
            system.current_report = report_name
            system.create_charts()
        elif choice == "5":
            if not system.reports:
                print("No reports available. Create a report first.")
                continue
            report_name = input(f"Enter report name from available reports {list(system.reports.keys())}: ")
            if report_name not in system.reports:
                print(f"Report '{report_name}' does not exist.")
                continue
            system.current_report = report_name
            financial_loss_per_unit = float(input("Enter financial loss per unit: "))
            system.calculate_financial_impact(financial_loss_per_unit)
        elif choice == "6":
            if not system.reports:
                print("No reports available to view. Create a report first.")
                continue
            report_name = input(f"Enter report name from available reports {list(system.reports.keys())}: ")
            system.view_report(report_name)
        elif choice == "7":
            if not system.reports:
                print("No reports available. Create a report first.")
                continue
            report_name = input(f"Enter report name from available reports {list(system.reports.keys())}: ")
            if report_name not in system.reports:
                print(f"Report '{report_name}' does not exist.")
                continue
            system.current_report = report_name
            system.save_report()
        elif choice == "8":
            if not system.reports:
                print("No reports available. Create a report first.")
                continue
            report_name = input(f"Enter report name from available reports {list(system.reports.keys())}: ")
            if report_name not in system.reports:
                print(f"Report '{report_name}' does not exist.")
                continue
            system.current_report = report_name
            system.create_backup()
        elif choice == "9":
            system.clear_cache()
        elif choice == "10":
            system.archive_versions()
        elif choice == "11":
            print("Exiting Risk Management System. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")


# Виклик меню
if __name__ == "__main__":
    menu()

