import pywikibot


class WikidataHandler():
    """
    Returns all the names for a named entity, if it can be found in wikidata.
    An internet connection must be available for this to work
    """

    def get_named_entities(self, named_entity):
        try:
            site = pywikibot.Site("en", "wikipedia")
            page = pywikibot.Page(site, named_entity)
            item = pywikibot.ItemPage.fromPage(page)
            item_dict = item.get()
            names = item_dict['aliases']['en']
        except Exception:
            names = []

        return names