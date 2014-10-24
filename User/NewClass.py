import sublime, sublime_plugin
import os

headerTemplate = """\
#ifndef $CLASS_CAPS_H
#define $CLASS_CAPS_H

// System

// Project

/**
 ******************************************************************************
 *
 *                   $CLASS
 *
 ******************************************************************************
 */
class $CLASS
{

public:
  $CLASS();
  virtual ~$CLASS();

public:

private: // helpers

private: // members

};

#endif
"""

bodyTemplate = """\

// System
#include <cstdio>

// Project
#include <$CLASS.h>

$CLASS::$CLASS()
{

}

$CLASS::~$CLASS()
{
}

"""

class NewClass(sublime_plugin.TextCommand):
   def run(self, edit):
      self.view.window().show_input_panel("Class Name", "", self.on_done, None, None)

   def on_done(self, className):
      window = self.view.window()
      path = os.path.dirname(self.view.file_name())

      def writeAndOpen(path, contents):
         file = open(path, "w")
         file.write(contents)
         file.close()
         window.open_file(path)

      writeAndOpen(path + "/" + className + ".h",
                   headerTemplate.replace("$CLASS_CAPS", className.upper()).replace("$CLASS", className))

      writeAndOpen(path + "/" + className + ".cxx",
                   bodyTemplate.replace("$CLASS_CAPS", className.upper()).replace("$CLASS", className))
