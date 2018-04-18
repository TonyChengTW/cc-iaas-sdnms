class BackendManager(object):
    def __init__():
        self.firewall = Firewall()
        self.waf = Waf()
        self.switch = Switch()

    def use_firewall(self, index=0, identity=None, selector=None):
        if selector is None:
            self.firewall.index = index
            self.firewall.identity = identity
        else:
            self.firewall.index = selector.get_index()
            self.firewall.identity = selector.get_identity()

    def use_waf(self, index=0, identity=None, selector=None):
        if selector is None:
            self.waf.index = index
            self.waf.identity = identity
        else:
            self.waf.index = selector.get_index()
            self.waf.identity = selector.get_identity()

    def use_switch(self, index=0, identity=None, selector=None):
        if selector is None:
            self.switch.index = index
            self.switch.identity = identity
        else:
            self.switch.index = selector.get_index()
            self.switch.identity = selector.get_identity()

    def call_firewall(self, method=None, *args=None, **kwargs=None)
        fn = getattr(self.firewall, method)
        return fn(*args, **kwargs)

    def call_waf(self, method=None, *args=None, **kwargs=None)
        fn = getattr(self.waf, method)
        return fn(*args, **kwargs)

    def call_switch(self, method=None, *args=None, **kwargs=None)
        fn = getattr(self.switch, method)
        return fn(*args, **kwargs)
