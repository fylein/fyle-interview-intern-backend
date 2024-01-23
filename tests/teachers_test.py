import unittest
from flask import Flask
import json
from unittest.mock import patch
from core.apis.assignments.teacher import teacher_assignments_resources
from core.models.assignments import Assignment
from core.apis.responses import APIResponse


class TestTeacherAssignments(unittest.TestCase):

    def setUp(self):
        app = Flask(__name__)
        app.config['TESTING'] = True
        app.register_blueprint(teacher_assignments_resources)
        self.app = app.test_client()

    @patch('core.apis.assignments.teacher.list_assignments')
    def test_list_assignments(self, mock_get_assignments_by_teacher):
        mock_get_assignments_by_teacher.return_value = [{'assignment_id': 1, 'title': 'Assignment 1'}]

        headers = {'X-Principal': '{"user_id": 1, "teacher_id": 1}'}
        response = self.app.get('/teacher/assignments', headers=headers)

        try:
           data = json.loads(response.data.decode('utf-8'))

           self.assertEqual(response.status_code, 200)
           self.assertIn('data', data)
           self.assertEqual(data['data'], [{'assignment_id': 1, 'title': 'Assignment 1'}])
        except json.decoder.JSONDecodeError as e:
            print(f"JSONDecodeError: {e}")
            print("Response Content:", response.data)

    @patch('core.apis.assignments.teacher.grade_assignment')
    def test_grade_assignment(self, mock_mark_grade):
        mock_mark_grade.return_value = {'assignment_id': 1, 'title': 'Assignment 1', 'grade': 90}

        headers = {'X-Principal': '{"user_id": 1, "teacher_id": 1}'}
        payload = {'id': 1, 'grade': 90}
        response = self.app.post('/teacher/assignments/grade', json=payload, headers=headers)
        try:
          data = json.loads(response.data.decode('utf-8'))

          self.assertEqual(response.status_code, 200)
          self.assertIn('data', data)
          self.assertEqual(data['data'], {'assignment_id': 1, 'title': 'Assignment 1', 'grade': 90})
        except json.decoder.JSONDecodeError as e:
            print(f"JSONDecodeError: {e}")
            print("Response Content:", response.data)

if __name__ == '__main__':
    unittest.main()
