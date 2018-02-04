import numpy as np
import csv

class Captions:
    def __init__(self):
        self.lyrics = []
        self.generic = []
        self.sentimental = []
        self.funny = []
        self.selfie = []
        self.fetchCaptions()


    def fetchCaptions(self):

        with open('insta_captions.csv', newline='') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
            i = 0
            for row in spamreader:
                caption = ', '.join(row)

                if '\"' in caption:
                    caption = caption.strip('\"')
                if i == 0:
                    caption = caption.strip(caption[0])

                if 'captions_' in caption:
                    header = caption
                    i = 1
                    continue

                if header == 'captions_lyric':
                    self.lyrics.append(caption)
                elif header == 'captions_generic':
                    self.generic.append(caption)
                elif header == 'captions_sentimental':
                    self.sentimental.append(caption)
                elif header == 'captions_funny':
                    self.funny.append(caption)
                elif header == 'captions_selfie':
                    self.selfie.append(caption)


    # pass in array of wanted captions. If any category caption is wanted, construct array of all of them first then send in
    def findCaptionsWith(self, keyword, captionType = None):
        captionSuggestions = []
        possibleCaptions = self.getCaptionsByType(captionType)

        for caption in possibleCaptions:
            if keyword in caption:
                captionSuggestions.append(caption)

        return captionSuggestions

    # pass a list which has been refined to only have the user specified keywork, as well as the list of tags from the photo
    # pass throuhg refined list, looking for first tag. If less than 3 captions with that tag are found, go to second
    # tag, third tag, etc.
    def findRefinedCaptionsWith(self, tags, refinedCaptions, captionType = None):
        n = 3 # num of captions to return
        captionSuggestions = []
        # change from linear to counting number of captions then return greatest ones
        if len(refinedCaptions) == n:
            return refinedCaptions
        elif len(refinedCaptions) < n:
            typeCaptions = self.getCaptionsByType(captionType)
            for tag in tags:
                for cap in typeCaptions:
                    if tag in cap:  # if tag is in the refined caption
                        refinedCaptions.append(cap)
                    if len(refinedCaptions) >= n:
                        return refinedCaptions

            return refinedCaptions # if no more are found
        else:
            for tag in tags:
                for refCap in refinedCaptions:
                    if tag in refCap: # if tag is in the refined caption
                        captionSuggestions.append(refCap)

                    if len(captionSuggestions) >= n:
                        return captionSuggestions

            return captionSuggestions # if no more are found


    def getCaptionsByType(self, type):
        if type == "lyric":
            return self.lyrics
        elif type == "generic":
            return self.generic
        elif type == "sentimental":
            return self.sentimental
        elif type == "funny":
            return self.funny
        elif type == "selfie":
            return self.selfie
        else:
            return [self.lyrics, self.generic, self.sentimental, self.funny, self.selfie]

    def getLyric(self): return self.lyrics
    def getGeneric(self): return self.generic
    def getSentimental(self): return self.sentimental
    def getFunny(self): return self.funny
    def getSelfie(self): return self.selfie
