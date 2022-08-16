import unittest
from Strategy.MeasureStrategy import MSE
from Strategy.MissingDataStrategy import MCAR
from eraser import Eraser
from pipeline import *
from crowner import *
from reviewer import Reviewer


class TestComponentBuilder(unittest.TestCase):
    def test_component_builder(self):
        """ """

        # Arrange/Act
        c = (
            ComponentBuilder(Crowner)
            .column_name("sepal.length")
            .strategy(Mean())
            .build()
        )

        # Assert
        self.assertIsInstance(c, Crowner)


class TestPipeline(unittest.TestCase):
    def setUp(self):
        self.input_file = "iris_missing.csv"
        self.input_file_non_categorical = "iris_missing_noncategorical.csv"
        self.output_file = "crowner_test.csv"

    def test_pipeline_len(self):
        c = (
            ComponentBuilder(Crowner)
            .column_name("sepal.length")
            .strategy(Mean())
            .build()
        )

        p = Pipeline().add_component(c)

        self.assertEqual(1, len(p))

    def test_pipeline_iter(self):
        c = (
            ComponentBuilder(Crowner)
            .column_name("sepal.length")
            .strategy(Mean())
            .build()
        )

        # case 1
        p = Pipeline().add_component(c)
        for i in p:
            self.assertEqual(c, i)

        # case 2
        p = Pipeline().add_component(c)
        self.assertEqual(c, next(p))

    def test_pipeline_runnable(self):
        p = (
            Pipeline()
            .add_component(
                ComponentBuilder(Eraser)
                .column_name("sepal.length")
                .missing_rate(0.3)
                .strategy(MCAR())
                .build()
            )
            .add_component(
                ComponentBuilder(Crowner)
                .column_name("sepal.length")
                .strategy(Mean())
                .build()
            )
            .add_component(
                ComponentBuilder(Reviewer)
                .column_name("sepal.length")
                .strategy(MSE())
                .build()
            )
        )(self.input_file)

        self.assertEqual(True, True)
