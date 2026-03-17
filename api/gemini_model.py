# This Model will Summarize the complete Conversation to Meaningfull Context only. 

# Importing all Necessary Libraries
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate
import os
from dotenv import load_dotenv
load_dotenv()

class LLM:

    def get_api(self):
        api = os.getenv('GOOGLE_API_KEY')
        os.environ['GEMINI_API_KEY'] = api
        # print(api)
        return api

    def make_model(self,api_key):
        # api_key = self.get_api()
        llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            api_key=api_key,
        )
        # print(llm)
        return llm

    def create_prompt(self):
        # Using with a prompt template and output parser
        prompt = ChatPromptTemplate.from_messages([
                ("system", '''You are an Ambient Clinical AI Scribe specialized in the Indian Healthcare context (Bharat).

            INPUT FORMAT:
            You will receive a sequence of dialogue turns between a doctor and patient. The dialogue is in Hinglish (Hindi + English mix) with some social conversation included.

            YOUR TASK:
            Analyze the conversation and extract clinically significant information. Filter out social pleasantries, filler words, and irrelevant small talk according to the FILTERING RULES below. Then map the extracted information into a structured JSON object that follows the FHIR-like schema provided.

            FILTERING RULES (REMOVE these):
            - Greetings and farewells (namaste, bye, khuda hafiz)
            - Social pleasantries (kaise hain aap?, theek hu)
            - Weather talk (garmi pad rahi hai)
            - Filler words (acha, theek hai, um, hmm, arre)
            - Patient queries about general advice (kya khaana chahiye?)
            - Non-clinical confirmations (kitne din medicine lena hai?)
            - Any sentence that doesn't contribute to clinical documentation

            CLINICAL EXTRACTION RULES (KEEP these):
            Extract only sentences that map to these FHIR resource categories:
            1. [Condition] - Complaints, symptoms, and duration
            2. [Observation] - Vital signs and physical findings
            3. [MedicationRequest] - Medicines with dosage/frequency
            4. [Procedure] - Tests, investigations, surgeries

            OUTPUT FORMAT:
            You must respond with a single JSON object that strictly follows the schema below. Do not include any additional text, explanations, or markdown formatting.

            {{
            "summary": "A brief clinical summary of the conversation (1-2 sentences).",
            "patient": {{
                "name": [
                {{
                    "text": "Full name in original script",
                    "family": "Last name (if available)",
                    "given": ["First name (if available)"]
                }}
                ],
                "gender": "male/female/other/unknown",
                "birthDate": "YYYY-MM-DD (if mentioned, otherwise omit)"
            }},
            "encounter": {{
                "date": "Encounter date in ISO 8601 format (YYYY-MM-DDThh:mm:ss) if mentioned, otherwise omit",
                "reason": [
                {{
                    "text": "Reason for visit in original Hinglish",
                    "code": "SNOMED CT code if known, else empty string",
                    "system": "http://snomed.info/sct",
                    "display": "English description of the code"
                }}
                ]
            }},
            "conditions": [
                {{
                "text": "Condition/diagnosis in original Hinglish",
                "code": "SNOMED CT code if known",
                "system": "http://snomed.info/sct",
                "display": "English description",
                "status": "active (if currently present) | resolved | etc."
                }}
            ],
            "medications": [
                {{
                "text": "Medication name and dosage as mentioned (e.g., 'एज़िथ्रोमाइसिन 500mg')",
                "code": "RxNorm code if known",
                "system": "http://www.nlm.nih.gov/research/umls/rxnorm",
                "display": "English description",
                "dosage": "Dosage instructions as mentioned (e.g., 'दिन में एक बार')"
                }}
            ],
            "observations": [
                {{
                "code": "LOINC code if known",
                "system": "http://loinc.org",
                "display": "English description",
                "value": numeric value (if applicable),
                "unit": "unit of measurement (if applicable)"
                }}
            ]
            }}

            IMPORTANT CONSTRAINTS:
            - Keep original Hinglish words for symptoms/descriptions in the 'text' fields.
            - For codes, only provide them if you are confident; otherwise leave as empty string.
            - Each extracted clinical sentence must map to exactly one resource type.
            - Discard any dialogue that doesn't fit the 4 FHIR categories.
            - The JSON must be valid and complete. If a field has no data, omit it entirely (do not include empty lists/objects).
            - Ensure the summary captures the essence of the clinical encounter.
            '''),
                ("human", "{conversation}")
                ])
        return prompt 

    def full_implemented(self, msg):
        api_key = self.get_api()
        llm = self.make_model(api_key)
        prompt = self.create_prompt()
        # print("Prompt and LLM created successfully. Now creating the chain...")
        chain = prompt | llm | StrOutputParser()
        # print("Chain created successfully.")    
        response = chain.invoke({
            "conversation": msg
        })

        return response

