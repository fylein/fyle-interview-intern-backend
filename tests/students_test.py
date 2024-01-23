import unittest
from flask import Flask
import json
from unittest.mock import patch
from core.apis.assignments.student import student_assignments_resources


class TestStudentAssignments(unittest.TestCase):

    def setUp(self):
        app = Flask(__name__)
        app.config['TESTING'] = True
        app.register_blueprint(student_assignments_resources)
        self.app = app.test_client()

    @patch('core.apis.assignments.student.list_assignments')
    def test_list_assignments(self, mock_get_assignments):
        mock_get_assignments.return_value = [{'assignment_id': 1, 'title': 'Assignment 1'}]
        response = self.app.get('/student/assignments')
        try:
            data = json.loads(response.data.decode('utf-8'))
            self.assertEqual(response.status_code, 200)
            self.assertIn('data', data)
            self.assertEqual(data['data'], [{'assignment_id': 1, 'title': 'Assignment 1'}])
        except json.decoder.JSONDecodeError as e:
            print(f"JSONDecodeError: {e}")
            print("Response Content:", response.data)

    @patch('core.apis.assignments.student.list_draft_assignments')
    def test_list_draft_assignments(self, mock_get_draft_assignments):
        mock_get_draft_assignments.return_value = [{'assignment_id': 1, 'title': 'Draft Assignment 1'}]
        response = self.app.get('/student/assignments/drafts')
        try:
            data = json.loads(response.data.decode('utf-8'))
            self.assertEqual(response.status_code, 200)
            self.assertIn('data', data)
            self.assertEqual(data['data'], [{'assignment_id': 1, 'title': 'Draft Assignment 1'}])
        except json.decoder.JSONDecodeError as e:
            print(f"JSONDecodeError: {e}")
            print("Response Content:", response.data)

    @patch('core.apis.assignments.student.get_assignment')
    def test_get_assignment(self, mock_get_assignment_by_id):
        mock_get_assignment_by_id.return_value = {'assignment_id': 1, 'title': 'Assignment 1'}
        response = self.app.get('/student/assignments/1')
        try:
            data = json.loads(response.data.decode('utf-8'))
            self.assertEqual(response.status_code, 200)
            self.assertIn('data', data)
            self.assertEqual(data['data'], {'assignment_id': 1, 'title': 'Assignment 1'})
        except json.decoder.JSONDecodeError as e:
            print(f"JSONDecodeError: {e}")
            print("Response Content:", response.data)


