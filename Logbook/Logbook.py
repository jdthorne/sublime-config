import sublime, sublime_plugin
import os
import subprocess
import shutil
from datetime import date, timedelta

LOGBOOK_DIR = "/Users/james/Logbook"
TEMPLATE = "/Users/james/Logbook/Template.logbook"

class Logbook(sublime_plugin.WindowCommand):
  def run(self):
    window = self.window

    # Yesterday
    yesterday = date.today() - timedelta(1)
    yesterday_path = LOGBOOK_DIR + yesterday.strftime("/%Y/%m %B/")
    yesterday_file = yesterday_path + yesterday.strftime("%d %A, %B %d, %Y.logbook")

    from_yesterday = ""

    if os.path.exists(yesterday_file):
      found = False
      for line in open(yesterday_file):
        if found:
          from_yesterday += line
        if line.startswith(": For Tomorrow"):
          found = True

    # Today
    today = date.today()
    today_path = LOGBOOK_DIR + today.strftime("/%Y/%m %B/")
    today_file = today_path + today.strftime("%d %A, %B %d, %Y.logbook")

    # Create Today
    if not os.path.exists(today_path):
      os.makedirs(today_path)

    if not os.path.isfile(today_file):
      new_file = open(today_file, "w")
      for line in open(TEMPLATE):
        line = line.replace("$YESTERDAY", from_yesterday.strip())
        line = line.replace("$DATE", today.strftime("%A, %B %d, %Y"))
        new_file.write(line)

      new_file.close()

    for w in sublime.windows():
      for v in w.views():
        if v.file_name().lower().strip().encode('utf8') == today_file.lower().strip().encode('utf8'):
          v.run_command("save")

    subprocess.Popen(["/Users/james/Logbook/.scripts/update-tags.py"])
    subprocess.Popen(["/bin/s", LOGBOOK_DIR, today_file])