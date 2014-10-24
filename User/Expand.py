import sublime, sublime_plugin
import re
import os

class Expand(sublime_plugin.TextCommand):
   def run(self, edit):
      selection = self.view.substr(self.view.sel()[0])

      className = os.path.basename(self.view.file_name()).split(".")[0]

      lines = []
      for line in selection.split("\n"):
         line = re.sub(" *(virtual +)?([^( ']+) +(test[a-zA-Z_0-9]+[(][^\"]*[)]) *( = 0)? *;", "\\2 " + className + "::\\3\n{\n  // Arrange\n  \n  // Act\n  \n  // Assert\n  printf(\"Warning: [" + className + "] Test not written\\\\n\");\n}\n", line)
         line = re.sub(" *(static +)?(virtual +)?([^( ']+) +([a-zA-Z_0-9]+\\([^\"]*\\))((.* const)?) *( = 0)? *; *", "\\3 " + className + "::\\4\\5\n{\n  printf(\"Warning: [" + className + "] '\\4' is not implemented\\\\n\");\n}\n", line)
         line = re.sub(" *static ([^ ].+) ([A-Z_]+);", "\\1 " + className + "::\\2 = ;", line)
         line = re.sub(" *extern (const )?([^ ].+) ([A-Z_]+);", "\\1\\2 " + className + "::\\3 = ;", line)
         line = re.sub(" *class *([A-Z][a-zA-Z0-9_]+);", "#include <\\1.h>", line)
         line = re.sub(" *CPPUNIT_TEST[(](.*)[)];", "  void \\1();", line)
         line = re.sub(" *CPPUNIT_DATA_TEST[(](.*)[)];", "  void \\1();\n  void \\1_data();", line)
         line = re.sub(" *CPPUNIT_FETCH[(](.*), (.*)[)];", "  addColumn<\\1>(\"\\2\");", line)

         line = re.sub(" *TEST[(](.*)[)]", "TEST(\\1)\n{\n  // Arrange\n  \n  // Act\n  \n  // Assert\n  printf(\"Warning: [" + className + "] Test not written\\\\n\");\n}\n", line)

         lines.append(line)

      self.view.replace(edit, self.view.sel()[0], "\n".join(lines))
