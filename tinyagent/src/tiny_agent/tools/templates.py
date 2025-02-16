from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from typing import Dict, Type, Optional

from tinyagent.src.tiny_agent.tools.notes import Notes
from tinyagent.src.utils.logger_utils import log

"""
Constants defining the structure and format of various medical note templates.
These are designed to be appended to system prompts to guide note generation.
"""

HANDOFF_TEMPLATE = '''
# Clinical Handoff Notes Template

## Header Information
- Date: [DATE]
- Shift: [SHIFT TYPE]
- Provider: [PROVIDER NAME]
- Service: [SERVICE NAME]

## Patient SBAR Format
For each patient, include:

### Patient Identification
- Name: [PATIENT NAME]
- Room: [ROOM NUMBER]

### Situation
[Brief description of current situation/reason for admission]

### Background
- Primary Diagnosis: [DIAGNOSIS]
- Relevant History: [KEY HISTORICAL POINTS]

### Assessment
- Current Status: [CURRENT CONDITION]
- Vital Signs: [RECENT VITALS]
- Labs/Studies: [RELEVANT RESULTS]

### Recommendation
- Plan: [TREATMENT PLAN]
- Tasks: [PENDING TASKS]
- Critical Follow-up: [IMPORTANT FOLLOW-UP ITEMS]
'''

ADMISSION_TEMPLATE = '''
# Admission Note Template

## Patient Information
- Name: [PATIENT NAME]
- MRN: [MEDICAL RECORD NUMBER]
- DOB: [DATE OF BIRTH]
- Admitting Provider: [PROVIDER NAME]
- Service: [SERVICE NAME]

## Core Documentation Elements
1. Chief Complaint
[Primary reason for admission]

2. History of Present Illness
[Detailed chronological history]

3. Past Medical History
[Relevant medical history]

4. Medications
### Home Medications
[List of current medications]

5. Allergies
[Known allergies and reactions]

6. Review of Systems
[Systematic review of symptoms]

7. Physical Examination
- Vital Signs: [CURRENT VITALS]
[Detailed physical examination findings]

8. Assessment and Plan
[Problem-based assessment and treatment plan]
'''

PROCEDURE_TEMPLATE = '''
# Procedure Note Template

## Patient Information
- Name: [PATIENT NAME]
- MRN: [MEDICAL RECORD NUMBER]
- Procedure: [PROCEDURE NAME]

## Provider Information
- Attending: [ATTENDING NAME]
- Assistant(s): [ASSISTANT NAMES]

## Pre-Procedure Documentation
- Indication: [PROCEDURE INDICATION]
- Consent: [CONSENT STATUS]
- Time Out Status: [TIMEOUT CONFIRMATION]

## Procedure Details
- Anesthesia Type: [ANESTHESIA DETAILS]
- Procedure Description: [DETAILED DESCRIPTION]
- Complications: [ANY COMPLICATIONS]
- Estimated Blood Loss: [BLOOD LOSS AMOUNT]

## Post-Procedure Information
- Disposition: [POST-PROCEDURE STATUS]
- Instructions: [POST-PROCEDURE INSTRUCTIONS]
'''

DISCHARGE_TEMPLATE = '''
# Discharge Summary Template

## Patient Information
- Name: [PATIENT NAME]
- MRN: [MEDICAL RECORD NUMBER]
- Admission Date: [ADMIT DATE]
- Discharge Date: [DISCHARGE DATE]
- Discharging Provider: [PROVIDER NAME]

## Hospital Course Summary
1. Principal Diagnosis
[PRIMARY DIAGNOSIS]

2. Secondary Diagnoses
[ADDITIONAL DIAGNOSES]

3. Hospital Course
[BRIEF SUMMARY OF HOSPITAL STAY]

4. Procedures Performed
[LIST OF PROCEDURES]

5. Consultations
[CONSULTING SERVICES]

## Discharge Planning
1. Discharge Condition
[PATIENT'S CONDITION AT DISCHARGE]

2. Medications
[DISCHARGE MEDICATION LIST]

3. Follow-up Instructions
[DETAILED FOLLOW-UP PLAN]

4. Warning Signs
[SYMPTOMS REQUIRING MEDICAL ATTENTION]

## Care Team Information
- Primary Team: [TEAM MEMBERS]
- Consulting Services: [CONSULTANT LIST]
'''

@dataclass
class TemplateContext:
    """Holds data needed to render a template"""
    title: str
    created_at: datetime = datetime.now()
    additional_data: Dict = None

    def __post_init__(self):
        if self.additional_data is None:
            self.additional_data = {}

class NoteTemplate(ABC):
    """Base class for all note templates"""
    
    @abstractmethod
    def generate_content(self, context: TemplateContext) -> str:
        """Generate the content for the note based on the template and context"""
        pass

    @abstractmethod
    def get_folder(self) -> Optional[str]:
        """Return the folder where this type of note should be stored"""
        pass

class HandoffTemplate(NoteTemplate):
    """
    Template for patient handoffs using SBAR format
    (Situation, Background, Assessment, Recommendation)
    """
    def generate_content(self, context: TemplateContext) -> str:
        patients = context.additional_data.get('patients', [])
        shift_date = context.created_at.strftime('%Y-%m-%d')
        shift_time = context.additional_data.get('shift', 'Day')
        
        content = f"""
        <h1>Clinical Handoff Notes - {shift_date} - {shift_time} Shift</h1>
        <p><strong>Provider:</strong> {context.additional_data.get('provider', '')}</p>
        <p><strong>Service:</strong> {context.additional_data.get('service', '')}</p>
        <hr>
        """
        
        # Add each patient's SBAR
        for patient in patients:
            content += f"""
            <div class="patient-sbar">
                <h2>Patient: {patient.get('name', '')} - Room: {patient.get('room', '')}</h2>
                
                <h3>Situation</h3>
                <p>{patient.get('situation', '')}</p>
                
                <h3>Background</h3>
                <p><strong>Diagnosis:</strong> {patient.get('diagnosis', '')}</p>
                <p><strong>Relevant History:</strong> {patient.get('background', '')}</p>
                
                <h3>Assessment</h3>
                <p><strong>Current Status:</strong> {patient.get('assessment', '')}</p>
                <p><strong>Vital Signs:</strong> {patient.get('vitals', '')}</p>
                <p><strong>Labs/Studies:</strong> {patient.get('labs', '')}</p>
                
                <h3>Recommendation</h3>
                <p><strong>Plan:</strong> {patient.get('plan', '')}</p>
                <p><strong>Tasks:</strong> {patient.get('tasks', '')}</p>
                <p><strong>Critical Follow-up:</strong> {patient.get('followup', '')}</p>
            </div>
            <hr>
            """
        
        return content

    def get_folder(self) -> str:
        return "Clinical Handoffs"

class AdmissionTemplate(NoteTemplate):
    """Template for admission notes following standard medical format"""
    
    def generate_content(self, context: TemplateContext) -> str:
        admission_date = context.created_at.strftime('%Y-%m-%d %H:%M')
        
        content = f"""
        <h1>Admission Note - {admission_date}</h1>
        
        <h2>Patient Information</h2>
        <p><strong>Name:</strong> {context.additional_data.get('patient_name', '')}</p>
        <p><strong>MRN:</strong> {context.additional_data.get('mrn', '')}</p>
        <p><strong>DOB:</strong> {context.additional_data.get('dob', '')}</p>
        <p><strong>Admitting Provider:</strong> {context.additional_data.get('provider', '')}</p>
        <p><strong>Service:</strong> {context.additional_data.get('service', '')}</p>
        
        <h2>Chief Complaint</h2>
        <p>{context.additional_data.get('chief_complaint', '')}</p>
        
        <h2>History of Present Illness</h2>
        <p>{context.additional_data.get('hpi', '')}</p>
        
        <h2>Past Medical History</h2>
        <p>{context.additional_data.get('pmh', '')}</p>
        
        <h2>Medications</h2>
        <h3>Home Medications</h3>
        <p>{context.additional_data.get('home_meds', '')}</p>
        
        <h2>Allergies</h2>
        <p>{context.additional_data.get('allergies', '')}</p>
        
        <h2>Review of Systems</h2>
        <p>{context.additional_data.get('ros', '')}</p>
        
        <h2>Physical Examination</h2>
        <p><strong>Vital Signs:</strong> {context.additional_data.get('vitals', '')}</p>
        <p>{context.additional_data.get('physical_exam', '')}</p>
        
        <h2>Assessment and Plan</h2>
        <p>{context.additional_data.get('assessment_plan', '')}</p>
        """
        return content

    def get_folder(self) -> str:
        return "Admission Notes"

class ProcedureTemplate(NoteTemplate):
    """Template for procedure notes following standard medical format"""
    
    def generate_content(self, context: TemplateContext) -> str:
        procedure_date = context.created_at.strftime('%Y-%m-%d %H:%M')
        
        content = f"""
        <h1>Procedure Note - {procedure_date}</h1>
        
        <h2>Patient Information</h2>
        <p><strong>Name:</strong> {context.additional_data.get('patient_name', '')}</p>
        <p><strong>MRN:</strong> {context.additional_data.get('mrn', '')}</p>
        <p><strong>Procedure:</strong> {context.additional_data.get('procedure_name', '')}</p>
        
        <h2>Providers</h2>
        <p><strong>Attending:</strong> {context.additional_data.get('attending', '')}</p>
        <p><strong>Assistant(s):</strong> {context.additional_data.get('assistants', '')}</p>
        
        <h2>Pre-Procedure</h2>
        <p><strong>Indication:</strong> {context.additional_data.get('indication', '')}</p>
        <p><strong>Consent:</strong> {context.additional_data.get('consent', '')}</p>
        <p><strong>Time Out Performed:</strong> {context.additional_data.get('timeout', 'Yes')}</p>
        
        <h2>Procedure Details</h2>
        <p><strong>Anesthesia:</strong> {context.additional_data.get('anesthesia', '')}</p>
        <p><strong>Description:</strong> {context.additional_data.get('description', '')}</p>
        <p><strong>Complications:</strong> {context.additional_data.get('complications', 'None')}</p>
        <p><strong>Estimated Blood Loss:</strong> {context.additional_data.get('blood_loss', '')}</p>
        
        <h2>Post-Procedure</h2>
        <p><strong>Disposition:</strong> {context.additional_data.get('disposition', '')}</p>
        <p><strong>Instructions:</strong> {context.additional_data.get('instructions', '')}</p>
        """
        return content

    def get_folder(self) -> str:
        return "Procedure Notes"

class DischargeSummaryTemplate(NoteTemplate):
    """Template for discharge summaries following standard medical format"""
    
    def generate_content(self, context: TemplateContext) -> str:
        discharge_date = context.created_at.strftime('%Y-%m-%d')
        
        content = f"""
        <h1>Discharge Summary</h1>
        
        <h2>Patient Information</h2>
        <p><strong>Name:</strong> {context.additional_data.get('patient_name', '')}</p>
        <p><strong>MRN:</strong> {context.additional_data.get('mrn', '')}</p>
        <p><strong>Admission Date:</strong> {context.additional_data.get('admission_date', '')}</p>
        <p><strong>Discharge Date:</strong> {discharge_date}</p>
        <p><strong>Discharging Provider:</strong> {context.additional_data.get('provider', '')}</p>
        
        <h2>Hospital Course</h2>
        <h3>Principal Diagnosis</h3>
        <p>{context.additional_data.get('principal_diagnosis', '')}</p>
        
        <h3>Secondary Diagnoses</h3>
        <p>{context.additional_data.get('secondary_diagnoses', '')}</p>
        
        <h3>Brief Hospital Course</h3>
        <p>{context.additional_data.get('hospital_course', '')}</p>
        
        <h3>Procedures Performed</h3>
        <p>{context.additional_data.get('procedures', '')}</p>
        
        <h3>Consultations</h3>
        <p>{context.additional_data.get('consultations', '')}</p>
        
        <h2>Discharge Information</h2>
        <h3>Discharge Condition</h3>
        <p>{context.additional_data.get('discharge_condition', '')}</p>
        
        <h3>Discharge Medications</h3>
        <p>{context.additional_data.get('discharge_medications', '')}</p>
        
        <h3>Follow-up Instructions</h3>
        <p>{context.additional_data.get('followup', '')}</p>
        
        <h3>Warning Signs</h3>
        <p>{context.additional_data.get('warning_signs', '')}</p>
        
        <h2>Care Team</h2>
        <p><strong>Primary Team:</strong> {context.additional_data.get('primary_team', '')}</p>
        <p><strong>Consulting Services:</strong> {context.additional_data.get('consulting_services', '')}</p>
        """
        return content

    def get_folder(self) -> str:
        return "Discharge Summaries"

class TemplateRegistry:
    """Registry for managing note templates"""
    
    def __init__(self):
        self._templates: Dict[str, Type[NoteTemplate]] = {}
        self._keywords: Dict[str, str] = {}
        
    def register_template(self, template_class: Type[NoteTemplate], *keywords: str):
        """Register a template class with associated keywords"""
        template_name = template_class.__name__
        self._templates[template_name] = template_class
        
        for keyword in keywords:
            self._keywords[keyword.lower()] = template_name
    
    def get_template(self, identifier: str) -> Optional[NoteTemplate]:
        """Get a template instance by name or keyword"""
        identifier = identifier.lower()
        
        # Try to find template by keyword
        template_name = self._keywords.get(identifier)
        
        # If not found by keyword, try direct template name
        if not template_name:
            template_name = identifier
            
        template_class = self._templates.get(template_name)
        return template_class() if template_class else None

class TemplatedNotes(Notes):
    """Extension of Notes class to support templates"""

    def __init__(self):
        super().__init__()
        self.template_registry = TemplateRegistry()
        
        self.template_registry.register_template(
            HandoffTemplate,
            "handoff", "sbar", "rounds", "signout"
        )
        
        self.template_registry.register_template(
            AdmissionTemplate,
            "admission", "admit", "h&p"
        )
        
        self.template_registry.register_template(
            ProcedureTemplate,
            "procedure", "operation", "surgery"
        )
        
        self.template_registry.register_template(
            DischargeSummaryTemplate,
            "discharge", "dc", "dcsummary"
        )
    
    def create_note_from_template(
        self,
        template_identifier: str,
        title: str,
        additional_data: Dict = None
    ) -> str:
        """Create a new note using a template"""
        template = self.template_registry.get_template(template_identifier)
        log(f"Creating note from template: {template_identifier}, title: {title}, additional_data: {additional_data}")
        if not template:
            return f"No template found for identifier: {template_identifier}"
            
        context = TemplateContext(
            title=title,
            additional_data=additional_data or {}
        )
        
        content = template.generate_content(context)
        folder = template.get_folder()
        
        return self.create_note(title, content, folder)
