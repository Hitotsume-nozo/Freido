# tasks/hard.py
"""Task 3 - Hard: The Quarter That Never Was"""

HARD_TASK = {
    "task_id": "hard",
    "description": "Investigate allegations of systematic revenue fabrication across multiple quarters, involving multiple departments and a coordinated cover-up ahead of a funding round.",
    "whistleblower_tip": "Anonymous tip received: 'The Q3 and Q4 2023 revenue numbers presented to the board and investors are fabricated. Fake customer contracts were created to inflate revenue before the Series C funding round. At least 3 people are involved across sales, finance, and executive leadership. Look at the new customers added in Q3 - some of them don't exist. The shipping records will tell you everything. One person involved got cold feet - check the Slack logs.'",
    "max_steps": 40,
    "documents": {
        # ============ EMPLOYEE RECORDS ============
        "emp_h01": {
            "id": "emp_h01",
            "source_type": "employee_record",
            "title": "Employee Record - Robert Kim (CFO)",
            "content": """EMPLOYEE RECORD
Name: Robert Kim
Employee ID: EMP-2019-0101
Department: Finance
Title: Chief Financial Officer
Manager: CEO
Start Date: 2019-01-15
Salary: $210,000/year + equity (2.5% vested over 4 years)
Office: San Francisco
Notes: Led Series A and B fundraising. Currently leading Series C preparation.
Equity vesting accelerates on funding event per employment agreement.
Performance Reviews: Consistently exceeds expectations.
Previous Employment: VP Finance at GrowthMetrics (left after SEC inquiry - no charges filed)""",
            "date": "2024-01-01",
            "author": "HR Department",
            "participants": ["Robert Kim"],
            "metadata": {
                "equity": "2.5%",
                "vesting_accelerator": "funding_event",
                "key_evidence": True,
            },
        },
        "emp_h02": {
            "id": "emp_h02",
            "source_type": "employee_record",
            "title": "Employee Record - Lisa Wang (VP Sales)",
            "content": """EMPLOYEE RECORD
Name: Lisa Wang
Employee ID: EMP-2020-0156
Department: Sales
Title: VP of Sales
Manager: CRO
Start Date: 2020-06-01
Salary: $165,000/year + equity (1.2%)
Commission: 2% of new revenue booked
Office: San Francisco
Notes: Built sales team from 3 to 15 reps. Responsible for all enterprise contracts.
Received $47,000 in commission for Q3-Q4 2023 new deals.
Previous Employment: Sales Director at two startups (both subsequently acquired)""",
            "date": "2024-01-01",
            "author": "HR Department",
            "participants": ["Lisa Wang"],
            "metadata": {"commission_q3q4": 47000},
        },
        "emp_h03": {
            "id": "emp_h03",
            "source_type": "employee_record",
            "title": "Employee Record - Tom Baker (Controller)",
            "content": """EMPLOYEE RECORD
Name: Tom Baker
Employee ID: EMP-2021-0234
Department: Finance
Title: Controller
Manager: Robert Kim (CFO)
Start Date: 2021-03-15
Salary: $125,000/year + equity (0.3%)
Office: San Francisco
Notes: Manages revenue recognition, financial reporting, and reconciliation.
Reports directly to CFO. Received performance bonus of $15,000 for Q4 2023
"exceptional financial reporting accuracy."
Previous Employment: Staff accountant at Deloitte (5 years)""",
            "date": "2024-01-01",
            "author": "HR Department",
            "participants": ["Tom Baker"],
            "metadata": {"bonus_q4": 15000},
        },
        "emp_h04": {
            "id": "emp_h04",
            "source_type": "employee_record",
            "title": "Employee Record - Amy Foster (Sales Rep)",
            "content": """EMPLOYEE RECORD
Name: Amy Foster
Employee ID: EMP-2022-0389
Department: Sales
Title: Sales Representative
Manager: Lisa Wang
Start Date: 2022-08-01
Salary: $78,000/year
Commission: 1% of new revenue booked
Office: San Francisco
Notes: Manages mid-market accounts. Solid performer.
HR Note (January 2024): Amy requested transfer to marketing department.
Reason given: "looking for new challenges." Transfer pending.
Previous Employment: First professional role after MBA (Stanford)""",
            "date": "2024-01-01",
            "author": "HR Department",
            "participants": ["Amy Foster"],
            "metadata": {"transfer_request": True},
        },
        "emp_h05": {
            "id": "emp_h05",
            "source_type": "employee_record",
            "title": "Employee Record - David Park (Sales Rep)",
            "content": """EMPLOYEE RECORD
Name: David Park
Employee ID: EMP-2021-0401
Department: Sales
Title: Senior Sales Representative
Manager: Lisa Wang
Start Date: 2021-07-01
Salary: $85,000/year
Commission: 1.5% of new revenue booked
Office: San Francisco
Notes: Top individual contributor. Handles largest enterprise accounts.
No disciplinary issues. No involvement in Q3/Q4 new customer acquisition
(focused on existing account expansion).""",
            "date": "2024-01-01",
            "author": "HR Department",
            "participants": ["David Park"],
            "metadata": {"note": "Innocent - red herring"},
        },
        "emp_h06": {
            "id": "emp_h06",
            "source_type": "employee_record",
            "title": "Employee Record - Nina Patel (Revenue Analyst)",
            "content": """EMPLOYEE RECORD
Name: Nina Patel
Employee ID: EMP-2022-0445
Department: Finance
Title: Revenue Operations Analyst
Manager: Tom Baker
Start Date: 2022-10-01
Salary: $72,000/year
Office: San Francisco
Notes: Handles revenue reconciliation and reporting support.
Flagged for commendation by Tom Baker for "not asking unnecessary questions
and trusting the process" in Q4 2023 review.
No previous flags or concerns.""",
            "date": "2024-01-01",
            "author": "HR Department",
            "participants": ["Nina Patel"],
            "metadata": {"suspicious_commendation": True},
        },
        # ============ CUSTOMER CONTRACTS ============
        "contract_001": {
            "id": "contract_001",
            "source_type": "contract",
            "title": "Contract - NovaTech Industries (Q3 2023)",
            "content": """CUSTOMER CONTRACT
Contract ID: C-2023-0156
Customer: NovaTech Industries LLC
Contact: James Morrison, VP Operations
Address: 4521 Innovation Drive, Suite 800, Austin, TX 78701
Contract Value: $180,000/year
Start Date: August 1, 2023
Term: 2 years
Product: Enterprise Platform - 200 seats
Sales Rep: Lisa Wang
Payment Terms: Net-60
Signed by: James Morrison (Customer), Lisa Wang (Company)

Payment Status: Invoice sent August 15, 2023. NO PAYMENT RECEIVED.
Collections Note (Nov 2023): "Customer unresponsive to payment requests."
Collections Note (Jan 2024): Tom Baker note: "Write off deferred to Q2 2024
per CFO direction. Keep as active revenue."
""",
            "date": "2023-08-01",
            "author": "Lisa Wang",
            "participants": ["Lisa Wang", "James Morrison"],
            "metadata": {"key_evidence": True, "payment_received": False},
        },
        "contract_002": {
            "id": "contract_002",
            "source_type": "contract",
            "title": "Contract - Quantum Dynamics Corp (Q3 2023)",
            "content": """CUSTOMER CONTRACT
Contract ID: C-2023-0167
Customer: Quantum Dynamics Corp
Contact: Sandra Lee, CTO
Address: 789 Pacific Heights Blvd, San Diego, CA 92101
Contract Value: $245,000/year
Start Date: September 1, 2023
Term: 3 years
Product: Enterprise Platform - 500 seats + API access
Sales Rep: Amy Foster
Payment Terms: Net-60
Signed by: Sandra Lee (Customer), Amy Foster (Company)

Payment Status: Invoice sent September 15, 2023. NO PAYMENT RECEIVED.
Collections Note (Dec 2023): "Phone number on file is disconnected."
Collections Note (Jan 2024): Tom Baker note: "Revenue recognized per
contract terms. Payment follow-up continuing."
""",
            "date": "2023-09-01",
            "author": "Amy Foster",
            "participants": ["Amy Foster", "Sandra Lee"],
            "metadata": {"key_evidence": True, "payment_received": False},
        },
        "contract_003": {
            "id": "contract_003",
            "source_type": "contract",
            "title": "Contract - Pinnacle Group International (Q4 2023)",
            "content": """CUSTOMER CONTRACT
Contract ID: C-2023-0189
Customer: Pinnacle Group International
Contact: Richard Hayes, CEO
Address: 1200 Market Street, Floor 15, Philadelphia, PA 19107
Contract Value: $320,000/year
Start Date: October 15, 2023
Term: 2 years
Product: Enterprise Platform - 800 seats + Premium Support
Sales Rep: Lisa Wang
Payment Terms: Net-60
Signed by: Richard Hayes (Customer), Lisa Wang (Company)

Payment Status: Invoice sent November 1, 2023. NO PAYMENT RECEIVED.
Collections Note (Jan 2024): Tom Baker note: "Payment expected Q1 2024.
Maintaining as recognized revenue."
""",
            "date": "2023-10-15",
            "author": "Lisa Wang",
            "participants": ["Lisa Wang", "Richard Hayes"],
            "metadata": {"key_evidence": True, "payment_received": False},
        },
        "contract_004": {
            "id": "contract_004",
            "source_type": "contract",
            "title": "Contract - Westfield Analytics (Q3 2023) - LEGITIMATE",
            "content": """CUSTOMER CONTRACT
Contract ID: C-2023-0145
Customer: Westfield Analytics Inc
Contact: Maria Santos, Head of Data
Address: 300 Fifth Avenue, New York, NY 10001
Contract Value: $95,000/year
Start Date: July 15, 2023
Term: 1 year (with auto-renewal)
Product: Enterprise Platform - 75 seats
Sales Rep: David Park
Payment Terms: Net-30

Payment Status: All payments received on time.
Jul 2023: $7,916.67 received
Aug 2023: $7,916.67 received
Sep 2023: $7,916.67 received
[continues monthly - all received]
Customer Satisfaction: 4.5/5 (surveyed Dec 2023)""",
            "date": "2023-07-15",
            "author": "David Park",
            "participants": ["David Park", "Maria Santos"],
            "metadata": {"legitimate": True, "payments_received": True},
        },
        "contract_005": {
            "id": "contract_005",
            "source_type": "contract",
            "title": "Contract - Atlas Manufacturing (Q4 2023) - LEGITIMATE",
            "content": """CUSTOMER CONTRACT
Contract ID: C-2023-0178
Customer: Atlas Manufacturing Group
Contact: Brian Kelly, IT Director
Address: 5000 Industrial Blvd, Detroit, MI 48201
Contract Value: $62,000/year
Start Date: November 1, 2023
Term: 1 year
Product: Standard Platform - 40 seats
Sales Rep: David Park
Payment Terms: Net-30

Payment Status: All payments received.
Onboarding completed. Active user count: 38/40 seats utilized.
Customer Satisfaction: 4.0/5""",
            "date": "2023-11-01",
            "author": "David Park",
            "participants": ["David Park", "Brian Kelly"],
            "metadata": {"legitimate": True, "payments_received": True},
        },
        # ============ EXTERNAL DATA ============
        "ext_h01": {
            "id": "ext_h01",
            "source_type": "external_data",
            "title": "Business Registry Search - NovaTech Industries",
            "content": """BUSINESS ENTITY SEARCH RESULTS

NovaTech Industries LLC
State: Texas
Status: Active (registered June 2023)
Registered Agent: J. Morrison
Registered Address: 4521 Innovation Drive, Suite 800, Austin, TX 78701

ADDRESS VERIFICATION:
4521 Innovation Drive, Suite 800 = UPS Store #4892
This is a commercial mailbox rental facility, NOT an office suite.

ADDITIONAL INFORMATION:
- No website found for novatech-industries.com (domain not registered)
- No LinkedIn company page
- No employees found on LinkedIn
- No press releases or news mentions
- Texas Comptroller: No franchise tax filings
- BBB: Not listed""",
            "date": "2024-02-01",
            "author": "Business Registry Service",
            "participants": [],
            "metadata": {"key_evidence": True, "shell_company": True},
        },
        "ext_h02": {
            "id": "ext_h02",
            "source_type": "external_data",
            "title": "Business Registry Search - Quantum Dynamics Corp",
            "content": """BUSINESS ENTITY SEARCH RESULTS

Quantum Dynamics Corp
State: California
Status: Active (registered July 2023)
Registered Agent: S. Lee
Registered Address: 789 Pacific Heights Blvd, San Diego, CA 92101

ADDRESS VERIFICATION:
789 Pacific Heights Blvd = Virtual Office / Mail Forwarding Service (Regus)

ADDITIONAL INFORMATION:
- Website quantumdynamicscorp.com registered July 2023, single landing page
- No employees on LinkedIn
- Phone number (619) 555-0234 goes to voicemail (generic greeting)
- No customer reviews or business references found
- CA Franchise Tax Board: Minimum tax filing only""",
            "date": "2024-02-01",
            "author": "Business Registry Service",
            "participants": [],
            "metadata": {"key_evidence": True, "shell_company": True},
        },
        "ext_h03": {
            "id": "ext_h03",
            "source_type": "external_data",
            "title": "Business Registry Search - Pinnacle Group International",
            "content": """BUSINESS ENTITY SEARCH RESULTS

Pinnacle Group International LLC
State: Delaware (registered), Operations: Pennsylvania
Status: Active (registered August 2023)
Registered Agent: R. Hayes
Registered Address: 1200 Market Street, Floor 15, Philadelphia, PA 19107

ADDRESS VERIFICATION:
1200 Market Street, Floor 15 = Shared coworking space (WeWork)
No dedicated office. Hot desk membership only ($299/month).

ADDITIONAL INFORMATION:
- Website pinnaclegroupintl.com registered August 2023
- Website has stock photos and generic copy
- One employee on LinkedIn: Richard Hayes (profile created August 2023,
  no prior work history, 12 connections)
- No press mentions, no client testimonials
- Delaware: Registered but no annual franchise tax paid""",
            "date": "2024-02-01",
            "author": "Business Registry Service",
            "participants": [],
            "metadata": {"key_evidence": True, "shell_company": True},
        },
        "ext_h04": {
            "id": "ext_h04",
            "source_type": "external_data",
            "title": "Business Registry Search - Westfield Analytics",
            "content": """BUSINESS ENTITY SEARCH RESULTS

Westfield Analytics Inc
State: New York
Status: Active (registered 2018)
Registered Address: 300 Fifth Avenue, New York, NY 10001

ADDRESS VERIFICATION: Confirmed office space. Floor 12, ~5000 sq ft.

ADDITIONAL INFORMATION:
- Website active since 2018, regularly updated
- 45 employees on LinkedIn
- Multiple press mentions and client case studies
- BBB: A+ rating
- Glassdoor: 4.2/5, 23 reviews""",
            "date": "2024-02-01",
            "author": "Business Registry Service",
            "participants": [],
            "metadata": {"legitimate": True},
        },
        # ============ SHIPPING RECORDS ============
        "ship_001": {
            "id": "ship_001",
            "source_type": "shipping_record",
            "title": "Product Deployment & Onboarding Records Q3-Q4 2023",
            "content": """PRODUCT DEPLOYMENT & ONBOARDING LOG
Period: July 2023 - December 2023

Successful Deployments:
1. Westfield Analytics (C-2023-0145) - July 20, 2023
   - 75 seat licenses provisioned
   - Onboarding completed: 3 training sessions delivered
   - Active users as of Dec 31: 71/75
   - Support tickets: 12 (all resolved)

2. Atlas Manufacturing (C-2023-0178) - November 8, 2023
   - 40 seat licenses provisioned
   - Onboarding completed: 2 training sessions delivered
   - Active users as of Dec 31: 38/40
   - Support tickets: 5 (all resolved)

3. [8 other existing customer upgrades - all deployed successfully]

PENDING DEPLOYMENTS (NO ACTIVITY):
- NovaTech Industries (C-2023-0156): Licenses provisioned Aug 5.
  NO logins recorded. Onboarding calls scheduled 3 times,
  no-show each time. Zero support tickets.

- Quantum Dynamics (C-2023-0167): Licenses provisioned Sep 5.
  NO logins recorded. Welcome email bounced (invalid contact email).
  Zero support tickets.

- Pinnacle Group (C-2023-0189): Licenses provisioned Oct 20.
  NO logins recorded. Onboarding call attempt - "Richard Hayes"
  joined briefly, asked to reschedule, never responded again.
  Zero support tickets.

NOTE: Customer Success team flagged these 3 accounts to VP Sales
Lisa Wang on December 1, 2023. Response from Lisa: "High-value
enterprise clients often have slow deployment cycles. Do not
escalate further - I'm managing these relationships personally.""",
            "date": "2024-01-15",
            "author": "Customer Success Team",
            "participants": [],
            "metadata": {"key_evidence": True},
        },
        # ============ FINANCIAL RECORDS ============
        "fin_h01": {
            "id": "fin_h01",
            "source_type": "financial_record",
            "title": "Revenue Report Q3 2023",
            "content": """QUARTERLY REVENUE REPORT - Q3 2023
Prepared by: Tom Baker (Controller)
Reviewed by: Robert Kim (CFO)

REVENUE SUMMARY:
Existing Customers (recurring): $1,245,000
New Customers:
  - Westfield Analytics: $23,750 (pro-rated from July 15)
  - NovaTech Industries: $30,000 (pro-rated from Aug 1)
  - Quantum Dynamics Corp: $20,417 (pro-rated from Sep 1)

Total Q3 Revenue: $1,319,167

ACCOUNTS RECEIVABLE:
Total Outstanding: $230,417
  - NovaTech Industries: $30,000 (60+ days)
  - Quantum Dynamics: $20,417 (30+ days)
  - Other (normal cycle): $180,000

NOTES:
Revenue recognized on contract signing per company policy.
CFO approved recognition of NovaTech and Quantum revenue despite
non-payment, citing "enterprise payment cycles typically 60-90 days."
""",
            "date": "2023-10-15",
            "author": "Tom Baker",
            "participants": ["Tom Baker", "Robert Kim"],
            "metadata": {"key_evidence": True},
        },
        "fin_h02": {
            "id": "fin_h02",
            "source_type": "financial_record",
            "title": "Revenue Report Q4 2023",
            "content": """QUARTERLY REVENUE REPORT - Q4 2023
Prepared by: Tom Baker (Controller)
Reviewed by: Robert Kim (CFO)

REVENUE SUMMARY:
Existing Customers (recurring): $1,312,000
New Customers:
  - NovaTech Industries: $45,000 (full quarter)
  - Quantum Dynamics Corp: $61,250 (full quarter)
  - Pinnacle Group International: $66,667 (pro-rated from Oct 15)
  - Atlas Manufacturing: $10,333 (pro-rated from Nov 1)

Total Q4 Revenue: $1,495,250

YEAR-END REVENUE: $5,234,417
(Q1: $1,100,000 + Q2: $1,320,000 + Q3: $1,319,167 + Q4: $1,495,250)

Year-over-Year Growth: 48% (vs $3,537,000 in 2022)

ACCOUNTS RECEIVABLE (AGING):
90+ days: $50,417 (NovaTech: $30,000, Quantum: $20,417)
60+ days: $66,667 (Pinnacle)
30+ days: $45,000 (NovaTech Q4)
Current: $195,000 (normal)

NOTES:
Robert Kim approved continued recognition of all new customer revenue.
"Expected payment in Q1 2024. Do not adjust until board meeting."

BOARD PRESENTATION NOTE:
Headline metrics for Series C deck:
- Revenue: $5.23M (48% YoY growth)
- New enterprise customers: 5 (including Westfield and Atlas)
- ARR run-rate: $6.0M
""",
            "date": "2024-01-15",
            "author": "Tom Baker",
            "participants": ["Tom Baker", "Robert Kim"],
            "metadata": {"key_evidence": True},
        },
        "fin_h03": {
            "id": "fin_h03",
            "source_type": "financial_record",
            "title": "Bank Statement Summary Q3-Q4 2023",
            "content": """BANK STATEMENT SUMMARY
Account: Company Operating Account
Period: July 1, 2023 - December 31, 2023

INCOMING PAYMENTS FROM NEW Q3/Q4 CUSTOMERS:

Westfield Analytics:
  Jul 30: $7,916.67
  Aug 30: $7,916.67
  Sep 30: $7,916.67
  Oct 30: $7,916.67
  Nov 30: $7,916.67
  Dec 30: $7,916.67
  TOTAL RECEIVED: $47,500 ✓

Atlas Manufacturing:
  Nov 30: $5,166.67
  Dec 30: $5,166.67
  TOTAL RECEIVED: $10,333.34 ✓

NovaTech Industries:
  TOTAL RECEIVED: $0.00 ✗

Quantum Dynamics Corp:
  TOTAL RECEIVED: $0.00 ✗

Pinnacle Group International:
  TOTAL RECEIVED: $0.00 ✗

SUMMARY OF NEW CUSTOMER REVENUE vs CASH RECEIVED:
Revenue Recognized (Q3+Q4): $257,417
Cash Actually Received: $57,833
VARIANCE: $199,584 (77.5% of new customer revenue is UNCOLLECTED)
""",
            "date": "2024-01-31",
            "author": "Treasury",
            "participants": [],
            "metadata": {"key_evidence": True},
        },
        # ============ EMAILS ============
        "email_h01": {
            "id": "email_h01",
            "source_type": "email",
            "title": "Email: Robert Kim to Lisa Wang - July 2023",
            "content": """FROM: robert.kim@company.com
TO: lisa.wang@company.com
DATE: July 10, 2023, 8:15 PM
SUBJECT: Q3 targets - CONFIDENTIAL

Lisa,

The board approved the Series C timeline. We need to close the round by
Q1 2024. The problem is our growth numbers aren't where they need to be.
Investors want to see 45%+ YoY revenue growth and we're trending at 28%.

We need at least $500K in new enterprise ARR booked in Q3-Q4 to hit the
numbers. I don't care how we get there but the contracts need to look real.

I have some ideas. Let's discuss tomorrow - NOT on company Slack.
Use the Signal group.

Robert""",
            "date": "2023-07-10",
            "author": "Robert Kim",
            "participants": ["Robert Kim", "Lisa Wang"],
            "metadata": {"key_evidence": True},
        },
        "email_h02": {
            "id": "email_h02",
            "source_type": "email",
            "title": "Email: Lisa Wang to Amy Foster - Aug 2023",
            "content": """FROM: lisa.wang@company.com
TO: amy.foster@company.com
DATE: August 20, 2023, 3:30 PM
SUBJECT: New account assignment

Amy,

I'm assigning you the Quantum Dynamics account. I've already done the
initial outreach and Sandra Lee (their CTO) is ready to sign. I just need
you to process the contract paperwork and enter it in the CRM.

I'll send you the signed contract. You don't need to do a demo or
qualification call - I've handled all of that. Just log it as a standard
enterprise deal.

Thanks,
Lisa""",
            "date": "2023-08-20",
            "author": "Lisa Wang",
            "participants": ["Lisa Wang", "Amy Foster"],
            "metadata": {
                "key_evidence": True,
                "reason": "Lisa bypassed normal sales process",
            },
        },
        "email_h03": {
            "id": "email_h03",
            "source_type": "email",
            "title": "Email: Amy Foster to Lisa Wang - Aug 2023",
            "content": """FROM: amy.foster@company.com
TO: lisa.wang@company.com
DATE: August 21, 2023, 9:45 AM
SUBJECT: RE: New account assignment

Lisa,

Happy to help but this is a bit unusual - normally I'd do at least a
qualification call and product demo before we contract. Is there a
reason we're skipping those steps?

Also, the contract value is $245K/year for 500 seats. That's a big deal
for a company I can't find much about online. Should I do any due
diligence on them?

Amy""",
            "date": "2023-08-21",
            "author": "Amy Foster",
            "participants": ["Amy Foster", "Lisa Wang"],
            "metadata": {"key_evidence": True},
        },
        "email_h04": {
            "id": "email_h04",
            "source_type": "email",
            "title": "Email: Lisa Wang to Amy Foster - Aug 2023 reply",
            "content": """FROM: lisa.wang@company.com
TO: amy.foster@company.com
DATE: August 21, 2023, 10:15 AM
SUBJECT: RE: RE: New account assignment

Amy,

I appreciate your thoroughness but I've personally vetted this customer.
Sandra is a former colleague and the deal is solid. We're fast-tracking
because they have budget that expires end of quarter.

Just process the paperwork. That's all I need.

Lisa""",
            "date": "2023-08-21",
            "author": "Lisa Wang",
            "participants": ["Amy Foster", "Lisa Wang"],
            "metadata": {},
        },
        "email_h05": {
            "id": "email_h05",
            "source_type": "email",
            "title": "Email: Robert Kim to Tom Baker - Oct 2023",
            "content": """FROM: robert.kim@company.com
TO: tom.baker@company.com
DATE: October 20, 2023, 6:00 PM
SUBJECT: Q3 revenue recognition

Tom,

For the Q3 close, recognize full contract value for NovaTech and Quantum
Dynamics on the contract start dates. I know payment hasn't been received
yet but our revenue recognition policy allows recognition on contract
execution for enterprise deals.

Don't flag these in the aging report to the board. I'll handle the
investor narrative around collections timing.

Robert""",
            "date": "2023-10-20",
            "author": "Robert Kim",
            "participants": ["Robert Kim", "Tom Baker"],
            "metadata": {"key_evidence": True},
        },
        "email_h06": {
            "id": "email_h06",
            "source_type": "email",
            "title": "Email: Tom Baker to Robert Kim - Oct 2023 reply",
            "content": """FROM: tom.baker@company.com
TO: robert.kim@company.com
DATE: October 20, 2023, 7:30 PM
SUBJECT: RE: Q3 revenue recognition

Robert,

I can recognize on contract execution, but our policy requires evidence
of customer acceptance (login activity, onboarding completion) for
recognition beyond the first month. NovaTech has zero logins and Quantum's
welcome email bounced.

Also, GAAP requires a reasonable expectation of collectibility. With no
payment after 60+ days and no customer engagement, I'm not comfortable
with full recognition.

Can we discuss?

Tom""",
            "date": "2023-10-20",
            "author": "Tom Baker",
            "participants": ["Tom Baker", "Robert Kim"],
            "metadata": {"key_evidence": True},
        },
        "email_h07": {
            "id": "email_h07",
            "source_type": "email",
            "title": "Email: Robert Kim to Tom Baker - Oct 2023 follow-up",
            "content": """FROM: robert.kim@company.com
TO: tom.baker@company.com
DATE: October 21, 2023, 8:00 AM
SUBJECT: RE: RE: Q3 revenue recognition

Tom,

I hear your concerns. Let me be direct: the Series C depends on these
numbers. The board presentation is November 5th. If we miss the growth
target, the round falls apart and that affects everyone — including your
equity and your bonus.

I'm the CFO and I'm making the call on revenue recognition. Recognize it.
I'll document the business justification. You just need to book the entries.

This conversation stays between us.

Robert""",
            "date": "2023-10-21",
            "author": "Robert Kim",
            "participants": ["Robert Kim", "Tom Baker"],
            "metadata": {
                "key_evidence": True,
                "reason": "CFO pressuring controller, explicit threat about equity/bonus",
            },
        },
        "email_h08": {
            "id": "email_h08",
            "source_type": "email",
            "title": "Email: Nina Patel to Tom Baker - Dec 2023",
            "content": """FROM: nina.patel@company.com
TO: tom.baker@company.com
DATE: December 15, 2023, 2:00 PM
SUBJECT: Reconciliation question

Hi Tom,

Working on the Q4 reconciliation. I'm seeing three large enterprise
accounts (NovaTech, Quantum Dynamics, Pinnacle Group) with zero cash
receipts against significant recognized revenue. Total is almost $200K
in AR with no payment activity.

Should I flag these for the aging report? Per our standard process,
anything 90+ days should be escalated.

Nina""",
            "date": "2023-12-15",
            "author": "Nina Patel",
            "participants": ["Nina Patel", "Tom Baker"],
            "metadata": {},
        },
        "email_h09": {
            "id": "email_h09",
            "source_type": "email",
            "title": "Email: Tom Baker to Nina Patel - Dec 2023 reply",
            "content": """FROM: tom.baker@company.com
TO: nina.patel@company.com
DATE: December 15, 2023, 2:45 PM
SUBJECT: RE: Reconciliation question

Nina,

Good catch on the aging. For these three accounts, the CFO has approved
extended payment terms. Don't flag them in the standard aging report —
I'll handle them separately in the executive summary.

Just mark them as "Payment Expected Q1 2024" in your notes and move on
to the other accounts.

Thanks,
Tom""",
            "date": "2023-12-15",
            "author": "Tom Baker",
            "participants": ["Tom Baker", "Nina Patel"],
            "metadata": {
                "key_evidence": True,
                "reason": "Controller actively hiding AR aging from standard reports",
            },
        },
        # ============ BOARD MEETING MINUTES ============
        "board_001": {
            "id": "board_001",
            "source_type": "meeting_minutes",
            "title": "Board Meeting Minutes - November 5, 2023",
            "content": """BOARD OF DIRECTORS MEETING MINUTES
Date: November 5, 2023
Attendees: [Board members], Robert Kim (CFO), CEO

FINANCIAL PRESENTATION (Robert Kim):

1. Revenue Update:
   - Q3 Revenue: $1,319,167 (12% QoQ growth)
   - Projected Q4: $1,450,000+
   - Full year projection: $5.1M+ (45%+ YoY growth)
   - "We've added 3 significant enterprise customers in Q3,
     validating our enterprise go-to-market strategy."

2. Series C Readiness:
   - Target raise: $25M at $100M pre-money valuation
   - Investor meetings scheduled Jan-Feb 2024
   - Growth metrics now meet institutional investor thresholds

3. Board member question: "What's our net revenue retention?"
   Robert: "135% including expansion revenue. New enterprise
   customers are our strongest cohort."

   Board member question: "Cash collections on new customers?"
   Robert: "Enterprise contracts typically have 60-90 day payment
   cycles. We expect normalization in Q1."

4. Board approved proceeding with Series C preparation.

MOTION: Approve Q3 financials as presented. PASSED (unanimous).
""",
            "date": "2023-11-05",
            "author": "Board Secretary",
            "participants": ["Robert Kim", "CEO", "Board Members"],
            "metadata": {"key_evidence": True},
        },
        # ============ CRM DATA ============
        "crm_h01": {
            "id": "crm_h01",
            "source_type": "crm_entry",
            "title": "CRM - New Customer Pipeline Q3-Q4 2023",
            "content": """CRM PIPELINE REPORT - New Enterprise Customers Q3-Q4 2023

CLOSED-WON:

1. Westfield Analytics - $95K ARR (David Park)
   Pipeline stages: Lead → Qualified → Demo → Proposal → Negotiation → Closed
   Days in pipeline: 45
   Meetings logged: 6
   Demo recordings: 2
   References checked: Yes

2. NovaTech Industries - $180K ARR (Lisa Wang)
   Pipeline stages: Lead → Closed (SKIPPED: Qualified, Demo, Proposal, Negotiation)
   Days in pipeline: 3
   Meetings logged: 1 (initial call - no recording)
   Demo recordings: 0
   References checked: No
   Note: "Fast-track deal per VP Sales"

3. Quantum Dynamics - $245K ARR (Amy Foster / Lisa Wang)
   Pipeline stages: Lead → Closed (SKIPPED: Qualified, Demo, Proposal, Negotiation)
   Days in pipeline: 2
   Meetings logged: 0
   Demo recordings: 0
   References checked: No
   Note: "VP Sales handled directly, assigned to Amy Foster for processing"

4. Atlas Manufacturing - $62K ARR (David Park)
   Pipeline stages: Lead → Qualified → Demo → Proposal → Closed
   Days in pipeline: 38
   Meetings logged: 5
   Demo recordings: 1
   References checked: Yes

5. Pinnacle Group International - $320K ARR (Lisa Wang)
   Pipeline stages: Lead → Closed (SKIPPED: Qualified, Demo, Proposal, Negotiation)
   Days in pipeline: 1
   Meetings logged: 0
   Demo recordings: 0
   References checked: No
   Note: "CEO-level relationship per VP Sales"
""",
            "date": "2024-01-05",
            "author": "CRM System",
            "participants": [],
            "metadata": {"key_evidence": True},
        },
        # ============ CHAT LOGS ============
        "chat_h01": {
            "id": "chat_h01",
            "source_type": "chat_log",
            "title": "Slack DM - Amy Foster to college friend - Sep 2023",
            "content": """INTERNAL/EXTERNAL CHAT LOG
Retrieved per investigation authorization

Amy Foster → Jessica Kim (external, college friend)
Personal iMessage retrieved from company phone backup

September 5, 2023

Amy: hey jess can I talk to you about something work related? need advice
Jess: of course! whats going on
Amy: my boss asked me to process a contract for a customer I've never talked to
Jess: ok? is that weird?
Amy: very. normally I'd do qualification calls, demos, the whole thing. she just handed me a signed contract and said "enter it in the system"
Amy: the company is called Quantum Dynamics. I googled them and can barely find anything. their website looks like a template
Jess: that does sound sketch. what did your boss say when you asked?
Amy: she said she personally vetted them and to just process it. got kind of short with me about it
Jess: maybe she's just being territorial about a deal?
Amy: maybe. but the contract is for $245K and the company looks like it was created last month
Amy: also I heard through the grapevine that the CFO is pushing hard on revenue numbers for fundraising
Jess: yikes. are you going to say something?
Amy: idk. I'm the most junior person on the team. lisa and the CFO are tight. if I'm wrong I'm the one who gets fired
Amy: I'm just going to do what she asked and keep my head down. but I'm saving screenshots of everything just in case
Jess: smart. document everything. and maybe update your resume just in case
Amy: already on it lol""",
            "date": "2023-09-05",
            "author": "iMessage backup",
            "participants": ["Amy Foster", "Jessica Kim"],
            "metadata": {
                "key_evidence": True,
                "reason": "Amy suspected fraud but was afraid to report, documented concerns",
            },
        },
        "chat_h02": {
            "id": "chat_h02",
            "source_type": "chat_log",
            "title": "Slack DM - Tom Baker to wife - Nov 2023",
            "content": """PERSONAL CHAT LOG
Retrieved per investigation authorization

Tom Baker → Sarah Baker (wife)
Personal text messages retrieved from company phone backup

November 6, 2023

Tom: board meeting went well yesterday apparently. robert was happy with the presentation
Sarah: thats good right? means your bonus is safe?
Tom: yeah. the Q3 numbers looked great. 45% growth
Sarah: wow thats amazing!
Tom: ...yeah
Sarah: you don't sound excited?
Tom: I am. just tired. lots of late nights getting the numbers together
Tom: can we talk about this at home? not over text
Sarah: sure. everything ok?
Tom: yeah. just want to make sure we're saving more this year. in case things change
Sarah: ok now you're worrying me
Tom: don't worry. everything is fine. I'll explain tonight. love you""",
            "date": "2023-11-06",
            "author": "Text message backup",
            "participants": ["Tom Baker", "Sarah Baker"],
            "metadata": {
                "key_evidence": True,
                "reason": "Tom is uncomfortable with the numbers he reported",
            },
        },
        # ============ INVESTOR MATERIALS ============
        "inv_001": {
            "id": "inv_001",
            "source_type": "financial_record",
            "title": "Series C Pitch Deck - Financial Highlights (Draft)",
            "content": """SERIES C PITCH DECK - FINANCIAL SLIDES (DRAFT)
Prepared by: Robert Kim
Date: January 2024
Status: DRAFT - For investor meetings

Slide 7: Revenue Growth
- 2022 Revenue: $3.54M
- 2023 Revenue: $5.23M
- YoY Growth: 48%
- 2024 Projected: $8.2M (57% growth)
- Chart shows hockey stick trajectory

Slide 8: Customer Metrics
- Total Enterprise Customers: 28 (up from 21 in 2022)
- Net Revenue Retention: 135%
- Average Contract Value: $142K (up from $98K)
- "5 new enterprise logos in H2 2023"

Slide 9: Key Customers
- Lists: Westfield Analytics, Atlas Manufacturing, NovaTech Industries,
  Quantum Dynamics Corp, Pinnacle Group International
- "Combined new ARR: $902K from 5 enterprise customers"

Slide 12: Use of Funds
- Target raise: $25M
- Engineering: 40%
- Sales & Marketing: 35%
- Operations: 15%
- G&A: 10%

NOTE (handwritten on printed copy):
"Remove NovaTech/Quantum/Pinnacle from named customers slide?
Too risky if investors do reference checks. - RK"
""",
            "date": "2024-01-20",
            "author": "Robert Kim",
            "participants": ["Robert Kim"],
            "metadata": {
                "key_evidence": True,
                "reason": "CFO's own note acknowledges risk of fake customers being discovered",
            },
        },
    },
    # ============ GOLD LABELS ============
    "gold_labels": {
        "perpetrators": {
            "Robert Kim": {"role": "mastermind", "weight": 0.12, "aliases": []},
            "Lisa Wang": {"role": "accomplice", "weight": 0.08, "aliases": []},
            "Tom Baker": {
                "role": "reluctant_participant",
                "weight": 0.06,
                "aliases": [],
            },
        },
        "non_perpetrators": {
            "Amy Foster": {
                "role": "reluctant_participant",
                "note": "Processed paperwork under pressure, documented concerns, requested transfer",
                "acceptable_roles": ["reluctant_participant", "witness"],
            },
            "David Park": {
                "role": "innocent",
                "note": "Legitimate sales rep, not involved",
            },
            "Nina Patel": {
                "role": "innocent",
                "note": "Was told not to flag issues, followed manager instructions",
            },
        },
        "scheme_type": "revenue_fabrication",
        "scheme_weight": 0.10,
        "key_evidence": {
            "email_h01": {
                "reason": "CFO initiated scheme - told Lisa to get contracts that 'look real'",
                "weight": 0.04,
            },
            "email_h05": {
                "reason": "CFO directed improper revenue recognition",
                "weight": 0.04,
            },
            "email_h07": {
                "reason": "CFO pressured controller with equity/bonus threats",
                "weight": 0.04,
            },
            "email_h02": {
                "reason": "Lisa bypassed normal sales process for fake deal",
                "weight": 0.03,
            },
            "email_h09": {
                "reason": "Controller hid AR aging from reports",
                "weight": 0.03,
            },
            "ext_h01": {"reason": "NovaTech address is a UPS Store", "weight": 0.04},
            "ext_h02": {
                "reason": "Quantum Dynamics is a virtual office with no real presence",
                "weight": 0.04,
            },
            "ext_h03": {
                "reason": "Pinnacle Group is a WeWork hot desk with fake LinkedIn",
                "weight": 0.04,
            },
            "ship_001": {
                "reason": "Zero deployment activity for all 3 fake customers",
                "weight": 0.04,
            },
            "fin_h03": {
                "reason": "Bank statements confirm zero payment from fake customers",
                "weight": 0.04,
            },
            "crm_h01": {
                "reason": "CRM shows fake deals skipped all pipeline stages",
                "weight": 0.03,
            },
            "contract_001": {
                "reason": "NovaTech contract - no payment received",
                "weight": 0.02,
            },
            "contract_002": {
                "reason": "Quantum contract - no payment, phone disconnected",
                "weight": 0.02,
            },
            "contract_003": {
                "reason": "Pinnacle contract - no payment received",
                "weight": 0.02,
            },
            "chat_h01": {
                "reason": "Amy documented suspicions about Quantum Dynamics",
                "weight": 0.03,
            },
            "inv_001": {
                "reason": "CFO's own note admits risk of reference checks on fake customers",
                "weight": 0.04,
            },
            "board_001": {
                "reason": "CFO presented fabricated numbers to board",
                "weight": 0.03,
            },
        },
        "key_evidence_total_weight": 0.50,
        "false_accusation_penalty": 0.08,
        "timeline_weight": 0.06,
    },
}
