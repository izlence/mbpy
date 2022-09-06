import inspect 
import sqlite3

#from data import customconfig #working 
#import customconfig

class mbdb():       

    # @staticmethod
    # def get_db_path(pWhichDb):
    #     #print(pTableClass._db_)        
    #     return customconfig.db[pWhichDb]        
               


    @staticmethod
    def executeCursor(db_path, psql, pparams):
        try:
            db = sqlite3.connect(db_path)
            cursor = db.cursor()        
            cursor.execute(psql, pparams)            
            return cursor
        except Exception as ex:
            print(ex)

        return None
        
    @staticmethod        
    def NonQuery(db_path, psql, pparams):
        try:
            db = sqlite3.connect(db_path)
            cursor = db.cursor()        
            cursor.execute(psql, pparams)
            intr = cursor.rowcount
            cursor.close()
            if intr>0:
                db.commit()
            return intr
        except Exception as ex:
            print(ex)

        return 0

    @staticmethod        
    def Scalar(db_path, psql, pparams):
        try:
            db = sqlite3.connect(db_path)
            cursor = db.cursor()        
            cursor.execute(psql, pparams)
            rec = cursor.fetchone()
            cursor.close()
            return rec
        except Exception as ex:
            print(ex)

        return None
        


    @staticmethod
    def insertTable(db_path, pcls:any):
        '''
        inserts a record into sqlite table.
        '''
        
        fields = []
        vals = []
        
        # getmembers() returns all the  members of an object  
        for it in inspect.getmembers(pcls):        
            # to remove private and protected functions 
            if not it[0].startswith('_'):           
                # To remove other methods that doesnot start with a underscore 
                if not inspect.ismethod(it[1]):
                    if(it[0]=="id"):
                        id_record=it[1]
                        continue

                    fields.append(it[0]) # + "=?")
                    vals.append(it[1])                    
                    #print(it[0], it[1])

        #print(pcls.__class__.__name__)
        table_name = type(pcls).__name__

        q = "INSERT OR IGNORE INTO " + table_name + " (" + ", ".join(fields) + ") VALUES ("
        q += "?, " * (len(fields)-1)
        q += "? )"

        return mbdb.NonQuery(db_path, q, vals)
        #return mbdb.NonQuery(pcls._db_, q, vals)


    @staticmethod
    def updateTable(db_path, pcls:any):
        fields = []
        vals = []
        
        # getmembers() returns all the  members of an object  
        for it in inspect.getmembers(pcls):        
            # to remove private and protected functions 
            if not it[0].startswith('_'):           
                # To remove other methods that doesnot start with a underscore 
                if not inspect.ismethod(it[1]):
                    if(it[0]=="id"):
                        id_record=it[1]
                        continue

                    fields.append(it[0] + "=?")
                    vals.append(it[1])                    
                    #print(it[0], it[1]) 

        #print(pcls.__class__.__name__)
        table_name = type(pcls).__name__

        q="UPDATE " + table_name + " SET " + ", ".join(fields) + " WHERE id=?"
        vals.append(id_record)
        return mbdb.NonQuery(db_path, q, vals)
        #return mbdb.NonQuery(pcls._db_, q, vals)



    @staticmethod
    def deleteRecord(db_path, pcls:any):        
        # getmembers() returns all the  members of an object  
        for it in inspect.getmembers(pcls):        
            # to remove private and protected functions 
            if not it[0].startswith('_'):           
                # To remove other methods that doesnot start with a underscore 
                if not inspect.ismethod(it[1]):
                    if(it[0]=="id"):
                        id_record=it[1]
                        break

        #print(pcls.__class__.__name__)
        table_name = type(pcls).__name__

        q="DELETE FROM " + table_name + " WHERE id=?"
        return mbdb.NonQuery(db_path, q, (id_record, ))
        #return mbdb.NonQuery(pcls._db_, q, (id_record, ))


    @staticmethod
    def getOne(db_path, pcls:any, pcriteria, pvals=()):
        table_name = type(pcls).__name__
        q="SELECT * FROM " + table_name + " WHERE " + pcriteria + " LIMIT 1"
        values = pvals
        
        #if(pid > 0):
           #q="SELECT * FROM tblurl WHERE id = ?"        
            #values = (pid,)

        mycursor = mbdb.executeCursor(db_path, q, values)
        #mycursor = mbdb.executeCursor(pcls._db_, q, values)
        #return mycursor.fetchone()

        rec = mycursor.fetchone()
        if rec==None:
            return False

        map = {}
        for d in mycursor.description:
            map[d[0]] = len(map)
        #print(rec[map["id"]])        

        # getmembers() returns all the  members of an object  
        for it in inspect.getmembers(pcls):        
            # to remove private and protected functions 
            if not it[0].startswith('_'):           
                # To remove other methods that doesnot start with a underscore 
                if not inspect.ismethod(it[1]):
                   pcls.__dict__[it[0]]=rec[map[it[0]]]
                   #print(it)

        return True



    @staticmethod
    def getAll(db_path, query, pvals=()):
        values = pvals        
        mycursor = mbdb.executeCursor(db_path, query, values)
        return mycursor.fetchall()