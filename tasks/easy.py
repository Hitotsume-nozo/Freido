"""Tasks 1 - Easy: The Expense Report Fraud"""

EASY_TASK = {
    "task_id": "easy",
    "description": "Investigate a tip about fraudulent expense reports submitted by a sales team member.",
    "whistleblower_tip": "Anonymous tip received: 'A member of the sales team has been submitting fake expense reports for client dinners that never happened. Check the receipts from Bella Italia restaurant in March and April. The numbers don't add up.'",
    "max_steps": 20,
    "documents": {
        # ============ EMPLOYEE RECORDS ============
        "emp_001": {
            "id": "emp_001",
            "source_type": "employee_record",
            "title": "Employee Record - David Chen",
            "content": """EMPLOYEE RECORD
Name: David Chen
Employee ID: EMP-2019-0342
Department: Sales
Title: Senior Sales Manager
Manager: Patricia Holmes
Start Date: 2019-06-15
Salary: $95,000/year
Office: New York
Travel Authorization Level: Up to $500/meal, requires receipts
Notes: Top performer Q1-Q2 2023. Received sales excellence award.""",
            "date": "2024-01-01",
            "author": "HR Department",
            "participants": ["David Chen"],
            "metadata": {"department": "Sales", "role": "Senior Sales Manager"},
        },
        "emp_002": {
            "id": "emp_002",
            "source_type": "employee_record",
            "title": "Employee Record - Patricia Holmes",
            "content": """EMPLOYEE RECORD
Name: Patricia Holmes
Employee ID: EMP-2017-0198
Department: Sales
Title: VP of Sales
Manager: CEO
Start Date: 2017-03-01
Salary: $145,000/year
Office: New York
Travel Authorization Level: Up to $1000/meal
Notes: Oversees team of 8 sales representatives.""",
            "date": "2024-01-01",
            "author": "HR Department",
            "participants": ["Patricia Holmes"],
            "metadata": {"department": "Sales", "role": "VP of Sales"},
        },
        "emp_003": {
            "id": "emp_003",
            "source_type": "employee_record",
            "title": "Employee Record - Mike Reynolds",
            "content": """EMPLOYEE RECORD
Name: Mike Reynolds
Employee ID: EMP-2020-0456
Department: Sales
Title: Sales Representative
Manager: David Chen
Start Date: 2020-09-01
Salary: $72,000/year
Office: New York
Travel Authorization Level: Up to $200/meal
Notes: Solid performer, no disciplinary issues.""",
            "date": "2024-01-01",
            "author": "HR Department",
            "participants": ["Mike Reynolds"],
            "metadata": {"department": "Sales", "role": "Sales Representative"},
        },
        "emp_004": {
            "id": "emp_004",
            "source_type": "employee_record",
            "title": "Employee Record - Jennifer Walsh",
            "content": """EMPLOYEE RECORD
Name: Jennifer Walsh
Employee ID: EMP-2021-0523
Department: Sales
Title: Sales Representative
Manager: David Chen
Start Date: 2021-01-15
Salary: $70,000/year
Office: New York
Travel Authorization Level: Up to $200/meal
Notes: New to team, shows promise.""",
            "date": "2024-01-01",
            "author": "HR Department",
            "participants": ["Jennifer Walsh"],
            "metadata": {"department": "Sales", "role": "Sales Representative"},
        },
        "emp_005": {
            "id": "emp_005",
            "source_type": "employee_record",
            "title": "Employee Record - Robert Kim",
            "content": """EMPLOYEE RECORD
Name: Robert Kim
Employee ID: EMP-2018-0267
Department: Finance
Title: Accounts Payable Manager
Manager: CFO
Start Date: 2018-08-20
Salary: $88,000/year
Office: New York
Notes: Processes all expense reimbursements. Clean record.""",
            "date": "2024-01-01",
            "author": "HR Department",
            "participants": ["Robert Kim"],
            "metadata": {"department": "Finance", "role": "Accounts Payable Manager"},
        },
        # ============ EXPENSE REPORTS ============
        "exp_001": {
            "id": "exp_001",
            "source_type": "expense_report",
            "title": "Expense Report - David Chen - March 5",
            "content": """EXPENSE REPORT
Submitted by: David Chen (EMP-2019-0342)
Date of Expense: March 5, 2024
Category: Client Entertainment
Vendor: Bella Italia Restaurant, 245 Park Ave, New York
Amount: $387.50
Attendees: David Chen, Mark Thompson (Acme Corp)
Purpose: Q2 contract renewal discussion
Receipt: #BI-20240305-0892
Approved by: Patricia Holmes
Status: REIMBURSED""",
            "date": "2024-03-05",
            "author": "David Chen",
            "participants": ["David Chen", "Mark Thompson"],
            "metadata": {
                "amount": 387.50,
                "vendor": "Bella Italia",
                "status": "reimbursed",
            },
        },
        "exp_002": {
            "id": "exp_002",
            "source_type": "expense_report",
            "title": "Expense Report - David Chen - March 12",
            "content": """EXPENSE REPORT
Submitted by: David Chen (EMP-2019-0342)
Date of Expense: March 12, 2024
Category: Client Entertainment
Vendor: Bella Italia Restaurant, 245 Park Ave, New York
Amount: $425.00
Attendees: David Chen, Sarah Lopez (TechVentures)
Purpose: New partnership exploration dinner
Receipt: #BI-20240312-1104
Approved by: Patricia Holmes
Status: REIMBURSED""",
            "date": "2024-03-12",
            "author": "David Chen",
            "participants": ["David Chen", "Sarah Lopez"],
            "metadata": {
                "amount": 425.00,
                "vendor": "Bella Italia",
                "status": "reimbursed",
            },
        },
        "exp_003": {
            "id": "exp_003",
            "source_type": "expense_report",
            "title": "Expense Report - David Chen - March 22",
            "content": """EXPENSE REPORT
Submitted by: David Chen (EMP-2019-0342)
Date of Expense: March 22, 2024
Category: Client Entertainment
Vendor: Bella Italia Restaurant, 245 Park Ave, New York
Amount: $412.75
Attendees: David Chen, James Wright (GlobalTech)
Purpose: Product demo follow-up dinner
Receipt: #BI-20240322-1287
Approved by: Patricia Holmes
Status: REIMBURSED""",
            "date": "2024-03-22",
            "author": "David Chen",
            "participants": ["David Chen", "James Wright"],
            "metadata": {
                "amount": 412.75,
                "vendor": "Bella Italia",
                "status": "reimbursed",
            },
        },
        "exp_004": {
            "id": "exp_004",
            "source_type": "expense_report",
            "title": "Expense Report - David Chen - April 3",
            "content": """EXPENSE REPORT
Submitted by: David Chen (EMP-2019-0342)
Date of Expense: April 3, 2024
Category: Client Entertainment
Vendor: Bella Italia Restaurant, 245 Park Ave, New York
Amount: $398.25
Attendees: David Chen, Lisa Park (InnovateCo)
Purpose: Annual renewal dinner
Receipt: #BI-20240403-1456
Approved by: Patricia Holmes
Status: REIMBURSED""",
            "date": "2024-04-03",
            "author": "David Chen",
            "participants": ["David Chen", "Lisa Park"],
            "metadata": {
                "amount": 398.25,
                "vendor": "Bella Italia",
                "status": "reimbursed",
            },
        },
        "exp_005": {
            "id": "exp_005",
            "source_type": "expense_report",
            "title": "Expense Report - Mike Reynolds - March 8",
            "content": """EXPENSE REPORT
Submitted by: Mike Reynolds (EMP-2020-0456)
Date of Expense: March 8, 2024
Category: Client Entertainment
Vendor: Joe's Steakhouse, 188 Broadway, New York
Amount: $156.80
Attendees: Mike Reynolds, Tom Garcia (SmallBiz Inc)
Purpose: Quarterly check-in lunch
Receipt: #JS-20240308-0234
Approved by: David Chen
Status: REIMBURSED""",
            "date": "2024-03-08",
            "author": "Mike Reynolds",
            "participants": ["Mike Reynolds", "Tom Garcia"],
            "metadata": {
                "amount": 156.80,
                "vendor": "Joe's Steakhouse",
                "status": "reimbursed",
            },
        },
        "exp_006": {
            "id": "exp_006",
            "source_type": "expense_report",
            "title": "Expense Report - Jennifer Walsh - March 15",
            "content": """EXPENSE REPORT
Submitted by: Jennifer Walsh (EMP-2021-0523)
Date of Expense: March 15, 2024
Category: Client Entertainment
Vendor: Corner Bistro, 331 W 4th St, New York
Amount: $134.50
Attendees: Jennifer Walsh, Amy Chen (StartupXYZ)
Purpose: New client introduction lunch
Receipt: #CB-20240315-0567
Approved by: David Chen
Status: REIMBURSED""",
            "date": "2024-03-15",
            "author": "Jennifer Walsh",
            "participants": ["Jennifer Walsh", "Amy Chen"],
            "metadata": {
                "amount": 134.50,
                "vendor": "Corner Bistro",
                "status": "reimbursed",
            },
        },
        # ============ EXTERNAL DATA ============
        "ext_001": {
            "id": "ext_001",
            "source_type": "external_data",
            "title": "Bella Italia Restaurant - Business Listing",
            "content": """BUSINESS LISTING - Bella Italia Restaurant
Address: 245 Park Ave, New York, NY 10167
Phone: (212) 555-0147
Type: Italian Fine Dining
Hours: Mon-Fri 11:30am-10pm, Sat 5pm-11pm, Sun CLOSED
Capacity: 85 seats
Average dinner for two: $120-$180

TEMPORARY CLOSURE NOTICE:
Bella Italia was CLOSED for renovation from March 10 to March 30, 2024.
Reopened March 31, 2024.
Source: NYC Department of Health records, Building Permit #BP-2024-11234""",
            "date": "2024-04-15",
            "author": "NYC Business Directory",
            "participants": [],
            "metadata": {"closed_from": "2024-03-10", "closed_to": "2024-03-30"},
        },
        # ============ CALENDAR / TRAVEL ============
        "cal_001": {
            "id": "cal_001",
            "source_type": "calendar_entry",
            "title": "David Chen - Travel Calendar March 2024",
            "content": """TRAVEL & CALENDAR - David Chen - March 2024

March 1-4: New York (office)
March 5: New York - Client meetings (Acme Corp visit logged in CRM)
March 6-7: New York (office)
March 8-9: TRAVEL - Chicago Sales Conference
March 10-13: TRAVEL - Chicago Sales Conference (confirmed hotel: Hilton Chicago, booking #HC-98234)
March 14: Travel day - Chicago to New York (Flight UA-2847, departed 2:30pm CST, arrived 6:15pm EST)
March 15-19: New York (office)
March 20-21: TRAVEL - Boston client visits (confirmed hotel: Marriott Boston, booking #MB-45123)
March 22: Travel day - Boston to New York (Amtrak Acela, departed 4:00pm, arrived 8:30pm)
March 23-31: New York (office)""",
            "date": "2024-03-31",
            "author": "Corporate Travel System",
            "participants": ["David Chen"],
            "metadata": {
                "travel_days": [
                    "2024-03-08",
                    "2024-03-09",
                    "2024-03-10",
                    "2024-03-11",
                    "2024-03-12",
                    "2024-03-13",
                    "2024-03-14",
                    "2024-03-20",
                    "2024-03-21",
                    "2024-03-22",
                ]
            },
        },
        # ============ EMAILS ============
        "email_001": {
            "id": "email_001",
            "source_type": "email",
            "title": "Email: David Chen to Mark Thompson - March 4",
            "content": """FROM: david.chen@company.com
TO: mark.thompson@acmecorp.com
DATE: March 4, 2024, 3:15 PM
SUBJECT: Dinner tomorrow?

Hi Mark,

Looking forward to catching up tomorrow to discuss the Q2 renewal. I made a reservation at Bella Italia for 7pm. Let me know if that works.

Best,
David""",
            "date": "2024-03-04",
            "author": "David Chen",
            "participants": ["David Chen", "Mark Thompson"],
            "metadata": {},
        },
        "email_002": {
            "id": "email_002",
            "source_type": "email",
            "title": "Email: Mark Thompson reply - March 4",
            "content": """FROM: mark.thompson@acmecorp.com
TO: david.chen@company.com
DATE: March 4, 2024, 4:02 PM
SUBJECT: RE: Dinner tomorrow?

David,

Sounds great! See you there at 7.

Mark""",
            "date": "2024-03-04",
            "author": "Mark Thompson",
            "participants": ["David Chen", "Mark Thompson"],
            "metadata": {},
        },
        "email_003": {
            "id": "email_003",
            "source_type": "email",
            "title": "Email: David Chen to Sarah Lopez - March 11",
            "content": """FROM: david.chen@company.com
TO: sarah.lopez@techventures.com
DATE: March 11, 2024, 10:30 AM
SUBJECT: Partnership dinner

Hi Sarah,

I'd love to discuss a potential partnership over dinner tomorrow evening. Are you free? I know a great Italian place.

David""",
            "date": "2024-03-11",
            "author": "David Chen",
            "participants": ["David Chen", "Sarah Lopez"],
            "metadata": {},
        },
        "email_004": {
            "id": "email_004",
            "source_type": "email",
            "title": "Email: Sarah Lopez reply - March 11",
            "content": """FROM: sarah.lopez@techventures.com
TO: david.chen@company.com
DATE: March 11, 2024, 11:45 AM
SUBJECT: RE: Partnership dinner

Hi David,

I appreciate the invite but I'm actually traveling this week - I'm in San Francisco until the 18th. Can we reschedule for late March?

Sarah""",
            "date": "2024-03-11",
            "author": "Sarah Lopez",
            "participants": ["David Chen", "Sarah Lopez"],
            "metadata": {
                "key_evidence": True,
                "reason": "Sarah declined dinner for March 12 - she was in SF",
            },
        },
        "email_005": {
            "id": "email_005",
            "source_type": "email",
            "title": "Email: David Chen to Robert Kim - March 28",
            "content": """FROM: david.chen@company.com
TO: robert.kim@company.com
DATE: March 28, 2024, 9:15 AM
SUBJECT: Expense reimbursements

Hi Robert,

Just checking on the status of my March expense reports. I submitted four client dinner receipts from Bella Italia. Can you confirm they've been processed?

Thanks,
David""",
            "date": "2024-03-28",
            "author": "David Chen",
            "participants": ["David Chen", "Robert Kim"],
            "metadata": {},
        },
        "email_006": {
            "id": "email_006",
            "source_type": "email",
            "title": "Email: Robert Kim reply - March 28",
            "content": """FROM: robert.kim@company.com
TO: david.chen@company.com
DATE: March 28, 2024, 10:45 AM
SUBJECT: RE: Expense reimbursements

David,

Yes, all four have been approved by Patricia and processed for reimbursement. You should see them in your next paycheck.

Regards,
Robert""",
            "date": "2024-03-28",
            "author": "Robert Kim",
            "participants": ["David Chen", "Robert Kim"],
            "metadata": {},
        },
        # ============ POLICY DOCUMENT ============
        "policy_001": {
            "id": "policy_001",
            "source_type": "policy_document",
            "title": "Company Expense Reimbursement Policy",
            "content": """EXPENSE REIMBURSEMENT POLICY
Effective: January 1, 2024

Section 3: Client Entertainment
- All client meals must be accompanied by itemized receipts
- Maximum: $500/person for Senior Managers and above
- Maximum: $200/person for all other employees
- Attendees must be listed with full names and company affiliations
- Expenses must be submitted within 30 days
- Manager approval required for all expenses
- Receipts must be original (no photocopies)

Section 5: Fraud
- Submitting false or inflated expense reports is grounds for immediate termination
- All expenses are subject to random audit by Finance department
- Employees must cooperate fully with any expense investigation""",
            "date": "2024-01-01",
            "author": "Finance Department",
            "participants": [],
            "metadata": {},
        },
        # ============ CRM DATA ============
        "crm_001": {
            "id": "crm_001",
            "source_type": "crm_entry",
            "title": "CRM - Client Interaction Log - March 2024",
            "content": """CRM CLIENT INTERACTION LOG - March 2024

David Chen's logged interactions:

March 5 - Acme Corp (Mark Thompson)
  Type: In-person dinner
  Notes: Discussed Q2 renewal. Mark positive on continuing.
  Next steps: Send updated proposal by March 8.
  CRM Status: Logged ✓

March 12 - TechVentures (Sarah Lopez)
  Type: In-person dinner
  Notes: Explored partnership opportunities. Sarah interested in integration.
  Next steps: Schedule follow-up call.
  CRM Status: Logged ✓

March 22 - GlobalTech (James Wright)
  Type: In-person dinner
  Notes: Product demo follow-up. James wants to pilot Q3.
  Next steps: Send pilot agreement.
  CRM Status: Logged ✓

April 3 - InnovateCo (Lisa Park)
  Type: In-person dinner
  Notes: Annual renewal discussion. Lisa confirmed renewal.
  Next steps: Process renewal paperwork.
  CRM Status: Logged ✓

NOTE: No other sales reps have logged interactions with TechVentures
or GlobalTech in March 2024. InnovateCo's contract was actually renewed
by Jennifer Walsh on March 20 per separate CRM entry.""",
            "date": "2024-04-05",
            "author": "CRM System",
            "participants": ["David Chen"],
            "metadata": {"key_evidence": True},
        },
        "crm_002": {
            "id": "crm_002",
            "source_type": "crm_entry",
            "title": "CRM - InnovateCo Account History",
            "content": """CRM ACCOUNT HISTORY - InnovateCo

Account Manager: Jennifer Walsh (reassigned from David Chen on Feb 1, 2024)

Recent Interactions:
Feb 15 - Jennifer Walsh: Introductory call with Lisa Park
March 1 - Jennifer Walsh: Product demo for new features
March 20 - Jennifer Walsh: Renewal signed. 2-year extension.
March 20 - Jennifer Walsh notes: "Lisa mentioned she hasn't spoken with David in months. Smooth transition."

Contract Value: $45,000/year
Status: RENEWED""",
            "date": "2024-04-05",
            "author": "CRM System",
            "participants": ["Jennifer Walsh", "Lisa Park"],
            "metadata": {
                "key_evidence": True,
                "reason": "Lisa Park says she hasn't spoken to David in months, contradicting his April 3 expense claim",
            },
        },
    },
    # ============ GOLD LABELS FOR GRADING ============
    "gold_labels": {
        "perpetrators": {"David Chen": {"role": "mastermind", "weight": 0.30}},
        "scheme_type": "expense_fraud",
        "scheme_weight": 0.20,
        "key_evidence": {
            "exp_002": {
                "reason": "Expense for March 12 dinner at Bella Italia - restaurant was closed for renovation",
                "weight": 0.08,
            },
            "exp_003": {
                "reason": "Expense for March 22 dinner at Bella Italia - restaurant was closed for renovation",
                "weight": 0.08,
            },
            "ext_001": {
                "reason": "Bella Italia was closed March 10-30 for renovation",
                "weight": 0.08,
            },
            "email_004": {
                "reason": "Sarah Lopez declined March 12 dinner - was in San Francisco, contradicting expense report",
                "weight": 0.08,
            },
            "cal_001": {
                "reason": "David was in Chicago March 10-13, could not have dined in NYC March 12",
                "weight": 0.08,
            },
            "crm_002": {
                "reason": "Lisa Park told Jennifer Walsh she hasn't spoken to David in months - contradicts April 3 dinner claim",
                "weight": 0.08,
            },
        },
        "key_evidence_total_weight": 0.40,
        "false_accusation_penalty": 0.10,
        "timeline_weight": 0.10,
    },
}
