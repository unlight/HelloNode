import sublime
import sublime_plugin
import os
import subprocess

# view.run_command("hello_node")

PLUGIN_FOLDER = os.path.dirname(os.path.realpath(__file__))
SETTINGS_FILE = "HelloNode.sublime-settings"
NODE_PATH = None

settings = sublime.load_settings(SETTINGS_FILE)

class HelloNodeCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		args = [get_node_path(), PLUGIN_FOLDER + "/hello.js"]
		for region in self.view.sel():
			# output = run_process(args)
			# pos = region.begin()
			# self.view.insert(edit, pos, output)
			
			sublime.set_timeout_async(lambda: self.view.run_command("long_loop"), 0)

class LongLoopCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		output = run_process([get_node_path(), PLUGIN_FOLDER + "/longloop.js"])
		region = self.view.sel()[0]
		pos = region.begin()
		self.view.insert(edit, pos, output)

def run_process(args):
	cmd = '"' + '" "'.join(args) + '"'
	startupinfo = subprocess.STARTUPINFO()
	startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
	output = subprocess.Popen(cmd, stdout=subprocess.PIPE, startupinfo=startupinfo).communicate()[0]
	return output.decode("utf-8")

def get_node_path():

	global NODE_PATH

	if NODE_PATH is not None:
		return NODE_PATH

	# Find path.
	node_path = settings.get("node_path")

	path = os.environ.get("PATH", "").split(os.pathsep)
	path.insert(0, node_path)
	extensions = os.environ.get("PATHEXT", "").split(os.pathsep)
	for directory in path:
		base = os.path.join(directory, "node")
		options = [base] + [(base + ext) for ext in extensions]
		for filename in options:
			if os.path.exists(filename):
				NODE_PATH = filename
				break
	
	if NODE_PATH is not None:
		return NODE_PATH

	# Suggest to define path.
	message = "Node.js was not found in the default path. Please specify the location."
	if sublime.ok_cancel_dialog(message):
		sublime.active_window().open_file(PLUGIN_FOLDER + "/" + SETTINGS_FILE)
	else:
		message = "You won't be able to use this plugin without specifying the path to Node.js."
		sublime.error_message(message)
