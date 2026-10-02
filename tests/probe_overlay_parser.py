#!/usr/bin/env python3
"""Optional local probe of the installed Claude Code body boundary and sentinels.

Run with Python and Node; no Claude session or model invocation is started.
This executes extracted boundary statements, not the YAML metadata parser.
"""

from pathlib import Path
import hashlib
import json
import re
import subprocess

binary = Path('/usr/bin/claude').read_bytes()
version = re.search(rb'// Version: ([^\n]+)', binary).group(1).decode()
print(f'Claude Code {version} sha256=' + hashlib.sha256(binary).hexdigest(), flush=True)
source = binary.decode('utf-8', errors='replace')
jw = re.search(r'function jw\(e\)\{return e.charCodeAt\(0\)===65279\?e.slice\(1\):e\}', source).group()
jk = re.search(r'jk=(/\^---.*?/),qj=', source).group(1)
start = source.index('function Ms(e,n,r){let o=e;e=jw(e);')
stop = source.index(',l=(p)=>p', start)
# Execute the installed body-boundary statements. The remaining Ms code parses
# YAML metadata but returns the same `s` on both success and parse failure.
boundary = source[start:stop] + ';return{content:s}}'
start = source.index('var TF="\\uFFFF",pz="\\uFFFE";')
stop = source.index('import{lstat as DRn', start)
interpolation = source[start:stop]
clean = b'---\nname: fixture\ndescription: $1 !`echo example`\n---\nbody\n'
fixtures = {
    'LF': clean,
    'CR-only': clean.replace(b'\n', b'\r'),
    'CRLF': clean.replace(b'\n', b'\r\n'),
    'mixed': clean.replace(b'\n', b'\r', 1),
    'invalid-UTF8': clean + b'\xff',
    'NUL': clean + b'\0',
    'BOM': b'\xef\xbb\xbf' + clean,
    'FFFE': clean + b'\xef\xbf\xbe',
    'FFFF': clean + b'\xef\xbf\xbf',
}
script = jw + '\nconst jk=' + jk + ';\n' + boundary + '\n' + interpolation + '\n'
script += 'const fixtures=' + json.dumps({k:v.hex() for k,v in fixtures.items()}) + ';\n'
script += r'''
console.log('Node ' + process.version + ': extracted jw, jk, Ms boundary; complete jTe with empty arguments');
for (const [label, hex] of Object.entries(fixtures)) {
  const bytes = Buffer.from(hex, 'hex');
  const text = bytes.toString('utf8');
  const body = Ms(text).content;
  const altered = jTe(body, '', false) !== body;
  console.log(`${label}: frontmatter=${jk.test(jw(text))}, bodyHasHeaderTokens=${body.includes('$1')}, decodeChanged=${!Buffer.from(text).equals(bytes)}, interpolationRewrites=${altered}`);
}
'''
subprocess.run(['node'], input=script, text=True, check=True)
