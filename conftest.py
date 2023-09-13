def pytest_unconfigure(config):
    capmanager = config.pluginmanager.getplugin("capturemanager")
    capmanager.suspend_global_capture(in_=True)
