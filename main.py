#import things
from telethon import TelegramClient, events
from specs import id,hash,token4
import re
import asyncio
import pymongo
import datetime


#logging the client in mongo
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["telegram"]
col = db["messages information"]


#introduce the class
class mosiyobot(TelegramClient):
    def __init__(self, name, api_id, api_hash,col):
        super().__init__(name, api_id, api_hash)
        self.add_event_handler(self.start_bot, events.NewMessage(pattern='/start'))
        self.add_event_handler(self.addition, events.NewMessage)
        self.add_event_handler(self.subtraction, events.NewMessage)
        self.add_event_handler(self.multiplication, events.NewMessage)
        self.add_event_handler(self.division, events.NewMessage)
        self.add_event_handler(self.power1, events.NewMessage)
        self.add_event_handler(self.power2, events.NewMessage)
        self.add_event_handler(self.errors, events.NewMessage)
         
 
##functions
#start function
    async def start_bot(self, event): 
        await event.reply('سلام،من ربات محاسبنده ام!') 
        raise events.StopPropagation  
  
    
#addition function        
    async def addition(self, event): 
        if re.findall('\+',event.text) == ['+']:
            num = event.text.replace(' ','')
            list = num.split('+')
            answer = str(float(list[0])+float(list[1]))
            await event.reply(answer)
#mongo db part
            the_now=datetime.datetime.now()
            now='{0}:{1}:{2}'.format(the_now.hour,the_now.minute,the_now.second) 
            dict = {'question': event.text ,'answer':answer, 'time': now, 'message_id':event.message.id,'user_id':event.message.peer_id.user_id }
            x = col.insert_one(dict)  
            
            
#subtraction function   
    async def subtraction(self, event): 
        if re.findall('\-',event.text)==['-']:
            num = event.text.replace(' ','')
            list = num.split('-')
            answer = str(float(list[0])-float(list[1]))
            await event.reply(answer)
#mongo db part
            the_now=datetime.datetime.now()
            now='{0}:{1}:{2}'.format(the_now.hour,the_now.minute,the_now.second) 
            dict = {'question': event.text ,'answer':answer, 'time': now, 'message_id':event.message.id,'user_id':event.message.peer_id.user_id }
            x = col.insert_one(dict)    
        
        
#multiplication function   
    async def multiplication(self, event): 
        founded = re.findall('\*|\×',event.text)
        if founded == ['*'] or founded==['×']:
            num = event.text.replace(' ','')
            list = re.split('\*|\×',num)
            answer = str(float(list[0])*float(list[1]))
            await event.reply(answer)
#mongo db part
            the_now=datetime.datetime.now()
            now='{0}:{1}:{2}'.format(the_now.hour,the_now.minute,the_now.second) 
            dict = {'question': event.text ,'answer':answer, 'time': now, 'message_id':event.message.id,'user_id':event.message.peer_id.user_id }
            x = col.insert_one(dict)          


#division
    async def division(self, event): 
        founded = re.findall('/|÷',event.text)
        if founded == ['/'] or founded==['÷']:
            num = event.text.replace(' ','')
            list = re.split('/|÷',num)
            number = float(list[0])/float(list[1])
            answer = f'{number:.4f}'
            await event.reply(f'{answer}بفرما،برات تا چار رقم اعشار زدم صفا كني!')
#mongo db part
            the_now=datetime.datetime.now()
            now='{0}:{1}:{2}'.format(the_now.hour,the_now.minute,the_now.second) 
            dict = {'question': event.text ,'answer':answer, 'time': now, 'message_id':event.message.id,'user_id':event.message.peer_id.user_id }
            x = col.insert_one(dict)     
  
   
#power part 1
    async def power1(self, event): 
        if re.findall('توان',event.text)==['توان']:
            num = event.text.replace(' ','')
            list = num.split('بهتوان')
            answer = str(float(list[0])**float(list[1]))
            tafsir=f'{list[0]}**{list[1]}'
            await event.reply(answer)
#mongo db part
            the_now=datetime.datetime.now()
            now='{0}:{1}:{2}'.format(the_now.hour,the_now.minute,the_now.second) 
            dict = {'question': event.text ,'answer':answer,'tafsir':tafsir, 'time': now, 'message_id':event.message.id,'user_id':event.message.peer_id.user_id }
            x = col.insert_one(dict)    
 
  
#power part2                
    async def power2(self, event): 
        if re.findall('جذر',event.text)==['جذر']:
            num = event.text.replace(' ','')
            list = num.split('جذر')
            number = float(list[1])**0.5
            tafsir=f'√{list[1]}'
            answer = f'{number:.4f}'
            await event.reply(f'{answer}بفرما،برات تا چار رقم اعشار زدم صفا كني!')
#mongo db part
            the_now=datetime.datetime.now()
            now='{0}:{1}:{2}'.format(the_now.hour,the_now.minute,the_now.second) 
            dict = {'question': event.text ,'answer':answer,'tafsir':tafsir, 'time': now, 'message_id':event.message.id,'user_id':event.message.peer_id.user_id }
            x = col.insert_one(dict)         


#errors
    async def errors(self,event):
        if re.findall('\+',event.text) != ['+'] and re.findall('\-',event.text)!=['-'] and \
            re.findall('\*|\×',event.text)!=['×'] and re.findall('\*|\×',event.text)!=['*'] and \
                re.findall('/|÷',event.text)!=['÷'] and re.findall('/|÷',event.text)!=['/'] and \
                    re.findall('توان',event.text)!=['توان'] and re.findall('جذر',event.text)!=['جذر'] :
                    
                       await event.reply('جان؟')
            
   
       
#build the data base        
async def mongodb(self):               
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client["telegram"]
    col = db["messages information"]
    self.col=col

   
#turn the bot on       
the_bot = mosiyobot('bot',id,hash,col)
the_bot.start(bot_token=token4)
the_bot.run_until_disconnected()
# :)