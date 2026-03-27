import frappe
import requests

def job_applicant_mail(doc, method):
    # safety check
    if not doc.email_id:
        return

    frappe.sendmail(
        recipients=[doc.email_id],
        subject="Application Received",
        message=f"""
        Hello {doc.applicant_name},

        Your application has been received successfully.

        Thanks & Regards  
        HR Team
        """
    )
    
def daily_hr_report():
    # sample data (baad me real data bhi fetch kar sakte ho)
    message = """
    <h3>Daily HR Report</h3>
    <p>System is working fine.</p>
    """

    frappe.sendmail(
        recipients=["prajapatiaditya399@gmail.com"],
        subject="Daily HR Report",
        message=message
    )

    frappe.logger().info("Daily HR Report Sent")   
    
def check_duplicate_applicant(doc, method):

    if not doc.email_id:
        return

    # check duplicate (excluding current doc)
    existing = frappe.db.exists(
        "Job Applicant",
        {
            "email_id": doc.email_id,
            "name": ["!=", doc.name]
        }
    )

    if existing:
        frappe.throw("Applicant with this email already exists!")    
    
def send_sms(doc, method):

    # mobile number check
    if not doc.phone_number:
        return

    url = "https://api.textlocal.in/send/"   # example SMS API

    payload = {
        "apikey": "YOUR_API_KEY",   # 👈 apni API key daalna
        "numbers": doc.phone_number,
        "message": f"Hello {doc.applicant_name}, your application is received."
    }

    try:
        response = requests.post(url, data=payload)

        frappe.logger().info(response.text)

    except Exception as e:
        frappe.log_error(str(e), "SMS Error")