import sublime, sublime_plugin

class Comment(sublime_plugin.TextCommand):
	def run(self, edit):
		cursor = self.view.sel()[0].begin()
		self.view.insert(edit, cursor, comment)

		cursor = self.view.sel()[0].begin()
		self.view.sel().clear()
		self.view.sel().add(sublime.Region(cursor - 95 + 8))

comment = """\
/**
 ******************************************************************************
 *
 *                   
 *
 ******************************************************************************
 */"""
