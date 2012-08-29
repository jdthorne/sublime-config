import sublime, sublime_plugin

highlights = []

class HighlightSelection(sublime_plugin.TextCommand):
   def run(self, edit, clear=False):
      global highlights

      if clear:
         highlights = []
         self.view.add_regions("highlights", [], "highlightedtext")
         return

      if len(self.view.sel()) > 0:
         selection = self.view.substr(self.view.sel()[0])
         if len(selection) > 0:
            highlights.append(selection)

      results = []
      for text in highlights:
         results += self.view.find_all(text, sublime.LITERAL)

      self.view.add_regions("highlights", results, "highlightedtext", "dot", sublime.DRAW_OUTLINED);
