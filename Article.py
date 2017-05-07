import articleCrawler

class NewsArticle:
        ArticleID = 0
        ArticleTitle = None
        SectionName = None
        ArticleDate = None
        ThumbnailImageURL = None
        Video = False
        Link = None
        Text = None

        def log(self):
                print("\tArticle ID : " + str(self.ArticleID))
                print("\tArticle Title : " + str(self.ArticleTitle))
                print("\tArticle Section : " + str(self.SectionName))
                print("\tArticle Date : " + str(self.ArticleDate))
                print("\tThumbnail URL : " + str(self.ThumbnailImageURL))
                print("\tVideo? : " + str(self.Video))
                print("\tArticle Link : " + str(self.Link))
                print("\tText : " + str(self.Text))

        def get_contents(self):
                self.Text = articleCrawler.get_text(self.Link)
