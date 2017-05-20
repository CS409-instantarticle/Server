from dep import *
from get_text import *
from jsonify_content import *

class NewsArticle:
    ArticleID = 0
    ArticleTitle = None
    SectionName = None
    ArticleDate = None
    ThumbnailImageURL = None
    Video = False
    Link = None
    Press = None
    Raw_contents = None
    Contents = []

    def log(self):
        print("\tArticle ID : " + str(self.ArticleID))
        print("\tArticle Title : " + str(self.ArticleTitle))
        print("\tArticle Section : " + str(self.SectionName))
        print("\tArticle Date : " + str(self.ArticleDate))
        print("\tThumbnail URL : " + str(self.ThumbnailImageURL))
        print("\tVideo? : " + str(self.Video))
        print("\tArticle Link : " + str(self.Link))
        print("\tContents : " + str(self.Contents))

    def get_contents(self):
        texts = get_text(self.Link)
        self.Raw_contents = texts
        self.Contents = jsonify_content(texts)
        
    def write(self):
        with open("articles/%s%s" % (self.ArticleDate.replace(":", "").replace("-", "").replace(" ", ""), self.ArticleID), "w") as f:
            f.write(str(self))
    
    def __str__(self):
        d = dict()
        d["ArticleID"] = str(self.ArticleID)
        d["ArticleTitle"] = str(self.ArticleTitle)
        d["SectionName"] = str(self.SectionName)
        d["ArticleDate"] = str(self.ArticleDate)
        d["Press"] = str(self.Press)
        d["ThumbnailImageURL"] = str(self.ThumbnailImageURL)
        d["Video"] = str(self.Video)
        d["Link"] = str(self.Link)
        d["Contents"] = (self.Contents)
        return str(d)
