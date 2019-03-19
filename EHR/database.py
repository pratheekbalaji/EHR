import pymysql


class Database:
    def __init__(self):
        host = "localhost"
        user = "root"
        password = "root"
        db = "ehr"
        self.con = pymysql.connect(host=host, user=user, password=password, db=db, cursorclass=pymysql.cursors.
                                   DictCursor)
        self.cur = self.con.cursor()

    def patient_details(self, name):
        patient = self.cur.execute(
            'Select p.FullName,p.SSN,p.BirthDate,p.Gender,p.DeathDate from ehr.patients p where p.First="%s"' % name)
        details = self.cur.fetchall()
        return details

    def observations(self, name):
        observations = self.cur.execute(
            'SELECT o.Description, o.Units, o.Value,o.Date  FROM ehr.patients p, ehr.observations o where p.Id=o.patient and p.First="%s"' % name)
        result = self.cur.fetchall()
        return result

    def medications(self, name):
        result = self.cur.execute(
            'SELECT m.Description,  m.Reason,m.Start,m.Stop  FROM ehr.patients p, ehr.medications m where p.Id=m.patient and p.First="%s" Order By m.start DESC' % name)
        medications = self.cur.fetchall()
        return medications
    def conditions (self, name):
        result = self.cur.execute(
            'SELECT c.Description, c.Start,c.Stop  FROM ehr.patients p, ehr.conditions c where p.Id=c.patient and p.First="%s" Order By c.Start DESC' % name)
        conditions = self.cur.fetchall()
        return conditions

    def allergies (self, name):
        result = self.cur.execute(
            'SELECT a.Description, a.Start,a.Stop  FROM ehr.patients p, ehr.allergies a where p.Id=a.patient and p.First="%s" Order By a.Start DESC' % name)
        allergies = self.cur.fetchall()
        return allergies

    def procedures (self, name):
        result = self.cur.execute(
            'SELECT a.Description, date(a.Date)  FROM ehr.patients p, ehr.procedures a where p.Id=a.patient and p.First="%s" Order By a.Date DESC' % name)
        procedures = self.cur.fetchall()
        return procedures

