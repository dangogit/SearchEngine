class ConfigClass:
    def __init__(self):
        self.corpusPath = r'C:\Users\dorle\Data'
        self.savedFileMainFolder = ''
        self.saveFilesWithStem = self.savedFileMainFolder + "/WithStem"
        self.saveFilesWithoutStem = self.savedFileMainFolder + "/WithoutStem"
        self.savePostingFile = self.savedFileMainFolder + "/PostingFile"
        self.toStem = False

    def get__corpusPath(self):
        return self.corpusPath
