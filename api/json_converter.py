import json
from datetime import datetime
import re

class FHIRProcessor:
    """A reusable class to process and format FHIR responses"""
    
    def __init__(self):
        self.version = "1.0.0"
    
    def process_response(self, response_data):
        """
        Main method to process FHIR response - one call does it all
        """
        return self._clean_and_format_fhir_response(response_data)
    
    def _clean_and_format_fhir_response(self, response_data):
        # If response_data is a string, parse it as JSON
        if isinstance(response_data, str):
            try:
                # Extract JSON if it's embedded in text
                json_match = re.search(r'```json\n(.*?)\n```', response_data, re.DOTALL)
                if json_match:
                    response_data = json.loads(json_match.group(1))
                else:
                    response_data = json.loads(response_data)
            except json.JSONDecodeError:
                return {"error": "Invalid JSON format"}
        
        # Handle nested response structure
        if isinstance(response_data, dict) and 'response' in response_data:
            json_str = response_data['response']
            return self._clean_and_format_fhir_response(json_str)
        
        # Create formatted output structure
        formatted_output = {
            "summary": response_data.get("summary", ""),
            "fhir_mapping": {
                "patient": self._format_patient_info(response_data.get("patient", {})),
                "encounter": self._format_encounter_info(response_data.get("encounter", {})),
                "conditions": self._format_conditions(response_data.get("conditions", [])),
                "observations": self._format_observations(response_data.get("observations", [])),
                "vital_signs": self._extract_vital_signs(response_data.get("observations", []))
            },
            "metadata": {
                "generated_at": datetime.now().isoformat(),
                "version": "FHIR R4",
                "total_conditions": len(response_data.get("conditions", [])),
                "total_observations": len(response_data.get("observations", []))
            }
        }
        
        return formatted_output
    
    def _format_patient_info(self, patient_data):
        if not patient_data:
            return {}
        
        name = patient_data.get("name", [{}])[0]
        
        return {
            "full_name": f"{name.get('given', [''])[0]} {name.get('family', '')}".strip(),
            "first_name": name.get('given', [''])[0] if name.get('given') else "",
            "last_name": name.get('family', ''),
            "gender": patient_data.get("gender", "").capitalize(),
            "birth_date": patient_data.get("birthDate", ""),
            "age": self._calculate_age(patient_data.get("birthDate", ""))
        }
    
    def _format_encounter_info(self, encounter_data):
        if not encounter_data:
            return {}
        
        reasons = encounter_data.get("reason", [])
        primary_reason = reasons[0] if reasons else {}
        
        return {
            "visit_reason": primary_reason.get("text", ""),
            "visit_date": datetime.now().strftime("%Y-%m-%d"),
            "visit_type": "Initial Consultation"
        }
    
    def _format_conditions(self, conditions_list):
        formatted_conditions = []
        
        for condition in conditions_list:
            formatted_cond = {
                "description": condition.get("text", ""),
                "clinical_status": condition.get("status", "active").capitalize(),
                "code": {
                    "value": condition.get("code", ""),
                    "system": condition.get("system", ""),
                    "display": condition.get("display", "")
                } if condition.get("code") else None
            }
            formatted_conditions.append(formatted_cond)
        
        return formatted_conditions
    
    def _format_observations(self, observations_list):
        formatted_observations = []
        
        for obs in observations_list:
            formatted_obs = {
                "description": obs.get("text", obs.get("display", "")),
                "category": self._categorize_observation(obs),
                "value": obs.get("value"),
                "unit": obs.get("unit", ""),
                "code": {
                    "value": obs.get("code", ""),
                    "system": obs.get("system", ""),
                    "display": obs.get("display", "")
                } if obs.get("code") else None
            }
            formatted_observations.append(formatted_obs)
        
        return formatted_observations
    
    def _extract_vital_signs(self, observations_list):
        vital_signs = {}
        
        for obs in observations_list:
            if obs.get("code") == "8480-6":  # Systolic BP
                vital_signs["blood_pressure_systolic"] = f"{obs.get('value')} {obs.get('unit', 'mmHg')}"
            elif obs.get("code") == "8462-4":  # Diastolic BP
                vital_signs["blood_pressure_diastolic"] = f"{obs.get('value')} {obs.get('unit', 'mmHg')}"
            elif obs.get("code") == "72593-5":  # Pain scale
                vital_signs["pain_level"] = f"{obs.get('value')}/10"
        
        if "blood_pressure_systolic" in vital_signs and "blood_pressure_diastolic" in vital_signs:
            vital_signs["blood_pressure"] = f"{vital_signs['blood_pressure_systolic']}/{vital_signs['blood_pressure_diastolic']}"
        
        return vital_signs
    
    def _categorize_observation(self, observation):
        text = observation.get("text", "").lower() or observation.get("display", "").lower()
        
        if any(word in text for word in ["blood pressure", "systolic", "diastolic"]):
            return "Vital Sign"
        elif any(word in text for word in ["pain", "headache"]):
            return "Symptom"
        elif any(word in text for word in ["coffee", "water", "diet", "exercise"]):
            return "Lifestyle"
        elif any(word in text for word in ["sleep"]):
            return "Sleep Pattern"
        elif any(word in text for word in ["muscle", "tightness", "spasm"]):
            return "Physical Finding"
        else:
            return "General Observation"
    
    def _calculate_age(self, birth_date):
        if not birth_date:
            return "Unknown"
        
        try:
            birth = datetime.strptime(birth_date, "%Y-%m-%d")
            today = datetime.now()
            age = today.year - birth.year - ((today.month, today.day) < (birth.month, birth.day))
            return f"{age} years"
        except:
            return "Unknown"
    
    def save_to_file(self, formatted_data, filename="fhir_mapping_output.json"):
        """Save formatted data to a JSON file"""
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(formatted_data, f, indent=2, ensure_ascii=False)
        return f"Data saved to {filename}"
    
    def get_summary(self, formatted_data):
        """Get a quick summary from formatted data"""
        if not formatted_data or 'fhir_mapping' not in formatted_data:
            return "No data available"
        
        patient = formatted_data['fhir_mapping']['patient']
        encounter = formatted_data['fhir_mapping']['encounter']
        vital_signs = formatted_data['fhir_mapping']['vital_signs']
        
        return {
            "patient": f"{patient.get('full_name', 'Unknown')} ({patient.get('age', 'Unknown')}, {patient.get('gender', 'Unknown')})",
            "visit_reason": encounter.get('visit_reason', 'Unknown'),
            "conditions_count": len(formatted_data['fhir_mapping']['conditions']),
            "observations_count": len(formatted_data['fhir_mapping']['observations']),
            "blood_pressure": vital_signs.get('blood_pressure', 'N/A'),
            "pain_level": vital_signs.get('pain_level', 'N/A')
        }

