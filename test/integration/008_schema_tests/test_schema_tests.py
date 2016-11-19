from test.integration.base import DBTIntegrationTest

from dbt.task.test import TestTask
from dbt.project import read_project

class FakeArgs(object):
    def __init__(self):
        self.threads = 1
        self.data = False
        self.schema = True

class TestSchemaTests(DBTIntegrationTest):

    def setUp(self):
        DBTIntegrationTest.setUp(self)
        self.run_sql_file("test/integration/008_schema_tests/seed.sql")
        self.run_sql_file("test/integration/008_schema_tests/seed_failure.sql")
    
    @property
    def project_config(self):
        return {
            "test-paths": []
        }

    @property
    def schema(self):
        return "schema_tests_008"

    @property
    def models(self):
        return "test/integration/008_schema_tests/models"

    def run_schema_validations(self):
        project = read_project('dbt_project.yml')
        args = FakeArgs()

        test_task = TestTask(args, project)
        return test_task.run()

    def test_simple_dependency(self):
        self.run_dbt()
        test_results = self.run_schema_validations()

        for result in test_results:
            # assert that all deliberately failing tests actually fail
            if 'failure' in result.model.name:
                self.assertFalse(result.errored)
                self.assertFalse(result.skipped)
                self.assertTrue(result.status > 0)

            # assert that actual tests pass
            else:
                self.assertFalse(result.errored)
                self.assertFalse(result.skipped)
                # status = # of failing rows
                self.assertEqual(result.status, 0)
