import desktop

class MatchingUI(desktop.DesktopUI):
    window = 0

    def __init__(self, ui, obj):
        self.window = ui
        super().setscreen(self.window.screenW, self.window.screenH)
        super().reset()
        self.setup()
        self.display(obj['gameBoard'], obj['next'], obj['cursor'], obj['timer'], obj['formula'])

    def setup(self): 
        super().setup()
        
        for i in range(2):
            super().framelist[1].destroy
            del super().framelist[1]

        super().framelist[1] = desktop.Frame(height = (super().getScreenH() / 10) * 8, width = super().getScreenW(), bg = super().backgroundC)
        super().framelist[1].pack_propagate(False)
        super().framelist[1].place(x = 0, y = super().getScreenH() / 10)

        bottomFrame = desktop.Frame(height = super().getScreenH() / 10, width = super().getScreenW(), bg = super().backgroundC)
        bottomFrame.pack_propagate(False)
        bottomFrame.place (y = super().getScreenH() * 9/10, x = 0)
        super().addFrame(bottomFrame)

    def display(self, boardState, nextP, cursor, timer, formula):
        for i in range (4):
            for j in range (10):
                if boardState[i, j] == "XX":
                    cardSuffix = "back"
                else:
                    cardSuffix = str(boardState[i, j])

                cardFilename = "card_" + cardSuffix +".png"

                if cursor == [i, j]:
                    cardFrame = desktop.Frame(super().framelist[1], height = super().getScreenH() / 5 - 20, width = super().getScreenW() / 10 - 20, bg = super().backgroundC, highlightthickness = 10)
                    cardImage = super().imageCreation(cardFilename, super().getScreenH() / 5 - 45, super().getScreenW() / 10 - 45, "/match/cards")
                else:
                    cardFrame = desktop.Frame(super().framelist[1], height = super().getScreenH() / 5 - 20, width = super().getScreenW() / 10 - 20, bg = super().backgroundC)
                    cardImage = super().imageCreation(cardFilename, super().getScreenH() / 5 - 20, super().getScreenW() / 10 - 20, "/match/cards")
               
                cardFrame.pack_propagate(False)
                cardFrame.grid(row = i, column = j, padx = 10, pady = 10) 

                label = desktop.Label(cardFrame, image = cardImage, bg = super().backgroundC)
                label.img = cardImage
                label.place(x = 0, y = 0)
        
        label = desktop.Label (super().framelist[0], text = nextP[0] + " select a card from the board. Time Remaining: " + str(timer), bg = super().backgroundC, font = super().setFontSize(int((super().getScreenH() / 30))), fg = 'white')
        label.place(anchor = "center", x = super().getScreenW() / 2, y = super().getScreenH() / 20)

        label2 = desktop.Label (super().framelist[2], text = "Next Player: " + nextP[1], bg = super().backgroundC, font = super().setFontSize(int((super().getScreenH() / 30))), fg = 'white')
        label2.place(anchor = "center", x = super().getScreenW() / 2, y = super().getScreenH() / 20)