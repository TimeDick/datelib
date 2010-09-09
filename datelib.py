#!/usr/bin/env python
"""
Copyright (c) 2010  Alex Goretoy <alex@goretoy.com>

This lib offers extensions to the standard python 2.5+
datetime and dateutil.relativedelta modules. 
It allows to work with start and end dates with ease.
"""
__author__ = "Aleksandr Ilyich Goretoy <alex@goretoy.com>"
__license__ = "PSF License"

from datetime import date,timedelta
from dateutil.relativedelta import relativedelta #imported for use in _add() and _sub()
from sys import _getframe #imported for use in calc()

import time #used in date_object_from_string()

class datelib(object):
    """
    datelib - works with dates, allows to add or subract months,days or years with ease
    usage: 
        from datelib import datelib
        d=datelib()
        d.dates_list()
        
>>> datelib.datelib("jun 5, 1980", "feb 20, 1981","%b %d, %Y","%Y-%m-%d").dates_list()
['1980-06-05', '1980-07-05', '1980-08-05', '1980-09-05', '1980-10-05', '1980-11-05', '1980-12-05', '1981-01-05', '1981-02-05', '1981-02-20']

        
    """
    def __init__(self, start=date.today()-timedelta(days=365), end=date.today(), fmt="", format="", direction="add", amount='1', modify='months', point="start"):
        """
__init__() - internal function used for object initialization
    start - startdate. date defaults to one year ago today
    end - enddate, defaults to today
    point - modify start or end date?, default start
    direction - add or sub on calulation?, default add
    modify - modification type, months, days, years, default months
    amount - amount to modify, default 1 
    format - date objects string format, default ""
        no format returns datetime.date objects
    fmt - format of init startdate and end date, used to convert to date object
                    
        """
        if isinstance(start, str):
            start = self.date_object_from_string(start, fmt)
        if isinstance(end, str):
            end = self.date_object_from_string(end, fmt)
            
        self.start_date=self._startdate=self.startdate=start
        self.end_date=self._enddate=self.enddate=end
        """
            start_date & end_date - used to set  new date and reset the date with reset_*()
            _startdate & _enddate - used to keep original init dates
            startdate & enddate - used in calculations/modifications of dates
        """
        self.direction=direction
        self._direction=direction
        self.point=point
        self._point=point
        self.modify=modify
        self._modify=modify
        self.amount=amount
        self._amount=amount
        self.format=format
        self._format=format

        self.prefs(point=point,direction=direction,modify=modify,amount=amount,format=format)

    def date_object_from_string(self,string,format):
        """
date_object_from_string() -> datetime.date object
    string - string representation of a date
    format - format of the string
            
        """
        
        #if format is srong it will raise a ValueError
        d=time.strptime(string,format)
        l = [ int(i) for i in time.strftime("%Y %m %d", d).split()]
        return date( l[0], l[1], l[2] )
        
    def dates_list(self,*targs,**dargs):
        """
dates_list() - takes params same as prefs()
    returns list of formatted/calculated dates
                
        """
        self.prefs(*targs,**dargs)
        l=[]
        #setting first elem, startdate
        try:
            if self.format!="":
                l=[self.startdate.strftime(self.format)]
            else:
                l=[self.startdate]
        except ValueError:
            l=["%s"%self.startdate]
        #set remaining elems
        while self.startdate<self.enddate:
            l.append(self.calc()[0])        
        self.reset_dates(*targs)
        return l
    def dates_dict(self,*targs,**dargs):
        """
dates_dict() - takes params same as prefs()
    returns dict key/value pair of formatted/calculated dates
    key is a date, value is timedelta enddate-startdate 
                
        """
        self.prefs(*targs,**dargs)
        d={}
        #setting first elem, startdate
        try:
            if self.format!="":
                d[self.startdate.strftime(self.format)]=self.dates_diff()
            else:
                d[self.startdate]=self.dates_diff()
        except ValueError:
            d["%s"%self.startdate]=self.dates_diff()
        #set remaining elems
        while self.startdate<self.enddate:
            a=self.calc()[0]
            d[a]=self.dates_diff()
        self.reset_dates(*targs)
        return d
    def dates_diff(self,*targs):
        """
dates_diff() - return timedelta difference between startdata and enddate
    takes nothing, a tuple, a list or 2 date objects as params
    return enddate - startdate timedelta
                
        """
        start,end=(self.startdate,self.enddate)
        if targs:
            if(len(targs)==1):
                if(type(targs[0])==type(()) or targs[0] == type([])):
                    if(len(targs[0])==2):
                        if(type(targs[0][0])==type(date.today()) and targs[0][1] == type(date.today())):
                            start,end=(targs[0][0],targs[0][1])
            elif(len(targs)== 2):
                if(type(targs[0])==type(date.today()) and targs[1] == type(date.today())):
                    start,end=(targs[0],targs[1])            
        return end-start

    def _add(self,*targs):
        """
_add - sets delta to add onto startdate or enddate 
    modify - can be months,days or years
    amount - can be any positive digit
            
        """
        if(targs):
            for targ in targs:
                if(str(targ).isdigit()):
                    self.amount=targ
                    
                #elif(allowed_vprefs.has_key(targ)):
                #elif(targ=='months' or targ=='days' or targ=='years'):
                #    self.modify=targ
            #using eval since idk a way to set months.days,years at self._t
        #self.delta =  eval("relativedelta("+self.modify+"=+int("+self.a+"))")
        try:
            if self.modify == 'months':
                self.delta = relativedelta(months=int(self.amount))
            if self.modify == 'days':
                self.delta = relativedelta(days=int(self.amount))
            if self.modify == 'years':
                self.delta = relativedelta(years=int(self.amount))
        except ValueError:
            if self.modify == 'months':
                self.delta = relativedelta(months=1)
            if self.modify == 'days':
                self.delta = relativedelta(days=1)
            if self.modify == 'years':
                self.delta = relativedelta(years=1)
    def _sub(self,*targs):
        """
_sub - sets delta to substract from startdate or enddate
    modify - can be months,days or years
    amount - can be any positive digit
            
        """
        #self._direction_check(*targs)
        #allowed_vprefs={ 'months':'t','days':'t','years':'t' }
        if(targs):
            for targ in targs:
                if(str(targ).isdigit()):
                    self.amount=targ
                #elif(allowed_vprefs.has_key(targ)):
                #elif(targ=='months' or targ=='days' or targ=='years'):
                #    self.modify=targ
            #using eval since idk a way to set months.days,years at self._t
        #self.delta =  eval("relativedelta("+self.modify+"=-int("+self.a+"))")
        try:
            if self.modify == 'months':
                self.delta = relativedelta(months=-int(self.amount))
            if self.modify == 'days':
                self.delta = relativedelta(days=-int(self.amount))
            if self.modify == 'years':
                self.delta = relativedelta(years=-int(self.amount))
        except ValueError:
            if self.modify == 'months':
                self.delta = relativedelta(months=-1)
            if self.modify == 'days':
                self.delta = relativedelta(days=-1)
            if self.modify == 'years':
                self.delta = relativedelta(years=-1)
    def calc(self,*targs,**dargs):
        """
calc() - calculate dates values based on set preferences
    calls _start or _end, based on direction set by prefs()
    takes same params as prefs()                
    returns tuple of datetime.date start and end dates
    format dates if format string is set
                
        d=datelib()
        d.calc() #returns calculated dates tuple
        
        """    
        
        self.prefs(*targs,**dargs)
        if _getframe(1).f_code.co_name != "__call__":
            x=getattr(self,'_%s'%self.point,None)
            if callable(x):
                x()
        else:
            if targs:
                for targ in targs:
                    if targ:
                        if type(targ) == type(True):
                            x=getattr(self,'_%s'%self.point,None)
                            if callable(x):
                                x()        
        try:
            if self.format!="":
                return (self.startdate.strftime(self.format),self.enddate.strftime(self.format))
            else:
                return (self.startdate,self.enddate)
        except ValueError:
            return ("%s"%self.startdate,"%s"%self.enddate)       
    def _start(self):
        """
_start() - internal function to calculate delta of startdate
            
        """
        while self.startdate <= self.enddate:
            self.startdate+=self.delta
            if self.startdate >= self.enddate:
                self.startdate=self.enddate
            return self.startdate
    def _end(self):
        """
_end() - internal function to calculate delta of enddate
            
        """
        while self.startdate <= self.enddate:
            self.enddate+=self.delta
            if self.startdate >= self.enddate:
                self.enddate=self.startdate
            return self.enddate
    def orig_prefs_dict(self):
        """
orig_prefs_dict() - takes no arguments, returns original object init preferences key/value pair dictionary
        
        """
        return {'start':self._startdate, 'end':self._enddate, 'format':self._format, 'direction':self._direction, "amount":self._amount, "modify": self._modify, 'point':self._point}
    def prefs_dict(self):
        """
prefs_dict() - takes no arguments, returns preferences key/value pair dictionary
        
        """
        return {'start':self.startdate, 'end':self.enddate, 'format':self.format, 'direction':self.direction, "amount":self.amount, "modify": self.modify, 'point':self.point}
    def orig_prefs_list(self):
        """
orig_prefs_list() - takes no arguments, returns original object init preferences list
    returns [start, end, format, direction, amount, modify, point]
        """
        return [self._startdate,self._enddate,self._format,self._direction,self._amount,self._modify,self._point]
    def prefs_list(self):
        """
prefs_list() - takes no arguments, returns preferences list
    returns [start, end, format, direction, amount, modify, point]
        """
        return [self.startdate,self.enddate,self.format,self.direction,self.amount,self.modify,self.point]
    def prefs(self,*targs,**dargs):
        """
prefs() - Allows to change point, direction and months, days or years.
    start - excepts a datetime object to set startdate
        prefs(datetime.date.today())
        prefs(start=datetime.date.today())
    end - excepts a datetime object to set the enddate
        prefs(end=datetime.date.today())
    format - excepts a format string to format the dates
        prefs("%Y%m%d") - 20030808
        prefs(format="") - no date formatting,returns objects
    point - start or end, start or end date?
        prefs("start") - set startdate to be modified
        prefs(point="start") - same, start to be modified
        prefs("end") - set enddate to be modified
        prefs(point="end") - same, end to be modified
    direction - add or sub, increment or decrement date?
        prefs("add") - add on modification, default
        prefs(direction="add") - same, add on modify, default
        prefs("sub") - subtract on modification
        prefs(direction="sub") - same, subtract on modify
    modify - months, days or years, modify months,days or years?
        prefs("months") - set to modify months, default
        prefs("days") - set to modify days
        prefs("years") - set to modify years
        prefs(t="months") - same, set to modify months, default
        ...
    amount - amount of days,months years to add or subtrac on each calculation
        prefs(1) - set to modify date by 1
        prefs(a="7") - set to modify date by 7
                
        prefs('add',"7","days","%m-%d-%Y")

        """
        #check and set prefs
        self._set_prefs(*targs,**dargs)
        #call set direction with type and amount
        x=getattr(self,'_%s'%self.direction,None)
        if callable(x):
            x(self.modify,self.amount)
        else:
            raise AttributeError
        return self.prefs_dict()
    def reset_prefs(self,*targs,**dargs):
        """
reset_prefs() - reset prefs to object initialized prefs
    any params passed to this function override init prefs
    takes same params as prefs()
                
        """
        #set prefs to default from obj init, overriding those with any passed params
        return self.prefs(point=self._point,direction=self._direction,modify=self._modify,amount=self._amount,format=self._format,*targs,**dargs)
    def reset_start(self,*targs):
        """
reset_start() - resets startdate to date param or previous object
    takes date object to set new date, returns startdate object
                
        """
        if len(targs) == 1:
            if(type(targs[0]) == type(date.today())):
                if targs[0] < self.enddate:
                    self.startdate=targs[0]
                    self.start_date=targs[0]
            else:
                self.startdate=self.start_date
        else:
            self.startdate=self.start_date
        return self.startdate
    def reset_end(self,*targs):
        """
reset_end() - resets enddate to date param or previous object
    takes date object to set new date, returns enddate object
                
        """
        if len(targs) == 1:
            if(type(targs[0]) == type(date.today())):
                if self.startdate < targs[0]:
                    self.enddate=targs[0]
                    self.end_date=targs[0]
            else:
                self.enddate=self.end_date
        else:
            self.enddate=self.end_date
        return self.enddate
    def reset_dates(self,*targs):
        """
reset_dates() - resets both start and end date
    takes no params or 2 datetime.date objects  
        or tuple with start and end datetime.date objects
        or list with start and end datetime.date objects
    returns startdate and enddate tuple
    eg.
    reset_dates(date(2001,1,1),date.today())
    reset_dates((date(2001,1,1),date.today()))
    reset_dates([date(2001,1,1),date.today()])
                
        """
        a,b=(None,None)
        if targs:
            if len(targs) == 1:
                if(type(targs[0]) == type(()) or type(targs[0]) == type([])):
                    if(len(targs[0]) == 1):
                        a,b=(self.reset_start(targs[0][0]),self.reset_end())
                    elif(len(targs[0]) == 2):
                        a,b =(self.reset_start(targs[0][0]), self.reset_end(targs[0][1]))
                else: 
                    a,b =(self.reset_start(targs[0]), self.reset_end())
            elif len(targs) == 2:
                    a,b = (self.reset_start(targs[0]), self.reset_end(targs[1]))
            
        else:
            a,b = (self.reset_start(), self.reset_end())
        return (a,b)
    def reset(self,*targs,**dargs):
        """
reset() - resets preferences and start and end dates
    calls reset_prefs() and reset_dates() with params
    return dates tuple from reset_dates()
                
        """
        self.reset_prefs(*targs,**dargs)
        return self.reset_dates(*targs,**dargs)
    def _set_prefs(self,*targs,**dargs):
        """
_set_prefs() - internal function used by prefs()
    check and set preferences based on params
                
        """
        allowed_kprefs=['dates','start','end','format','point','direction','modify','amount']
        allowed_vprefs={ 'start':'point','end':'point','add':'direction','sub':'direction','months':'modify','days':'modify','years':'modify'}
        if(dargs):
#            try:
            for k,v in dargs.items():
                if(allowed_kprefs.index(k)>-1):
                    if(allowed_vprefs.has_key(v)):
                        setattr(self,'%s'%k,'%s'%v)
                    elif(str(v).isdigit()):
                        self.amount=v
                    elif(type(v)==type(date.today())):
                        x=getattr(self,'reset_%s',None)
                        if callable(x):
                            x(v)
                    elif(k=='format'):
                        self.format=v
                    elif(type(v)==type(()) or type(v)==type([])):
                        if(k=='dates'):
                            self.reset_dates(v)
#            except IndexError:
#                raise IndexError
#            except KeyError:
#                raise KeyError
        if(targs):
            for targ in targs:
                if allowed_vprefs.has_key(targ):
                    setattr(self,'%s'%allowed_vprefs[targ],targ)
                elif(str(targ).isdigit()):
                    self.amount=targ
                elif(type(targ)==type(date.today())):
                    self.reset_start(targ)
                elif(str(targ).find("%")>-1):
                    self.format=targ
                elif(targ==""):
                    self.format=targ
                elif(type(targ) == type(()) or type(targ) == type([])):
                    if(len(targ) == 1):
                        self.reset_start(targ[0])
                    elif(len(targ) == 2):
                        #self.reset_start(targ[0])
                        #self.reset_end(targ[1])
                        self.reset_dates((targ[0],targ[1]))
                    else:
                        self.reset_dates()
    def __call__(self,*targs,**dargs):
        """
__call__() - internal function that allows calling datelib instance directly
    Allows to call the datelib instance object, return start and end date in tuple
    as strings or as datetime.date objects
                
    d=datelib()
    d() #returns dates tuple
    d(True) #returns calculated dates tuple
                
        """
        return self.calc(*targs,**dargs)
        
    def __str__(self):
        """
__str__ - return string representation of start and end date tuple
    if no format string is set then return datetime.date objects
                
        """
        try:
            if self.format!="":
                return repr((self.startdate.strftime(self.format),self.enddate.strftime(self.format)))
            else:
                return repr((self.startdate,self.enddate))
        except ValueError:
            return repr(("%s"%self.startdate,"%s"%self.enddate))

