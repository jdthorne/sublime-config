import sublime, sublime_plugin
import re
import os
import time

viewsToLoad = []

class HighlightAckResults(sublime_plugin.TextCommand):
   def run(self, edit):
      self.window = self.view.window()
      if self.window == None:
         return

      views = {}
      viewRegions = {}
      for view in self.window.views():
         views[view.file_name()] = view
         viewRegions[view.file_name()] = []

      for line in open("/home/jthorne/.ackResults"):
         match = re.match("^([-a-zA-Z0-9_/.]+[.](cxx|h))[:]([0-9]+)[:](.*)$", line)

         if match != None:
            file, ext, line, message = match.groups()
            file = os.path.abspath(file)

            if "no relevant classes found" in message.lower():
               continue

            if not file in views:
               viewsToLoad.append(file)
               views[file] = self.window.open_file(file + ":" + str(line), sublime.ENCODED_POSITION)
               viewRegions[file] = []

            viewRegions[file].append( views[file].line(views[file].text_point(int(line) - 1, 0)) )

      for file in views:
         views[file].add_regions("ack", viewRegions[file], "highlightedtext", "bookmark", sublime.DRAW_OUTLINED);


class HighlightAckUpdater(sublime_plugin.EventListener):
   def on_load(self, view):
      if view.file_name() in viewsToLoad:
         viewsToLoad.remove(view.file_name())
         view.run_command("highlight_ack_results")
