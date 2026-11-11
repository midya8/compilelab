import json
from pathlib import Path
from .make_cases import controls
p=Path(__file__).resolve().parents[1]
expected=[{'name':n,'input':x} for n,x in controls()]
assert json.loads((p/'docs/cases.json').read_text())==expected
assert json.loads((p/'docs/example.json').read_text())==expected[0]['input']
print('12 controls and default example match native source')
