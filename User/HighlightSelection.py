import sublime, sublime_plugin

highlights = []

class HighlightSelection(sublime_plugin.TextCommand):
   def run(self, edit, clear=False, add=True):
      global highlights

      if add:
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

class HighlightListener(sublime_plugin.EventListener):
   def on_modified(self, view):
      h = HighlightSelection(view)
      h.run(None, add=False)

   def on_activated(self, view):
      h = HighlightSelection(view)
      h.run(None, add=False)
