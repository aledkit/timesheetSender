import smtplib
import ssl
import json
import tkinter as tk
from tkinter import messagebox
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 465
DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
DEBUG = True

def generate_hours():
    """
    GUI for user input of hours
    :return: List of hours [[Week1], [Week2]]
    """
    result = []

    def calculate_and_close():
        nonlocal result
        try:
            row_1 = [int(entry.get()) for entry in row_1_entries]
            row_2 = [int(entry.get()) for entry in row_2_entries]
            result = [row_1, row_2]
            total = sum(row_1) + sum(row_2)
            messagebox.showinfo("Total Hours", f"Total Hours: {total}")
            root.destroy()
        except ValueError:
            messagebox.showerror("Input Error", "Please enter valid numbers for hours.")

    root = tk.Tk()
    root.title("Enter Weekly Hours")
    tk.Label(root, text="Day").grid(row=0, column=0, padx=5, pady=5)
    for i, day in enumerate(DAYS):
        tk.Label(root, text=day).grid(row=0, column=i + 1, padx=5, pady=5)
    tk.Label(root, text="Week 1").grid(row=1, column=0, padx=5, pady=5)
    tk.Label(root, text="Week 2").grid(row=2, column=0, padx=5, pady=5)

    row_1_entries = []
    row_2_entries = []

    for i in range(len(DAYS)):
        entry_row_1 = tk.Entry(root, width=5)
        entry_row_1.insert(0, "8")
        entry_row_1.grid(row=1, column=i + 1, padx=5, pady=5)
        row_1_entries.append(entry_row_1)

        entry_row_2 = tk.Entry(root, width=5)
        entry_row_2.insert(0, "8")
        entry_row_2.grid(row=2, column=i + 1, padx=5, pady=5)
        row_2_entries.append(entry_row_2)

    tk.Button(root, text="Submit", command=calculate_and_close).grid(row=3, columnspan=6, pady=10)
    root.mainloop()
    return result

def generate_body():
    """
    Generate the email body with a 5x3 HTML table, including total hours.
    :return: str
    """
    hours = generate_hours()
    hours_row_1 = hours[0]  # First row of hours
    hours_row_2 = hours[1]  # Second row of hours
    total_hours = sum(hours_row_1) + sum(hours_row_2)

    table_html = f"""
    <!DOCTYPE html>
    <html>
        <head>
            <style>
                table {{
                    border-collapse: collapse;
                    width: 50%;
                    text-align: center;
                    margin: 20px 0;
                }}
                th, td {{
                    border: 1px solid black;
                    padding: 8px;
                }}
                th {{
                    background-color: #f2f2f2;
                }}
            </style>
        </head>
        <body>
            <h3>Weekly Timesheet</h3>
            <table>
                <tr>
                    <th>Day</th>
                    {"".join(f"<th>{day}</th>" for day in DAYS)}
                </tr>
                <tr>
                    <td>Week 1</td>
                    {"".join(f"<td>{hour}</td>" for hour in hours_row_1)}
                </tr>
                <tr>
                    <td>Week 2</td>
                    {"".join(f"<td>{hour}</td>" for hour in hours_row_2)}
                </tr>
            </table>
            <p><strong>Total Hours:</strong> {total_hours}</p>
        </body>
    </html>
    """
    return table_html

def get_secrets():
    """
    Load secrets from a JSON file.
    :return: dict of secrets (sender_email, sender_password, recipient_email)
    """
    with open('secrets.json') as secrets:
        s = json.load(secrets)
        return s

def main():
    """
    Main function to send the email with the 5x3 table.
    """
    secrets = get_secrets()
    sender_email = secrets['sender_email']
    password = secrets['sender_password']
    receiver_email = secrets['recipient_email']
    test_email = secrets['test_email']

    context = ssl.create_default_context()

    message = MIMEMultipart()
    message['From'] = sender_email
    if DEBUG:
        message['To'] = test_email
    else:
        message['To'] = receiver_email
    message['Subject'] = 'Weekly Timesheet'

    body = generate_body()
    message.attach(MIMEText(body, 'html'))  # Attach as HTML content explicitly

    with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message.as_string())

if __name__ == '__main__':
    main()