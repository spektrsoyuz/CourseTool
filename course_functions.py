#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Filename: course_functions.py
Author: Seth Christie
"""
import json
import time

from styleframe import StyleFrame
import yaml
from bs4 import BeautifulSoup, MarkupResemblesLocatorWarning
import pandas as pd
import requests
import warnings

warnings.filterwarnings("ignore", category=MarkupResemblesLocatorWarning)

excel_headers = ['Tag', 'Name', 'Coreqs', 'Prereqs', 'Standing', 'Section', 'Instructor', 'Time', 'Date', 'Building',
                 'Room', 'Avail']


# -------------------------------------------------- functions ---------------------------------------------------------

def strip_html(html_text):
    """
    Function to strip HTML code from a String
    :param html_text: HTML code to be stripped
    :return: String with HTML code stripped
    """
    soup = BeautifulSoup(html_text, 'html.parser')
    plain_text = soup.get_text()
    return plain_text


def get_course_data(csv_file, tags, catalog_url, export_all):
    """
    Function to parse through Kettering Courses A-Z and the Kettering
    Argos Class Schedule to create a dictionary containing available courses
    for a given term.
    :param csv_file: Specified csv file from Argos
    :param tags: List of acceptable course tags
    :param catalog_url: URL to the course catalog (undergrad/grad)
    :param export_all: Should the function include courses with no sections?
    :return: Dictionary containing a list of available courses
    """
    course_list = {}
    df = None
    try:
        df = pd.read_csv(csv_file)
        # drop useless columns
        df = df.drop(columns=['TYPE', 'PART', 'MAX', 'WL_Max', 'WL_Actual', 'CAMPUS'])
    except FileNotFoundError as e:
        print(f'[CourseTool] CSV file was not found: {e}')

    for tag in tags:
        courses = {}
        tag_url = f'{catalog_url}{tag.lower()}'
        print(f'[CourseTool] Retrieving courses from {tag_url}')

        # send HTML content request to page
        response = retry_get(tag_url)

        courseblocks = BeautifulSoup(response.text, 'html.parser').find_all('div', 'courseblock')
        for courseblock in courseblocks:
            courseblocktitle = courseblock.find('p', 'courseblocktitle').text.split('\xa0')

            # if dataframe exists, check if course exists in dataframe
            if df is not None:
                subjects = df['SUBJ'].values
                tags = df['NUMB'].values
                courseids = [f'{subject}-{tag}' for subject, tag in zip(subjects, tags)]

                if courseblocktitle[0] not in courseids and not export_all:
                    continue

            courseblockdesc = str(courseblock.find('p', 'courseblockdesc')).split('<br/>')

            # default values
            coreqs = 'None'
            prereqs = 'None'
            standing = 'None'
            desc = strip_html(courseblockdesc[-3]).replace('\n', ' ')

            for line in courseblockdesc:
                # check for class standing
                if 'Minimum Class Standing:' in line:
                    standing = line.split(':')[1].strip()

                # check for prereqs
                if 'Prerequisites:' in line:
                    prereqs = strip_html(line).replace('Prerequisites: ', '')

                # check for coreqs
                if 'Corequisites:' in line:
                    coreqs = strip_html(line).replace('Corequisites: ', '')

                # check if course is a special topics course
            if '391' in courseblocktitle[0]:
                desc = 'None'

            # format course dictionary
            course = {
                'tag': courseblocktitle[0],
                'name': courseblocktitle[2].replace('\n', ''),
                'coreqs': coreqs.replace('\n', ''),
                'prereqs': prereqs.replace('\n', ''),
                'standing': standing,
                'desc': desc.replace('  ', ' '),
                'credits': courseblocktitle[-1].replace(' Credits', ''),
                'sections': get_sections(df, courseblocktitle),
            }

            # add course into tag courses
            courses[courseblocktitle[0]] = course

        # add tag courses into final course list
        course_list[tag] = courses

    return course_list


def get_sections(df, course):
    """
    Function to return a dictionary containing each section for a given course
    :param df: Dataframe containing sections
    :param course: Course tag 'MATH-204', 'ECON-201', etc.
    :return: Dictionary containing sections for a given course
    """
    sections = {}
    title_parts = course[0].split('-')

    if df is None:
        return sections

    df_sections = df[(df['SUBJ'] == title_parts[0]) & (df['NUMB'] == title_parts[1])].copy()
    dict_sections = df_sections.to_dict(orient='records')

    for entry in dict_sections:
        # Parse course dates
        dates = [entry['M'], entry['T'], entry['W'], entry['TH'], entry['F']]
        dates = [item for item in dates if item != ' ']

        # Get section data
        section = entry['SEC']
        instructor = entry['INSTRUCTOR']
        time = entry['TIME']
        date = ', '.join(dates)
        building = entry['BLDG']
        room = entry['ROOM']
        avail = entry['AVAIL']

        # Format section block
        sectionblock = {
            'instructor': instructor,
            'time': time,
            'date': date,
            'building': building,
            'room': room,
            'avail': avail
        }

        # Dump block into sections
        sections[section] = sectionblock

    return sections


def get_mech_electives(self, courses):
    """
    Function to return a dictionary containing all courses eligible as ME Electives
    :param self: Tkinter interface
    :param courses: Dictionary containing all the courses
    :return: Dictionary containing all ME Elective options
    """
    electives = {}

    for tag in courses.keys():
        courseblock = {}

        for course in courses[tag].keys():
            tag, num = course.split('-')
            if len(num) > 3:
                num = num[:-1]

            # Check if course is > 300 and < 600
            if not (300 <= int(num) < 600):
                continue

            # Check course against filter
            if (tag in self.parent.MISC_CFILTER or num in self.parent.MISC_CFILTER
                or course in self.parent.MISC_CFILTER) and course not in self.parent.MISC_CAFILTER:
                continue

            courseblock[course] = courses[tag][course]

        if not courseblock:
            continue

        electives[tag] = courseblock

    return electives


def get_adv_electives(self, courses):
    """
    Function to return a dictionary containing all courses eligible as Advanced electives
    :param self: Tkinter interface
    :param courses: Dictionary containing all the courses
    :return: Dictionary containing all Advanced Elective options
    """
    electives = {}

    for tag in courses.keys():
        courseblock = {}

        for course in courses[tag].keys():
            tag, num = course.split('-')
            if len(num) > 3:
                num = num[:-1]

            # Check if course is > 300 and < 600
            if not (int(num) < 600):
                continue

            # Check course against filter
            if (tag in self.parent.MISC_ADVFILTER or num in self.parent.MISC_ADVFILTER
                    or course in self.parent.MISC_ADVFILTER):
                continue

            courseblock[course] = courses[tag][course]

        if not courseblock:
            continue

        electives[tag] = courseblock

    return electives


def dict_to_df(courses):
    """
    Function to convert a Dictionary of courses into a Pandas DataFrame
    :param courses: Dictionary containing courses
    :return: DataFrame containing courses
    """
    data = []

    for subject in courses:
        for courseblock in courses[subject]:
            if not courses[subject][courseblock]['sections']:
                data.append([
                    courses[subject][courseblock]['tag'],
                    courses[subject][courseblock]['name'],
                    courses[subject][courseblock]['coreqs'],
                    courses[subject][courseblock]['prereqs'],
                    courses[subject][courseblock]['standing'],
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                    None
                ])
            else:
                for section in courses[subject][courseblock]['sections']:
                    data.append([
                        courses[subject][courseblock]['tag'],
                        courses[subject][courseblock]['name'],
                        courses[subject][courseblock]['coreqs'],
                        courses[subject][courseblock]['prereqs'],
                        courses[subject][courseblock]['standing'],
                        section,
                        courses[subject][courseblock]['sections'][section]['instructor'],
                        courses[subject][courseblock]['sections'][section]['time'],
                        courses[subject][courseblock]['sections'][section]['date'],
                        courses[subject][courseblock]['sections'][section]['building'],
                        courses[subject][courseblock]['sections'][section]['room'],
                        courses[subject][courseblock]['sections'][section]['avail'],
                    ])
    return StyleFrame(pd.DataFrame(data, columns=excel_headers))


def export_courses(courses, filetype, filename):
    """
    Function to export a dictionary of courses to a given file format
    :param courses: Dictionary of courses to be exported
    :param filetype: File format for the export
    :param filename: Name and location of the export
    :return: None
    """
    match filetype:
        case 'json':
            with open(filename, 'w', encoding='utf-8') as file:
                json.dump(courses, file, ensure_ascii=False, indent=2)

        case 'yaml':
            with open(filename, 'w', encoding='utf-8') as file:
                yaml.dump(courses, file)

        case 'xlsx':
            with StyleFrame.ExcelWriter(filename) as writer:
                sf = dict_to_df(courses)
                sf.to_excel(
                    excel_writer=writer,
                    best_fit=excel_headers
                )

        case _:
            with open(filename, 'w', encoding='utf-8') as file:
                json.dump(courses, file, ensure_ascii=False, indent=2)

    print(f'[CourseTool] Exported courses to {filename}.')


def retry_get(url, max_retries=3):
  for attempt in range(max_retries):
    try:
      response = requests.get(url)
      return response
    except Exception as e:
      print(f"[CourseTool] Attempt {attempt + 1} failed: {e}")
      time.sleep(1)  # wait 1 second before retrying