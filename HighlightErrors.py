import sublime, sublime_plugin
import re
import os
import time

class HighlightErrors(sublime_plugin.TextCommand):
   def run(self, edit):
      self.window = self.view.window()
      if self.window == None:
         return

      views = {}
      viewErrorRegions = {}
      viewWarningRegions = {}
      for view in self.window.views():
         views[view.file_name()] = view
         viewErrorRegions[view.file_name()] = []
         viewWarningRegions[view.file_name()] = []

      for line in open("/home/jthorne/.lastBuildOutputNormalized"):
         match = re.match("^([-a-zA-Z0-9_/.]+[.](cxx|h))[:]([0-9]+)[:](.*)$", line)

         if match != None:
            file, ext, line, message = match.groups()
            file = os.path.abspath(file)

            if "no relevant classes found" in message.lower():
               continue

            if not file in views:
               views[file] = self.window.open_file(file)
               viewErrorRegions[view.file_name()] = []
               viewWarningRegions[view.file_name()] = []

            if "error" in message.lower():
               viewErrorRegions[file].append( views[file].line(views[file].text_point(int(line) - 1, 0)) )
            else:
               viewWarningRegions[file].append( views[file].line(views[file].text_point(int(line) - 1, 0)) )

      for file in views:
         views[file].add_regions("error", viewErrorRegions[file], "error", "bookmark", sublime.DRAW_OUTLINED);
         views[file].add_regions("errorwarning", viewWarningRegions[file], "errorwarning", "bookmark", sublime.DRAW_OUTLINED);


class HighlightUpdater(sublime_plugin.EventListener):
   def on_load(self, view):
      view.run_command("highlight_errors")
