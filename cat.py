#!/usr/bin/python -s
#
#  py-cat
#
#  Implements a subset of the GNU 'cat' functionality in python, with  added
#  option of inserting delay between characters...
#
#  This  program is free software: you can redistribute it and/or modify  it
#  under  the  terms of the GNU General Public License as published  by  the
#  Free  Software  Foundation, either version 3 of the License, or (at  your
#  option) any later version.
#
#  This  program  is  distributed in the hope that it will  be  useful,  but
#  WITHOUT   ANY   WARRANTY;   without  even   the   implied   warranty   of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General
#  Public License for more details.
#
#  You  should have received a copy of the GNU General Public License  along
#  with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#  20 Mar 16   0.1   - Initial version - MEJT
#   3 Apr 16   0.2   - Reads input files line by line, added ability to read
#                      from standard input - MEJT
#  25 Nov 17   0.3   - Tidied up parameter parsing code and added ability to
#                      parse values for parameters - MEJT
#                    - Added an optional delay between characters - MEJT
#                    - Version number now a 'constant' - MEJT
#
 
import sys, os
import time
 
VERSION = 0.3
 
def _about():
  sys.stdout.write(
    "Usage: " + sys.argv[0] + "[OPTION]... [FILE]...\n" +
    "Concatenate FILE(s)to standard output.\n" + "\n" +
    "  -b, --number-nonblank    number nonempty output lines," + 
    " overrides -n\n" + 
    "  -n, --number             number all output lines \n" +
    "  -r, --restart            line numbers start at zero, implies -n\n" +
    "  -s, --squeeze-blank      suppress repeated empty output lines\n" +
    "  -d, --delay              delay between each byte\n" +
    "  -?, --help               display this help and exit\n" +
    "      --version            output version information and exit\n\n" +
    "Example:\n" +
    "  " + _os.path.basename(sys.argv[0]) + " f g\t   output f's contents, then g's contents.\n")
  raise SystemExit
 
def _version():
  sys.stdout.write(os.path.basename(sys.argv[0]) + " " + str(VERSION) +"\n"
    "License GPLv3+: GNU GPL version 3 or later <http://gnu.org/licenses/gpl.html>.\n"
    "This is free software: you are free to change and redistribute it.\n"
    "There is NO WARRANTY, to the extent permitted by law.\n")
  raise SystemExit
 
def _error(_error):
  sys.stderr.write(os.path.basename(sys.argv[0]) + ": " + _error + "\n")
  raise SystemExit
 
def _print(_line):
  global _number, _nonblank, _strip, _count, _blanks
  if len(_line) > 1: _blanks = 0
  if not(_blanks > 1 and _strip):
    if _number and not(len(_line) == 1 and _nonblank):
      _count += 1
      sys.stdout.write("%6d  " % _count)
    for _char in _line:
      sys.stdout.write(_char)
      sys.stdout.flush()
      time.sleep(_delay/1000.0)
  _blanks += 1
 
_names = []
_restart = False
_number = False
_nonblank = False
_strip = False
_delay = 0
_count = 1
 
while _count < len(sys.argv):
  _arg = sys.argv [_count]
  if _arg[:1] == "-" and len(_arg) > 1:
    if _arg in ["--squeeze-blank", "-s"]:
      _strip = True
    elif _arg in ["--restart", "-r"]:
      _number = True
      _restart = True
    elif _arg in ["--number", "-n"]:
      _number = True
    elif _arg in ["--number-nonblank", "-b"]:
      _number = True
      _nonblank = True
    elif _arg in ["--delay","-d"]:
      _count += 1
      if _count < len(sys.argv):
        _delay = sys.argv [_count]
        try: 
          _delay = int(_delay)
          if _delay < 0 or _delay > 5000:
            _error("delay out of range")
        except ValueError:
          _error("delay invalid")
    elif _arg in ["--help", "-?"]:
      _about()
    elif _arg in "--version":
      _version()
    else:
      if _arg[:2] == "--":
        _error ("unrecognized option -- '" + (_arg + "'"))
      else:
        _error ("invalid option -- '" + (_arg[1:] + "'"))
  else:
    _names.append(_arg) # If it isn't a qualified 
  _count += 1
 
if not len(_names) : _names.append("-") # Default to stdin.
 
_count = 0
_blanks = 0
for _name in _names: 
  if _restart : _count = 0
  try:
    if _name== "-": # Handle input from standard input.
      _line = sys.stdin.readline() # Read ahead.
      while _line:
        _print(_line)
        _line = sys.stdin.readline()
    else: # Read from file.
      with open(_name, 'r') as _file:
        for _line in _file:
          _print(_line)
  except IOError as _err:
    _error(_name + ": " + _err.strerror)
  except KeyboardInterrupt: # Catch ^C
    sys.stdout.write("\n")
    sys.exit(0) 
