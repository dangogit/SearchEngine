class ConfigClass:
    def __init__(self):
        self.corpusPath = r'C:\Users\Daniel\Desktop\BGU\שנה ג\סמסטר ה\אחזור מידע\עבודות\Data'
        self.savedFileMainFolder = ''
        self.saveFilesWithStem = self.savedFileMainFolder + "/WithStem"
        self.saveFilesWithoutStem = self.savedFileMainFolder + "/WithoutStem"
        self.savePostingFile = self.savedFileMainFolder + "/PostingFile"
        self.toStem = False

        print('Project was created successfully..')

    def get__corpusPath(self):
        return self.corpusPath
