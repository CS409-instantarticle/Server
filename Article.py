import articleCrawler

class NewsArticle:
        ArticleID = 0
        ArticleTitle = None
        ArticleDate = None
        ThumbnailImageURL = None
        Video = False
        Link = None
        Text = None

        def log(self):
                print("	Article ID : " + str(self.ArticleID))
                print("	Article Title : " + str(self.ArticleTitle))
                print("	Article Date : " + str(self.ArticleDate))
                print("	Thumbnail URL : " + str(self.ThumbnailImageURL))
                print("	Video? : " + str(self.Video))
                print("	Article Link : " + str(self.Link))
                print("	Text : " + str(self.Text))

        def get_contents(self):
                self.Text = articleCrawler.get_text(self.Link)