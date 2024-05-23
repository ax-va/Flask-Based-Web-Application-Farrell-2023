class PageVisit:
    """ Counts the visits of the web page """
    VISITS = 0

    @classmethod
    def increment_visits(cls) -> int:
        cls.VISITS += 1
        return cls.VISITS
