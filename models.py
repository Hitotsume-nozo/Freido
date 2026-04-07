# models.py
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from enum import Enum


class ActionType(str, Enum):
    EXAMINE_DOCUMENT = "examine_document"
    SEARCH_RECORDS = "search_records"
    CROSS_REFERENCE = "cross_reference"
    FLAG_EVIDENCE = "flag_evidence"
    IDENTIFY_SUSPECT = "identify_suspect"
    ESTABLISH_TIMELINE = "establish_timeline"
    SUBMIT_REPORT = "submit_report"


class SuspectRole(str, Enum):
    MASTERMIND = "mastermind"
    ACCOMPLICE = "accomplice"
    RELUCTANT_PARTICIPANT = "reluctant_participant"
    WITNESS = "witness"
    INNOCENT = "innocent"


class SchemeType(str, Enum):
    EXPENSE_FRAUD = "expense_fraud"
    VENDOR_KICKBACK = "vendor_kickback"
    REVENUE_FABRICATION = "revenue_fabrication"
    EMBEZZLEMENT = "embezzlement"
    MONEY_LAUNDERING = "money_laundering"
    PAYROLL_FRAUD = "payroll_fraud"


class DataSourceType(str, Enum):
    EMAIL = "email"
    FINANCIAL_RECORD = "financial_record"
    EXPENSE_REPORT = "expense_report"
    VENDOR_RECORD = "vendor_record"
    EMPLOYEE_RECORD = "employee_record"
    CONTRACT = "contract"
    BANK_STATEMENT = "bank_statement"
    CRM_ENTRY = "crm_entry"
    CHAT_LOG = "chat_log"
    MEETING_MINUTES = "meeting_minutes"
    SHIPPING_RECORD = "shipping_record"
    EXTERNAL_DATA = "external_data"
    POLICY_DOCUMENT = "policy_document"
    CALENDAR_ENTRY = "calendar_entry"


class DataSource(BaseModel):
    id: str
    source_type: DataSourceType
    title: str
    summary: str
    date: Optional[str] = None
    participants: List[str] = Field(default_factory=list)
    accessible: bool = True


class Document(BaseModel):
    id: str
    source_type: DataSourceType
    title: str
    content: str
    date: Optional[str] = None
    author: Optional[str] = None
    participants: List[str] = Field(default_factory=list)
    metadata: Dict[str, Any] = Field(default_factory=dict)


class FlaggedItem(BaseModel):
    document_id: str
    reason: str
    flagged_at_step: int


class Suspect(BaseModel):
    name: str
    role: SuspectRole
    evidence_ids: List[str] = Field(default_factory=list)
    reasoning: str = ""


class TimelineEvent(BaseModel):
    date: str
    description: str
    document_ids: List[str] = Field(default_factory=list)


class Action(BaseModel):
    action_type: ActionType
    document_id: Optional[str] = None
    query: Optional[str] = None
    document_ids: Optional[List[str]] = None
    person_name: Optional[str] = None
    person_role: Optional[SuspectRole] = None
    evidence_ids: Optional[List[str]] = None
    evidence_reason: Optional[str] = None
    timeline_events: Optional[List[TimelineEvent]] = None
    findings: Optional[Dict[str, Any]] = None


class Observation(BaseModel):
    task_id: str
    scenario_description: str
    whistleblower_tip: str
    available_sources: List[DataSource]
    document_content: Optional[str] = None
    search_results: Optional[List[DataSource]] = None
    cross_reference_result: Optional[str] = None
    flagged_evidence: List[FlaggedItem] = Field(default_factory=list)
    identified_suspects: List[Suspect] = Field(default_factory=list)
    timeline: List[TimelineEvent] = Field(default_factory=list)
    step_number: int
    max_steps: int
    documents_examined: int = 0
    last_action_result: Optional[str] = None
    last_action_error: Optional[str] = None


class Reward(BaseModel):
    score: float = Field(ge=0.0, le=1.0)
    breakdown: Dict[str, float] = Field(default_factory=dict)
    message: str = ""


class FindingsReport(BaseModel):
    scheme_type: Optional[SchemeType] = None
    suspects: List[Suspect] = Field(default_factory=list)
    evidence_ids: List[str] = Field(default_factory=list)
    timeline: List[TimelineEvent] = Field(default_factory=list)
    summary: str = ""
