import os
from bs4 import BeautifulSoup
import utilities
import nltk

class transcriptObject():
    
    def getFileName(self):
        return self.file[5:]    
    
    #@return = cleaned title
    def getCaseName(self):
        temp = ''.join(self.getSoup().title.text)
        temp = nltk.wordpunct_tokenize(temp)
        return ' '.join(utilities.remove_punctuation(temp))
        
    #@return = year the case was first brought to lower court
    def getCaseYear(self):
        return self.file[:4]
    
    def getDocketNumber(self):
        docket = self.file.replace('.xml', '')[15:]
        clean_docket = []
        for char in list(docket):
            if char.isdigit() or char == '-':
                clean_docket.append(char)
        return ''.join(clean_docket)

    #@return = tuple of the date of the cases arguement to the supreme court
    #@format = (year, month, day)
    def getDateOfArg(self):
        desc = ['day', 'month', 'year']
        year = self.file_name[0:4]
        month = self.file_name[4:6]
        day = self.file_name[6:8]
        date_of_arg = [day, month, year]
        return dict(zip(desc, date_of_arg))

    #@return = transcript XML file for use with BeautifulSoup API
    def getSoup(self):
        x = open(self.getFullPath(), 'r')
        return BeautifulSoup(x)                    
                                                            
    #@return = 2D tuple of the format ( (speaker_id(0), speaker_name(0), role_in_court_room, gender) , ... )
    #@data = all speakers in transcript
    def getSpeakerInfo(self):
        speakerInfo = []
        for speaker in self.soup.findAll("speaker"):
            speakerInfo.append( {'id': speaker['id'],
                                 'name': speaker.text,
                                 'type': speaker['type'],
                                 'gender': speaker['gender']} )
        return speakerInfo

    #@return = full directory path of transcript on users disk
    def getFullPath(self):
        return os.path.join(os.getcwd(),
                            'Transcripts', 
                            self.getCaseYear(), 
                            self.getFileName())                    
    
    
    def getSpeakerIds(self):
        speakerIds = []
        for speaker in self.speaker_info:
            speakerIds.append(speaker['id'])
        return speakerIds                
    
    
    #transcript object class constructor
    def __init__(self, file): 
        #fileName is initially of format   year/transcript_file_name.xml
        #this is pulled directly from corpus in the Transcripts directory
        self.file = file
        
        self.file_name = self.getFileName()
        self.case_name = self.getCaseName()
        self.case_year = self.getCaseYear()
        self.docket_number = self.getDocketNumber() 
        self.date_of_arg = self.getDateOfArg()
        
        self.soup = self.getSoup()  #for use with BeautifulSoup API
            
        self.full_file_path = self.getFullPath()  

        self.speaker_info = self.getSpeakerInfo()
        self.speaker_ids = self.getSpeakerIds()




                
