# tasks/medium.py
"""Task 2 - Medium: The Vendor Kickback"""

MEDIUM_TASK = {
    "task_id": "medium",
    "description": "Investigate a tip about procurement fraud involving a vendor receiving preferential treatment and inflated contract values.",
    "whistleblower_tip": "Anonymous tip received: 'Something is off with our vendor contracts. Apex Solutions keeps winning bids even though their prices are way above market rate. The procurement lead Sarah Martinez always pushes for them. I think there might be a personal connection. Also look at who approved these - James Wilson flagged concerns months ago but then suddenly stopped objecting.'",
    "max_steps": 30,
    "documents": {
        # ============ EMPLOYEE RECORDS ============
        "emp_m01": {
            "id": "emp_m01",
            "source_type": "employee_record",
            "title": "Employee Record - Sarah Martinez",
            "content": """EMPLOYEE RECORD
Name: Sarah Martinez (née Sarah Reeves)
Employee ID: EMP-2018-0312
Department: Procurement
Title: Senior Procurement Lead
Manager: VP Operations
Start Date: 2018-05-14
Salary: $105,000/year
Office: Chicago
Emergency Contact: Maria Reeves (mother)
Spouse: Carlos Martinez
Notes: Manages vendor relationships for IT and office supplies.
Annual performance reviews consistently 'exceeds expectations.'""",
            "date": "2024-01-01",
            "author": "HR Department",
            "participants": ["Sarah Martinez"],
            "metadata": {
                "department": "Procurement",
                "maiden_name": "Reeves",
                "spouse": "Carlos Martinez",
            },
        },
        "emp_m02": {
            "id": "emp_m02",
            "source_type": "employee_record",
            "title": "Employee Record - James Wilson",
            "content": """EMPLOYEE RECORD
Name: James Wilson
Employee ID: EMP-2019-0289
Department: Finance
Title: Senior Financial Analyst
Manager: CFO
Start Date: 2019-02-01
Salary: $92,000/year
Office: Chicago
Notes: Responsible for vendor payment approval and cost analysis.
Performance note (Q3 2023): "James raised valid cost concerns about several
vendor contracts but has since aligned with procurement's recommendations."
Disciplinary: None""",
            "date": "2024-01-01",
            "author": "HR Department",
            "participants": ["James Wilson"],
            "metadata": {"department": "Finance"},
        },
        "emp_m03": {
            "id": "emp_m03",
            "source_type": "employee_record",
            "title": "Employee Record - Tom Bradley",
            "content": """EMPLOYEE RECORD
Name: Tom Bradley
Employee ID: EMP-2020-0401
Department: Procurement
Title: Procurement Analyst
Manager: Sarah Martinez
Start Date: 2020-07-15
Salary: $68,000/year
Office: Chicago
Notes: Assists with vendor evaluation and bid analysis. Reports to Sarah Martinez.""",
            "date": "2024-01-01",
            "author": "HR Department",
            "participants": ["Tom Bradley"],
            "metadata": {"department": "Procurement"},
        },
        "emp_m04": {
            "id": "emp_m04",
            "source_type": "employee_record",
            "title": "Employee Record - Diana Foster",
            "content": """EMPLOYEE RECORD
Name: Diana Foster
Employee ID: EMP-2017-0156
Department: IT
Title: IT Director
Manager: CTO
Start Date: 2017-09-01
Salary: $130,000/year
Office: Chicago
Notes: Submits IT procurement requests. No involvement in vendor selection process.""",
            "date": "2024-01-01",
            "author": "HR Department",
            "participants": ["Diana Foster"],
            "metadata": {"department": "IT"},
        },
        # ============ VENDOR RECORDS ============
        "vendor_001": {
            "id": "vendor_001",
            "source_type": "vendor_record",
            "title": "Vendor Profile - Apex Solutions LLC",
            "content": """VENDOR PROFILE
Company: Apex Solutions LLC
Vendor ID: V-2022-0089
Address: 1847 Industrial Parkway, Suite 300, Naperville, IL 60563
Registered Agent: Carlos Martinez-Reeves
Incorporation Date: January 15, 2022
State: Illinois
Business Type: IT consulting and equipment supply
Annual Revenue (reported): $1.2M
Employees: 4
Primary Contact: Michael Torres, Sales Director
Phone: (630) 555-0198

BANK DETAILS ON FILE:
First National Bank, Account ending in 7834

VENDOR RATING: Preferred (upgraded from Standard on March 2023 by Sarah Martinez)""",
            "date": "2024-01-01",
            "author": "Vendor Management System",
            "participants": [],
            "metadata": {
                "registered_agent": "Carlos Martinez-Reeves",
                "key_evidence": True,
            },
        },
        "vendor_002": {
            "id": "vendor_002",
            "source_type": "vendor_record",
            "title": "Vendor Profile - TechSupply Corp",
            "content": """VENDOR PROFILE
Company: TechSupply Corp
Vendor ID: V-2019-0034
Address: 500 Technology Drive, Schaumburg, IL 60173
Incorporation Date: 2015
Business Type: IT equipment and services
Annual Revenue: $45M
Employees: 120
Primary Contact: Rachel Green, Account Manager
Vendor Rating: Standard
Notes: Long-standing vendor. Competitive pricing. Lost several recent bids to Apex Solutions.""",
            "date": "2024-01-01",
            "author": "Vendor Management System",
            "participants": [],
            "metadata": {},
        },
        "vendor_003": {
            "id": "vendor_003",
            "source_type": "vendor_record",
            "title": "Vendor Profile - Meridian IT Services",
            "content": """VENDOR PROFILE
Company: Meridian IT Services
Vendor ID: V-2020-0056
Address: 200 Commerce Blvd, Evanston, IL 60201
Business Type: IT consulting
Annual Revenue: $28M
Employees: 85
Vendor Rating: Standard
Notes: Submitted bids for 3 contracts in 2023, won 0. Pricing was within 5% of market rate.""",
            "date": "2024-01-01",
            "author": "Vendor Management System",
            "participants": [],
            "metadata": {},
        },
        # ============ PROCUREMENT RECORDS ============
        "proc_001": {
            "id": "proc_001",
            "source_type": "financial_record",
            "title": "Procurement Contract - Network Equipment Q1 2023",
            "content": """PROCUREMENT CONTRACT
Contract ID: PC-2023-0034
Description: Network switches and routers for office upgrade
Date Awarded: February 15, 2023
Vendor Selected: Apex Solutions LLC
Contract Value: $187,000
Bid Comparison:
  - Apex Solutions: $187,000
  - TechSupply Corp: $134,000 (LOWEST BID)
  - Meridian IT: $141,000
Selection Justification (by Sarah Martinez):
"Apex Solutions offers superior service guarantees and faster delivery timeline.
Their technical specifications exceed requirements."
Approved by: James Wilson (Finance), Sarah Martinez (Procurement)
Notes: TechSupply Corp filed informal complaint about selection criteria.""",
            "date": "2023-02-15",
            "author": "Sarah Martinez",
            "participants": ["Sarah Martinez", "James Wilson"],
            "metadata": {"apex_premium": "39.6%", "key_evidence": True},
        },
        "proc_002": {
            "id": "proc_002",
            "source_type": "financial_record",
            "title": "Procurement Contract - Server Infrastructure Q2 2023",
            "content": """PROCUREMENT CONTRACT
Contract ID: PC-2023-0067
Description: Server hardware and installation for data center expansion
Date Awarded: May 22, 2023
Vendor Selected: Apex Solutions LLC
Contract Value: $342,000
Bid Comparison:
  - Apex Solutions: $342,000
  - TechSupply Corp: $245,000 (LOWEST BID)
  - DataCore Systems: $258,000
Selection Justification (by Sarah Martinez):
"Apex Solutions provides end-to-end installation support and 24/7 maintenance
that other vendors cannot match at this scale."
Approved by: James Wilson (Finance), Sarah Martinez (Procurement)""",
            "date": "2023-05-22",
            "author": "Sarah Martinez",
            "participants": ["Sarah Martinez", "James Wilson"],
            "metadata": {"apex_premium": "39.6%", "key_evidence": True},
        },
        "proc_003": {
            "id": "proc_003",
            "source_type": "financial_record",
            "title": "Procurement Contract - Software Licenses Q3 2023",
            "content": """PROCUREMENT CONTRACT
Contract ID: PC-2023-0098
Description: Enterprise software license renewal and new seats
Date Awarded: August 10, 2023
Vendor Selected: Apex Solutions LLC
Contract Value: $156,000
Bid Comparison:
  - Apex Solutions: $156,000
  - SoftwareDirect: $112,000 (LOWEST BID)
  - TechSupply Corp: $118,000
Selection Justification (by Sarah Martinez):
"Consolidating with Apex Solutions for volume discount potential
across all IT procurement."
Approved by: James Wilson (Finance), Sarah Martinez (Procurement)""",
            "date": "2023-08-10",
            "author": "Sarah Martinez",
            "participants": ["Sarah Martinez", "James Wilson"],
            "metadata": {"apex_premium": "39.3%", "key_evidence": True},
        },
        "proc_004": {
            "id": "proc_004",
            "source_type": "financial_record",
            "title": "Procurement Contract - Office Supplies Q4 2023",
            "content": """PROCUREMENT CONTRACT
Contract ID: PC-2023-0112
Description: Annual office supplies and furniture
Date Awarded: November 5, 2023
Vendor Selected: OfficeMax Direct
Contract Value: $45,000
Bid Comparison:
  - OfficeMax Direct: $45,000 (LOWEST BID)
  - SupplyCo: $47,500
Selection Justification (by Sarah Martinez):
"Standard selection - lowest qualified bid."
Approved by: James Wilson (Finance), Sarah Martinez (Procurement)""",
            "date": "2023-11-05",
            "author": "Sarah Martinez",
            "participants": ["Sarah Martinez", "James Wilson"],
            "metadata": {"note": "Legitimate procurement - red herring"},
        },
        "proc_005": {
            "id": "proc_005",
            "source_type": "financial_record",
            "title": "Procurement Contract - Cybersecurity Q1 2024",
            "content": """PROCUREMENT CONTRACT
Contract ID: PC-2024-0015
Description: Cybersecurity software suite and monitoring
Date Awarded: January 30, 2024
Vendor Selected: Apex Solutions LLC
Contract Value: $278,000
Bid Comparison:
  - Apex Solutions: $278,000
  - CyberGuard Pro: $195,000 (LOWEST BID)
  - TechSupply Corp: $201,000
Selection Justification (by Sarah Martinez):
"Apex Solutions' integrated approach with our existing infrastructure
makes them the only viable option for seamless deployment."
Approved by: James Wilson (Finance), Sarah Martinez (Procurement)
NOTE: Finance flagged this contract for review but flag was removed 3 days later.""",
            "date": "2024-01-30",
            "author": "Sarah Martinez",
            "participants": ["Sarah Martinez", "James Wilson"],
            "metadata": {"apex_premium": "42.6%", "key_evidence": True},
        },
        # ============ MARKET PRICE DATA ============
        "market_001": {
            "id": "market_001",
            "source_type": "external_data",
            "title": "IT Equipment Market Price Report 2023-2024",
            "content": """MARKET PRICE ANALYSIS - IT Equipment & Services
Source: Industry Benchmark Report, Q4 2023

Average market prices for comparable contracts:
- Network equipment (enterprise, 200+ nodes): $125,000 - $150,000
- Server infrastructure (mid-size data center): $230,000 - $270,000
- Enterprise software licenses (500 seats): $105,000 - $125,000
- Cybersecurity suite (enterprise): $180,000 - $210,000

Note: Prices above represent median competitive bids. Premiums above 15%
typically indicate either specialized requirements or non-competitive procurement.

Apex Solutions LLC is NOT listed in any major IT vendor directory or
industry certification database (CompTIA, Gartner, etc.)""",
            "date": "2024-01-15",
            "author": "Industry Analysis Group",
            "participants": [],
            "metadata": {"key_evidence": True},
        },
        # ============ EMAILS ============
        "email_m01": {
            "id": "email_m01",
            "source_type": "email",
            "title": "Email: James Wilson to Sarah Martinez - Feb 2023",
            "content": """FROM: james.wilson@company.com
TO: sarah.martinez@company.com
DATE: February 10, 2023, 2:30 PM
SUBJECT: Concerns about Apex Solutions bid

Sarah,

I've reviewed the bids for the network equipment contract. Apex Solutions
is coming in at $187K - that's nearly 40% above TechSupply's bid of $134K.
I can't find justification for this premium in their proposal. Their
"superior service guarantees" aren't substantially different from TechSupply's
standard SLA.

I'm not comfortable approving this without a better explanation for the
cost difference.

James""",
            "date": "2023-02-10",
            "author": "James Wilson",
            "participants": ["James Wilson", "Sarah Martinez"],
            "metadata": {"key_evidence": True},
        },
        "email_m02": {
            "id": "email_m02",
            "source_type": "email",
            "title": "Email: Sarah Martinez to James Wilson - Feb 2023",
            "content": """FROM: sarah.martinez@company.com
TO: james.wilson@company.com
DATE: February 10, 2023, 4:15 PM
SUBJECT: RE: Concerns about Apex Solutions bid

James,

I understand the price difference looks significant, but I've worked
with Apex before and their delivery and support are genuinely in a
different league. TechSupply has had delivery delays on 3 of their
last 5 contracts industry-wide.

Let's discuss offline. I can walk you through the technical
differentiation in more detail. Coffee tomorrow?

Sarah""",
            "date": "2023-02-10",
            "author": "Sarah Martinez",
            "participants": ["James Wilson", "Sarah Martinez"],
            "metadata": {},
        },
        "email_m03": {
            "id": "email_m03",
            "source_type": "email",
            "title": "Email: James Wilson to CFO - May 2023",
            "content": """FROM: james.wilson@company.com
TO: cfo@company.com
DATE: May 18, 2023, 11:00 AM
SUBJECT: Vendor cost concerns - CONFIDENTIAL

Hi,

I wanted to flag something that's been bothering me. This is the second
major IT contract going to Apex Solutions at significantly above-market
rates. The server contract bid is $342K vs TechSupply at $245K - that's
a 40% premium again.

Sarah's justifications sound reasonable on paper but I'm seeing a pattern.
I'd like to recommend a procurement audit.

Regards,
James""",
            "date": "2023-05-18",
            "author": "James Wilson",
            "participants": ["James Wilson", "CFO"],
            "metadata": {"key_evidence": True},
        },
        "email_m04": {
            "id": "email_m04",
            "source_type": "email",
            "title": "Email: CFO to James Wilson - May 2023",
            "content": """FROM: cfo@company.com
TO: james.wilson@company.com
DATE: May 19, 2023, 9:30 AM
SUBJECT: RE: Vendor cost concerns - CONFIDENTIAL

James,

Thanks for flagging. I'll mention it to the VP of Operations but honestly
procurement decisions have been Sarah's domain and her results have been
solid overall. Let's keep an eye on it but I don't want to create friction
with the ops team right now - we're in the middle of the expansion.

Approve the contract for now and we'll revisit in Q4.

Thanks""",
            "date": "2023-05-19",
            "author": "CFO",
            "participants": ["James Wilson", "CFO"],
            "metadata": {},
        },
        "email_m05": {
            "id": "email_m05",
            "source_type": "email",
            "title": "Email: Sarah Martinez to James Wilson - Aug 2023",
            "content": """FROM: sarah.martinez@company.com
TO: james.wilson@company.com
DATE: August 8, 2023, 5:45 PM
SUBJECT: Software license contract

James,

Heads up - the software license contract is going to Apex Solutions.
I know you've had concerns in the past but I've negotiated favorable
terms and they're bundling maintenance that would cost extra with other vendors.

I hope we can move forward without the back-and-forth this time. I've
already discussed with VP Ops and they're supportive.

Thanks for your cooperation,
Sarah""",
            "date": "2023-08-08",
            "author": "Sarah Martinez",
            "participants": ["James Wilson", "Sarah Martinez"],
            "metadata": {
                "key_evidence": True,
                "reason": "Pressure on James to stop objecting",
            },
        },
        "email_m06": {
            "id": "email_m06",
            "source_type": "email",
            "title": "Email: James Wilson to personal email - Aug 2023",
            "content": """FROM: james.wilson@company.com
TO: jwilson.personal@gmail.com
DATE: August 8, 2023, 6:30 PM
SUBJECT: FW: Software license contract

[Forwarded message from Sarah Martinez]

Note to self: Something is definitely wrong here but CFO told me to
drop it and Sarah is making it clear I should stop pushing back.
Keeping a record of everything just in case. Third contract to Apex
at ~40% premium. Saving copies of all bid comparisons at home.

Not sure what to do. Don't want to be the troublemaker but this
doesn't pass the smell test.""",
            "date": "2023-08-08",
            "author": "James Wilson",
            "participants": ["James Wilson"],
            "metadata": {
                "key_evidence": True,
                "reason": "Shows James was pressured into silence",
            },
        },
        "email_m07": {
            "id": "email_m07",
            "source_type": "email",
            "title": "Email: Sarah Martinez to personal email - Jan 2024",
            "content": """FROM: sarah.martinez@company.com
TO: s.martinez.home@gmail.com
DATE: January 25, 2024, 7:12 PM
SUBJECT: no subject

C says the cybersecurity contract needs to close by end of month.
Told him to keep the bid under 300 this time - J almost caused problems
last round. Need to be more careful with the justification language.

Remind C: separate account for the consulting fees. Don't use the
joint one anymore.""",
            "date": "2024-01-25",
            "author": "Sarah Martinez",
            "participants": ["Sarah Martinez"],
            "metadata": {
                "key_evidence": True,
                "reason": "'C' is Carlos (husband), 'J' is James Wilson, mentions separate accounts",
            },
        },
        # ============ FINANCIAL DISCLOSURES ============
        "fin_m01": {
            "id": "fin_m01",
            "source_type": "financial_record",
            "title": "Employee Financial Disclosure - Sarah Martinez 2023",
            "content": """ANNUAL FINANCIAL DISCLOSURE
Employee: Sarah Martinez
Year: 2023
Required per company Conflict of Interest Policy

Outside Business Interests: None declared
Family Business Interests: None declared
Potential Conflicts of Interest: None declared

Spouse Name: Carlos Martinez
Spouse Employer: Self-employed consultant (marketing)

Signed: Sarah Martinez
Date: January 15, 2024""",
            "date": "2024-01-15",
            "author": "Sarah Martinez",
            "participants": ["Sarah Martinez"],
            "metadata": {
                "key_evidence": True,
                "reason": "Failed to disclose husband's connection to Apex Solutions",
            },
        },
        # ============ CORPORATE REGISTRY ============
        "ext_m01": {
            "id": "ext_m01",
            "source_type": "external_data",
            "title": "Illinois Corporate Registry - Apex Solutions LLC",
            "content": """ILLINOIS SECRETARY OF STATE - BUSINESS ENTITY SEARCH

Entity Name: Apex Solutions LLC
File Number: LLC-2022-00891234
Status: Active
Formation Date: January 15, 2022
Registered Agent: Carlos Martinez-Reeves
Agent Address: 1847 Industrial Parkway, Suite 300, Naperville, IL 60563

Members/Managers:
  - Carlos Martinez-Reeves (Managing Member, 80%)
  - Michael Torres (Member, 20%)

Annual Report Filed: Yes (2023, 2024)

RELATED ENTITIES:
Carlos Martinez-Reeves is also registered agent for:
  - CMR Consulting LLC (formed 2020, Status: Active)
  - Reeves Family Trust (formed 2019)""",
            "date": "2024-03-01",
            "author": "IL Secretary of State",
            "participants": [],
            "metadata": {
                "key_evidence": True,
                "reason": "Carlos Martinez-Reeves = Carlos Martinez (Sarah's husband) using his wife's maiden name (Reeves)",
            },
        },
        # ============ MEETING MINUTES ============
        "meet_m01": {
            "id": "meet_m01",
            "source_type": "meeting_minutes",
            "title": "Procurement Review Meeting - Q3 2023",
            "content": """PROCUREMENT REVIEW MEETING MINUTES
Date: September 15, 2023
Attendees: Sarah Martinez, Tom Bradley, Diana Foster, VP Operations

Agenda: Q3 Vendor Performance Review

1. IT Procurement Summary:
   Sarah presented Q3 procurement results. Total IT spend: $685,000.
   Noted strong performance from Apex Solutions across all contracts.

2. Vendor Consolidation Strategy:
   Sarah proposed consolidating IT procurement with fewer vendors for
   "volume discounts and operational simplicity." Recommended Apex Solutions
   as primary IT vendor going forward.

3. Diana Foster raised question about whether Apex Solutions has
   capacity to handle consolidated volume given their small size (4 employees).
   Sarah assured that Apex is "scaling rapidly."

4. Tom Bradley noted that bid documentation for recent contracts was
   "thorough and well-organized."

Action Items:
- Sarah to prepare vendor consolidation proposal for Q4
- Tom to compile vendor performance metrics

NOTE: James Wilson was invited but did not attend.""",
            "date": "2023-09-15",
            "author": "Tom Bradley",
            "participants": ["Sarah Martinez", "Tom Bradley", "Diana Foster"],
            "metadata": {},
        },
        # ============ BANK RECORDS ============
        "bank_m01": {
            "id": "bank_m01",
            "source_type": "bank_statement",
            "title": "Company Payment Records to Apex Solutions 2023-2024",
            "content": """ACCOUNTS PAYABLE - PAYMENT HISTORY
Vendor: Apex Solutions LLC (V-2022-0089)

2023:
Feb 28 - $187,000 (PC-2023-0034, Network Equipment)
Jun 15 - $342,000 (PC-2023-0067, Server Infrastructure)
Sep 01 - $156,000 (PC-2023-0098, Software Licenses)

2024:
Feb 15 - $278,000 (PC-2024-0015, Cybersecurity)

TOTAL PAID TO APEX SOLUTIONS: $963,000

All payments to: First National Bank, Account ending 7834
Payment method: Wire transfer
Approved by: James Wilson (Finance)

NOTE: Apex Solutions has no outstanding invoices or payment disputes.
Payment terms: Net-30, all paid within terms.""",
            "date": "2024-03-01",
            "author": "Accounts Payable System",
            "participants": [],
            "metadata": {"total_paid": 963000},
        },
        # ============ CHAT LOGS ============
        "chat_m01": {
            "id": "chat_m01",
            "source_type": "chat_log",
            "title": "Slack DM - Tom Bradley to friend - Oct 2023",
            "content": """INTERNAL CHAT LOG - PRIVATE CHANNEL
Retrieved per investigation authorization

Tom Bradley → Alex Chen (Engineering, friend)
October 3, 2023

Tom: hey can I ask you something in confidence?
Alex: sure whats up
Tom: does it seem weird to you that we keep using the same vendor for everything IT?
Alex: idk I don't deal with procurement. which vendor?
Tom: Apex Solutions. Sarah pushes them for every contract. their prices are way higher than everyone else
Alex: maybe they're just better?
Tom: they have 4 employees dude. we're paying them almost a million dollars
Alex: lol that is a lot. have you said anything?
Tom: no way. Sarah's my boss. last time someone questioned her vendor picks (james from finance) she basically shut him down. I just do the paperwork
Alex: yeah I wouldn't rock the boat either. probably just has a good relationship with them
Tom: yeah probably. forget I said anything""",
            "date": "2023-10-03",
            "author": "Slack System",
            "participants": ["Tom Bradley", "Alex Chen"],
            "metadata": {
                "key_evidence": True,
                "reason": "Tom noticed pattern but was afraid to report",
            },
        },
    },
    # ============ GOLD LABELS ============
    "gold_labels": {
        "perpetrators": {
            "Sarah Martinez": {"role": "mastermind", "weight": 0.20},
            "Carlos Martinez": {
                "role": "accomplice",
                "aliases": ["Carlos Martinez-Reeves"],
                "weight": 0.10,
            },
        },
        "non_perpetrators": {
            "James Wilson": {
                "role": "witness",
                "note": "Raised concerns but was pressured into silence",
            },
            "Tom Bradley": {
                "role": "witness",
                "note": "Noticed pattern but afraid to report",
            },
        },
        "scheme_type": "vendor_kickback",
        "scheme_weight": 0.15,
        "key_evidence": {
            "vendor_001": {
                "reason": "Registered agent is Carlos Martinez-Reeves (Sarah's husband)",
                "weight": 0.06,
            },
            "ext_m01": {
                "reason": "Corporate registry confirms Carlos Martinez-Reeves owns Apex",
                "weight": 0.06,
            },
            "fin_m01": {
                "reason": "Sarah failed to disclose husband's business on conflict of interest form",
                "weight": 0.06,
            },
            "proc_001": {
                "reason": "First inflated contract - 40% above lowest bid",
                "weight": 0.04,
            },
            "proc_002": {
                "reason": "Second inflated contract - 40% above lowest bid",
                "weight": 0.04,
            },
            "proc_005": {
                "reason": "Fourth inflated contract - finance flag removed",
                "weight": 0.04,
            },
            "email_m01": {"reason": "James raised concerns early", "weight": 0.03},
            "email_m03": {"reason": "James escalated to CFO", "weight": 0.03},
            "email_m05": {
                "reason": "Sarah pressured James to stop objecting",
                "weight": 0.04,
            },
            "email_m07": {
                "reason": "Sarah's personal email reveals coordination with 'C' (Carlos)",
                "weight": 0.06,
            },
            "market_001": {
                "reason": "Apex not in any industry directory, prices 35-40% above market",
                "weight": 0.04,
            },
        },
        "key_evidence_total_weight": 0.45,
        "false_accusation_penalty": 0.10,
        "timeline_weight": 0.10,
    },
}
