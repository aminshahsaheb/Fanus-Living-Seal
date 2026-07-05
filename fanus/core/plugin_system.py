import importlib
import os


class PluginSystem:

    def __init__(self):
        self.plugins = {}

    def register(self, name, plugin):
        self.plugins[name] = plugin
        return {"registered": name, "total": len(self.plugins)}

    def load(self, module_path):
        try:
            module = importlib.import_module(module_path)
            name = module_path.split(".")[-1]
            self.plugins[name] = module
            return {"loaded": name, "status": "ok"}
        except Exception as e:
            return {"error": str(e), "status": "failed"}

    def run(self, name, method, *args, **kwargs):
        if name not in self.plugins:
            return {"error": "plugin not found"}
        plugin = self.plugins[name]
        if hasattr(plugin, method):
            return getattr(plugin, method)(*args, **kwargs)
        return {"error": "method not found"}

    def list_plugins(self):
        return list(self.plugins.keys())

    def stats(self):
        return {"total_plugins": len(self.plugins), "plugins": self.list_plugins()}
