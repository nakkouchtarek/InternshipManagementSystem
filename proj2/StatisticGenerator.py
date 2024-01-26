import matplotlib.pyplot as plt
from pymongo import MongoClient
from datetime import datetime
import mpld3
import matplotlib
import plotly.express as px

matplotlib.use('agg')

class StatisticGenerator:
    def __init__(self):
        self.db = MongoClient("mongodb://localhost:27017").ftest
        self.students_collection_name = "Students"
        self.internships_collection_name = "Internships"
        self.reports_collection_name = "reports"


    def visualize_internship_durations(self):
        internships_data = self.db[self.internships_collection_name].find()

        companies = []
        durations = []

        for internship in internships_data:
            if internship['company_name'] != '' and internship['start_date'] != '' and internship['end_date'] != '':
                companies.append(internship['company_name'])
                start_date = datetime.strptime(internship['start_date'], "%Y-%m-%d")
                end_date = datetime.strptime(internship['end_date'], "%Y-%m-%d")
                duration = (end_date - start_date).days
                durations.append(duration)

        plt.figure(figsize=(10, 6))
        plt.bar(companies, durations, color='green')
        plt.xlabel('Company')
        plt.ylabel('Internship Duration (days)')
        plt.title('Internship Durations by Company')
        plt.xticks(rotation=45, ha='right')

        fig = px.bar(x=companies, y=durations, color=companies,
                    labels={'x': 'Company', 'y': 'Internship Duration (days)'},
                    title='Internship Durations by Company')

        fig.write_html('./graphs/internship_durations.html')

    def visualize_report_types(self):
        report_types_data = self.db[self.reports_collection_name].aggregate([
            {"$group": {"_id": "$fileType", "count": {"$sum": 1}}}
        ])

        report_types = []
        counts = []
        for report_type in report_types_data:
            report_types.append(report_type['_id'])
            counts.append(report_type['count'])

        plt.figure(figsize=(8, 8))
        plt.pie(counts, labels=report_types, autopct='%1.1f%%', startangle=140)
        plt.title('Distribution of Report Types')

        fig = px.pie(names=report_types, values=counts,
                    labels=report_types,
                    title='Distribution of Report Types', hole=0.3)

        fig.write_html('./graphs/report_types.html')

    def visualize_internships_by_theme(self):
        internships_data = self.db[self.internships_collection_name].find()

        themes = []
        for internship in internships_data:
            if internship['theme'] != '':
                themes.append(internship['theme'])

        plt.figure(figsize=(10, 6))
        plt.hist(themes, bins=20, color='skyblue', edgecolor='black')
        plt.xlabel('Internship Theme')
        plt.ylabel('Number of Internships')
        plt.title('Internships by Theme')

        fig = px.histogram(x=themes, color=themes,
                        labels={'x': 'Internship Theme', 'y': 'Number of Internships'},
                        title='Internships by Theme')

        fig.write_html('./graphs/internships_by_theme.html')

    def visualize_internships_per_theme(self):
        internships_data = self.db[self.internships_collection_name].aggregate([
            {"$group": {"_id": "$theme", "count": {"$sum": 1}}}
        ])

        themes = []
        counts = []
        for internship in internships_data:
            themes.append(internship['_id'])
            counts.append(internship['count'])

        plt.figure(figsize=(10, 6))
        plt.bar(themes, counts, color='purple')
        plt.xlabel('Internship Theme')
        plt.ylabel('Number of Internships')
        plt.title('Internships per Theme')
        plt.xticks(rotation=45, ha='right')

        fig = px.bar(x=themes, y=counts, color=themes, labels={'x': 'Internship Theme', 'y': 'Number of Internships'},
                 title='Internships per Theme')
        
        fig.write_html('./graphs/internships_per_theme.html')

    def visualize_students_per_year(self):
        students_data = self.db[self.students_collection_name].aggregate([
            {"$group": {"_id": "$year", "count": {"$sum": 1}}}
        ])

        years = []
        student_counts = []

        for student in students_data:
            years.append(student['_id'])
            student_counts.append(student['count'])

        years = [int(elem) for elem in years]
        student_counts = [int(elem) for elem in student_counts]

        plt.figure(figsize=(10, 6))
        plt.bar(years, student_counts, color='orange')
        plt.xlabel('Year')
        plt.ylabel('Number of Students')
        plt.title('Students per Year')

        fig = px.bar(x=years, y=student_counts, color=years,
                 labels={'x': 'Year', 'y': 'Number of Students'},
                 title='Students per Year')

        fig.write_html('./graphs/students_per_year.html')

    def generate_graphs(self):
        self.visualize_internship_durations()
        self.visualize_report_types()
        self.visualize_internships_by_theme()
        self.visualize_internships_per_theme()
        self.visualize_students_per_year()