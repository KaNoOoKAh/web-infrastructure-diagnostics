bash -lc cat > /mnt/data/create_report.py <<'PY'
from docx import Document
from docx.shared import Pt

doc=Document()
t=doc.add_heading('AI Systems Observation Report',0)
p=doc.add_paragraph()
p.add_run('Purpose: ').bold=True
p.add_run('Document known, publicly reported issues affecting AI assistants and AI search systems. Safety-check sections describe only checks actually performed during this review and known limitations.')

issues=[
('Hallucinations / Incorrect Answers','Users and researchers report AI systems sometimes provide incorrect answers with high confidence. Public research and vendor statements acknowledge hallucinations remain an unresolved challenge.','Checks actually performed: reviewed publicly reported sources and vendor documentation. Limitation: no access to internal model logs, telemetry, weights, safety systems, incident databases, or production monitoring.'),
('Failure to Express Uncertainty','Systems may generate a likely answer instead of stating uncertainty when evidence is insufficient.','Checks actually performed: reviewed published explanations discussing incentives that can encourage guessing. Limitation: cannot independently inspect training or evaluation procedures.'),
('Memory and Context Inconsistency','Users report assistants occasionally forget relevant context while retaining less useful information.','Checks actually performed: compared recurring public user reports. Limitation: no access to user-specific memory systems or backend state.'),
('Instruction Drift','Some users report responses that become repetitive, corrective, or deviate from requested tasks during long conversations.','Checks actually performed: reviewed public complaints and examples. Limitation: unable to run large-scale controlled testing across production deployments.'),
('Reliability and Availability Problems','Reports include loading loops, duplicate responses, stalled sessions, unavailable history, and service interruptions.','Checks actually performed: reviewed publicly reported service issues. Limitation: cannot inspect platform operational telemetry.'),
('AI Search Citation Problems','Studies report incorrect citations, fabricated references, and inaccurate source attribution in AI search products.','Checks actually performed: reviewed reported findings from publicly available studies and articles. Limitation: did not independently reproduce all study results.')]

for title,desc,checks in issues:
    doc.add_heading(title, level=1)
    doc.add_paragraph(desc)
    doc.add_paragraph(checks)

h=doc.add_heading('Important Limitation', level=1)
doc.add_paragraph('I cannot truthfully document internal safety checks, audits, protocols, diagnostics, or system verification activities that I did not perform. Any claim that internal safety systems were tested, validated, or inspected would be speculative. This report therefore distinguishes between publicly reported issues and the limited verification steps actually performed during preparation.')

path='/mnt/data/AI_Observation_Report.docx'
doc.save(path)
print(path)
PY
python3 /mnt/data/create_report.py
