import csv
import matplotlib.pyplot as plt
from datetime import datetime
from collections import defaultdict

successful_logins = 0
failed_logins = 0

ip_count = defaultdict(int)
user_count = defaultdict(int)

with open("sample_log.txt", "r") as file:

    for line in file:

        line = line.strip()

        if "SUCCESS" in line:
            successful_logins += 1

        elif "FAILED" in line:
            failed_logins += 1

            # Extract IP
            ip = line.split("ip=")[1]
            ip_count[ip] += 1

            # Extract Username
            user = line.split("user=")[1].split()[0]
            user_count[user] += 1

# Find most targeted user
# Determine Risk Level

if failed_logins <= 2:
    risk = "LOW"

elif failed_logins <= 5:
    risk = "MEDIUM"

else:
    risk = "HIGH"
max_user = None
max_attempts = 0

for user, count in user_count.items():
    if count > max_attempts:
        max_attempts = count
        max_user = user

# Print report
print("========== SECURITY REPORT ==========")
print("Successful Logins :", successful_logins)
print("Failed Logins     :", failed_logins)
print("Risk Level        :", risk)

print("\nSuspicious IP Addresses")
current_time = datetime.now()

report = "=========================================\n"
report += "     CYBERSECURITY LOG ANALYZER REPORT\n"
report += "=========================================\n\n"
report += f"Generated On : {current_time}\n\n"
report += f"Successful Logins : {successful_logins}\n"
report += f"Failed Logins     : {failed_logins}\n"
report += f"Risk Level        : {risk}\n\n"
report += "Suspicious IP Addresses\n"

found = False

for ip, count in ip_count.items():

    if count >= 3:
        print(ip, "->", count, "failed login attempts")

        report += f"{ip} -> {count} failed login attempts\n"

        found = True

if not found:
    print("No suspicious IP found.")
    report += "No suspicious IP found.\n"

print("\nMost Targeted User")
print(max_user, "->", max_attempts, "failed login attempts")
if failed_logins >= 5:
    print("\n⚠ WARNING: Possible Brute Force Attack Detected!")

report += "\nMost Targeted User\n"
report += f"{max_user} -> {max_attempts} failed login attempts\n"

# Save report
with open("security_report.txt", "w") as file:
    file.write(report)

print("\nSecurity report saved successfully!")
with open("security_report.csv", "w", newline="") as file:

    writer = csv.writer(file)

    writer.writerow(["Type", "Value"])

    writer.writerow(["Successful Logins", successful_logins])
    writer.writerow(["Failed Logins", failed_logins])
    writer.writerow(["Risk Level", risk])

    writer.writerow([])

    writer.writerow(["Suspicious IP", "Failed Attempts"])

    for ip, count in ip_count.items():

        if count >= 3:

            writer.writerow([ip, count])

print("CSV Report Created Successfully!")

# Create Login Analysis Chart

labels = ["Successful", "Failed"]
values = [successful_logins, failed_logins]

plt.figure(figsize=(6,4))

plt.bar(labels, values)

plt.title("Cybersecurity Login Analysis")

plt.xlabel("Login Type")

plt.ylabel("Number of Logins")

plt.savefig("login_analysis.png")

plt.show()
# Create Pie Chart

plt.figure(figsize=(6,6))

plt.pie(
    values,
    labels=labels,
    autopct="%1.1f%%",
    startangle=90
)

plt.title("Login Distribution")

plt.savefig("login_distribution.png")

plt.show()