import articleCrawler

def split_by_img(text):
    if text.find("<img") != -1:
        start_index = text.find("<img")
        end_index = start_index
        while text[end_index] != '>':
            end_index += 1
        return [text[:start_index],text[start_index:end_index+1]] + split_by_img(text[end_index+1:])
    else:
        return [text]

class Content:
        index = None
        type = None
        content = None

        def __init__(self, i,t,c):
                self.index = i
                self.type = t
                self.content = c

class NewsArticle:
        ArticleID = 0
        ArticleTitle = None
        SectionName = None
        ArticleDate = None
        ThumbnailImageURL = None
        Video = False
        Link = None
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
                texts = articleCrawler.get_text(self.Link)
                splited_contents = split_by_img(texts)

                #Remove blanks
                for i in range(len(splited_contents)):
                        splited_contents[i] = splited_contents[i].lstrip()
                if splited_contents[0] == '':
                        splited_contents.remove(splited_contents[0])

                index = 0
                contents = []
                for conts in splited_contents:
                        if conts.find("<img") != -1:
                                # Image contents
                                contents.append(Content(index, "image", conts).__dict__)
                        else:
                                # Text contents
                                contents.append(Content(index, "text", conts).__dict__)
                        # Image description not yet processed
                        index += 1
                self.Contents = contents