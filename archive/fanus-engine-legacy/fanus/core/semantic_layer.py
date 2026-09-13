class SemanticCore:
    """
    تبدیل فانوس از rule-based به meaning-based system
    """

    def embed(self, text):
        # فعلاً ساده، بعداً می‌تونه مدل واقعی بشه
        return hash(text) % 1000

    def similarity(self, a, b):
        return 1 - abs(self.embed(a) - self.embed(b)) / 1000
