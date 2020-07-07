import subprocess
import re
from distutils import spawn  # py2 compat
import csv

def to_text(path):
    if spawn.find_executable("pdftotext"):  # shutil.which('pdftotext'):
        out, err = subprocess.Popen(
            ["pdftotext", '-table', '-enc', 'UTF-8', path, '-'], stdout=subprocess.PIPE
        ).communicate()
        return out
    else:
        raise EnvironmentError('pdftotext not installed. Can be down')

extracted_str = to_text("Covid_Bengaluru_01June_2020 Bulletin-70 English.pdf")
extracted_str = extracted_str.decode('utf-8')
extracted_str = re.sub(' +', ' ', extracted_str)

start = re.search("Status Of Active Containment Zones In BBMP", extracted_str)
end = re.search("Note: The codes used for Containment Zone Identification represent the following:", extracted_str)

table = extracted_str[start.end():end.start()]
tableLines = re.split(r'\n', table)

lines = []
for line in tableLines:
    if not line.strip('').strip('\r') or not line:
        continue
    match = re.search("(?P<SNo>\d+)\s+(?P<ZoneID>\w+\s-\s\d+)\s(?P<IdenDate>\d{2}-\d{2}-\d{4})\s(?P<Loc>.+)\s(?P<Cases>\d+)\s(?P<NormalDate>\d{2}-\d{2}-\d{4})\s(?P<Status>\w+)", line)
    if match:
        current_row = []
        for field, value in match.groupdict().items():
            current_row.append(value)
        lines.append(current_row)
        continue
    #print('ignoring *%s* because it doesn\'t match anything', line)

with open("out.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerows(lines)