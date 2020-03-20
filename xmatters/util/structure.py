class Structure(object):

    # Searches the object and returns the associated values in an array
    def searchOnKey(self, keyword, obj):
        val = None
        for data in obj:
            value = self.doSearch(keyword, data)
            if value:
                if obj[data].strip() != '':
                    val = obj[data]
                break

        return val

    def doSearch(self, keyword, obj):
        try:
            obj.index(str(keyword))
            value = True
        except:
            value = False
        return value
