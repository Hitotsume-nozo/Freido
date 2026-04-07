# environment.py
import copy
from typing import Tuple, Dict, Any, Optional, List
from models import (
    Action,
    ActionType,
    Observation,
    Reward,
    DataSource,
    DataSourceType,
    FlaggedItem,
    Suspect,
    TimelineEvent,
    SuspectRole,
    SchemeType,
    Document,
)
from graders import FraudInvestigationGrader
from tasks.easy import EASY_TASK
from tasks.medium import MEDIUM_TASK
from tasks.hard import HARD_TASK


TASKS = {
    "easy": EASY_TASK,
    "medium": MEDIUM_TASK,
    "hard": HARD_TASK,
}


class FraudInvestigationEnv:
    def __init__(self, task_id: str = "easy"):
        if task_id not in TASKS:
            raise ValueError(
                f"Unknown task_id: {task_id}. Choose from: {list(TASKS.keys())}"
            )
        self.task_id = task_id
        self.task_config = TASKS[task_id]
        self.documents: Dict[str, Dict] = {}
        self.gold_labels: Dict = {}
        self.grader: Optional[FraudInvestigationGrader] = None

        # Episode state
        self.flagged_evidence: List[FlaggedItem] = []
        self.identified_suspects: List[Suspect] = []
        self.timeline: List[TimelineEvent] = []
        self.examined_docs: set = set()
        self.step_count: int = 0
        self.max_steps: int = 0
        self.done: bool = False
        self.action_history: List[Action] = []
        self.last_content: Optional[str] = None
        self.last_search_results: Optional[List[DataSource]] = None
        self.last_cross_ref: Optional[str] = None
        self.last_action_result: Optional[str] = None
        self.submitted_scheme: Optional[str] = None

    def reset(self) -> Observation:
        self.documents = copy.deepcopy(self.task_config["documents"])
        self.gold_labels = copy.deepcopy(self.task_config["gold_labels"])
        self.grader = FraudInvestigationGrader(self.gold_labels)
        self.flagged_evidence = []
        self.identified_suspects = []
        self.timeline = []
        self.examined_docs = set()
        self.step_count = 0
        self.max_steps = self.task_config["max_steps"]
        self.done = False
        self.action_history = []
        self.last_content = None
        self.last_search_results = None
        self.last_cross_ref = None
        self.last_action_result = None
        self.submitted_scheme = None
        return self._build_observation()

    def step(self, action: Action) -> Tuple[Observation, Reward, bool, dict]:
        if self.done:
            obs = self._build_observation()
            reward = self._compute_reward()
            return obs, reward, True, {"error": "Episode already done"}

        self.step_count += 1
        error = None
        self.last_content = None
        self.last_search_results = None
        self.last_cross_ref = None

        try:
            self._apply_action(action)
        except Exception as e:
            error = str(e)
            self.last_action_result = f"Error: {error}"

        self.action_history.append(action)

        if action.action_type == ActionType.SUBMIT_REPORT:
            self.done = True
        elif self.step_count >= self.max_steps:
            self.done = True

        reward = self._compute_reward()
        obs = self._build_observation(error=error)
        info = {
            "steps_taken": self.step_count,
            "documents_examined": len(self.examined_docs),
            "evidence_flagged": len(self.flagged_evidence),
            "suspects_identified": len(self.identified_suspects),
        }

        return obs, reward, self.done, info

    def state(self) -> dict:
        return {
            "task_id": self.task_id,
            "step_count": self.step_count,
            "max_steps": self.max_steps,
            "done": self.done,
            "examined_docs": list(self.examined_docs),
            "flagged_evidence": [f.model_dump() for f in self.flagged_evidence],
            "identified_suspects": [s.model_dump() for s in self.identified_suspects],
            "timeline": [t.model_dump() for t in self.timeline],
            "action_history": [a.model_dump() for a in self.action_history],
        }

    def _apply_action(self, action: Action):
        if action.action_type == ActionType.EXAMINE_DOCUMENT:
            self._examine_document(action)
        elif action.action_type == ActionType.SEARCH_RECORDS:
            self._search_records(action)
        elif action.action_type == ActionType.CROSS_REFERENCE:
            self._cross_reference(action)
        elif action.action_type == ActionType.FLAG_EVIDENCE:
            self._flag_evidence(action)
        elif action.action_type == ActionType.IDENTIFY_SUSPECT:
            self._identify_suspect(action)
        elif action.action_type == ActionType.ESTABLISH_TIMELINE:
            self._establish_timeline(action)
        elif action.action_type == ActionType.SUBMIT_REPORT:
            self._submit_report(action)
        else:
            raise ValueError(f"Unknown action type: {action.action_type}")

    def _examine_document(self, action: Action):
        doc_id = action.document_id
        if not doc_id:
            raise ValueError("document_id required for examine_document")
        if doc_id not in self.documents:
            raise ValueError(f"Document not found: {doc_id}")
        doc = self.documents[doc_id]
        self.examined_docs.add(doc_id)
        self.last_content = doc["content"]
        self.last_action_result = f"Examined document: {doc['title']}"

    def _search_records(self, action: Action):
        query = action.query
        if not query:
            raise ValueError("query required for search_records")
        query_lower = query.lower()
        results = []
        for doc_id, doc in self.documents.items():
            searchable = (
                doc.get("title", "")
                + " "
                + doc.get("content", "")
                + " "
                + " ".join(doc.get("participants", []))
            ).lower()
            if query_lower in searchable:
                results.append(
                    DataSource(
                        id=doc_id,
                        source_type=DataSourceType(doc["source_type"]),
                        title=doc["title"],
                        summary=doc["content"][:150] + "...",
                        date=doc.get("date"),
                        participants=doc.get("participants", []),
                    )
                )
        self.last_search_results = results
        self.last_action_result = f"Search '{query}': {len(results)} results found"

    def _cross_reference(self, action: Action):
        doc_ids = action.document_ids
        if not doc_ids or len(doc_ids) < 2:
            raise ValueError("At least 2 document_ids required for cross_reference")
        docs = []
        for did in doc_ids:
            if did not in self.documents:
                raise ValueError(f"Document not found: {did}")
            docs.append(self.documents[did])
            self.examined_docs.add(did)

        # Build cross reference summary
        parts = []
        for i, doc in enumerate(docs):
            parts.append(f"--- Document {i + 1}: {doc['title']} ---\n{doc['content']}")
        self.last_cross_ref = "\n\n".join(parts)
        self.last_content = self.last_cross_ref
        self.last_action_result = f"Cross-referenced {len(doc_ids)} documents"

    def _flag_evidence(self, action: Action):
        doc_id = action.document_id
        reason = action.evidence_reason
        if not doc_id:
            raise ValueError("document_id required for flag_evidence")
        if not reason:
            raise ValueError("evidence_reason required for flag_evidence")
        if doc_id not in self.documents:
            raise ValueError(f"Document not found: {doc_id}")
        # Don't duplicate flags
        existing = {f.document_id for f in self.flagged_evidence}
        if doc_id not in existing:
            self.flagged_evidence.append(
                FlaggedItem(
                    document_id=doc_id,
                    reason=reason,
                    flagged_at_step=self.step_count,
                )
            )
        self.last_action_result = f"Flagged evidence: {doc_id}"

    def _identify_suspect(self, action: Action):
        name = action.person_name
        role = action.person_role
        if not name:
            raise ValueError("person_name required for identify_suspect")
        if not role:
            raise ValueError("person_role required for identify_suspect")
        # Update if already identified
        for i, s in enumerate(self.identified_suspects):
            if s.name.lower() == name.lower():
                self.identified_suspects[i] = Suspect(
                    name=name,
                    role=role,
                    evidence_ids=action.evidence_ids or [],
                    reasoning=action.evidence_reason or "",
                )
                self.last_action_result = f"Updated suspect: {name} ({role.value})"
                return
        self.identified_suspects.append(
            Suspect(
                name=name,
                role=role,
                evidence_ids=action.evidence_ids or [],
                reasoning=action.evidence_reason or "",
            )
        )
        self.last_action_result = f"Identified suspect: {name} ({role.value})"

    def _establish_timeline(self, action: Action):
        events = action.timeline_events
        if not events:
            raise ValueError("timeline_events required for establish_timeline")
        self.timeline = events
        self.last_action_result = f"Timeline established with {len(events)} events"

    def _submit_report(self, action: Action):
        findings = action.findings or {}
        if "scheme_type" in findings:
            self.submitted_scheme = findings["scheme_type"]
        self.last_action_result = "Investigation report submitted"

    def _compute_reward(self) -> Reward:
        if not self.grader:
            return Reward(score=0.0, message="No grader initialized")

        scheme = self.submitted_scheme
        if not scheme:
            # Try to infer from findings
            for action in reversed(self.action_history):
                if action.findings and "scheme_type" in action.findings:
                    scheme = action.findings["scheme_type"]
                    break

        result = self.grader.grade(
            identified_suspects=self.identified_suspects,
            flagged_evidence=self.flagged_evidence,
            scheme_type=scheme,
            timeline=self.timeline,
        )

        return Reward(
            score=result["score"],
            breakdown=result["breakdown"],
            message=result["message"],
        )

    def _get_available_sources(self) -> List[DataSource]:
        sources = []
        for doc_id, doc in self.documents.items():
            sources.append(
                DataSource(
                    id=doc_id,
                    source_type=DataSourceType(doc["source_type"]),
                    title=doc["title"],
                    summary=doc["content"][:100] + "..."
                    if len(doc["content"]) > 100
                    else doc["content"],
                    date=doc.get("date"),
                    participants=doc.get("participants", []),
                )
            )
        return sources

    def _build_observation(self, error: Optional[str] = None) -> Observation:
        return Observation(
            task_id=self.task_id,
            scenario_description=self.task_config["description"],
            whistleblower_tip=self.task_config["whistleblower_tip"],
            available_sources=self._get_available_sources(),
            document_content=self.last_content,
            search_results=self.last_search_results,
            cross_reference_result=self.last_cross_ref,
            flagged_evidence=list(self.flagged_evidence),
            identified_suspects=list(self.identified_suspects),
            timeline=list(self.timeline),
            step_number=self.step_count,
            max_steps=self.max_steps,
            documents_examined=len(self.examined_docs),
            last_action_result=self.last_action_result,
            last_action_error=error,
        )
