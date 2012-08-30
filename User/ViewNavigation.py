import sublime, sublime_plugin

history = []
forwardHistory = []

class ViewNavigation(sublime_plugin.TextCommand):
   def run(self, edit, direction):
      global history
      global forwardHistory

      file = self.view.file_name()
      if direction == "back":
         forwardHistory.append(file)

         while (file == self.view.file_name()):
            if len(history) == 0:
               return

            file = history.pop()

         self.view.window().open_file(file)

      else:
         while (file == self.view.file_name()):
            if len(forwardHistory) == 0:
               return

            file = forwardHistory.pop()

         self.view.window().open_file(file)

class ViewHistory(sublime_plugin.EventListener):
   def on_activated(self, view):
      global history

      file = view.file_name()
      if len(history) > 0 and (history[-1] == file):
         return

      history.append(file)
