import re
class Input:
    def __init__(self,*args,**kwargs):
        if kwargs:
            for key,val in kwargs.items():
                if key=='filename' or key=='fn':
                    self.filename=val
        elif args:
            for arg in args:
                self.filename=arg
        else:
            self.filename=''

        ''' Data format
        '''
        self._cellfields_=('number','material','density','geometry','parameters')
        self._surfacefields_=('number','transformation','mnemonic','list')
        self._datafields_=('source','tally','material')
        ''' Data storage
        '''
        self.message={}
        self.title=''
        self.cell={}
        self.surface={}
        self.data={}
        self.data['current']=''
        self.err=[]

        ''' Temporary data
        '''
        self._tmpcell_={}
        self._tmpsurface_={}

    def open(self,filename):
        self.filename=filename

    def readMessage(self,line):
        var=line.split()
        key=''
        value=''
        for word in var:
            if word=='':
                continue
            if '=' in word:
                tmp=word.split('=')
                if tmp[0]!='':
                    key=tmp[0]
                if tmp[1]!='':
                    value=tmp[1]
            else:
                if key=='':
                    key=word
                elif value=='':
                    value=word
            if not (key=='' or value==''):
                message[key]=value
    def readTitle(self,line):
        self.title=line.strip()

    def trucExpr(self,word):
        tmp=word
        tmp=re.sub(' +\(','(',tmp)
        tmp=re.sub(' +\)',')',tmp)
        tmp=re.sub(' +:',':',tmp)
        tmp=re.sub(' +#','#',tmp)
        tmp=re.sub('\( +','(',tmp)
        tmp=re.sub('\) +',')',tmp)
        tmp=re.sub(': +',':',tmp)
        tmp=re.sub('# +','#',tmp)
        tmp=re.sub(' +',' ',tmp)
        return tmp
    def readCell(self,line):
        if len(line[0:5].split())==0:
        else:
            flag=True
            for key in self._cellfields_[0:4]:
                if key not in _tmpcell_.keys():
                    flag=False
            if flag:
                self.cell.append(self._tmpcell_)
            else:
                self.err.append(line)
            self._tmpcell_.clear()
        words=line.split()
        for word in words:
            field=''
            for entry in self._cellfields_:
                if entry not in self._tmpcell_.keys():
                    field=entry
                    break
            if field in self._cellfields_[0:3]:
                self._tmpcell_[field]=word
            elif field==self._cellfields_[3]:
                self._tmpcell_[field]=[]
                self._tmpcell_[field].append(self.trucExpr(word))
            elif field==self._cellfields_[4]:
                if '=' in word:
                    tmp=word.split('=')
                    self._tmpcell_[field]={}
                    if len(tmp>1):
                        self._tmpcell_[field][tmp[0]]=tmp[1]
                else:
                    self._tmpcell_[self._cellfields_[3]].append(self.trucExpr(word))
            else:
                tmp=word.split('=')
                if len(tmp>1):
                    self._tmpcell_[self._cellfields_[4]][tmp[0]]=tmp[1]

    def readSurface(self,line):
        ''' Save last cell
        '''
        if not self._tmpcell_:
            self.cell.append(self._tmpcell_)
            self._tmpcell_.clear()
        words=line.split()
        tmp=line[0:5]
        tmp=tmp.strip()
        if tmp=='':
        else:
            if self._tmpsurface_:
                self.surface.append(self._tmpsurface_)
                self._tmpsurface_.clear()
            for word in words:
                field=''
                for i in self._surfacefields_:
                    if i not in self._tmpsurface_.keys():
                        field=i
                        break
                if field==self._surfacefields_[1]:
                    try:
                        int(word)
                    except ValueError:
                        field=self._surfacefields_[2]
                        self._tmpsurface_[field]=word
                elif field=='':
                    self._tmpsurface_[self._surfacefields_[3]].append(word)
                elif field==self._surfacefields_[3]:
                    self._tmpsurface_[field]=[]
                    self._tmpsurface_[field].append(word)
                else:
                    self._tmpsurface_[field]=word

    def readData(self,line):
        mnemonic=line[0:5]
        mnemonic=mnemonic.strip()
        if mnemonic=='':
        else:
            words=line.split()
            field=words[0].lower()
            for i in self._datafields_:
                if i.lower()==field:
                    self.data['current']=i
            '''Source card
            '''
            if self.data['current']==self._datafields_[0]:
                self.data.source={}
                key=''
                val=''
                for word in words:
                    tmp=word.split('=')
                    tmp=[i for i in tmp if i]
                    if '=' in word:
                        val=''
                        if len(tmp)<1 and not key:
                            self.err.append(line)
                        elif len(tmp<2):
                            if key and '='+tmp[0]==word.strip():
                                val=tmp[0]
                            elif key and val and tmp[0]+'='==word.strip():
                                self.data.source[key]=val
                                key=tmp[0]
                                val=''
                    else:
                        if not key:
                            key=tmp[0]
                        elif not val:
                            val=tmp[0]
                        else:
                            if type(val)==list:
                                val.append(tmp[0])
                            else:
                                lst=[]
                                lst.append(val)
                                lst.append(tmp[0])
                                val=lst
                if key and val:
                    self.data.source[key]=val
                else:
                    self.err.append(line)
            '''Tally card
            '''
            elif self.data['current']==self._datafields_[1]:
            '''Material card
            '''
            elif self.data['current']==self._datafields_[2]:
                if words[0][0:2].lower()=='mt':
                    if not 'mt' in self.data.keys():
                        self.data['mt']={}
                    elif not type(self.data['mt'])==dict:
                        self.data['mt']={}
                    self.data['current']
            else:
                '''Mode card
                '''
                if field.lower()=='mode':
                    self.data[field]=[]
                    for word in words:
                        self.data[field].append(word)
                '''NPS card
                '''
                elif field.lower()=='nps':
                    self.data[field]=words[1]


    def initiate(self):
        flag=0
        with open(self.filename) as fp:
            first_line=fp.readline().strip()
            if re.search('message',first_line.lower(),re.IGNORECASE):
                flag=-1
        with open(self.filename) as fp:
            for line in enumerate(fp):
                ''' Skip comment lines
                '''
                tmp=line[0:5]
                if tmp.strip()[0].lower()=='c':
                    continue
                ''' Remove inline comment and newline
                '''
                line=line.split('$',1)[0].strip()
                if line in ['\n','\r\n']:
                    ++flag
                ''' Read message
                '''
                if flag<0:
                    self.readMessage(line)
                '''Read title
                '''
                elif flag==0:
                    self.readTitle(line)
                    ++flag
                ''' Read cell
                '''
                elif flag==1:
                    self.readCell(line)
                ''' Read surface
                '''
                elif flag==2:
                    self.readSurface(line)
                ''' Read data
                '''
                elif flag==3:
                    self.readData(line):
                else:
                    continue

    def compare(self,rival,output):
        sub=Input(rival)
        sub.initiate()
        with open(output,'w') as writer:
            if self.lattice!=sub.lattice:
                writer.write('Lattice differ\r\n')
            if self.cell!=sub.cell:
                writer.write('Cell differ\r\n')
            if self.roi!=sub.roi:
                writer.write('ROI differ\r\n')
            if self.universe!=sub.universe:
                writer.write('Universe differ\r\n')
            if self.surface!=sub.surface:
                writer.write('Surface differ\r\n')
            if self.material!=sub.material:
                writer.write('Material differ\r\n')
            if self.tally!=sub.tally:
                writer.write('Tally differ\r\n')
            if self.data!=sub.data:
                writer.write('Data differ')
            if self.source!=sub.source:
                writer.write('Source differ\r\n')
