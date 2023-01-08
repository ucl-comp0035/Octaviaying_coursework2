from flask import Flask
from flask_restful import Api, Resource
import pandas
import sqlite3


class Controller:
    def __init__(self):
        self.app = Flask(__name__)
        self.api = Api(self.app)
        self.api.add_resource(DataController, '/data')
        self.api.add_resource(CountryController, '/country/<country>')
        self.api.add_resource(IndicatorController, '/indicator/<name>')

    def run(self):
        self.app.run()

class DataController(Resource):
    def __init__(self):
        self.service = Service()

    def get(self):
        res = self.service.find_overall()
        return {'data':res}

class CountryController(Resource):

    def __init__(self):
        self.service = Service()
    def get(self,country):
        res = self.service.find_country(country)
        return {'data':res}

class IndicatorController(Resource):
    def __init__(self):
        self.service = Service()

    def get(self,name):
        res = self.service.find_indicator(name)

class Service:
    def __init__(self):
        self.dao = Dao()

    def find_country(self, country):
        res = self.dao.find_country(country)
        return res

    def find_overall(self):
        res = self.dao.find_overall()
        return res

    def find_indicator(self,name):
        res = self.dao.find_indicator()
        return res

class Dao:
    def __init__(self):
        self.table_country = "country"
        self.table_indicator = "indicator"
        self.table_education = "education"
        self.table_charts = "charts"
        self.db = sqlite3.connect("../resource/data.sqlite")
        df = pandas.read_csv("../resource/education_chn.csv")
        df1 = df[['Country Name','Country ISO3']].drop_duplicates()
        df1.rename(columns={'Country ISO3':'ISO3','Country Name':'name'},inplace=True)
        df1.to_sql(self.table_country, self.db, if_exists='replace', index=False)
        df1 = df[['Indicator Code','Indicator Name']].drop_duplicates()
        df1.rename(columns={'Indicator Code':'code','Indicator Name':'name'},inplace=True)
        df1.to_sql(self.table_indicator, self.db, if_exists='replace', index=False)
        df1 = df[['Indicator Code','Country ISO3','Year','Value']].drop_duplicates()
        df1.rename(columns={'Indicator Code':'indicator code',
                            'Country ISO3':'country ISO3',
                            'Year':'year',
                            'Value':'value'},inplace=True)
        df1.to_sql(self.table_education, self.db, if_exists='replace', index=False)

        df = pandas.read_csv("../resource/qc_education_chn.csv")
        df.to_sql(self.table_charts, self.db, if_exists='replace', index=False,
                  dtype={'Year': "date", 'Value': "float"})

    def find_country(self, country):
        cursor = self.db.cursor()
        cursor.execute('select * from {} where "Country Name"="{}"'.format(self.table_country, country))
        res = cursor.fetchall()
        cursor.close()
        print(res)
        return res

    def find_overall(self):
        cursor = self.db.cursor()
        cursor.execute('select * from {}'.format(self.table_country))
        res = cursor.fetchall()
        cursor.close()
        return res

    def find_indicator(self,name):
        cursor = self.db.cursor()
        cursor.execute('select * from {} where "Indicator Name"="{}"'.format(self.table_country, name))
        res = cursor.fetchall()
        cursor.close()
        return res


if __name__ == '__main__':
    controller = Controller()
    controller.run()
