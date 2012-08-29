import os
import sublime, sublime_plugin

class ToggleTest(sublime_plugin.TextCommand):
   def run(self, edit):
      targetFile = self.view.file_name()

      path = self.view.file_name()
      file = os.path.basename(path)
      directory = os.path.dirname(path)

      if "/Test" in path:
         targetFile = os.path.abspath( directory + "/../../" + file[4:] )
      else:
         targetFile = os.path.abspath( directory + "/test/" + file.split(".")[0] + "/Test" + file )

      self.view.window().open_file(targetFile)


