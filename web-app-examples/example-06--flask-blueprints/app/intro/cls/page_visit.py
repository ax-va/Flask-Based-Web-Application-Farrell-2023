class PageVisit:
    """ Counts the visits of the web page """
    visits = 0

    @classmethod
    def increment_visits(cls) -> int:
        cls.visits += 1
        return cls.visits
