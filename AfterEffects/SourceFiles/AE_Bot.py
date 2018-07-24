import csv

from glob import glob

class User:
    def __init__(self, BASEPATH, code):
        self.BASEPATH = BASEPATH
        self.code = code

        self.MusicPath = self.BASEPATH + 'Music/'
        self.NewPath = self.MusicPath + 'New/'
        self.OldPath = self.MusicPath + 'Old/'
        self.CurrentPath = self.MusicPath + 'Current/'
        self.TestPath = self.BASEPATH + 'Test/'
        self.AEPath = self.BASEPATH + 'AfterEffects/'
        self.AESourcePath = self.AEPath + 'SourceFiles/'


user = User('C:/Users/corma/Documents/GitHub/YT-Music-AI/', 'cd')
marilyn = User('C:/Users/mjgro/Documents/GitHub/YT-Music-AI/', 'mg')
Path = user.BASEPATH
FileName = "MusicData.csv"
NewMusicPath = user.NewPath
CurrentMusicPath = user.CurrentPath
OldMusicPath = user.OldPath
TestMusicPath = user.TestPath
AEPath = user.AEPath
AESourcePath = user.AESourcePath


def error(errorMessage):
    print(">ERROR:\t" + str(errorMessage))\

def csvToXML(entry):
    xmlFile = 'musicTrack.xml'
    xmlData = open(xmlFile, 'w')
    write = '''
    <?xml version="1.0"?>\n
    <?mso-application progid="Excel.Sheet"?>
    <Workbook xmlns="urn:schemas-microsoft-com:office:spreadsheet" xmlns:o="urn:schemas-microsoft-com:office:office" xmlns:x="urn:schemas-microsoft-com:office:excel" xmlns:ss="urn:schemas-microsoft-com:office:spreadsheet" xmlns:html="http://www.w3.org/TR/REC-html40">\n
      <Styles>\n
        <Style ss:ID="Default" ss:Name="Normal">\n
          <Alignment ss:WrapText="1"/>\n
        </Style>\n
      </Styles>\n
      <Worksheet ss:Name="AscentTemplate.aep">\n
        <Table>\n
          <Row ss:Index="1">\n
            <Cell ss:Index="1">\n
              <Data ss:Type="String">ID</Data>\n
            </Cell>\n
            <Cell ss:Index="2">\n
              <Data ss:Type="String">original text</Data>\n
            </Cell>\n
          </Row>\n
          <Row ss:Index="2">\n
            <Cell ss:Index="1">\n
              <Data ss:Type="Number">1</Data>\n
            </Cell>\n
            <Cell ss:Index="2">\n
              <Data ss:Type="String">
              '''
    write += entry + '''
              </Data>\n
            </Cell>\n
          </Row>\n
        </Table>\n
      </Worksheet>\n
    </Workbook>\n
    '''
    xmlData.write(write)
    xmlData.close()


if __name__ == "__main__":
    # TODO move selected song and wallpaper to /AfterEffects/SourceFiles/
    # Write Track info for AscentTemplate
    musicFileList = glob(AESourcePath + '*.mp3')
    if musicFileList.__len__() != 1:
        error("Erroneous number of mp3s in /AfterEffects/SourceFiles/")
    else:
        track = str(musicFileList[0])[str(AESourcePath).__len__():]
        track = track.split('-')[:-1]
        artist = track[0]
        song = track[1]
        entry = str(str(artist.title() + '-' + song.title()))
        csvToXML(entry)
