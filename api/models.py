from django.db import models
from django.contrib.postgres.fields import JSONField
import os

# Models for Postgres
class Companys(models.Model):
    company = models.CharField(max_length=64)
    state = models.CharField(max_length=2)
    data = JSONField()

    #redefining print statement for this object
    def __str__(self):
        new_str = ', '.join([self.company, self.state])
        return new_str

    class Meta:
        """
            can't create primary key because default id is created by Django ORM,
            so create a unique field combining company and state instead
        """
        unique_together = (("company", "state"),)
        """
            verbose_name_plural is for the django admin display, displays Companys
            instead of Companyss
        """
        verbose_name_plural = "Companys"

    """
        addCompany creates entries for each state
        given a folderPath, we get all of the json menu data files per state and create a Companys object to add to the database
        each file is labeled as such, CompanyNameStateAbrreviation.txt (example is McDonaldsCA.txt)
        json.load() takes a file object to create the json dictionary data vs json.loads() takes a string
    """
    def addCompany(folderPath):
        listOfFiles = os.listdir(folderPath)
        for i in range(len(listOfFiles)):
            fileName = listOfFiles[i]
            stateAbbr = fileName[-6:-4]
            companyName = fileName[:-6]
            filePath = folderPath + "\\" + fileName
            print(fileName)
            if "wordsToIgnore" not in filePath:
                menuDataFile = open(filePath, "r")
                jsonData = json.load(menuDataFile)
                companyToAdd = Companys(company=companyName,state=stateAbbr, data=jsonData)
                companyToAdd.save()
                print(companyName + " : " + stateAbbr)
                #print(jsonData)
                menuDataFile.close()

    def updateCompany(folderPath):
        listOfFiles = os.listdir(folderPath)
        for i in range(len(listOfFiles)):
            fileName = listOfFiles[i]
            stateAbbr = fileName[-6:-4]
            companyName = fileName[:-6]
            filePath = folderPath + "\\" + fileName
            print(fileName)
            if "wordsToIgnore" not in filePath:
                menuDataFile = open(filePath, "r")
                jsonData = json.load(menuDataFile)
                Companys.objects.filter(company=companyName, state=stateAbbr).update(data=jsonData)
                print(companyName + " : " + stateAbbr)
                #print(jsonData)
                menuDataFile.close()
