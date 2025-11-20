import os
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

def create_sample_pdf(filename, content):
    c = canvas.Canvas(filename, pagesize=letter)
    text = c.beginText(40, 750)
    text.setFont("Helvetica", 12)
    
    for line in content.split('\n'):
        text.textLine(line)
        
    c.drawText(text)
    c.save()

sample_notes = [
    """
    Patient Name: John Doe
    DOB: 01/01/1980
    MRN: 123456
    
    Chief Complaint: Chest pain.
    
    HPI: Mr. Doe presents with substernal chest pain starting 2 hours ago. 
    He denies shortness of breath.
    
    Plan:
    1. EKG
    2. Troponin
    3. Admit to Cardiology
    """,
    """
    Patient Name: Jane Smith
    DOB: 05/12/1975
    Address: 123 Main St, Springfield, IL
    
    Subjective: Patient complains of severe headache.
    
    Objective: BP 140/90. HR 80.
    
    Assessment: Migraine.
    
    Plan: Ibuprofen 400mg. Follow up with Dr. House.
    """
]

def main():
    os.makedirs("sample_data", exist_ok=True)
    
    for i, note in enumerate(sample_notes):
        filename = f"sample_data/note_{i+1}.pdf"
        create_sample_pdf(filename, note)
        print(f"Created {filename}")

if __name__ == "__main__":
    main()
